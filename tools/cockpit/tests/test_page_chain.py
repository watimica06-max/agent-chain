"""§20 on the page: the dashboard's line, the banner, a launch that asks
first, and Paramètres → « Installer / mettre à jour la chaîne ». The chain's
state and the install are stubs here; test_chain.py runs the real ones."""
import pytest

pytest.importorskip("playwright")

import chain  # noqa: E402
import server  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from test_page import browser, page  # noqa: E402,F401

BEHIND = {"state": "en retard", "summary": "Chaîne en retard de 2 commits — installée : abc1234 du 2026-10-01",
          "commit": "abc1234", "date": "2026-10-01", "chain_commit": "def5678", "chain_date": "2026-10-06",
          "behind": 2, "subjects": ["def5678 Chaîne — deux", "bcd3456 Chaîne — un"], "modified": []}
UP = {**BEHIND, "state": "à jour", "summary": "Chaîne à jour — def5678 du 2026-10-06", "commit": "def5678",
      "behind": None, "subjects": []}


def test_not_up_to_date_shows_and_asks(tmp_path, page, monkeypatch):
    now = {"st": BEHIND}
    monkeypatch.setattr(server, "chain_state", lambda app: now["st"])
    with FakeServer(tmp_path) as s:
        page.goto(s.url + "#dashboard")
        page.wait_for_selector("#chain-banner", state="visible")
        assert BEHIND["summary"] in page.locator("#chain-banner").inner_text()
        assert page.locator("#chain-line").inner_text() == BEHIND["summary"]
        page.goto(s.url + "#settings")
        page.reload()
        page.wait_for_selector("#set-chain li")
        assert page.locator("#set-chain li").all_inner_texts() == BEHIND["subjects"]

        # A launch asks first: dismissed, nothing runs; accepted, it runs.
        asked = []

        def answer(d):
            asked.append(d.message)
            d.accept() if "Lancer quand même" not in d.message or len(asked) > 2 else d.dismiss()
        page.on("dialog", answer)
        page.locator("#set-commands button", has_text="/1_lexique").click()
        page.wait_for_timeout(500)
        assert any(BEHIND["summary"] in m for m in asked)
        assert not s.rn.is_running(str(s.app_root))
        page.locator("#set-commands button", has_text="/1_lexique").click()
        page.wait_for_function("document.querySelector('#tb-run').classList.contains('running')", timeout=8000)
        assert s.rn.is_running(str(s.app_root))
        s.call(s.rn.stop_now(str(s.app_root)))


def test_the_install_button_asks_before_overwriting(tmp_path, page, monkeypatch):
    now = {"st": {**BEHIND, "state": "modifiée sur place", "summary": "Chaîne modifiée sur place — 1 fichier : .claude/agents/a.md",
                  "modified": [".claude/agents/a.md"], "subjects": []}}
    monkeypatch.setattr(server, "chain_state", lambda app: now["st"])
    calls = []

    def fake_install(app, root, confirm=False, push=True):
        calls.append(confirm)
        if not confirm:
            raise chain.NeedsConfirm([".claude/agents/a.md"])
        now["st"] = UP
        return {"commit": "def5678", "date": "2026-10-06", "written": [".claude/agents/a.md"], "removed": [],
                "app_commit": "9a9a9a9", "message": "chain: def5678 2026-10-06", "pushed": True, "push_error": None}
    monkeypatch.setattr(server.chain_mod, "install", fake_install)
    with FakeServer(tmp_path) as s:
        page.goto(s.url + "#settings")
        page.wait_for_selector("#set-chain li")
        assert page.locator("#set-chain li").all_inner_texts() == [".claude/agents/a.md"]
        asked = []
        page.on("dialog", lambda d: (asked.append(d.message), d.accept()))
        page.locator("#btn-chain").click()
        page.wait_for_function("document.querySelector('#chain-msg').textContent.includes('Installée')", timeout=8000)
        assert calls == [False, True] and ".claude/agents/a.md" in asked[0]
        assert "chain: def5678 2026-10-06" in page.locator("#chain-msg").inner_text()
        page.wait_for_selector("#chain-banner", state="hidden")
        assert page.locator("#chain-line").inner_text() == UP["summary"]
