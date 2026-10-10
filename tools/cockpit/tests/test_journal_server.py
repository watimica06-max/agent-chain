"""1.20 — the cycle journal through the server: a line per run of each kind
(a click, a programme's, « Continuer ») and each outcome; its commit
`journal: <command> — <outcome>` and its push; the stored relay still the
chain's after that commit (G-HEAD — failing without the fix); a line left
uncommitted committed alone before the next launch, never swept into the
command's `chore: answers`, and harmless when it is; the screen's data, the
reconstruction and the report written and committed only on confirmation;
the phone reads, never writes. Bare repositories play GitHub; no chain
command runs — the SDK client is a fake that commits as a command would."""
import asyncio
import json
import os
import subprocess

import pytest
from aiohttp import DummyCookieJar
from aiohttp.test_utils import TestClient, TestServer
from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock

import journal
import runner as runner_mod
import scan as scan_mod
import server
import stats as stats_mod
import sync
from state import State
from syncworld import app_world, head
from test_chain import git, write
from test_journal import QFILE
from test_runner import FakeClient, result
from test_server import post

F = "docs/features/f"


@pytest.fixture(autouse=True)
def journal_on(monkeypatch):
    monkeypatch.setattr(server, "JOURNAL", True)


def chain_like(repo, files, message, relay):
    """A fake command that does what a chain command does to git: its files
    committed, merged `--no-ff` from a worktree's commit, then its relay."""
    async def script(c):
        git(repo, "checkout", "-q", "-b", "wt-tmp")
        for rel, text in files:
            write(repo, rel, text)
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "-m", message)
        git(repo, "checkout", "-q", "master")
        git(repo, "merge", "--no-ff", "-q", "-m", f"Merge {c.prompts[0]}", "wt-tmp")
        git(repo, "branch", "-q", "-D", "wt-tmp")
        yield AssistantMessage(content=[TextBlock("Je travaille.")], model="m")
        yield result(f"Fait.\n{relay}")
    return script


def served(tmp_path, body, scripts, folder=None, store=True):
    remote, a, b = folder or app_world(tmp_path, "app")
    st = State(str(tmp_path / "config.json"))
    st.add_app(str(a))
    st.open_pair(str(a), "f")
    st.activate(str(a))
    queue = list(scripts)
    made = []

    def factory(cwd, can_use_tool, **kw):
        s = queue.pop(0) if queue else scripts[-1]
        c = FakeClient(s, can_use_tool)
        made.append(c)
        return c
    stx = stats_mod.Store(str(tmp_path / "stats.sqlite")) if store else None
    rn = runner_mod.Runner(client_factory=factory, on_end=server.make_on_end(st), mode_getter=lambda: st.mode,
                           log_dir=str(tmp_path / "logs"), stats=stx)
    app = server.make_app(st, rn, picker=lambda initial: str(a))

    async def go():
        async with TestClient(TestServer(app, host="127.0.0.1"), cookie_jar=DummyCookieJar()) as c:
            c.ctx = {"state": st, "rn": rn, "app": a, "remote": remote, "other": b, "made": made, "store": stx}
            return await body(c)
    return asyncio.run(go())


async def until(pred, timeout=20.0):
    for _ in range(int(timeout / 0.05)):
        v = pred()
        if v:
            return v
        await asyncio.sleep(0.05)
    raise AssertionError("jamais arrivé")


def subject(repo, ref="HEAD"):
    return git(repo, "log", "-1", "--format=%s", ref).strip()


async def run_and_journal(c, command="2_structure", args="f", **extra):
    a = c.ctx["app"]
    n = len(git(a, "log", "--format=%s", "--grep=^journal:").splitlines())
    r = await post(c, "/api/run", {"command": command, "args": args, **extra})
    assert r.status == 200, await r.text()
    assert await c.ctx["rn"].wait_ended(str(a), 10)
    await until(lambda: len(git(a, "log", "--format=%s", "--grep=^journal:").splitlines()) > n)
    return journal.read(journal.journal_path(str(a), "f"))


STRUCTURE = ("feat: f structure", [(f"{F}/produit.md", "# Produit\n"),
                                   (f"{F}/questions-redacteur-01.md", QFILE.format(a1="", a2=""))],
             "Next: answer questions, then run /2_structure f")


# ------------------------------------------------------------ §1 a line per run, committed

def test_a_line_per_run_committed_and_pushed(tmp_path):
    async def body(c):
        a = c.ctx["app"]
        rows = await run_and_journal(c)
        assert len(rows) == 1
        e = rows[0]
        assert e["command"] == "/2_structure f" and e["computer"] == journal.computer_name()
        assert e["outcome"] == journal.QUESTIONS and e["next"] == "répondre → /2_structure"
        assert e["created"] == ["questions-redacteur-01.md"] and e["duration_s"] is not None
        assert e["programme"] is None
        # Its commit: the journal alone, its subject, pushed.
        assert subject(a) == "journal: /2_structure f — questions"
        assert git(a, "show", "--name-only", "--format=", "HEAD").split() == [f"{F}/journal.md"]
        await until(lambda: git(c.ctx["remote"], "rev-parse", "master").strip() == head(a))
        assert git(a, "status", "--porcelain") == ""
        # The other computer sees it once it pulls.
        git(c.ctx["other"], "pull", "-q", "--ff-only")
        assert journal.read(journal.journal_path(str(c.ctx["other"]), "f")) == rows
    a_world = app_world(tmp_path, "app")
    a = a_world[1]
    served(tmp_path, body, [chain_like(a, STRUCTURE[1], STRUCTURE[0], STRUCTURE[2])], folder=a_world)


def test_a_push_that_fails_leaves_the_commit_to_the_next_launch(tmp_path):
    from syncworld import offline, online

    async def body(c):
        a, remote = c.ctx["app"], c.ctx["remote"]
        offline(a)
        rows = await run_and_journal(c)
        assert subject(a).startswith("journal: ") and len(rows) == 1
        assert git(remote, "rev-parse", "master").strip() != head(a)
        online(a, remote)
        # The next launch: « non envoyé » pushed first (1.12), the journal with it.
        await run_and_journal(c, "1_lexique")
        await until(lambda: git(remote, "rev-parse", "master").strip() == head(a))
    world = app_world(tmp_path, "app")
    a = world[1]
    served(tmp_path, body, [chain_like(a, STRUCTURE[1], STRUCTURE[0], STRUCTURE[2]),
                            chain_like(a, [(f"{F}/lexique.md", "# L\n")], "feat: lexique", "Next: run /2_structure f")],
           folder=world)


@pytest.mark.parametrize("fixed", [True, False])
def test_the_relay_stays_the_chains_after_the_journal_commit(tmp_path, monkeypatch, fixed):
    """G-HEAD drops a relay when HEAD moved without a run of the cockpit:
    the journal's commit must not count. Without the fix — the relay's HEAD
    not carried onto the journal's commit — the relay is dropped."""
    if not fixed:
        monkeypatch.setattr(State, "carry_relay_heads", lambda self, app, old, new: 0)

    async def body(c):
        a = c.ctx["app"]
        await run_and_journal(c)
        assert subject(a).startswith("journal: ")
        # « Où on en est ? »: the stored Next: is checked against the files.
        r = await post(c, "/api/check", {"reason": "bouton"})
        d = (await r.json())["decision"]
        if fixed:
            assert d["source"] == "chaine" and d["dropped"] is None, d.get("message")
            assert d["next"]["kind"] == "answer" and d["next"]["command"] == "2_structure"
            assert c.ctx["state"].relay(str(a), "f")["head"] == head(a)
        else:
            assert d["source"] == "dossier" and d["dropped"]["rule"] == "G-HEAD"
    world = app_world(tmp_path, "app")
    served(tmp_path, body, [chain_like(world[1], STRUCTURE[1], STRUCTURE[0], STRUCTURE[2])], folder=world)


def test_a_line_left_uncommitted_is_committed_alone_before_the_next_launch(tmp_path):
    """A journal line the cockpit could not commit — written, the commit
    failed — would be swept into the next command's `chore: answers` (its
    `git add docs/features/<name>/`). It is committed alone first."""
    def answers_then_work(repo):
        async def script(c):
            # cmd/*.md: `git add docs/features/<name>/ && git commit -m "chore: answers"`
            git(repo, "add", f"{F}/")
            if git(repo, "status", "--porcelain", f"{F}/").strip():
                git(repo, "commit", "-q", "-m", "chore: answers")
            yield result("Fait.\nNext: run /3_decoupe f")
        return script

    async def body(c):
        a = c.ctx["app"]
        await run_and_journal(c)
        # The next line could not be committed: it sits on the disk.
        journal.append(journal.journal_path(str(a), "f"), {
            "at": "2026-10-10T12:00", "computer": "AUTRE", "command": "/2_structure f", "outcome": "fait",
            "next": "/3_decoupe"}, "f")
        # And she answered a question meanwhile.
        q = a / F / "questions-redacteur-01.md"
        q.write_text(q.read_text(encoding="utf-8").replace("Answer:\n", "Answer: Oui\n", 1), encoding="utf-8")
        s = await (await c.get("/api/state")).json()
        assert s["answers_pending"] == 1                    # the journal line is no answer
        await run_and_journal(c, "1_lexique")
        log = git(a, "log", "--format=%s", "-6").splitlines()
        i_pending = log.index(journal.PENDING_MESSAGE)
        i_answers = log.index("chore: answers")
        assert i_pending > i_answers                        # committed before the command's own
        pending = git(a, "log", "-1", "--format=%H", f"--grep=^{journal.PENDING_MESSAGE}$").strip()
        assert git(a, "show", "--name-only", "--format=", pending).split() == [f"{F}/journal.md"]
        ans = git(a, "log", "-1", "--format=%H", "--grep=^chore: answers$").strip()
        assert git(a, "show", "--name-only", "--format=", ans).split() == [f"{F}/questions-redacteur-01.md"]
        assert [e["computer"] for e in journal.read(journal.journal_path(str(a), "f"))][1] == "AUTRE"
        assert git(a, "status", "--porcelain") == ""
    world = app_world(tmp_path, "app")
    served(tmp_path, body, [chain_like(world[1], STRUCTURE[1], STRUCTURE[0], STRUCTURE[2]),
                            answers_then_work(world[1])], folder=world)


def test_a_line_swept_into_chore_answers_is_harmless(tmp_path):
    """A command run outside the cockpit sweeps an uncommitted line into its
    `chore: answers`: the line is in history all the same, the scan, the
    questions and « Envoyer mes réponses » read nothing of it, and no
    agent's file names it."""
    _, a, _ = app_world(tmp_path, "app")
    before = scan_mod.run_scan(str(a), "f")
    path = journal.journal_path(str(a), "f")
    journal.append(path, {"at": "2026-10-10T12:00", "computer": "PC", "command": "/1_lexique f",
                          "outcome": "questions", "next": "répondre → /1_lexique",
                          "created": ["questions-lexicographe-01.md"]}, "f")
    assert sync.answers_pending(str(a), "f") == 0
    sha = sync.commit_answers(str(a), "f")
    assert sha and git(a, "show", "--name-only", "--format=", "HEAD").split() == [f"{F}/journal.md"]
    after = scan_mod.run_scan(str(a), "f")
    assert after["proposal"] == before["proposal"] and after["opens"] == before["opens"]
    assert journal.read(path)[0]["command"] == "/1_lexique f"
    h = journal.history(str(a), "f")
    assert [q["file"] for q in h["questions"]] == ["questions-lexicographe-01.md"] and not h["blocking"]
    # No agent of the chain reads the journal: none names it.
    chain_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    for sub in ("agents", "commands", "formats", "grids"):
        d = os.path.join(chain_root, ".claude", sub)
        for root, _dirs, files in os.walk(d):
            for name in files:
                with open(os.path.join(root, name), encoding="utf-8", errors="replace") as fh:
                    assert "journal.md" not in fh.read(), os.path.join(root, name)


# ------------------------------------------------------------ each kind, each outcome

async def raises(c):
    yield AssistantMessage(content=[TextBlock("Je commence.")], model="m")
    raise RuntimeError("le processus de Claude Code s'est arrêté")


async def not_signed_in(c):
    yield AssistantMessage(content=[TextBlock("Not logged in · Please run /login")], model="<synthetic>",
                           error="authentication_failed")
    yield ResultMessage(subtype="success", duration_ms=1, duration_api_ms=0, is_error=True, num_turns=1,
                        session_id="s", result="Not logged in · Please run /login")


async def no_next(c):
    yield result("J'ai fini sans ligne Next.")


async def goes_on(c):
    yield result("Fait.\nNext: run /3_decoupe f")


async def waits(c):
    yield AssistantMessage(content=[TextBlock("Je travaille longtemps.")], model="m")
    await c.interrupted.wait()
    yield result("", terminal_reason="aborted_streaming")


def test_each_kind_and_outcome_gets_its_line(tmp_path):
    async def body(c):
        a, rn = c.ctx["app"], c.ctx["rn"]
        rows = await run_and_journal(c, "1_lexique")
        assert rows[-1]["outcome"] == journal.ERROR and "s'est arrêté" in rows[-1]["note"]
        assert subject(a) == "journal: /1_lexique f — erreur"
        rows = await run_and_journal(c, "1_lexique")
        assert rows[-1]["outcome"] == journal.NOT_LOGGED
        rows = await run_and_journal(c, "1_lexique")
        assert rows[-1]["outcome"] == journal.NO_NEXT
        # « Continuer »: the same session, a line of its own.
        n = len(rows)
        r = await post(c, "/api/continue-session", {})
        assert r.status == 200, await r.text()
        assert await rn.wait_ended(str(a), 10)
        await until(lambda: subject(a) == "journal: /1_lexique f — fait")
        rows = journal.read(journal.journal_path(str(a), "f"))
        assert len(rows) == n + 1 and rows[-1]["note"] == "suite de session" and rows[-1]["outcome"] == journal.DONE
        # Stopped: « Arrêter maintenant ».
        r = await post(c, "/api/run", {"command": "2_structure", "args": "f"})
        assert r.status == 200
        await until(lambda: c.ctx["made"][-1].prompts)
        await post(c, "/api/stop-now", {})
        assert await rn.wait_ended(str(a), 10)
        await until(lambda: subject(a) == "journal: /2_structure f — arrêté")
        rows = journal.read(journal.journal_path(str(a), "f"))
        assert rows[-1]["outcome"] == journal.STOPPED
        assert [e["command"] for e in rows] == ["/1_lexique f"] * 4 + ["/2_structure f"]
    served(tmp_path, body, [raises, not_signed_in, no_next, goes_on, waits])


def test_lancer_quand_meme_said_in_the_line(tmp_path):
    from test_usage import add_both

    async def body(c):
        add_both(c.ctx["store"], 0.95, 0.30)
        r = await post(c, "/api/run", {"command": "1_lexique", "args": "f"})
        assert r.status == 409
        rows = await run_and_journal(c, "1_lexique", usage_ok=True)
        assert rows[-1]["note"] == journal.OVERRIDE_NOTE
    served(tmp_path, body, [goes_on])


def test_a_programmes_lines_carry_its_name(tmp_path, monkeypatch):
    """The programme's commands, each its line, its name on each; the next
    command waits for the last one's line."""
    import autopilot as ap
    from test_pilot_server import CHAIN, chain_script, ended, served as pilot_served

    async def body(c):
        r = await post(c, "/api/pilot/start", {"preset": "besoin"})
        assert r.status == 200, await r.text()
        await ended(c)
        a = c.ctx["app"]
        path = journal.journal_path(str(a), "f")
        await until(lambda: len(journal.read(path)) == 3)
        rows = journal.read(path)
        assert [e["command"] for e in rows] == ["/1_lexique f", "/2_structure f", "/3_decoupe f"]
        assert {e["programme"] for e in rows} == {"Maintenant, jusqu'à ce qu'on ait besoin de moi"}
        assert [e["outcome"] for e in rows] == [journal.DONE, journal.DONE, journal.QUESTIONS]
    pilot_served(tmp_path, body, chain_script(CHAIN), monkeypatch=monkeypatch)


# ------------------------------------------------------------ the screen's data, §2–§4

def test_the_screen_reconstruction_and_report_committed_only_on_confirmation(tmp_path):
    async def body(c):
        a = c.ctx["app"]
        # Before 1.20: one run, its merge — in git alone.
        chain_like_now(a)
        j = await (await c.get("/api/journal")).json()
        assert j["exists"] is False and j["entries"] == [] and j["cycles"] == ["main"]
        assert [q["file"] for q in j["questions"]] == ["questions-lexicographe-01.md", "questions-decoupeur-01.md"]
        before = head(a)
        r = await post(c, "/api/journal/reconstruct", {})
        rec = await r.json()
        assert r.status == 200 and rec["count"] == 1 and not rec["committed"]
        assert "/3_decoupe f" in rec["preview"]["main"][0] and "reconstitué de git seul" in rec["preview"]["main"][0]
        assert head(a) == before and not os.path.exists(journal.journal_path(str(a), "f"))
        r = await post(c, "/api/journal/reconstruct", {"confirm": True})
        out = await r.json()
        assert r.status == 200 and out["committed"] and out["commit"]
        assert subject(a) == "journal: reconstitution du passé (1 lignes)"
        assert git(c.ctx["remote"], "rev-parse", "master").strip() == head(a)
        # Once: nothing left to build.
        assert (await (await post(c, "/api/journal/reconstruct", {})).json())["count"] == 0
        # The report: shown, not written; then written and committed.
        r = await post(c, "/api/journal/report", {})
        rep = await r.json()
        assert rep["preview"].startswith("# Rapport de fin de cycle — f") and not rep["committed"]
        assert not os.path.exists(journal.report_path(str(a), "f"))
        h = head(a)
        r = await post(c, "/api/journal/report", {"confirm": True})
        rep = await r.json()
        assert r.status == 200 and rep["committed"] and subject(a) == journal.REPORT_MESSAGE
        assert git(a, "show", "--name-only", "--format=", "HEAD").split() == [f"{F}/rapport-cycle.md"]
        assert head(a) != h
        j = await (await c.get("/api/journal")).json()
        assert j["report_exists"] and len(j["entries"]) == 1 and j["totals"]["runs"] == 1
        # The thresholds of Paramètres.
        r = await post(c, "/api/journal/thresholds", {"thresholds": {"repeat_runs": 4}})
        assert r.status == 200 and (await r.json())["thresholds"]["repeat_runs"] == 4
        r = await post(c, "/api/journal/thresholds", {"thresholds": {"repeat_runs": 0}})
        assert r.status == 400
    served(tmp_path, body, [goes_on])


def chain_like_now(repo):
    git(repo, "checkout", "-q", "-b", "wt-old")
    write(repo, f"{F}/questions-decoupeur-01.md", QFILE.format(a1="", a2=""))
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "feat: decoupe")
    git(repo, "checkout", "-q", "master")
    git(repo, "merge", "--no-ff", "-q", "-m", "Merge /3_decoupe f", "wt-old")
    git(repo, "push", "-q")


def test_the_phone_reads_the_journal_and_writes_nothing(tmp_path):
    from test_phone import ph_headers, login, turn_on

    async def body(c):
        await turn_on(c)
        cookie = await login(c)
        r = await c.get("/api/journal", headers=ph_headers(cookie=cookie, origin=None))
        assert r.status == 200 and "entries" in await r.json()
        for path in ("/api/journal/reconstruct", "/api/journal/report", "/api/journal/thresholds"):
            r = await c.post(path, data=json.dumps({"confirm": True}),
                             headers={"Content-Type": "application/json", **ph_headers(cookie=cookie)})
            assert r.status == 403, (path, r.status, await r.text())
            assert (await r.json())["error"] == "sur l'ordinateur", path
    served(tmp_path, body, [goes_on])
