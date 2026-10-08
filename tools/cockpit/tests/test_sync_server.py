"""1.12 — the cockpit always agreeing with GitHub, through its server: a
launch after a pull, refused on an overlapping file or a divergence, let
through offline, after a push; « Envoyer » refused then shown; « Réconcilier »;
« Envoyer mes réponses »; a run's final push checked; agent-chain pulled at
start; never an older chain over a newer one; « Ajouter depuis GitHub » and
core.longpaths; a private file absent from this computer. Bare repositories
play GitHub, in temporary folders; no chain command runs — the SDK client is
a fake."""
import asyncio
import json
import subprocess

import pytest

import apps as apps_mod
import chain
import donnees
import server
import sync
from donneesworld import data_world
from state import State
from syncworld import app_world, bare, change, head, offline, world
from test_apps import serve
from test_chain import CHAIN_FILES, commit, git, init, write
from test_runner import script_quick
from test_server import post


def listed(tmp_path, *folders):
    st = State(str(tmp_path / "config.json"))
    for f in folders:
        st.add_app(str(f))
        st.open_pair(str(f), "f")
    st.activate(str(folders[0]))
    return st


async def wait_for(pred, timeout=20.0):
    for _ in range(int(timeout / 0.05)):
        v = pred()
        if v:
            return v
        await asyncio.sleep(0.05)
    raise AssertionError("jamais arrivé")


async def launch(c, rn, app):
    r = await post(c, "/api/run", {"command": "1_lexique", "args": "f"})
    data = await r.json()
    if r.status == 200:
        assert await rn.wait_ended(str(app), 10)
    return r.status, data


# ------------------------------------------------------------ §2 before a launch

def test_launch_behind_pulled_then_launched(tmp_path):
    _, a, b = app_world(tmp_path, "app")
    sha = change(b, "docs/features/f/lexique.md", "# Lexique\n", push=True)

    async def body(c, st, rn):
        status, data = await launch(c, rn, a)
        assert status == 200, data
        assert "récupéré" in data["sync"]["notice"] and data["sync"]["sync"]["state"] == sync.UP_TO_DATE
        assert head(a) == sha
        assert git(a, "rev-list", "--merges", "--count", "HEAD").strip() == "0"
    serve(tmp_path, body, state=listed(tmp_path, a), script=script_quick)


def test_launch_behind_with_overlapping_uncommitted_file_refused(tmp_path):
    _, a, b = app_world(tmp_path, "app")
    q = "docs/features/f/questions-lexicographe-01.md"
    change(b, q, (b / q).read_text(encoding="utf-8").replace("Answer:\n", "Answer: oui\n", 1), push=True)
    (a / q).write_text((a / q).read_text(encoding="utf-8").replace("Answer:\n", "Answer: non\n", 1), encoding="utf-8")
    before = head(a)

    async def body(c, st, rn):
        status, data = await launch(c, rn, a)
        assert status == 409 and q in data["error"]
        assert data["sync_refused"]["files"] == [q]
        assert not rn.is_running(str(a)) and head(a) == before
        assert "Answer: non" in (a / q).read_text(encoding="utf-8")
    serve(tmp_path, body, state=listed(tmp_path, a), script=script_quick)


def test_launch_diverged_refused(tmp_path):
    _, a, b = app_world(tmp_path, "app")
    change(b, "README.md", "B\n", push=True)
    mine = change(a, "notes.md", "A\n")

    async def body(c, st, rn):
        status, data = await launch(c, rn, a)
        assert status == 409 and data["sync_refused"]["reconcile"] and "Réconcilier" in data["error"]
        assert not rn.is_running(str(a)) and head(a) == mine
        s = await (await c.get("/api/state")).json()
        assert s["sync"]["state"] == sync.DIVERGED
    serve(tmp_path, body, state=listed(tmp_path, a), script=script_quick)


def test_launch_offline_goes_with_a_notice(tmp_path):
    _, a, _ = app_world(tmp_path, "app")
    offline(a)

    async def body(c, st, rn):
        status, data = await launch(c, rn, a)
        assert status == 200 and "injoignable" in data["sync"]["notice"]
    serve(tmp_path, body, state=listed(tmp_path, a), script=script_quick)


def test_launch_not_sent_pushed_first(tmp_path):
    remote, a, _ = app_world(tmp_path, "app")
    sha = change(a, "notes.md", "A\n")

    async def body(c, st, rn):
        status, data = await launch(c, rn, a)
        assert status == 200 and "envoyé" in data["sync"]["notice"]
        assert git(remote, "rev-parse", "master").strip() == sha
    serve(tmp_path, body, state=listed(tmp_path, a), script=script_quick)


def test_donnees_save_and_profile_go_through_the_sync(tmp_path, monkeypatch):
    monkeypatch.setattr(server, "DONNEES_PUSH", False)
    _, a, b = app_world(tmp_path, "app")
    change(b, "README.md", "B\n", push=True)
    change(a, "notes.md", "A\n")

    async def body(c, st, rn):
        r = await post(c, "/api/donnees/save", {"tab": "feature", "entries": []})
        assert r.status == 409 and (await r.json())["sync_refused"]["reconcile"]
        r = await post(c, "/api/deploy/profile", {"targets": []})
        assert r.status == 409 and (await r.json())["sync_refused"]["reconcile"]
        r = await post(c, "/api/chain/install", {"folder": str(a)})
        assert r.status == 409 and (await r.json())["sync_refused"]["reconcile"]
    serve(tmp_path, body, state=listed(tmp_path, a), script=script_quick)


# ------------------------------------------------------------ §3 after a run, « Envoyer »

def test_run_whose_final_push_was_refused_says_so(tmp_path):
    """The command commits; the other computer pushed meanwhile: GitHub
    refuses its push. The run's end carries the state that says it."""
    _, a, b = app_world(tmp_path, "app")

    async def script(c):
        change(a, "docs/features/f/lexique.md", "# Lexique\n", "lexique: f")
        change(b, "README.md", "B\n", push=True)
        from test_runner import result
        yield result("Fait.\nNext: done")

    async def body(c, st, rn):
        status, data = await launch(c, rn, a)
        assert status == 200
        run = rn.current(str(a))
        got = await wait_for(lambda: run.sync)
        assert got["state"] == sync.DIVERGED
        s = await (await c.get("/api/state")).json()
        assert s["run"]["sync"]["state"] == sync.DIVERGED and s["sync"]["state"] == sync.DIVERGED
    serve(tmp_path, body, state=listed(tmp_path, a), script=script)


def test_push_rejected_then_the_new_state_and_envoyer(tmp_path):
    remote, a, b = app_world(tmp_path, "app")
    change(a, "notes.md", "A\n")

    async def body(c, st, rn):
        r = await c.get("/api/sync", params={"folder": str(a)})
        assert (await r.json())["sync"]["state"] == sync.AHEAD
        rows = (await (await c.get("/api/apps")).json())["apps"]
        assert rows[0]["sync"]["state"] == sync.AHEAD
        change(b, "README.md", "B\n", push=True)
        r = await post(c, "/api/sync/push", {"folder": str(a)})
        data = await r.json()
        assert r.status == 409 and data["push"]["rejected"] and data["sync"]["state"] == sync.DIVERGED
        assert "divergé" in data["error"]
    serve(tmp_path, body, state=listed(tmp_path, a), script=script_quick)

    remote2, a2, _ = app_world(tmp_path / "deux", "app")
    sha = change(a2, "notes.md", "A\n")

    async def body2(c, st, rn):
        r = await post(c, "/api/sync/push", {"folder": str(a2)})
        data = await r.json()
        assert r.status == 200 and data["sync"]["state"] == sync.UP_TO_DATE
        assert git(remote2, "rev-parse", "master").strip() == sha
    serve(tmp_path / "deux", body2, state=listed(tmp_path / "deux", a2), script=script_quick)


# ------------------------------------------------------------ §4 « Réconcilier »

def test_reconcile_through_the_server(tmp_path):
    remote, a, b = app_world(tmp_path, "app")
    change(b, "README.md", "B\n", push=True)
    change(a, "notes.md", "A\n")
    _, a2, b2 = app_world(tmp_path / "x", "app")
    change(b2, "README.md", "B\n", push=True)
    mine = change(a2, "README.md", "A\n")

    async def body(c, st, rn):
        r = await post(c, "/api/sync/reconcile", {"folder": str(a)})
        data = await r.json()
        assert r.status == 200 and data["ok"] and data["pushed"] and data["sync"]["state"] == sync.UP_TO_DATE
        assert git(remote, "rev-parse", "master").strip() == head(a)
        r = await post(c, "/api/sync/reconcile", {"folder": str(a2)})
        data = await r.json()
        assert r.status == 409 and data["conflicts"] == ["README.md"] and "Claude Code" in data["error"]
        assert head(a2) == mine and data["sync"]["state"] == sync.DIVERGED
    serve(tmp_path, body, state=listed(tmp_path, a, a2), script=script_quick)


# ------------------------------------------------------------ §5 « Envoyer mes réponses »

def test_send_answers_from_the_page_and_from_the_row(tmp_path):
    remote, a, _ = app_world(tmp_path, "app")
    _, a2, _ = app_world(tmp_path / "x", "app")
    q = "docs/features/f/questions-lexicographe-01.md"
    for repo in (a, a2):
        (repo / q).write_text((repo / q).read_text(encoding="utf-8").replace("Answer:\n", "Answer: oui\n", 1),
                              encoding="utf-8")

    async def body(c, st, rn):
        s = await (await c.get("/api/state")).json()
        assert s["answers_pending"] == 1
        rows = {r["folder"]: r for r in (await (await c.get("/api/apps")).json())["apps"]}
        assert rows[str(a2)]["answers_pending"] == 1
        r = await post(c, "/api/answers/send", {})
        data = await r.json()
        assert r.status == 200 and data["commit"] and data["pushed"] and data["message"] == "chore: answers"
        assert git(a, "log", "-1", "--format=%s").strip() == "chore: answers"
        assert git(a, "show", "--name-only", "--format=", "HEAD").split() == [q]
        assert git(remote, "rev-parse", "master").strip() == head(a)
        assert (await (await c.get("/api/state")).json())["answers_pending"] == 0
        r = await post(c, "/api/answers/send", {"folder": str(a2)})
        data = await r.json()
        assert r.status == 200 and data["commit"] and data["pushed"]
        assert git(a2, "status", "--porcelain").strip() == ""
        # Nothing left: said, no commit.
        r = await post(c, "/api/answers/send", {})
        assert (await r.json())["commit"] is None
    serve(tmp_path, body, state=listed(tmp_path, a, a2), script=script_quick)


# ------------------------------------------------------------ §6 the chain

def chain_on_github(tmp_path):
    """agent-chain on GitHub and on two computers."""
    files = dict(CHAIN_FILES)
    remote, one, two = world(tmp_path / "agent-chain", files)
    chain._chain_cache.clear()
    chain._behind_cache.clear()
    chain._older_cache.clear()
    return remote, one, two


def test_agent_chain_pulled_at_start(tmp_path, monkeypatch):
    _, here, other = chain_on_github(tmp_path)
    sha = change(other, "tools/cockpit/x.py", "cockpit 2\n", push=True)
    monkeypatch.setattr(server, "CHAIN_ROOT", str(here))
    monkeypatch.setattr(server, "SYNC_CHAIN_AT_START", True)
    _, a, _ = app_world(tmp_path, "app")

    async def body(c, st, rn):
        s = await wait_for_state(c, lambda s: s["chain_sync"]["notice"])
        assert s["chain_sync"]["notice"] == server.CHAIN_RESTART
        assert head(here) == sha and s["chain_sync"]["sync"]["state"] == sync.UP_TO_DATE
    serve(tmp_path, body, state=listed(tmp_path, a), script=script_quick)


async def wait_for_state(c, pred, timeout=20.0):
    for _ in range(int(timeout / 0.1)):
        s = await (await c.get("/api/state")).json()
        if pred(s):
            return s
        await asyncio.sleep(0.1)
    raise AssertionError("jamais arrivé")


@pytest.mark.real_chain
def test_never_an_older_chain_over_a_newer_one(tmp_path, monkeypatch):
    remote, here, other = chain_on_github(tmp_path)
    app = tmp_path / "app"
    init(app)
    write(app, "docs/features/f/idees.md", "idea\n")
    commit(app, "app")
    # The other computer's chain moved on, and was installed from there.
    change(other, ".claude/agents/a.md", "agent a, two\n", push=True)
    chain.install(str(app), str(other), push=False)
    chain._older_cache.clear()
    st = chain.state(str(app), str(here))
    assert st["state"] == chain.NEWER and st["newer"] and "plus récente" in st["summary"]
    with pytest.raises(chain.InstallError, match="plus récente"):
        chain.install(str(app), str(here), confirm=True, push=False)
    lines = apps_mod.update_all([{"name": "app", "folder": str(app)}], lambda f: chain.state(f, str(here)),
                                lambda f: chain.install(f, str(here), push=False), lambda f: False)
    assert lines[0]["outcome"] == apps_mod.SKIPPED and "plus récente" in lines[0]["text"]
    monkeypatch.setattr(server, "CHAIN_ROOT", str(here))
    monkeypatch.setattr(server, "CHAIN_PUSH", False)
    monkeypatch.setattr(server, "chain_state", lambda f: chain.state(f, str(here)))

    async def body(c, st_, rn):
        r = await post(c, "/api/chain/install", {"folder": str(app), "confirm": True})
        assert r.status == 409 and "plus récente" in (await r.json())["error"]
        rows = (await (await c.get("/api/apps")).json())["apps"]
        assert rows[0]["chain"]["state"] == chain.NEWER and "plus récente" in rows[0]["chain"]["refused"]
    serve(tmp_path, body, state=listed(tmp_path, app), script=script_quick)
    # Once this computer's chain caught up, the install goes.
    git(here, "pull", "-q", "--ff-only")
    chain._chain_cache.clear()
    chain._older_cache.clear()
    assert chain.state(str(app), str(here))["state"] == chain.UP_TO_DATE


# ------------------------------------------------------------ §7 a second computer

def test_add_from_github_clones_and_lists(tmp_path):
    remote, a, _ = app_world(tmp_path, "app")
    parent = tmp_path / "second"
    parent.mkdir()

    async def body(c, st, rn):
        r = await post(c, "/api/apps/clone", {"url": str(remote), "parent": str(parent)})
        data = await r.json()
        assert r.status == 200, data
        dest = parent / "app"
        assert data["path"] == str(dest) and st.has_app(str(dest))
        assert (dest / "docs/features/f/idees.md").exists()
        assert sync.long_paths(str(dest)) is True
        r = await post(c, "/api/apps/clone", {"url": str(remote), "parent": str(parent)})
        assert r.status == 409 and "pas vide" in (await r.json())["error"]
        r = await post(c, "/api/apps/clone", {"url": str(tmp_path / "nulle-part.git"), "parent": str(tmp_path)})
        assert r.status == 409
    serve(tmp_path, body, state=listed(tmp_path, a), script=script_quick)


def test_add_sets_long_paths_and_tools_check_it(tmp_path):
    _, a, _ = app_world(tmp_path, "app")
    _, other, _ = app_world(tmp_path / "x", "autre")
    assert sync.long_paths(str(other)) is None

    async def body(c, st, rn):
        r = await post(c, "/api/apps/add", {"path": str(other)})
        assert r.status == 200 and sync.long_paths(str(other)) is True
        rows = {x["folder"]: x for x in (await (await c.get("/api/longpaths")).json())["apps"]}
        assert rows[str(a)]["value"] is None and rows[str(other)]["value"] is True
        r = await post(c, "/api/longpaths", {"folder": str(a)})
        assert r.status == 200 and sync.long_paths(str(a)) is True
    serve(tmp_path, body, state=listed(tmp_path, a), script=script_quick)


# ------------------------------------------------------------ §8 private files

def test_private_file_absent_from_this_computer(tmp_path, monkeypatch):
    monkeypatch.setattr(server, "DONNEES_PUSH", False)
    app = tmp_path / "app"
    data_world(app, question=False)
    folder = "docs/features/f/donnees"
    entries = [{"name": "releve-2026-09-14.csv", "what": "a statement", "source": "the bank", "date": "2026-09-14",
                "private": "no"},
               {"name": "compte-joint.csv", "what": "the joint account", "source": "the bank", "date": "2026-10-07",
                "private": "yes"}]
    res = donnees.save(str(app), folder, entries, push=False)
    assert res["commit"]
    assert "## compte-joint.csv" in (app / folder / "donnees.md").read_text(encoding="utf-8")
    assert f"{folder}/compte-joint.csv" in donnees.section_paths((app / ".gitignore").read_text(encoding="utf-8"))
    listing = donnees.listing(str(app), "feature", "f")
    row = next(e for e in listing["entries"] if e["name"] == "compte-joint.csv")
    assert row["elsewhere"] and not row["on_disk"]
    # A file git carries, absent: still refused.
    (app / folder / "releve-2026-09-14.csv").unlink()
    with pytest.raises(donnees.DataError, match="releve-2026-09-14.csv : le fichier n'est pas dans le dossier"):
        donnees.save(str(app), folder, entries, push=False)
