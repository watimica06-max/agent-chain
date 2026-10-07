"""1.7 — « Nouvelle application » (create.py, TECHNICAL_V1 §22): the form's
checks, the creation on scratch folders with and without a remote, a remote
that already holds commits, a failure at each step then « Reprendre », and
the routes. Every repository is built in tmp_path; nothing reaches GitHub."""
import asyncio
import json
import os
import subprocess

import pytest

import chain
import create
import server
from test_chain import CHAIN_FILES, commit, git, init, write
from test_server import post, with_client

pytestmark = pytest.mark.real_chain

SOCLE = os.path.join(chain.CHAIN_ROOT, ".claude", "scripts", "socle.py")
IDEA = "# Mon appli\r\n\r\nUne séance, des « tours », un chrono.\r\n"


@pytest.fixture
def chain_root(tmp_path, monkeypatch):
    """A scratch chain repository carrying the real socle.py."""
    root = tmp_path / "agent-chain"
    init(root)
    for rel, text in CHAIN_FILES.items():
        write(root, rel, text)
    (root / ".claude" / "scripts" / "socle.py").write_bytes(open(SOCLE, "rb").read())
    commit(root, "Chaîne — un")
    chain._chain_cache.clear()
    chain._behind_cache.clear()
    monkeypatch.setattr(server, "CHAIN_ROOT", str(root))
    monkeypatch.setattr(server, "CHAIN_PUSH", False)
    return root


@pytest.fixture
def idea(tmp_path):
    p = tmp_path / "idees-source.md"
    p.write_bytes(IDEA.encode("utf-8"))
    return p


def bare(tmp_path, name="remote.git"):
    r = tmp_path / name
    subprocess.run(["git", "init", "-q", "--bare", "-b", "master", str(r)], check=True)
    return r


def form(tmp_path, idea, **kw):
    f = {"name": "Mon Appli", "parent": str(tmp_path / "dev"), "folder": "", "idea": str(idea),
         "feature": "premiere-app", "remote": ""}
    f.update(kw)
    (tmp_path / "dev").mkdir(exist_ok=True)
    return f


def values(tmp_path, idea, chain_root, **kw):
    res = create.check(form(tmp_path, idea, **kw), chain_root=str(chain_root))
    assert res["ok"], res["errors"]
    v = res["values"]
    v.pop("idea_text")
    return v


class Recorder:
    def __init__(self):
        self.records, self.finished = [], []

    def save(self, rec):
        self.records.append(rec)

    def finish(self, v):
        self.finished.append(v["path"])
        return "ajoutée"


def make(v, chain_root, rec=None, record=None):
    rec = rec or Recorder()
    return create.Creation(v, rec.save, rec.finish, str(chain_root), record=record), rec


def subjects(repo):
    return git(repo, "log", "--format=%s").splitlines()


# ---------------------------------------------------------------- the form

def test_names_normalised():
    assert create.slug("Mon Appli Été !") == "mon-appli-ete"
    assert create.slug("  Hyrox — tracker 2 ") == "hyrox-tracker-2"
    assert create.slug("___") == ""


def test_the_form_refuses_and_shows(tmp_path, idea, chain_root):
    f = form(tmp_path, idea)
    res = create.check(f, chain_root=str(chain_root))
    assert res["ok"] and res["values"]["folder"] == "mon-appli"
    assert res["values"]["path"] == os.path.normpath(str(tmp_path / "dev" / "mon-appli"))
    assert res["values"]["idea_text"].splitlines() == ["# Mon appli", "", "Une séance, des « tours », un chrono."]
    # A folder that exists and is not empty: refused. Empty: accepted.
    (tmp_path / "dev" / "mon-appli").mkdir()
    assert create.check(f, chain_root=str(chain_root))["ok"]
    (tmp_path / "dev" / "mon-appli" / "x.txt").write_text("x")
    err = create.check(f, chain_root=str(chain_root))["errors"]
    assert "n'est pas vide" in err["folder"]
    # … unless this cockpit started creating it: « Reprendre ».
    res = create.check(f, resumable=[str(tmp_path / "dev" / "mon-appli")], chain_root=str(chain_root))
    assert res["ok"] and res["values"]["resume"]
    # A folder of the list, the chain's own repository.
    assert "déjà ce dossier" in create.check(form(tmp_path, idea, folder="autre"), listed=[str(tmp_path / "dev" / "autre")],
                                             chain_root=str(chain_root))["errors"]["folder"]
    assert "dépôt de la chaîne" in create.check(form(tmp_path, idea, parent=str(chain_root), folder="x"),
                                                chain_root=str(chain_root))["errors"]["folder"]
    # The feature: lower case, hyphens, no spaces — said with the proposal.
    e = create.check(form(tmp_path, idea, folder="b", feature="Ma Feature"), chain_root=str(chain_root))["errors"]
    assert "« ma-feature »" in e["feature"]
    assert "correction" in create.check(form(tmp_path, idea, folder="b", feature="bugfix-01"),
                                        chain_root=str(chain_root))["errors"]["feature"]
    # The idea file: there, .md or .txt, UTF-8, not empty.
    (tmp_path / "x.docx").write_text("x")
    assert ".md ou .txt" in create.check(form(tmp_path, tmp_path / "x.docx", folder="b"), chain_root=str(chain_root))["errors"]["idea"]
    (tmp_path / "vide.md").write_text("  \n")
    assert "vide" in create.check(form(tmp_path, tmp_path / "vide.md", folder="b"), chain_root=str(chain_root))["errors"]["idea"]
    (tmp_path / "latin.txt").write_bytes("séance".encode("latin-1"))
    assert "UTF-8" in create.check(form(tmp_path, tmp_path / "latin.txt", folder="b"), chain_root=str(chain_root))["errors"]["idea"]
    assert "remote" in create.check(form(tmp_path, idea, folder="b", remote="pas une adresse"),
                                    chain_root=str(chain_root))["errors"]
    assert create.check(form(tmp_path, idea, folder="b", remote="https://github.com/moi/mon-appli.git"),
                        chain_root=str(chain_root))["ok"]
    # The summary says no remote, and why pushes will fail.
    assert "rien n'est poussé" in create.summary(values(tmp_path, idea, chain_root, folder="c"))[1]


# ------------------------------------------------------------ the creation

def test_a_creation_without_a_remote(tmp_path, idea, chain_root):
    v = values(tmp_path, idea, chain_root)
    c, rec = make(v, chain_root)
    out = c.run()
    assert out["status"] == create.OK, out
    app = tmp_path / "dev" / "mon-appli"
    assert [s["status"] for s in out["steps"]] == [create.OK, create.NONE, create.OK, create.OK, create.OK, create.OK]
    assert "rien n'est poussé" in out["steps"][1]["detail"] and "rien n'est poussé" in out["steps"][2]["detail"]
    # Three commits, the chain's first.
    head = git(chain_root, "log", "-1", "--format=%h %cs").split()
    assert subjects(app) == ["feat: premiere-app — idées", "chore: scaffolding for the chain", f"chain: {head[0]} {head[1]}"]
    assert git(app, "rev-parse", "--abbrev-ref", "HEAD").strip() == "master"
    assert git(app, "status", "--porcelain").strip() == ""
    v2 = json.loads((app / ".claude" / "chain-version.json").read_text(encoding="utf-8"))
    assert v2["commit"] == git(chain_root, "rev-parse", "HEAD").strip() and ".claude/scripts/socle.py" in v2["files"]
    assert chain.state(str(app), str(chain_root))["state"] == chain.UP_TO_DATE
    assert (app / "docs" / "PRODUIT_GLOBAL.md").read_text(encoding="utf-8") == "# Application\n"
    assert (app / "docs" / "CURRENT_TECHNICAL_STATE.md").read_text(encoding="utf-8") == "# Technical state\n"
    assert (app / "docs" / "features" / "premiere-app" / "idees.md").read_bytes() == IDEA.encode("utf-8")
    assert (app / ".gitignore").read_text(encoding="utf-8").splitlines() == [
        ".claude/worktrees/", ".claude/settings.local.json", "docs/features/*/stop.md", "docs/features/*/stop1.md"]
    assert git(app, "show", "--name-only", "--format=", "HEAD").split() == ["docs/features/premiere-app/idees.md"]
    # « À fournir avant le code » went: the chain ships the skill and the
    # format, and /conventions writes the conventions.
    assert "provide" not in out
    assert rec.finished == [v["path"]]
    assert git(app, "remote").strip() == ""


def test_a_creation_with_a_remote_pushes_and_tracks(tmp_path, idea, chain_root):
    remote = bare(tmp_path)
    c, _ = make(values(tmp_path, idea, chain_root, remote=str(remote)), chain_root)
    out = c.run()
    assert out["status"] == create.OK, out
    app = tmp_path / "dev" / "mon-appli"
    assert all(s["detail"].endswith("poussé") for s in out["steps"][2:5])
    assert git(remote, "rev-parse", "master") == git(app, "rev-parse", "HEAD")
    assert git(app, "rev-parse", "--abbrev-ref", "@{u}").strip() == "origin/master"
    assert len(git(remote, "log", "--format=%s", "master").splitlines()) == 3


def test_a_remote_holding_commits_stops_at_step_2(tmp_path, idea, chain_root):
    remote = bare(tmp_path)
    other = tmp_path / "other"
    init(other)
    write(other, "README.md", "readme\n")
    commit(other, "Initial commit")
    git(other, "push", "-q", str(remote), "master")
    c, _ = make(values(tmp_path, idea, chain_root, remote=str(remote)), chain_root)
    out = c.run()
    assert out["status"] == create.FAILED and out["failed_at"] == "distant"
    assert "contient déjà des commits" in out["error"] and "rien n'est forcé" in out["error"]
    assert [s["status"] for s in out["steps"]] == [create.OK, create.FAILED] + [create.TODO] * 4
    app = tmp_path / "dev" / "mon-appli"
    assert git(app, "remote").strip() == "" and subprocess.run(
        ["git", "-C", str(app), "rev-parse", "-q", "--verify", "HEAD"], capture_output=True).returncode
    # Never deleted; what it holds is said.
    assert out["contents"] == [".git/", ".gitignore"]
    assert git(remote, "log", "--format=%s", "master").splitlines() == ["Initial commit"]


@pytest.mark.parametrize("failing", ["dossier", "distant", "chaine", "socle", "idees", "liste"])
def test_a_failure_at_each_step_then_reprendre(tmp_path, idea, chain_root, monkeypatch, failing):
    remote = bare(tmp_path)
    calls = {k: 0 for k, _ in create.STEPS}
    real = {k: getattr(create.Creation, "step_" + k) for k, _ in create.STEPS}
    state = {"armed": True}

    def spy(k):
        def f(self):
            calls[k] += 1
            if k == failing and state["armed"]:
                state["armed"] = False
                raise create.StepError(f"panne simulée à {k}")
            return real[k](self)
        return f
    for k in calls:
        monkeypatch.setattr(create.Creation, "step_" + k, spy(k))
    c, rec = make(values(tmp_path, idea, chain_root, remote=str(remote)), chain_root)
    out = c.run()
    i = [k for k, _ in create.STEPS].index(failing)
    assert out["status"] == create.FAILED and out["failed_at"] == failing and out["error"] == f"panne simulée à {failing}"
    assert [s["status"] for s in out["steps"][:i]] == [create.OK] * i
    assert all(s["status"] == create.TODO for s in out["steps"][i + 1:])
    # « Reprendre »: from the record config.json keeps, from that step on.
    stored = rec.records[-1]
    c2, rec2 = make(stored["values"], chain_root, record=json.loads(json.dumps(stored)))
    out = c2.run()
    assert out["status"] == create.OK, out
    assert calls == {k: (2 if k == failing else 1) for k in calls}
    app = tmp_path / "dev" / "mon-appli"
    assert len(subjects(app)) == 3 and git(app, "status", "--porcelain").strip() == ""
    assert git(remote, "rev-parse", "master") == git(app, "rev-parse", "HEAD")


def test_every_step_checks_what_is_there_and_does_not_redo_it(tmp_path, idea, chain_root):
    """A creation whose record was lost, run again on the folder it made:
    each step finds its work done, and no commit is added."""
    remote = bare(tmp_path)
    v = values(tmp_path, idea, chain_root, remote=str(remote))
    assert make(v, chain_root)[0].run()["status"] == create.OK
    app = tmp_path / "dev" / "mon-appli"
    head = git(app, "rev-parse", "HEAD")
    out = make(v, chain_root)[0].run()
    assert out["status"] == create.OK, out
    d = [s["detail"] for s in out["steps"]]
    assert d[0] == "déjà là" and "déjà poussé" in d[1]
    assert d[2].startswith("déjà installée") and d[2].endswith("déjà poussé")
    assert d[3] == "déjà là — déjà poussé" and d[4] == "déjà là — déjà poussé"
    assert git(app, "rev-parse", "HEAD") == head


def test_a_push_that_fails_stops_and_reprendre_pushes(tmp_path, idea, chain_root, monkeypatch):
    remote = bare(tmp_path)
    real = chain.push_branch
    n = {"calls": 0}

    def flaky(app):
        n["calls"] += 1
        if n["calls"] == 1:
            raise chain.InstallError("git push : unable to access 'https://github.com/': Could not resolve host")
        return real(app)
    monkeypatch.setattr(chain, "push_branch", flaky)
    c, rec = make(values(tmp_path, idea, chain_root, remote=str(remote)), chain_root)
    out = c.run()
    assert out["failed_at"] == "chaine" and "le commit est fait, le push a échoué" in out["error"]
    app = tmp_path / "dev" / "mon-appli"
    assert len(subjects(app)) == 1
    out = make(rec.records[-1]["values"], chain_root, record=rec.records[-1])[0].run()
    assert out["status"] == create.OK
    assert out["steps"][2]["detail"].startswith("déjà installée") and out["steps"][2]["detail"].endswith("— poussé")
    assert len(subjects(app)) == 3 and git(remote, "rev-parse", "master") == git(app, "rev-parse", "HEAD")


def test_an_idea_file_already_there_and_different_is_never_overwritten(tmp_path, idea, chain_root, monkeypatch):
    monkeypatch.setattr(create.Creation, "step_liste", lambda self: (create.OK, "x"))
    v = values(tmp_path, idea, chain_root)
    c, rec = make(v, chain_root)
    real = create.Creation.step_idees
    monkeypatch.setattr(create.Creation, "step_idees", lambda self: (_ for _ in ()).throw(create.StepError("panne")))
    c.run()
    monkeypatch.setattr(create.Creation, "step_idees", real)
    target = tmp_path / "dev" / "mon-appli" / "docs" / "features" / "premiere-app" / "idees.md"
    target.parent.mkdir(parents=True)
    target.write_text("autre chose\n", encoding="utf-8")
    out = make(v, chain_root, record=rec.records[-1])[0].run()
    assert out["failed_at"] == "idees" and "rien n'est écrasé" in out["error"]
    assert target.read_text(encoding="utf-8") == "autre chose\n"


# ----------------------------------------------------------------- routes

async def until_done(c):
    for _ in range(600):
        r = await (await c.get("/api/create")).json()
        if not r["going"]:
            return r
        await asyncio.sleep(0.05)
    raise AssertionError("la création ne finit pas")


def test_the_routes_create_resume_and_open_on_lexique(tmp_path, idea, chain_root, monkeypatch):
    real = create.Creation.step_socle
    armed = {"on": True}

    def once(self):
        if armed["on"]:
            armed["on"] = False
            raise create.StepError("panne simulée")
        return real(self)
    monkeypatch.setattr(create.Creation, "step_socle", once)
    f = form(tmp_path, idea, name="Atelier Été", feature="premiere-app")

    async def body(c, app_root, feat, rn):
        r = await (await post(c, "/api/create/check", f)).json()
        assert r["ok"] and r["values"]["folder"] == "atelier-ete" and r["idea_lines"][0] == "# Mon appli"
        assert len(r["summary"]) == 6
        bad = await post(c, "/api/create", {**f, "feature": "Ma feature"})
        assert bad.status == 400 and "feature" in (await bad.json())["errors"]
        r = await post(c, "/api/create", f)
        assert r.status == 200, await r.text()
        out = await until_done(c)
        assert out["last"]["status"] == create.FAILED and out["last"]["failed_at"] == "socle"
        assert [p["values"]["path"] for p in out["pending"]] == [out["last"]["values"]["path"]]
        path = out["last"]["values"]["path"]
        # The form now says « Reprendre » for that folder, never « Créer ».
        assert (await (await post(c, "/api/create/check", f)).json())["values"]["resume"]
        assert (await post(c, "/api/create", f)).status == 409
        r = await post(c, "/api/create/resume", {"path": path})
        assert r.status == 200
        out = await until_done(c)
        assert out["last"]["status"] == create.OK and out["pending"] == []
        assert "le relevé du dossier propose : Lancer /1_lexique premiere-app." in out["last"]["steps"][5]["detail"]
        s = await (await c.get("/api/state")).json()
        assert s["app_name"] == "Atelier Été" and s["feature"] == "premiere-app" and s["open"]
        assert s["decision"]["next"]["command"] == "1_lexique" and s["decision"]["next"]["args"] == "premiere-app"
        assert s["chain"]["state"] == chain.UP_TO_DATE
        assert "provide" not in s                    # « À fournir avant le code » went
        assert "deploie" not in [x["name"] for x in s["commands"]]
        assert (await post(c, "/api/create/resume", {"path": path})).status == 404
    with_client(tmp_path, body)


def test_abandon_leaves_the_folder(tmp_path, idea, chain_root, monkeypatch):
    monkeypatch.setattr(create.Creation, "step_chaine", lambda self: (_ for _ in ()).throw(create.StepError("panne")))
    f = form(tmp_path, idea)

    async def body(c, app_root, feat, rn):
        assert (await post(c, "/api/create", f)).status == 200
        out = await until_done(c)
        path = out["last"]["values"]["path"]
        r = await (await post(c, "/api/create/forget", {"path": path})).json()
        assert r["contents"] == [".git/", ".gitignore"]
        assert (await (await c.get("/api/create")).json())["pending"] == []
        assert os.path.isdir(os.path.join(path, ".git"))
        # Not resumable any more: the folder is not empty, the form refuses it.
        assert "n'est pas vide" in (await (await post(c, "/api/create/check", f)).json())["errors"]["folder"]
    with_client(tmp_path, body)


def test_no_provide_card_any_more():
    """« À fournir avant le code » went with socle.py's PROVIDE: the chain
    ships the skill and the format, /conventions writes the conventions."""
    assert not hasattr(server, "provide_lines") and not hasattr(server, "socle_module")


def test_a_creation_the_server_stopped_mid_step_is_offered_reprendre(tmp_path, idea, chain_root):
    """config.json holds it « en cours », and no server runs it: shown
    stopped at its step, and « Reprendre » finishes it."""
    v = values(tmp_path, idea, chain_root)
    c, rec = make(v, chain_root)
    c.steps[0]["status"] = create.OK
    c.steps[1]["status"] = create.NONE
    c.steps[2]["status"] = create.GOING
    c.status = create.GOING
    os.makedirs(v["path"])
    subprocess.run(["git", "init", "-q", "-b", "master", v["path"]], check=True)

    async def body(cl, app_root, feat, rn):
        server_state = cl.server.app[server.STATE_KEY]
        server_state.set_creation(c.record())
        out = await (await cl.get("/api/create")).json()
        p = out["pending"][0]
        assert out["going"] is None and p["status"] == create.FAILED and p["failed_at"] == "chaine"
        assert "interrompue" in p["error"]
        assert (await post(cl, "/api/create/resume", {"path": v["path"]})).status == 200
        out = await until_done(cl)
        assert out["last"]["status"] == create.OK, out["last"]
        assert len(subjects(tmp_path / "dev" / "mon-appli")) == 3
    with_client(tmp_path, body)
