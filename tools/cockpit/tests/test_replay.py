"""Cockpit 1.5, §0 — a page reopened during a run picks up where it stands:
its stream so far rebuilt from the run's log, its current agent, a
permission card that came while no page was open. Fake SDK client; no
chain command runs."""
import asyncio

import pytest

import runner as runner_mod
from test_runner import make_runner, next_event, script_with_permission

MESSAGE_EVENTS = {"text", "tool", "agent_started", "agent_background", "agent_ended"}


def test_the_log_gives_the_same_events_as_the_live_stream(tmp_path):
    async def go():
        rn, _ = make_runner(script_with_permission)
        rn.log_dir = str(tmp_path / "logs")
        q = rn.subscribe(str(tmp_path))
        run = await rn.start(str(tmp_path), "f", "f", "1_lexique", "f")
        perm = await next_event(q, "permission")
        # No page open: the run waits on the card, without limit.
        await asyncio.sleep(0.3)
        assert run.status == "running" and run.permissions
        mid, dropped = rn.replay(str(tmp_path))
        live = [(e["type"], e["data"]) for e in run.events if e["type"] in MESSAGE_EVENTS]
        assert dropped == 0
        assert [(e["type"], e["data"]) for e in mid if e["type"] in MESSAGE_EVENTS] == live
        # The card is in the replay, beside the log's events, in time order.
        assert [e["type"] for e in mid] == ["run_started", "status", "text", "agent_started", "text", "tool",
                                           "permission"]
        rn.answer_permission(str(tmp_path), perm["data"]["id"], True)
        await run.task
        end, _ = rn.replay(str(tmp_path))
        live = [(e["type"], e["data"]) for e in run.events if e["type"] in MESSAGE_EVENTS]
        assert [(e["type"], e["data"]) for e in end if e["type"] in MESSAGE_EVENTS] == live
        assert end[-1]["type"] == "run_ended"
        return run
    asyncio.run(go())


def test_a_long_run_is_cut_to_what_the_page_keeps(tmp_path, monkeypatch):
    monkeypatch.setattr(runner_mod, "REPLAY_MAX", 4)

    async def go():
        rn, _ = make_runner(script_with_permission)
        rn.log_dir = str(tmp_path / "logs")
        q = rn.subscribe(str(tmp_path))
        run = await rn.start(str(tmp_path), "f", "f", "1_lexique", "f")
        perm = await next_event(q, "permission")
        rn.answer_permission(str(tmp_path), perm["data"]["id"], True)
        await run.task
        evs, dropped = rn.replay(str(tmp_path))
        assert len(evs) == 4 and dropped > 0 and evs[-1]["type"] == "run_ended"
    asyncio.run(go())


# ------------------------------------------------------- in a headless browser

pytest.importorskip("playwright")
from playwright.sync_api import sync_playwright  # noqa: E402

from fakeapp import FakeServer  # noqa: E402


@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        try:
            b = p.chromium.launch(channel="msedge")
        except Exception as e:
            pytest.skip(f"Edge indisponible : {e}")
        yield b
        b.close()


def test_a_page_opened_during_a_run_shows_its_stream_its_agent_and_the_waiting_card(tmp_path, browser):
    with FakeServer(tmp_path) as s:
        # The run starts with no page open, and waits on a permission card.
        s.call(s.rn.start(str(s.app_root), "f", "f", "1_lexique", "f"))
        for _ in range(50):
            if s.rn.current(str(s.app_root)).permissions:
                break
            import time
            time.sleep(0.1)
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(s.url + "#chaine")
        page.wait_for_selector("#perm-banner .perm", timeout=8000)
        page.wait_for_function("document.getElementById('stream').textContent.includes('Je balaie idees.md.')")
        stream = page.locator("#stream").inner_text()
        assert "▶ /1_lexique f" in stream and "→ lexicographe" in stream and "Je lance le lexicographe." in stream
        assert page.locator("#agents .badge").all_inner_texts() == ["lexicographe"]
        # The title counts what waits: the folder's open entries and the card.
        page.wait_for_function("F !== null")
        n = page.evaluate("openCount()") + 1
        assert page.title() == f"({n}) Cockpit"
        # Answered from the reopened page: the run goes on, the agent hands back, its badge goes.
        page.locator("#perm-banner").get_by_role("button", name="Autoriser").click()
        page.wait_for_function("document.getElementById('stream').textContent.includes('a rendu la main')")
        page.wait_for_function("document.querySelectorAll('#agents .badge').length === 0")
        # Reopened once more after the end: the same stream, once.
        page.reload()
        page.wait_for_function("document.getElementById('stream').textContent.includes('■ Fin')")
        assert page.locator("#stream").inner_text().count("Je balaie idees.md.") == 1
        assert errors == []
        page.close()
