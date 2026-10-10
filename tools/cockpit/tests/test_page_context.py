"""Cockpit 1.4 — « À répondre » beside its document, the keyboard, and the
usage gauges, in a headless browser (Microsoft Edge through Playwright).
The SDK client is a fake: no chain command runs."""
import hashlib
import os
import re
import shutil
from datetime import datetime, timedelta

import pytest

pytest.importorskip("playwright")

import stats  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from test_stats import two_agents  # noqa: E402

PRODUCT = """# Produit

## Course

### B3 — Montre autonome
La montre est autonome pendant la course.

### B12 — Perte du lien
- La course continue.
- Elle se synchronise au retour.

### B13 — Suivant
Texte.
"""

MODEL = """# Model

### §1.2 Tokens
Rule.

### §1.3 Start time
The start time is **recorded** twice.
"""

IDEAS = """# Idées

Un atelier par station.

Chaque atelier compte. Les ateliers suivants attendent.

## Fin
Le dernier ATELIER ferme la course.
"""

LEX = """### Q1
Terms: atelier, station
Question: one thing or two?
Options:
- Les deux termes nomment la même chose.
- Ce sont deux choses distinctes.
- L'un est l'abréviation de l'autre.
Answer:

### Q2
Terms: course
Question: which meaning?
Options:
- Une seule signification.
- Deux significations.
Answer:
"""


@pytest.fixture
def page(browser):
    pg = browser.new_page(viewport={"width": 1400, "height": 860})
    pg.js_errors = []
    pg.posts = []
    pg.on("pageerror", lambda e: pg.js_errors.append(str(e)))
    pg.on("console", lambda m: pg.js_errors.append(m.text) if m.type == "error" else None)
    pg.on("request", lambda r: pg.posts.append(r.url) if r.method == "POST" else None)
    yield pg
    pg.close()


def no_real_errors(page):
    return [e for e in page.js_errors if "Failed to fetch" not in e and "net::ERR" not in e]


def digest(folder):
    return {str(p): hashlib.sha1(p.read_bytes()).hexdigest() for p in folder.rglob("*") if p.is_file()}


def card(page, rel, n):
    return page.locator(f'.entry[data-id="q:{rel}#{n}"]')


def open_answer(s, page, work="f"):
    s.state.open_pair(str(s.app_root), work)
    page.goto(s.url + "#answer")
    page.wait_for_selector(".entry.focused")


def lex_feature(s):
    feat = s.app_root / "docs" / "features" / "lex"
    feat.mkdir(parents=True)
    (feat / "idees.md").write_text(IDEAS, encoding="utf-8")
    (feat / "questions-lexicographe-01.md").write_text(LEX, encoding="utf-8")
    return feat


def test_the_focused_question_shows_its_passage(tmp_path, page):
    with FakeServer(tmp_path) as s:
        (s.feat / "desc-produit.md").write_text(PRODUCT, encoding="utf-8")
        (s.feat / "convertisseur" / "model.md").write_text(MODEL, encoding="utf-8")
        before = digest(s.feat)
        open_answer(s, page)
        page.posts.clear()               # the opening's scan (/api/check) is before any focus
        # A blocking file: no document, and the pane says why.
        assert page.locator(".entry.focused").first.get_attribute("data-id").startswith("b:")
        assert "Un blocage" in page.locator("#ctx-note").inner_text()

        card(page, "questions-sondeur-02.md", 1).click()
        page.wait_for_function("document.getElementById('ctx-docname').textContent === 'desc-produit.md'")
        hl = page.locator("#ctx-doc .ln.inrange")
        assert hl.count() == 3                                       # the whole of B12, its heading and its list
        assert hl.first.inner_text().startswith("B12 — Perte du lien")
        assert page.locator("#ctx-doc .ln.inrange.cur").count() == 3
        assert page.locator("#ctx-doc .h3").count() == 3 and page.locator("#ctx-doc .li").count() == 2
        assert page.locator("#ctx-count").inner_text() == "1 / 1"
        assert page.locator("#ctx-note").is_hidden()
        # The passage is scrolled into the pane.
        assert page.evaluate("""() => { const b = document.getElementById('ctx-doc').getBoundingClientRect();
            const r = document.querySelector('#ctx-doc .ln.inrange').getBoundingClientRect();
            return r.top >= b.top && r.bottom <= b.bottom; }""")

        # Not in the file: said plainly, nothing highlighted.
        card(page, "questions-sondeur-02.md", 2).click()
        page.wait_for_function("document.getElementById('ctx-note').textContent.includes('B14')")
        assert page.locator("#ctx-note").inner_text() == "B14 introuvable dans desc-produit.md."
        assert page.locator("#ctx-doc .inrange, #ctx-doc mark").count() == 0
        assert page.locator("#ctx-nav").is_hidden()

        # About the feature, not a block: no context, and why.
        card(page, "questions-sondeur-02.md", 3).click()
        page.wait_for_function("document.getElementById('ctx-docname').textContent === 'Pas de contexte'")
        assert "la question porte sur la feature" in page.locator("#ctx-note").inner_text()

        # A technical question: its entry in its own section.
        card(page, "convertisseur/technique-model.md", 1).click()
        page.wait_for_function("document.getElementById('ctx-docname').textContent === 'convertisseur/model.md'")
        assert page.locator("#ctx-doc .ln.inrange").first.inner_text().startswith("§1.3 Start time")
        assert page.locator("#ctx-doc .inrange b").inner_text() == "recorded"          # inline bold rendered
        assert "Hors de ce document : [B12: recorded start time]" in page.locator("#ctx-note").inner_text()

        # The pane never writes: no POST, no file touched.
        assert page.posts == [] and digest(s.feat) == before
        assert no_real_errors(page) == []


def test_occurrences_are_numbered_and_walked(tmp_path, page):
    with FakeServer(tmp_path) as s:
        lex_feature(s)
        open_answer(s, page, "lex")
        page.wait_for_function("document.getElementById('ctx-count').textContent === '1 / 4'")
        marks = page.locator("#ctx-doc mark")
        assert marks.all_inner_texts() == ["atelier", "station", "atelier", "ATELIER"]   # never « ateliers »
        assert page.locator("#ctx-doc mark.cur").inner_text() == "atelier"
        page.get_by_role("button", name="Suivante ›").click()
        assert page.locator("#ctx-count").inner_text() == "2 / 4"
        assert page.locator("#ctx-doc mark.cur").inner_text() == "station"
        page.get_by_role("button", name="‹ Précédente").click()
        page.get_by_role("button", name="‹ Précédente").click()
        assert page.locator("#ctx-count").inner_text() == "4 / 4"                        # it wraps
        assert page.locator("#ctx-doc mark.cur").inner_text() == "ATELIER"
        assert page.locator("#ctx-doc .h2 mark.cur").count() == 0 and page.locator("#ctx-doc mark.cur").count() == 1
        assert no_real_errors(page) == []


def test_the_keyboard(tmp_path, page):
    with FakeServer(tmp_path) as s:
        feat = lex_feature(s)
        open_answer(s, page, "lex")
        q1, q2 = card(page, "questions-lexicographe-01.md", 1), card(page, "questions-lexicographe-01.md", 2)
        assert "focused" in q1.get_attribute("class")
        # The digits choose an option of the focused question.
        page.keyboard.press("2")
        assert q1.locator(".opt.chosen").inner_text().startswith("Ce sont deux choses distinctes.")
        page.keyboard.press("7")                                       # no 7th option: nothing
        assert q1.locator(".opt.chosen").inner_text().startswith("Ce sont deux choses distinctes.")
        # T: into the text field — where no key fires.
        page.keyboard.press("t")
        assert page.evaluate("document.activeElement.tagName") == "TEXTAREA"
        page.keyboard.type("1 trop court")
        page.keyboard.press("Enter")
        page.keyboard.press("ArrowUp")
        assert q1.locator("textarea").input_value() == "1 trop court\n"
        assert q1.locator(".opt.chosen").inner_text().startswith("Ce sont deux choses distinctes.")
        assert "focused" in q1.get_attribute("class")
        # Échap leaves the field.
        page.keyboard.press("Escape")
        assert page.evaluate("document.activeElement.dataset.id") == "q:questions-lexicographe-01.md#1"
        # ↓ and Entrée: next; ↑: previous. The pane follows.
        page.keyboard.press("ArrowDown")
        assert "focused" in q2.get_attribute("class") and "focused" not in q1.get_attribute("class")
        page.wait_for_function("document.getElementById('ctx-what').textContent.startsWith('Termes : course')")
        page.keyboard.press("ArrowUp")
        assert "focused" in q1.get_attribute("class")
        page.keyboard.press("Enter")
        assert "focused" in q2.get_attribute("class")
        page.keyboard.press("1")
        assert q2.locator(".opt.chosen").inner_text().startswith("Une seule signification.")
        # Ctrl+S saves both, as the button would.
        page.keyboard.press("Control+s")
        page.wait_for_selector("#save-summary .sumline.ok")
        text = (feat / "questions-lexicographe-01.md").read_text(encoding="utf-8")
        assert "Answer: Ce sont deux choses distinctes. — 1 trop court" in text
        assert "Answer: Une seule signification." in text
        # The legend is there; off this screen the keys do nothing.
        assert "Ctrl" in page.locator("#keys-legend").inner_text()
        page.get_by_role("link", name="Tableau de bord").first.click()
        page.keyboard.press("2")
        assert page.evaluate("location.hash") == "#dashboard"
        assert no_real_errors(page) == []


# --------------------------------------------- 1.4.4, on the real files
# Frozen copies of docs/features/premiere-app-3/ as the Product Owner was
# answering it: the lexicographe's questions file and the idea file.
REAL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "context", "premiere-app-3")
REAL_Q = "questions-lexicographe-02.md"

SCROLLS = """() => { const d = document.getElementById('ctx-doc'), l = document.getElementById('answer-left');
  const c = document.querySelector('.entry.focused').getBoundingClientRect(), p = l.getBoundingClientRect();
  return {win: window.scrollY, main: document.getElementById('main').scrollTop, doc: d.scrollTop,
          docRoom: d.scrollHeight - d.clientHeight, left: l.scrollTop,
          cardSeen: c.bottom > p.top + 20 && c.top < p.bottom - 20,
          cur: [...d.querySelectorAll('mark.cur')].map((m) => m.dataset.k)}; }"""


def real_answer(s, page, width, n):
    feat = s.app_root / "docs" / "features" / "premiere-app-3"
    shutil.copytree(REAL, feat)
    page.set_viewport_size({"width": width, "height": 800})
    open_answer(s, page, "premiere-app-3")
    card(page, REAL_Q, n).click()
    page.wait_for_function(f"document.getElementById('ctx-what').textContent.includes('{n == 9 and 'arrivée estimée' or 'page de fin'}')")
    page.wait_for_function("document.querySelector('#ctx-doc mark.cur')")


def phrase_count(text, phrases):
    return sum(len(re.findall(r"(?<!\w)" + r"\s+".join(map(re.escape, p.split())) + r"(?!\w)", text, re.I))
               for p in phrases)


@pytest.mark.parametrize("width", [1280, 1024])
def test_a_term_of_several_words_is_highlighted_whole(tmp_path, page, width):
    with FakeServer(tmp_path) as s:
        real_answer(s, page, width, 9)
        phrases = ["arrivée estimée", "estimation du temps d'arrivée", "temps d'arrivée estimé"]
        n = phrase_count(open(os.path.join(REAL, "idees.md"), encoding="utf-8").read(), phrases)
        assert n == 8                                  # one across a line break: « arrivée⏎estimée »
        occ = page.evaluate("""() => { const o = {}; for (const m of document.querySelectorAll('#ctx-doc mark'))
            o[m.dataset.k] = (o[m.dataset.k] ? o[m.dataset.k] + ' ' : '') + m.textContent; return Object.values(o); }""")
        occ = [" ".join(m.split()).lower() for m in occ]
        assert len(occ) == n and set(occ) <= set(phrases)                  # the phrase, never one of its words
        assert occ.count("arrivée estimée") == 6
        assert page.locator("#ctx-count").inner_text() == f"1 / {n}"
        # Beside a one-word term, the phrase still wins: « page de fin », never « page » alone in it.
        card(page, REAL_Q, 4).click()
        page.wait_for_function("document.getElementById('ctx-what').textContent.includes('page de fin')")
        marks = [m.lower() for m in page.locator("#ctx-doc mark").all_inner_texts()]
        assert marks.count("page de fin") == 5 and marks.count("écran de fin") == 1
        assert page.evaluate("""() => [...document.querySelectorAll('#ctx-doc mark')].filter((m) =>
            m.textContent.toLowerCase() === 'page' && /^\\s+de fin/i.test(m.nextSibling ? m.nextSibling.textContent : '')).length""") == 0
        assert no_real_errors(page) == []


@pytest.mark.parametrize("width", [1280, 1024])
def test_next_and_previous_move_the_document(tmp_path, page, width):
    with FakeServer(tmp_path) as s:
        real_answer(s, page, width, 4)
        st = page.evaluate(SCROLLS)
        assert st["docRoom"] > 10000 and st["cur"] == ["0"]                 # the document scrolls in its pane
        moves = [("click", "#ctx-next", "2 / 72"), ("key", "ArrowRight", "3 / 72"), ("key", "ArrowRight", "4 / 72"),
                 ("key", "ArrowLeft", "3 / 72"), ("click", "#ctx-prev", "2 / 72")]
        for how, what, count in moves:
            before = page.evaluate(SCROLLS)
            if how == "click":
                page.click(what)
            else:
                page.keyboard.press(what)
            st = page.evaluate(SCROLLS)
            assert page.locator("#ctx-count").inner_text() == count
            assert st["cur"] == [str(int(count.split(" /")[0]) - 1)]
            assert st["doc"] != before["doc"]                                # the right pane moved
            assert st["win"] == 0 and st["main"] == 0                        # the page did not
            assert st["left"] == before["left"] and st["cardSeen"]
        # ↑ and ↓ stay on the questions.
        page.keyboard.press("ArrowDown")
        assert "focused" in card(page, REAL_Q, 5).get_attribute("class")
        page.keyboard.press("ArrowUp")
        assert "focused" in card(page, REAL_Q, 4).get_attribute("class")
        page.wait_for_function("document.getElementById('ctx-count').textContent.endsWith('/ 72')")
        # Never while typing: the arrows move the caret.
        shown = page.locator("#ctx-count").inner_text()
        page.keyboard.press("t")
        page.keyboard.type("ab")
        page.keyboard.press("ArrowLeft")
        page.keyboard.press("ArrowRight")
        assert page.locator("#ctx-count").inner_text() == shown
        assert card(page, REAL_Q, 4).locator("textarea").input_value() == "ab"
        assert "←" in page.locator("#keys-legend").inner_text() and "→" in page.locator("#keys-legend").inner_text()
        assert no_real_errors(page) == []


@pytest.mark.parametrize("width", [1280, 1024])
def test_scrolling_the_document_keeps_the_question(tmp_path, page, width):
    with FakeServer(tmp_path) as s:
        real_answer(s, page, width, 4)
        before = page.evaluate(SCROLLS)
        box = page.locator("#ctx-doc").bounding_box()
        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        page.mouse.wheel(0, 3000)
        page.wait_for_function(f"document.getElementById('ctx-doc').scrollTop > {before['doc'] + 1000}")
        st = page.evaluate(SCROLLS)
        assert st["win"] == 0 and st["main"] == 0 and st["left"] == before["left"] and st["cardSeen"]
        # Down to its end: the page still does not move.
        page.mouse.wheel(0, 60000)
        page.wait_for_function("(d => d.scrollTop >= d.scrollHeight - d.clientHeight - 1)(document.getElementById('ctx-doc'))")
        page.evaluate("() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))")
        st = page.evaluate(SCROLLS)
        assert st["win"] == 0 and st["main"] == 0 and st["left"] == before["left"] and st["cardSeen"]
        # The left pane scrolls on its own too, the right one stays. (In its
        # margin: a long question's text is a scroller of its own.)
        box = page.locator("#answer-left").bounding_box()
        page.mouse.move(box["x"] + 8, box["y"] + box["height"] / 2)
        page.mouse.wheel(0, 600)
        page.wait_for_function(f"document.getElementById('answer-left').scrollTop > {before['left']}")
        after = page.evaluate(SCROLLS)
        assert after["doc"] == st["doc"] and after["win"] == 0 and after["main"] == 0
        # Both panes end above the save bar.
        bar = page.locator("#answer-foot").bounding_box()
        for pane in ("#answer-left", "#ctx-pane"):
            b = page.locator(pane).bounding_box()
            assert abs(b["y"] + b["height"] - bar["y"]) <= 1
        assert no_real_errors(page) == []


def test_gauges_show_the_measure_and_its_age(tmp_path, page):
    store = stats.Store(str(tmp_path / "stats.sqlite"))
    at = (datetime.now() - timedelta(minutes=12)).isoformat(timespec="milliseconds")
    future = int((datetime.now() + timedelta(hours=3)).timestamp())
    past = int((datetime.now() - timedelta(hours=1)).timestamp())
    store.record_limit("r0", {"measured_at": at, "source": "usage", "window": "five_hour",
                              "utilization": 0.04, "resets_at": future, "status": None})
    store.record_limit("r0", {"measured_at": at, "source": "event", "window": "seven_day",
                              "utilization": 0.11, "resets_at": past, "status": "allowed"})
    with FakeServer(tmp_path, stats=store) as s:
        page.goto(s.url + "#dashboard")
        page.wait_for_selector("#gauge-five_hour .gp")
        g5 = page.locator("#gauge-five_hour").inner_text()
        assert "4 %" in g5 and "Reste 96 %" in g5 and "mesuré il y a 12 min" in g5 and "/usage" in g5
        g7 = page.locator("#gauge-seven_day")
        # A measure the reset has passed is never shown as current.
        assert "réinitialisée" in g7.inner_text() and "stale" in g7.get_attribute("class")
        assert no_real_errors(page) == []


def test_a_run_shows_each_hand_back_and_its_totals(tmp_path, page):
    store = stats.Store(str(tmp_path / "stats.sqlite"))
    with FakeServer(tmp_path, script=two_agents, stats=store, measure_limits=True) as s:
        page.goto(s.url + "#chaine")
        page.wait_for_selector("#flow-main li.step")
        s.call(s.rn.start(str(s.app_root), "f", "f", "1_lexique", "f"))
        page.wait_for_selector("#run-total")
        lines = page.locator("#stream .use").all_inner_texts()
        # Mid-run, no agent's output is known yet: it comes with the run's end.
        assert any(l.startswith("Pong — ") and "1,6 k lus (dont 0 en cache), écrits : à la fin du run" in l
                   for l in lines), lines
        assert any(l.startswith("Lexicographe — ") and "écrits : à la fin du run" in l for l in lines), lines
        total = page.locator("#run-total").inner_text()
        assert "Total du run" in total and "18 k lus (dont 12 k en cache), 768 écrits" in total
        # At the end: Pong alone used Haiku, its figure; the lexicographe shares
        # Opus with the orchestrator, unknown.
        end = page.locator("#run-end .muted.small").all_inner_texts()
        assert any(l.startswith("Pong — ") and l.endswith("68 écrits") for l in end), end
        assert any(l.startswith("Lexicographe — ") and l.endswith("écrits : inconnu") for l in end), end
        # The gauges took the end-of-run measure.
        page.get_by_role("link", name="Tableau de bord").first.click()
        page.wait_for_function("document.getElementById('gauge-five_hour').textContent.includes('5 %')")
        assert "mesuré à l'instant" in page.locator("#gauge-five_hour").inner_text()
        assert "18 k lus" in page.locator("#history").inner_text()
        assert no_real_errors(page) == []
