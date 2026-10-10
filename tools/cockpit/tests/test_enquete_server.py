"""1.21 — « Enquêtes » through the server. §1: every write, commit, push,
deletion and web call refused, the reading tools and commands allowed; 1.17's
threshold; one run at a time, an investigation included; the automatic pilot
never launches one. §2: the report written, committed and pushed in the
repository it concerns; a commit of docs/enquetes/ alone in agent-chain
neither restarts the server nor says « pas encore en service ». §3: the
question written from each kind of point and from a failed run. §4: the
correction prompt marked « à relire », never launched; the bug entry in the
Diagnostiqueur's format, written on confirmation only. §0: no repository
write holds the computer's network name. Bare repositories play GitHub; the
SDK client is a fake (enqueteworld.py)."""
import asyncio
import os
import re
import socket
import time
from datetime import datetime

import pytest
from aiohttp import DummyCookieJar
from aiohttp.test_utils import TestClient, TestServer

import enquete
import journal
import runner as runner_mod
import selfupdate
import server
import stats as stats_mod
import startup
import sync
from enqueteworld import ANSWER, READS, SONNET, WRITES, Factory, answering, saying, until_cancelled
from state import State
from syncworld import app_world, change, head
from test_chain import git, write
from test_runner import FakeClient, result
from test_server import post
from test_usage import add_both

TODAY = datetime.now().strftime("%Y-%m-%d")
Q = "Pourquoi l'écran de course remet-il le chrono à zéro ?"


def run_script(gate=None):
    async def script(c):
        if gate is not None:
            await gate.wait()
        yield result("Fait.\nNext: run /2_structure f")
    return script


def served(tmp_path, body, factory, world=None, script=None, store=True):
    remote, a, b = world or app_world(tmp_path, "app")
    st = State(str(tmp_path / "config.json"))
    st.add_app(str(a))
    st.open_pair(str(a), "f")
    st.activate(str(a))
    stx = stats_mod.Store(str(tmp_path / "stats.sqlite")) if store else None
    rn = runner_mod.Runner(client_factory=lambda cwd, cut, **kw: FakeClient(script or run_script(), cut),
                           on_end=server.make_on_end(st), mode_getter=lambda: st.mode,
                           log_dir=str(tmp_path / "logs"), stats=stx)
    inv = enquete.Investigator(stx, str(tmp_path / "logs"), client_factory=factory)
    app = server.make_app(st, rn, picker=lambda initial: str(a), investigator=inv)

    async def go():
        async with TestClient(TestServer(app, host="127.0.0.1"), cookie_jar=DummyCookieJar()) as c:
            c.ctx = {"state": st, "rn": rn, "app": a, "remote": remote, "other": b, "store": stx, "inv": inv,
                     "server_app": app, "factory": factory}
            return await body(c)
    return asyncio.run(go())


async def until(pred, timeout=20.0):
    for _ in range(int(timeout / 0.05)):
        v = pred()
        if v:
            return v
        await asyncio.sleep(0.05)
    raise AssertionError("jamais arrivé")


async def start(c, question=Q, target="application", **kw):
    r = await post(c, "/api/enquetes/start", {"question": question, "target": target, **kw})
    return r.status, await r.json()


async def finished(c):
    inv = c.ctx["inv"]
    await until(lambda: inv.current and inv.current.status == "ended" and (
        inv.current.outcome != "terminé" or inv.current.report is not None))
    return inv.current


def subject(repo, ref="HEAD"):
    return git(repo, "log", "-1", "--format=%s", ref).strip()


@pytest.fixture(autouse=True)
def _never_the_real_chain(tmp_path, monkeypatch):
    """agent-chain's reports are never this computer's: an empty scratch
    folder, unless the test builds its own scratch clone (chain_root)."""
    d = tmp_path / "pas-d-agent-chain"
    d.mkdir()
    monkeypatch.setattr(server, "CHAIN_ROOT", str(d))


@pytest.fixture
def chain_root(tmp_path, monkeypatch):
    """agent-chain: a scratch clone on a bare GitHub, never this computer's."""
    from selfupdateworld import chain_world
    remote, here, other = chain_world(tmp_path)
    monkeypatch.setattr(server, "CHAIN_ROOT", str(here))
    return remote, here, other


# ------------------------------------------------------------------ §1 read-only

def test_every_write_is_refused_every_read_allowed(tmp_path):
    f = Factory(answering(tools=WRITES + READS))

    async def body(c):
        a = c.ctx["app"]
        before = git(a, "rev-parse", "HEAD").strip()
        code, out = await start(c)
        assert code == 200, out
        inv = await finished(c)
        tried = f.made[0].tried
        assert [(n, ok) for n, _, ok in tried] == [(n, False) for n, _ in WRITES] + [(n, True) for n, _ in READS]
        assert len(inv.refused) == len(WRITES)
        whys = {r["what"]: r["why"] for r in inv.refused}
        assert "git commit" in whys["git commit -am 'x'"] and "git push" in whys["git push origin master"]
        assert "rm" in whys["rm -rf docs"] and "redirection" in whys["echo x > README.md"]
        assert "WebFetch" in whys[next(k for k in whys if "example.com" in k)]
        # The report says what was refused; nothing else moved but its own commit.
        text = (a / inv.report["path"]).read_text(encoding="utf-8")
        assert "## Ce que le cockpit a refusé" in text and "`git push origin master`" in text
        assert git(a, "rev-parse", "HEAD~1").strip() == before
        assert git(a, "status", "--porcelain") == ""
        # The options it was given: reading tools only, the gate on every tool.
        o = f.made[0].options
        assert o.tools == enquete.TOOLS and o.setting_sources == [] and o.cwd == str(a)
        assert o.hooks["PreToolUse"][0].matcher is None
    served(tmp_path, body, f)


def test_the_threshold_applies_and_is_passed_over_once_confirmed(tmp_path):
    f = Factory(answering())

    async def body(c):
        add_both(c.ctx["store"], 96, 20)
        code, out = await start(c)
        assert code == 409 and out["usage_block"]["windows"] and "Seuil de blocage" in out["error"]
        assert c.ctx["inv"].current is None
        code, out = await start(c, usage_ok=True)
        assert code == 200
        await finished(c)
        log = (tmp_path / "logs" / "consommation.log").read_text(encoding="utf-8")
        assert "l'enquête « Pourquoi l'écran de course" in log
    served(tmp_path, body, f)


def test_one_at_a_time_an_investigation_included(tmp_path):
    gate = asyncio.Event()
    run_gate = asyncio.Event()
    f = Factory(answering(gate=gate))

    async def body(c):
        a = c.ctx["app"]
        code, _ = await start(c)
        assert code == 200
        # A command, and a second investigation, wait for it.
        r = await post(c, "/api/run", {"command": "2_structure", "args": "f"})
        out = await r.json()
        assert r.status == 409 and out["busy_enquete"] and "une enquête est en cours" in out["error"]
        code, out = await start(c, "Une autre question ?")
        assert code == 409 and "une à la fois" in out["error"]
        s = await (await c.get("/api/state")).json()
        assert s["enquete"]["status"] == "going"
        upd = await post(c, "/api/cockpit/update", {})
        assert upd.status == 409 and "enquête" in (await upd.json())["error"]
        gate.set()
        await finished(c)
        # A command going: an investigation waits for it.
        r = await post(c, "/api/run", {"command": "2_structure", "args": "f"})
        assert r.status == 200, await r.text()
        code, out = await start(c, "Et pendant ce temps ?")
        assert code == 409 and "une commande tourne déjà" in out["error"]
        run_gate.set()
        assert await c.ctx["rn"].wait_ended(str(a), 10)
    served(tmp_path, body, f, script=run_script(run_gate))


def test_stopped_from_the_cockpit_leaves_no_report(tmp_path):
    f = Factory(until_cancelled())

    async def body(c):
        a = c.ctx["app"]
        n = len(git(a, "log", "--format=%s").splitlines())
        await start(c)
        await until(lambda: f.made)
        r = await post(c, "/api/enquetes/cancel", {})
        assert (await r.json())["cancelled"]
        inv = await finished(c)
        assert inv.outcome == "annulé" and inv.report is None
        assert len(git(a, "log", "--format=%s").splitlines()) == n
        assert not (a / "docs" / "enquetes").exists()
    served(tmp_path, body, f)


def test_the_automatic_pilot_never_launches_one_and_waits_for_it(tmp_path, monkeypatch):
    import autopilot as ap
    from test_pilot_server import CHAIN, chain_script, ended, pilot
    from test_pilot_server import served as pilot_served
    gate = asyncio.Event()
    f = Factory(answering(gate=gate))
    monkeypatch.setattr(server, "ENQUETE_CLIENT", f)

    async def body(c):
        code, _ = await start(c)
        assert code == 200
        r = await post(c, "/api/pilot/start", {"preset": "besoin"})
        assert r.status == 200, await r.text()
        for _ in range(100):
            p = (await pilot(c))["pilot"]
            if "l'enquête en cours" in (p.get("message") or "") or "l'enquête en cours" in str(p):
                break
            await asyncio.sleep(0.05)
        assert "l'enquête en cours" in str(p) and not c.ctx["made"]
        gate.set()
        p = await ended(c)
        assert p["reason_kind"] == ap.NEED
        assert [m.prompts[0] for m in c.ctx["made"]] == ["/1_lexique f", "/2_structure f", "/3_decoupe f"]
        # Its only investigation: hers.
        assert len(f.made) == 1
    pilot_served(tmp_path, body, chain_script(CHAIN), monkeypatch=monkeypatch)


# ------------------------------------------------------------------ §2 the report

def test_the_report_written_committed_and_pushed_in_the_application(tmp_path):
    f = Factory(answering())

    async def body(c):
        a, remote, other = c.ctx["app"], c.ctx["remote"], c.ctx["other"]
        code, out = await start(c, model="opus")
        assert code == 200 and out["enquete"]["target"] == "application"
        assert f.made and f.made[0].options.model == "opus"
        assert f"« {a.name} »" in f.made[0].prompts[0] or "l'application" in f.made[0].prompts[0]
        inv = await finished(c)
        rel = inv.report["path"]
        assert re.fullmatch(rf"docs/enquetes/{TODAY}-pourquoi-l-ecran-de-course-remet-il\.md", rel), rel
        text = (a / rel).read_text(encoding="utf-8")
        assert f"## La question\n\n{Q}" in text and ANSWER in text
        assert f"- Modèle : {SONNET} (choisi pour cette enquête)" in text
        assert "- Coût : 12 000 tokens lus · 800 écrits · " in text and "≈ 0,01 $ en équivalent API" in text
        assert f"- Date : {datetime.now().strftime('%d/%m/%Y')}" in text
        assert "- Ordinateur : ordinateur" in text and "- Cible : l'application" in text
        # Committed alone, pushed: the other computer sees it.
        assert subject(a).startswith("enquete: Pourquoi l'écran de course")
        assert git(a, "show", "--name-only", "--format=", "HEAD").split() == [rel]
        await until(lambda: git(remote, "rev-parse", "master").strip() == head(a))
        assert inv.report["pushed"] is True
        git(other, "pull", "-q", "--ff-only")
        assert (other / rel).read_text(encoding="utf-8") == text
        # Listed with its cost; readable.
        lst = await (await c.get("/api/enquetes")).json()
        row = next(x for x in lst["reports"] if x["path"] == rel)
        assert row["cost"].startswith("12 000 tokens lus") and row["target_kind"] == "application"
        assert row["computer"] == "ordinateur" and row["title"] == Q
        rep = await (await c.get(f"/api/enquetes/report?target=application&path={rel}")).json()
        assert rep["text"] == text and rep["prompt"] is None
        # Its cost in the stats, marked.
        import sqlite3
        with sqlite3.connect(c.ctx["store"].path) as db:
            rows = list(db.execute("SELECT command, kind, app FROM runs"))
        assert rows == [("(enquête)", "enquête", str(a))]
    served(tmp_path, body, f)


def test_a_clone_behind_github_is_pulled_before_the_report(tmp_path):
    """1.12's rules: what the other computer pushed is taken first — the
    report's commit sits on it and goes, never a divergence."""
    f = Factory(answering())

    async def body(c):
        a, remote, other = c.ctx["app"], c.ctx["remote"], c.ctx["other"]
        theirs = change(other, "docs/features/f/notes.md", "de l'autre ordinateur\n", "notes", push=True)
        await start(c)
        inv = await finished(c)
        assert inv.report["pushed"] is True
        assert git(a, "rev-parse", "HEAD~1").strip() == theirs
        assert git(remote, "rev-parse", "master").strip() == head(a)
    served(tmp_path, body, f)


def test_the_chain_reports_commit_neither_restarts_nor_says_pas_encore_en_service(tmp_path, monkeypatch, chain_root):
    remote, here, other = chain_root
    f = Factory(answering())
    spawned, asked = [], []

    def spawn(*a, **k):
        spawned.append(a)
        raise OSError("pas de nouveau serveur dans un test")
    monkeypatch.setattr(server, "SPAWN_SERVER", spawn)
    monkeypatch.setattr(server, "AUTO_RESTART", True)
    monkeypatch.setattr(server, "RESTART_POLL", 0.05)
    monkeypatch.setattr(startup, "ask_restart", lambda port: asked.append(port) or {"ok": False, "error": "test"})
    started = head(here)

    async def body(c):
        c.ctx["server_app"][server.PORT_KEY]["port"] = 65000
        code, out = await start(c, "Comment le cockpit sait-il qu'il doit redémarrer ?", target="chaine")
        assert code == 200, out
        inv = await finished(c)
        rel = inv.report["path"]
        assert subject(here).startswith("enquete: ") and head(here) != started
        assert git(here, "show", "--name-only", "--format=", "HEAD").split() == [rel]
        await until(lambda: git(remote, "rev-parse", "master").strip() == head(here))
        assert "- Cible : la chaîne et le cockpit" in (here / rel).read_text(encoding="utf-8")
        # HEAD moved — reports only: no restart, no « pas encore en service ».
        await asyncio.sleep(0.6)
        assert spawned == []
        ck = (await (await c.get("/api/cockpit")).json())["cockpit"]
        assert ck["state"] == selfupdate.UP_TO_DATE and ck["count"] == 0
        assert server.older_server({"started": started}, 65000) is False and asked == []
        # The other computer's report, pulled at once, quietly.
        git(other, "pull", "-q", "--ff-only")
        change(other, "docs/enquetes/2026-10-09-autre.md", "# Enquête — Autre\n\n- Ordinateur : perso\n",
               "enquete: Autre", push=True)
        await post(c, "/api/sync/refresh", {"chain": True})
        lst = await (await c.get("/api/enquetes")).json()
        assert {x["path"] for x in lst["reports"]} >= {rel, "docs/enquetes/2026-10-09-autre.md"}
        ck = (await (await c.get("/api/cockpit")).json())["cockpit"]
        assert ck["state"] == selfupdate.UP_TO_DATE
        await asyncio.sleep(0.3)
        assert spawned == []
        # A commit of code: the restart, and the banner — the test sees the difference.
        change(here, "tools/cockpit/nouveau.py", "x = 1\n", "cockpit: nouveau")
        await until(lambda: spawned)
        ck = (await (await c.get("/api/cockpit")).json())["cockpit"]
        assert ck["state"] == selfupdate.PULLED and ck["count"] >= 1
        assert server.older_server({"started": started}, 65000) is False and asked == [65000]
    served(tmp_path, body, f)


# ------------------------------------------------------------------ §3 from a problem

def test_the_question_prefilled_from_each_kind_of_point(tmp_path):
    f = Factory(answering())

    async def body(c):
        a = str(c.ctx["app"])
        tally = stats_mod.Tally()
        for i, (at, cmd) in enumerate([("2026-10-08T02:00", "/8_code f"), ("2026-10-08T15:00", "/8_code f"),
                                       ("2026-10-08T16:30", "/8_code f")]):
            c.ctx["store"].record_run(run_id=f"r{i}", feature="f", work="f", command=cmd, mode="auto",
                                      started_at=at + ":05", ended_at=at + ":59", tally=tally, next_line=None,
                                      outcome="terminé", log_path=f"C:/logs/{i}.jsonl", app=a)
        points = {
            "erreur": {"kind": "erreur", "at": "2026-10-08T02:00", "command": "/8_code f",
                       "text": "/8_code f a fini en erreur le 08/10 à 02:00."},
            "programme": {"kind": "programme", "at": "2026-10-08T02:00", "command": "/8_code f",
                          "programme": "Cette nuit", "text": "Le programme « Cette nuit » s'est arrêté."},
            "blocage": {"kind": "blocage", "at": "2026-10-08T18:30", "command": None, "agent": "realisateur",
                        "files": ["code/lot-01/blocked_realisateur-01.md", "code/lot-02/blocked_realisateur-01.md"],
                        "text": "2 fichiers de blocage de realisateur dans ce cycle."},
            "coût": {"kind": "coût", "at": "2026-10-08T15:00", "command": "/8_code f", "text": "Coûteux."},
            "sur place": {"kind": "sur place", "at": "2026-10-08T16:30", "command": "/8_code f",
                          "runs": [{"at": "2026-10-08T15:00", "command": "/8_code f"},
                                   {"at": "2026-10-08T16:30", "command": "/8_code f"}], "text": "Sur place."},
        }
        for kind, p in points.items():
            r = await post(c, "/api/enquetes/prefill", {"source": "point", "point": p, "cycle": "main"})
            out = await r.json()
            assert r.status == 200 and out["target"] == "chaine", out
            q = out["question"]
            assert q.startswith("Pourquoi") and f"Ce qui s'est passé : {p['text']}" in q, kind
            assert "feature « f », cycle principal" in q and os.path.join(a, "docs", "features", "f", "journal.md") in q
            if kind in ("erreur", "programme"):
                assert "C:/logs/0.jsonl" in q
            if kind == "coût":
                assert "C:/logs/1.jsonl" in q
            if kind == "sur place":
                assert "C:/logs/1.jsonl" in q and "C:/logs/2.jsonl" in q
            if kind == "blocage":
                assert os.path.join(a, "docs", "features", "f", "code", "lot-02", "blocked_realisateur-01.md") in q
                assert "n'est pas sur cet ordinateur" in q
        # The page never launches: a prefill starts nothing.
        assert c.ctx["inv"].current is None and not f.made
    served(tmp_path, body, f)


def test_the_question_prefilled_from_a_failed_run(tmp_path):
    async def failing(c):
        from claude_agent_sdk import ResultMessage
        yield ResultMessage(subtype="error_during_execution", duration_ms=1, duration_api_ms=1, is_error=True,
                            num_turns=1, session_id="s", result="Je n'ai pas pu lire le lot.",
                            errors=["Le lot 3 est introuvable"])

    async def body(c):
        a = c.ctx["app"]
        r = await post(c, "/api/enquetes/prefill", {"source": "run"})
        assert r.status == 404
        r = await post(c, "/api/run", {"command": "2_structure", "args": "f"})
        assert r.status == 200
        assert await c.ctx["rn"].wait_ended(str(a), 10)
        run = c.ctx["rn"].current(str(a))
        assert run.outcome == "erreur"
        out = await (await post(c, "/api/enquetes/prefill", {"source": "run"})).json()
        assert out["target"] == "chaine"
        q = out["question"]
        assert "/2_structure f a fini en erreur" in q and "« Le lot 3 est introuvable »" in q
        assert f"- le journal de run : {run.log_path}" in q and "Je n'ai pas pu lire le lot." in q
    served(tmp_path, body, Factory(answering()), script=failing)


# ------------------------------------------------------------------ §4 what follows

PROMPT = "Cockpit 1.22 — x.\n\n## 1 — What to change\n\n…\n\nCommit and push: `Cockpit 1.22 — x`"


def test_the_correction_prompt_marked_to_be_read_and_never_launched(tmp_path, chain_root):
    remote, here, _ = chain_root
    f = Factory(answering(), saying(PROMPT))

    async def body(c):
        code, _ = await start(c, "Pourquoi le journal écrit-il le nom réseau ?", target="chaine")
        inv = await finished(c)
        rel = inv.report["path"]
        # Only the chain's reports: an application's report is not here.
        r = await post(c, "/api/enquetes/prompt", {"path": "docs/enquetes/2026-01-01-absent.md"})
        assert r.status == 404
        r = await post(c, "/api/enquetes/prompt", {"path": rel})
        out = await r.json()
        assert r.status == 200, out
        prel = rel[:-3] + "-prompt.md"
        assert out["path"] == prel
        text = (here / prel).read_text(encoding="utf-8")
        assert text.startswith("> **À relire dans la conversation de conception avant de lancer.**")
        assert text.rstrip().endswith("Commit and push: `Cockpit 1.22 — x`")
        # The second call: no tool, one turn, the report whole in its prompt.
        second = f.made[1]
        assert second.options.tools == [] and second.options.max_turns == 1
        assert second.options.system_prompt["append"] == enquete.PROMPT_INSTRUCTION
        assert (here / rel).read_text(encoding="utf-8").strip() in second.prompts[0]
        assert subject(here).startswith("enquete: prompt de correction — ")
        await until(lambda: git(remote, "rev-parse", "master").strip() == head(here))
        # Never launched: nothing runs, no route runs it.
        assert c.ctx["rn"].going() is None and len(f.made) == 2
        assert not [x for x in c.ctx["server_app"].router.routes() if "launch" in (x.resource.canonical or "")]
        rep = await (await c.get(f"/api/enquetes/report?target=chaine&path={rel}")).json()
        assert rep["prompt"]["path"] == prel and rep["prompt"]["text"] == text
        lst = await (await c.get("/api/enquetes")).json()
        assert next(x for x in lst["reports"] if x["path"] == rel)["prompt"] == prel
    served(tmp_path, body, f)


BUG = ("Observé : le chrono repart de zéro après une pause.\nOù : sur l'écran de course\n"
       "Attendu : reprendre où il en était quand la course reprend.")
GAP = re.compile(r"^G\d{2} \S.*\. Elle devrait \S.*\.$")


def test_the_bug_entry_drafted_shown_then_written_on_confirmation(tmp_path):
    f = Factory(answering(), saying(BUG))

    async def body(c):
        a = c.ctx["app"]
        feat = a / "docs" / "features" / "f"
        await start(c)
        inv = await finished(c)
        rel = inv.report["path"]
        r = await post(c, "/api/enquetes/bug", {"path": rel})
        d = await r.json()
        assert r.status == 200, d
        assert d["entry"] == ("G01 Sur l'écran de course : le chrono repart de zéro après une pause. Elle devrait "
                              "reprendre où il en était quand la course reprend.")
        assert GAP.match(d["entry"]) and d["bugfix"] is None and d["new_bugfix"] == "bugfix-01"
        # Nothing written before her confirmation.
        assert not (feat / "bugfix-01").exists()
        # Her entry, changed by her, written to a new correction.
        mine = d["entry"].replace("après une pause", "après une pause de plus de 10 s")
        r = await post(c, "/api/enquetes/bug", {"path": rel, "entry": mine, "confirm": True})
        w = await r.json()
        assert r.status == 200 and w["bugfix"] == "bugfix-01"
        assert (feat / "bugfix-01" / "bug-list.md").read_text(encoding="utf-8") == mine + "\n"
        # The open correction next time: the next G<n>, appended — the same fields, no second call.
        calls = len(f.made)
        d2 = await (await post(c, "/api/enquetes/bug", {"path": rel, "fields": d["fields"]})).json()
        assert len(f.made) == calls and d2["bugfix"] == "bugfix-01" and d2["entry"].startswith("G02 ")
        await post(c, "/api/enquetes/bug", {"path": rel, "entry": d2["entry"], "confirm": True})
        text = (feat / "bugfix-01" / "bug-list.md").read_text(encoding="utf-8")
        assert [l[:3] for l in text.splitlines() if l.strip()] == ["G01", "G02"]
        assert all(GAP.match(l) for l in text.splitlines() if l.strip())
        # Once the diagnostic read it (desc-bug.md), a new correction.
        (feat / "bugfix-01" / "desc-bug.md").write_text("# x\n", encoding="utf-8")
        d3 = await (await post(c, "/api/enquetes/bug", {"path": rel, "fields": d["fields"]})).json()
        assert d3["bugfix"] is None and d3["new_bugfix"] == "bugfix-02" and d3["entry"].startswith("G01 ")
        w = await (await post(c, "/api/enquetes/bug", {"path": rel, "entry": "G07 Faux numéro. Elle devrait x.",
                                                        "confirm": True})).json()
        assert w["bugfix"] == "bugfix-02" and w["entry"] == "G01 Faux numéro. Elle devrait x."
        assert (feat / "bugfix-02" / "bug-list.md").read_text(encoding="utf-8") == "G01 Faux numéro. Elle devrait x.\n"
        assert (feat / "bugfix-01" / "bug-list.md").read_text(encoding="utf-8") == text
    served(tmp_path, body, f)


# ------------------------------------------------------------------ §0 the computer's name

NET = "PC-RESEAU-7Q3"


def test_no_repository_write_holds_the_network_name(tmp_path, monkeypatch):
    from test_journal_server import STRUCTURE, chain_like
    monkeypatch.setenv("COMPUTERNAME", NET)
    monkeypatch.setattr(socket, "gethostname", lambda: NET)
    monkeypatch.setattr(server, "JOURNAL", True)
    monkeypatch.setattr(server, "ASK_COMPUTER", True)
    world = app_world(tmp_path, "app")
    a = world[1]
    scripts = [chain_like(a, STRUCTURE[1], STRUCTURE[0], STRUCTURE[2]),
               chain_like(a, [("docs/features/f/lexique.md", "# L\n")], "feat: lexique", "Next: run /3_decoupe f")]
    queue = list(scripts)

    def script(c):
        return queue.pop(0)(c) if queue else scripts[-1](c)
    f = Factory(answering())

    async def body(c):
        st = c.ctx["state"]
        n = len(git(a, "log", "--format=%s", "--grep=^journal:").splitlines())
        r = await post(c, "/api/run", {"command": "2_structure", "args": "f"})
        out = await r.json()
        # The first run that writes with no nickname: asked, once.
        assert r.status == 200 and out["ask_computer"] is True
        assert (await (await c.get("/api/state")).json())["computer"]["wanted"] is True
        assert await c.ctx["rn"].wait_ended(str(a), 10)
        await until(lambda: len(git(a, "log", "--format=%s", "--grep=^journal:").splitlines()) > n)
        assert journal.read(journal.journal_path(str(a), "f"))[-1]["computer"] == "ordinateur"
        await start(c)
        inv = await finished(c)
        assert "- Ordinateur : ordinateur" in (a / inv.report["path"]).read_text(encoding="utf-8")
        # Her nickname: written from now on; never asked again.
        r = await post(c, "/api/computer", {"name": "travail"})
        assert (await r.json())["computer"] == {"name": "travail", "asked": True, "wanted": False, "label": "travail"}
        r = await post(c, "/api/run", {"command": "1_lexique", "args": "f"})
        assert (await r.json())["ask_computer"] is False
        assert await c.ctx["rn"].wait_ended(str(a), 10)
        await until(lambda: len(journal.read(journal.journal_path(str(a), "f"))) == 2)
        assert journal.read(journal.journal_path(str(a), "f"))[-1]["computer"] == "travail"
        # The end-of-cycle report and the reconstruction write it too.
        await post(c, "/api/journal/report", {"cycle": "main", "confirm": True})
        await post(c, "/api/journal/reconstruct", {"confirm": True})
        assert st.computer_label == "travail"
        # Nowhere in the repository, its history or GitHub's: the network name.
        for repo in (a, c.ctx["remote"]):
            assert NET not in git(repo, "log", "-p", "--all", "--format=%s%n%b")
        for root, _dirs, files in os.walk(a):
            if ".git" in root.split(os.sep):
                continue
            for name in files:
                with open(os.path.join(root, name), "rb") as fh:
                    assert NET.encode() not in fh.read(), os.path.join(root, name)
    served(tmp_path, body, f, world=world, script=script)


def test_the_nickname_in_parametres(tmp_path):
    async def body(c):
        st = c.ctx["state"]
        assert st.computer == {"name": "", "asked": False} and st.computer_label == "ordinateur"
        r = await post(c, "/api/computer", {"name": "a|b"})
        assert r.status == 400
        r = await post(c, "/api/computer", {"name": "x" * 41})
        assert r.status == 400
        r = await post(c, "/api/computer", {"name": ""})
        assert (await r.json())["computer"]["label"] == "ordinateur" and st.computer["asked"] is True
        await post(c, "/api/computer", {"name": "  perso  "})
        assert State(st.path).computer == {"name": "perso", "asked": True}
    served(tmp_path, body, Factory(answering()))
