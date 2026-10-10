"""1.12 — GitHub on the page, in a headless browser (Microsoft Edge through
Playwright): each state on its home row, the alerts and their buttons, the
state in the top bar, a launch refused when diverged, « Réconcilier » on a
conflict, « Envoyer », « Envoyer mes réponses », a run whose final push was
refused, a private file not on this computer, the long paths, « Ajouter
depuis GitHub ». Skipped when Playwright or Edge is missing. GitHub is a
bare repository in a temporary folder; no chain command runs."""
import pytest

pytest.importorskip("playwright")

import server  # noqa: E402
import sync  # noqa: E402
from claude_agent_sdk import AssistantMessage, TextBlock  # noqa: E402
from copies import built_once  # noqa: E402
from donneesworld import data_world  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from syncworld import app_world, change, head, offline  # noqa: E402
from test_chain import commit, git  # noqa: E402
from test_page import page, settled  # noqa: E402,F401
from test_runner import result  # noqa: E402

Q = "docs/features/f/questions-lexicographe-01.md"


def answer(repo, text="oui"):
    p = repo / Q
    p.write_bytes(p.read_bytes().replace(b"Answer:\n", f"Answer: {text}\n".encode(), 1))


@pytest.fixture
def five(tmp_path):
    """One application per state: à jour, en retard, non envoyé with an
    answer not committed, divergé on one same file, injoignable. Built once
    per run, copied here (copies.py)."""
    return built_once("five", tmp_path, _five)


def _five(tmp_path):
    apps = {}
    _, apps["Hyrox"], apps["hyrox_b"] = app_world(tmp_path, "hyrox")
    _, apps["Belivo"], b = app_world(tmp_path, "belivo")
    change(b, "README.md", "B\n", push=True)
    apps["remote_carnet"], apps["Carnet"], _ = app_world(tmp_path, "carnet")
    change(apps["Carnet"], "notes.md", "notes\n")
    answer(apps["Carnet"])
    _, apps["Budget"], b = app_world(tmp_path, "budget")
    change(b, "README.md", "B\n", push=True)
    answer(apps["Budget"])
    answer(apps["Budget"], "l'itinéraire")
    change(apps["Budget"], "README.md", "A\n")
    _, apps["Velo"], _ = app_world(tmp_path, "velo")
    offline(apps["Velo"])
    return apps


def serve_five(tmp_path, apps, **kw):
    s = FakeServer(tmp_path / "srv", opened=False, **kw)
    for name in ("Hyrox", "Belivo", "Carnet", "Budget", "Velo"):
        s.state.add_app(str(apps[name]))
        s.state.rename_app(str(apps[name]), name)
        s.state.open_pair(str(apps[name]), "f")
    return s


def page_errors(page):
    """The page's errors — a refusal the server answers 409 is not one."""
    return [e for e in page.js_errors if "status of 409" not in e and "Failed to fetch" not in e and "net::ERR" not in e]


def row(page, name):
    return page.locator(f'.home-card[data-name="{name}"]')


def chip(page):
    return " ".join(page.locator("#tb-sync").text_content().split())


def open_app(page, s, name):
    page.goto(s.url)
    row(page, name).click()
    page.wait_for_function("n => document.getElementById('side-name').textContent === n && S.app_name === n", arg=name)
    page.wait_for_function("document.getElementById('next-text').textContent !== '—'")


def test_home_rows_top_bar_and_alerts(tmp_path, page, five):
    with serve_five(tmp_path, five) as s:
        page.goto(s.url)
        page.wait_for_selector(".home-card .hc-sync .cst")
        got = {n: row(page, n).locator(".hc-sync .cst").inner_text() for n in ("Hyrox", "Belivo", "Carnet", "Budget", "Velo")}
        assert got == {"Hyrox": "à jour", "Belivo": "en retard", "Carnet": "non envoyé", "Budget": "divergé",
                       "Velo": "GitHub injoignable"}
        assert page.locator(".apps-head").inner_text().count("GitHub") == 1
        assert "rien de non commité" in row(page, "Hyrox").inner_text()
        assert "1 fichier non commité" in row(page, "Carnet").inner_text()
        # The alerts on the rows, with what settles each.
        assert row(page, "Carnet").locator("button.sync-push").is_visible()
        assert row(page, "Carnet").locator("button.sync-answers").is_visible()
        assert row(page, "Budget").locator("button.sync-reconcile").is_visible()
        # 1.14: « en retard » — « Récupérer », GitHub's version without launching.
        assert row(page, "Belivo").locator(".hc-alert > div").count() == 1
        assert row(page, "Belivo").locator("button.sync-pull").is_visible()
        for n in ("Hyrox", "Velo"):
            assert row(page, n).locator(".hc-alert > div").count() == 0, n
        # The top bar: hidden « à jour », said otherwise.
        open_app(page, s, "Hyrox")
        settled(page)
        assert not page.locator("#tb-sync").is_visible()
        open_app(page, s, "Budget")
        page.wait_for_function("document.getElementById('tb-sync').textContent.includes('divergé')")
        assert chip(page) == "GitHub : divergé"
        assert page.locator("#alerts .sync-alert button.sync-reconcile").is_visible()
        open_app(page, s, "Velo")
        page.wait_for_function("document.getElementById('tb-sync').textContent.includes('injoignable')")
        assert chip(page) == "GitHub : injoignable" and page.locator("#tb-sync").is_visible()
        assert not page_errors(page), page.js_errors


def test_launch_refused_when_diverged_then_reconcile_conflict(tmp_path, page, five):
    budget = five["Budget"]
    mine = head(budget)
    with serve_five(tmp_path, five) as s:
        open_app(page, s, "Budget")
        page.locator("#next-detail button.primary").click()
        page.wait_for_selector("#sync-banner:not(.hidden)")
        assert "Rien n'a été lancé" in page.locator("#sync-banner").inner_text()
        assert s.rn.going() is None
        page.locator("#sync-banner button.sync-reconcile").click()
        page.wait_for_selector("#sync-banner .conflict", timeout=30000)
        text = page.locator("#sync-banner").inner_text()
        assert "README.md" in text and "Claude Code" in text and "rien n'a changé" in text.lower()
        assert head(budget) == mine
        assert chip(page) == "GitHub : divergé"
        assert not page_errors(page), page.js_errors


def test_envoyer_from_the_row(tmp_path, page, five):
    carnet, remote = five["Carnet"], five["remote_carnet"]
    with serve_five(tmp_path, five) as s:
        page.goto(s.url)
        row(page, "Carnet").locator("button.sync-push").click()
        page.wait_for_function("document.querySelector('.home-card[data-name=\"Carnet\"] .hc-sync .cst')"
                               ".textContent === 'à jour'", timeout=30000)
        assert git(remote, "rev-parse", "master").strip() == head(carnet)
        assert "envoyé à GitHub" in page.locator("#sync-banner").inner_text()
        assert not page_errors(page), page.js_errors


def test_send_my_answers_on_a_repondre(tmp_path, page, five):
    carnet, remote = five["Carnet"], five["remote_carnet"]
    with serve_five(tmp_path, five) as s:
        open_app(page, s, "Carnet")
        page.goto(s.url + "#answer")
        page.wait_for_selector("#answers-send:not(.hidden)")
        assert "1 fichier de docs/features/f/" in page.locator("#answers-pending").inner_text()
        page.locator("#btn-send-answers").click()
        page.wait_for_selector("#answers-msg:not(:empty)", timeout=30000)
        assert "chore: answers" in page.locator("#answers-msg").inner_text()
        assert "envoyé à GitHub" in page.locator("#answers-msg").inner_text()
        page.wait_for_selector("#answers-send.hidden", state="attached")
        assert git(carnet, "log", "-1", "--format=%s").strip() == "chore: answers"
        assert git(remote, "rev-parse", "master").strip() == head(carnet)
        assert not page_errors(page), page.js_errors


def test_send_my_answers_from_the_row(tmp_path, page, five):
    budget = five["Budget"]
    answer_file = budget / "docs" / "features" / "f" / "idees.md"
    answer_file.write_text("# Idées\n\nUne réponse de plus.\n", encoding="utf-8")
    with serve_five(tmp_path, five) as s:
        page.goto(s.url)
        row(page, "Budget").locator("button.sync-answers").click()
        page.wait_for_selector("#sync-banner:not(.hidden)", timeout=30000)
        # Diverged: committed here, not sent — and « Réconcilier » offered.
        assert "divergé" in page.locator("#sync-banner").inner_text()
        assert page.locator("#sync-banner button.sync-reconcile").is_visible()
        assert git(budget, "log", "-1", "--format=%s").strip() == "chore: answers"
        assert not page_errors(page), page.js_errors


def test_run_whose_final_push_was_refused(tmp_path, page, five):
    hyrox, other = five["Hyrox"], five["hyrox_b"]

    async def rejected(c):
        change(hyrox, "docs/features/f/lexique.md", "# Lexique\n", "lexique: f")
        change(other, "README.md", "B\n", push=True)
        yield AssistantMessage(content=[TextBlock("git push : rejected")], model="m")
        yield result("Fait.\nNext: done")

    with serve_five(tmp_path, five, script=rejected) as s:
        open_app(page, s, "Hyrox")
        page.goto(s.url + "#chaine")
        page.wait_for_selector("#flow-main li.step")
        s.call(s.rn.start(str(hyrox), "f", "f", "1_lexique", "f"))
        page.wait_for_selector("#run-end .run-sync.bad", timeout=30000)
        text = page.locator("#run-end .run-sync").inner_text()
        assert "n'a pas abouti" in text and "Divergé" in text
        assert page.locator("#run-end button.sync-reconcile").is_visible()
        assert not page_errors(page), page.js_errors


def test_long_paths_and_add_from_github(tmp_path, page, five):
    remote, _, _ = app_world(tmp_path, "plan")
    parent = tmp_path / "second"
    parent.mkdir()
    git(five["Hyrox"], "config", "--local", "core.longpaths", "true")
    with serve_five(tmp_path, five) as s:
        open_app(page, s, "Hyrox")
        page.goto(s.url + "#settings")
        page.wait_for_selector("#longpaths li")
        assert page.locator('#longpaths li[data-folder$="hyrox\\\\A"] button.lp-set').count() == 0
        belivo = page.locator("#longpaths li", has_text="Belivo")
        assert "core.longpaths absent" in belivo.inner_text()
        belivo.locator("button.lp-set").click()
        page.wait_for_function("[...document.querySelectorAll('#longpaths li')].find(l => l.textContent.includes('Belivo'))"
                               ".textContent.includes('core.longpaths=true')")
        assert sync.long_paths(str(five["Belivo"])) is True
        page.goto(s.url)
        page.locator("#btn-app-clone").click()
        page.locator("#clone-url").fill(str(remote))
        page.locator("#clone-parent").fill(str(parent))
        assert page.locator("#clone-path").inner_text() == str(parent / "app")
        page.locator("#btn-clone").click()
        page.wait_for_selector('.home-card[data-name="app"]', timeout=30000)
        assert "clonée" in page.locator("#apps-msg").inner_text()
        assert sync.long_paths(str(parent / "app")) is True
        assert not page_errors(page), page.js_errors


def test_private_file_not_on_this_computer(tmp_path, page, monkeypatch):
    monkeypatch.setattr(server, "DONNEES_PUSH", False)
    with FakeServer(tmp_path) as s:
        data_world(s.app_root, question=False)
        feat = s.app_root / "docs" / "features" / "f" / "donnees"
        (feat / "donnees.md").write_bytes((feat / "donnees.md").read_bytes() + (
            "\n## compte-joint.csv\nWhat: the joint account\nSource: the bank\nDate: 2026-10-07\nPrivate: yes\n"
        ).encode("utf-8"))
        (s.app_root / ".gitignore").write_bytes(
            "build/\n\n# Données privées — .claude/formats/donnees.md\ndocs/features/f/donnees/compte-joint.csv\n".encode())
        commit(s.app_root, "private")
        page.goto(s.url + "#donnees")
        page.get_by_role("tab", name="De la fonctionnalité").click()
        r = page.locator("#dn-list tr[data-name='compte-joint.csv']")
        r.wait_for()
        assert "pas sur cet ordinateur" in r.inner_text() and "fichier absent" not in r.inner_text()
        page.locator("#dn-list tr[data-name='releve-2026-09-14.csv'] button.dn-edit").click()
        page.locator("#dn-list tr[data-name='releve-2026-09-14.csv'] textarea, "
                     "#dn-list tr[data-name='releve-2026-09-14.csv'] input[name=what]").first.fill("a statement, edited")
        page.locator("#dn-save").click()
        page.wait_for_function("document.getElementById('dn-msg').textContent.includes('Enregistré')")
        assert "compte-joint.csv" in (feat / "donnees.md").read_text(encoding="utf-8")
        assert not page_errors(page), page.js_errors
