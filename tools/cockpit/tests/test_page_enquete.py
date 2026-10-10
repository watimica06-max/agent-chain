"""1.21 — « Enquêtes » in a headless browser (Microsoft Edge through
Playwright), desktop and phone: in « Mesure » after « Journal »; a new
investigation — her question, the target, the model, the read-only rule said
—, followed live, refusals in red, its report listed with its cost and read;
« Enquêter sur ce point » on a point à creuser and on a run that ended in
error, the question written and not launched; the correction prompt marked
« à relire », with no button that launches it; the bug entry shown, changed
by her, written only on « Ajouter »; this computer's nickname asked once,
and in Paramètres; the phone reads and starts nothing. No chain command, no
real Claude call; every repository is a scratch one."""
import os

import pytest

pytest.importorskip("playwright")

import journalworld  # noqa: E402
import server  # noqa: E402
from enqueteworld import READS, WRITES, Factory, answering, saying  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from test_chain import git  # noqa: E402
from test_page import no_real_errors, page, settled  # noqa: E402,F401
from test_page_phone import phone  # noqa: E402,F401

PROMPT = "Cockpit 1.22 — x.\n\n## 1\n\nQuote before changing…\n\nCommit and push: `Cockpit 1.22 — x`"
BUG = ("Observé : le chrono repart de zéro après une pause.\nOù : sur l'écran de course\n"
       "Attendu : reprendre où il en était.")


@pytest.fixture(autouse=True)
def _never_the_real_chain(tmp_path, monkeypatch):
    """agent-chain's reports are never this computer's: an empty scratch
    folder, unless the test builds its own scratch clone (chain_root)."""
    d = tmp_path / "pas-d-agent-chain"
    d.mkdir()
    monkeypatch.setattr(server, "CHAIN_ROOT", str(d))


@pytest.fixture
def chain_root(tmp_path, monkeypatch):
    from selfupdateworld import chain_world
    _, here, _ = chain_world(tmp_path / "c")
    monkeypatch.setattr(server, "CHAIN_ROOT", str(here))
    return here


def eq_server(tmp_path, monkeypatch, *scripts, script=None):
    f = Factory(*(scripts or (answering(),)))
    monkeypatch.setattr(server, "ENQUETE_CLIENT", f)
    s = FakeServer(tmp_path, **({"script": script} if script else {}))
    journalworld.make(s.app_root)
    s.factory = f
    return s


def open_eq(pg, s):
    pg.goto(s.url + "#enquetes")
    pg.wait_for_selector("#eq-list")
    settled(pg)


def launch(pg, question, target="application"):
    pg.locator("#eq-new").click()
    pg.locator("#eq-question").fill(question)
    pg.locator(f"input[name=eq-target][value={target}]").check()
    pg.locator("#eq-launch").click()


def test_a_new_investigation_followed_then_read(tmp_path, page, monkeypatch, chain_root):
    import asyncio
    gate = asyncio.Event()
    with eq_server(tmp_path, monkeypatch, answering(tools=WRITES[:5] + READS[:2], gate=gate)) as s:
        open_eq(page, s)
        ids = page.locator("#side a").evaluate_all("as => as.map(a => a.id)")
        assert ids[ids.index("nav-journal") + 1] == "nav-enquetes"
        assert page.locator("#tb-page").inner_text() == "Enquêtes"
        assert "Aucun rapport encore" in page.locator("#eq-list").inner_text()
        page.locator("#eq-new").click()
        labels = page.locator("#eq-target label").all_inner_texts()
        assert labels[0] == "L'application « app »" and labels[1].startswith("La chaîne et le cockpit — ")
        assert page.locator("#eq-model option").first.inner_text().startswith("Celui des commandes de la chaîne")
        assert [o for o in page.locator("#eq-model option").evaluate_all("os => os.map(o => o.value)")] == \
            ["", "opus", "sonnet", "haiku"]
        ro = page.locator("#eq-ro").inner_text()
        assert "Lecture seule, imposée par le cockpit" in ro and "ni commit, ni push, ni suppression" in ro
        page.locator("#eq-form-cancel").click()
        launch(page, "Pourquoi l'écran de course remet-il le chrono à zéro ?")
        page.wait_for_selector("#eq-current .eq-steps div.no")
        cur = page.locator("#eq-current").inner_text()
        assert "Enquête en cours" in cur and "Pourquoi l'écran de course" in cur
        page.wait_for_function("document.querySelectorAll('#eq-current .eq-steps div').length >= 7")
        no = page.locator("#eq-current .eq-steps div.no").all_inner_texts()
        assert len(no) == 5 and any("git push origin master" in x for x in no) and any("Write" in x for x in no)
        assert page.locator("#nav-eq-dot").is_visible()
        assert page.locator("#eq-stop").is_visible()
        s.loop.call_soon_threadsafe(gate.set)
        page.wait_for_selector("#eq-current .notice.ok")
        assert "Dernière enquête" in page.locator("#eq-current").inner_text()
        assert "commandes refusées par le cockpit" in page.locator("#eq-current").inner_text()
        assert page.locator("#nav-eq-dot").is_hidden()
        page.wait_for_selector("#eq-list .eq-item")
        item = page.locator("#eq-list .eq-item").first.inner_text()
        assert "12 000 tokens lus · 800 écrits" in item and "« app »" in item and "ordinateur" in item
        page.locator("#eq-current").get_by_role("button", name="Lire le rapport").click()
        page.wait_for_selector("#eq-reader .mdoc")
        rd = page.locator("#eq-reader").inner_text()
        assert "La question" in rd and "Ce que le cockpit a refusé" in rd and "En bref" in rd
        assert page.locator("#eq-bug").is_visible() and page.locator("#eq-prompt").count() == 0
        assert no_real_errors(page) == []


def test_enqueter_sur_ce_point_writes_the_question_and_launches_nothing(tmp_path, page, monkeypatch):
    with eq_server(tmp_path, monkeypatch) as s:
        page.goto(s.url + "#journal")
        page.wait_for_selector("#jn-points .jn-point .eq-go")
        n = page.locator("#jn-points .eq-go").count()
        assert n == page.locator("#jn-points .jn-point").count() and n >= 4
        point = page.locator("#jn-points .jn-point", has_text="n'était pas connecté")
        point.get_by_role("button", name="Enquêter sur ce point").click()
        page.wait_for_selector("#eq-form:not(.hidden)")
        q = page.locator("#eq-question").input_value()
        assert q.startswith("Pourquoi cette commande a-t-elle fini en erreur")
        assert "Ce qui s'est passé : /8_code f n'était pas connecté" in q and "journal.md" in q
        assert page.locator("input[name=eq-target][value=chaine]").is_checked()
        assert "relisez-la" in page.locator("#eq-msg").inner_text()
        # She can change it; nothing started.
        page.locator("#eq-question").fill(q + "\nEt sur l'autre ordinateur ?")
        settled(page)
        assert not s.factory.made
        page.locator("#eq-form-cancel").click()
        assert page.locator("#eq-form").is_hidden()
        assert no_real_errors(page) == []


def test_enqueter_on_a_run_that_ended_in_error(tmp_path, page, monkeypatch):
    async def failing(c):
        from claude_agent_sdk import ResultMessage
        yield ResultMessage(subtype="error_during_execution", duration_ms=1, duration_api_ms=1, is_error=True,
                            num_turns=1, session_id="s", result="Rien.", errors=["Le lot 3 est introuvable"])
    with eq_server(tmp_path, monkeypatch, script=failing) as s:
        page.goto(s.url + "#chaine")
        page.wait_for_selector("#side")
        s.call(s.rn.start(str(s.app_root), "f", "f", "2_structure", "f"))
        page.wait_for_selector("#run-enquete")
        page.locator("#run-enquete").click()
        page.wait_for_selector("#eq-form:not(.hidden)")
        q = page.locator("#eq-question").input_value()
        assert "/2_structure f a fini en erreur" in q and "« Le lot 3 est introuvable »" in q
        assert page.locator("input[name=eq-target][value=chaine]").is_checked()
        assert not s.factory.made
        assert no_real_errors(page) == []


def test_the_correction_prompt_is_marked_and_has_no_launch_button(tmp_path, page, monkeypatch, chain_root):
    with eq_server(tmp_path, monkeypatch, answering(), saying(PROMPT)) as s:
        open_eq(page, s)
        launch(page, "Pourquoi le journal écrit-il le nom réseau ?", "chaine")
        page.wait_for_selector("#eq-current .notice.ok")
        page.locator("#eq-current").get_by_role("button", name="Lire le rapport").click()
        page.wait_for_selector("#eq-prompt")
        assert page.locator("#eq-bug").count() == 0
        assert "ne se lance jamais depuis le cockpit" in page.locator("#eq-reader .eq-next").inner_text()
        page.locator("#eq-prompt").click()
        page.wait_for_selector("#eq-reader .eq-mark")
        assert page.locator("#eq-reader .eq-mark").inner_text() == "À relire dans la conversation de conception avant de lancer"
        pre = page.locator("#eq-reader .eq-prompt pre").inner_text()
        assert pre.startswith("> **À relire dans la conversation de conception avant de lancer.**")
        assert "Commit and push: `Cockpit 1.22 — x`" in pre
        buttons = page.locator("#eq-reader button").all_inner_texts()
        assert "Copier" in buttons and not [b for b in buttons if "Lancer" in b or "lancer" in b]
        assert "Aucun bouton ne le lance" in page.locator("#eq-reader .eq-prompt").inner_text()
        prel = page.locator("#eq-reader .eq-prompt .mono").inner_text()
        assert os.path.exists(os.path.join(server.CHAIN_ROOT, *prel.split("/")))
        settled(page)
        assert page.locator("#eq-list .eq-item .badge", has_text="prompt à relire").count() == 1
        assert no_real_errors(page) == []


def test_the_bug_entry_written_only_on_ajouter(tmp_path, page, monkeypatch):
    with eq_server(tmp_path, monkeypatch, answering(), saying(BUG)) as s:
        feat = s.app_root / "docs" / "features" / "f"
        open_eq(page, s)
        launch(page, "Pourquoi le chrono repart-il de zéro ?")
        page.wait_for_selector("#eq-current .notice.ok")
        page.locator("#eq-current").get_by_role("button", name="Lire le rapport").click()
        page.wait_for_selector("#eq-bug")
        page.locator("#eq-bug").click()
        page.wait_for_selector("#eq-bug-entry")
        entry = page.locator("#eq-bug-entry").input_value()
        assert entry == ("G01 Sur l'écran de course : le chrono repart de zéro après une pause. "
                         "Elle devrait reprendre où il en était.")
        assert "bugfix-01/bug-list.md — une nouvelle correction" in page.locator("#eq-reader .eq-bug").inner_text()
        assert "Diagnostiqueur" in page.locator("#eq-reader .eq-bug").inner_text()
        assert not (feat / "bugfix-01").exists()
        page.locator("#eq-bug-entry").fill(entry.replace("après une pause", "après une pause de 10 s"))
        page.get_by_role("button", name="Annuler").last.click()
        settled(page)
        assert not (feat / "bugfix-01").exists()
        page.locator("#eq-bug").click()
        page.wait_for_selector("#eq-bug-entry")
        page.locator("#eq-bug-entry").fill(entry.replace("après une pause", "après une pause de 10 s"))
        page.locator("#eq-bug-add").click()
        page.wait_for_selector("#eq-reader .notice.ok")
        assert (feat / "bugfix-01" / "bug-list.md").read_text(encoding="utf-8") == \
            entry.replace("après une pause", "après une pause de 10 s") + "\n"
        assert "Ajouté à docs/features/f/bugfix-01/bug-list.md" in page.locator("#eq-reader .notice.ok").inner_text()
        assert no_real_errors(page) == []


def test_the_phone_reads_and_starts_nothing(tmp_path, phone, monkeypatch):
    with eq_server(tmp_path, monkeypatch) as s:
        rel = "docs/enquetes/2026-10-10-pourquoi.md"
        p = s.app_root / rel
        p.parent.mkdir(parents=True)
        p.write_text("# Enquête — Pourquoi ?\n\n- Date : 10/10/2026 à 21:14\n- Ordinateur : travail\n"
                     "- Cible : l'application « app »\n- Modèle : claude-sonnet-5-5 (celui des commandes de la chaîne)\n"
                     "- Coût : 12 000 tokens lus · 800 écrits · 1 min 12 s\n\n## La question\n\nPourquoi ?\n\n"
                     "## La réponse\n\n**En bref** — Parce que. `tools/cockpit/server.py:12`\n", encoding="utf-8")
        phone.goto(s.url + "#dashboard")
        phone.wait_for_selector("#phone-nav")
        phone.locator("#phone-more").click()
        item = phone.locator("#phone-enquetes")
        assert "lecture seule" in item.inner_text()
        item.click()
        phone.wait_for_selector("#eq-list .eq-item")
        assert phone.locator("#eq-new").is_hidden() and phone.locator("#eq-form").is_hidden()
        assert "12 000 tokens lus" in phone.locator("#eq-list .eq-item").inner_text()
        phone.locator("#eq-list .eq-item").click()
        phone.wait_for_selector("#eq-reader .mdoc")
        assert "Parce que." in phone.locator("#eq-reader").inner_text()
        assert phone.locator("#eq-bug").count() == 0 and "Sur l'ordinateur" in phone.locator("#eq-reader .eq-next").inner_text()
        assert phone.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1")
        assert phone.locator("#phone-more").get_attribute("aria-current") == "page"
        assert no_real_errors(phone) == []


def test_the_nickname_asked_once_then_in_parametres(tmp_path, page, monkeypatch):
    monkeypatch.setattr(server, "ASK_COMPUTER", True)
    with eq_server(tmp_path, monkeypatch) as s:
        page.goto(s.url + "#dashboard")
        page.wait_for_selector("#side")
        settled(page)
        assert page.locator("#computer-ask").is_hidden()
        page.evaluate("postRun('2_structure', 'f')")
        page.wait_for_selector("#computer-ask:not(.hidden)")
        assert "Comment appeler cet ordinateur ?" in page.locator("#computer-ask").inner_text()
        assert "à la place du nom de l'ordinateur sur le réseau" in page.locator("#computer-ask").inner_text()
        page.locator("#computer-ask-later").click()
        page.wait_for_selector("#computer-ask.hidden", state="attached")
        assert s.state.computer == {"name": "", "asked": True} and s.state.computer_label == "ordinateur"
        page.reload()
        page.wait_for_selector("#side")
        settled(page)
        assert page.locator("#computer-ask").is_hidden()
        page.goto(s.url + "#settings")
        page.wait_for_selector("#sec-computer")
        page.locator("#computer-name").fill("travail")
        page.locator("#btn-computer").click()
        page.wait_for_selector("#computer-msg.ok")
        assert s.state.computer == {"name": "travail", "asked": True}
        assert no_real_errors(page) == []
