"""§20 — the chain installed into an application: its four states, an
install and an update on scratch repositories, and the refusals. Every
repository here is built in tmp_path; nothing reaches GitHub."""
import json
import subprocess

import pytest

import chain
import server
from copies import built_once
from test_runner import script_until_interrupted
from test_server import open_pair, post, with_client

pytestmark = pytest.mark.real_chain


def git(repo, *args):
    p = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, encoding="utf-8")
    assert p.returncode == 0, (args, p.stderr)
    return p.stdout


def init(repo, crlf=False):
    repo.mkdir(parents=True, exist_ok=True)
    git(repo, "init", "-q", "-b", "master")
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "config", "user.name", "T")
    git(repo, "config", "core.autocrlf", "true" if crlf else "false")


def write(repo, rel, text):
    p = repo.joinpath(*rel.split("/"))
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(text.encode("utf-8"))


def commit(repo, msg):
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", msg)
    return git(repo, "rev-parse", "HEAD").strip()


CHAIN_FILES = {
    ".claude/CLAUDE.md": "# Orchestrator\n",
    ".claude/agents/a.md": "agent a\n",
    ".claude/agents/b.md": "agent b\n",
    ".claude/commands/1_x.md": "---\ndescription: x\n---\nbody\n",
    ".claude/scripts/s.py": "print('s')\n",
    ".claude/grids/GRILLE_G.md": "grid\n",
    ".claude/formats/deploy-profile.md": "format\n",
    ".claude/skills/technical-state-format/SKILL.md": "---\nname: technical-state-format\n---\nskill\n",
    # Not the chain: never installed.
    ".claude/skills/other/SKILL.md": "another skill\n",
    "tools/cockpit/x.py": "cockpit\n",
    "docs/process/PROCESS_X.md": "process\n",
    ".claude/settings.local.json": "{}\n",
}


# What an install writes: the chain's files, nothing else.
INSTALLED = [".claude/CLAUDE.md", ".claude/agents/a.md", ".claude/agents/b.md", ".claude/commands/1_x.md",
             ".claude/scripts/s.py", ".claude/grids/GRILLE_G.md", ".claude/formats/deploy-profile.md",
             ".claude/skills/technical-state-format/SKILL.md"]


@pytest.fixture
def repos(tmp_path):
    """The chain's repository, and an application pushed to its bare
    GitHub — built once per run, copied here (copies.py)."""
    root, app, remote = built_once("chain-repos", tmp_path, _repos)
    chain._chain_cache.clear()
    chain._behind_cache.clear()
    return root, app, remote


def _repos(tmp_path):
    root = tmp_path / "chain"
    init(root)
    for rel, text in CHAIN_FILES.items():
        write(root, rel, text)
    commit(root, "chain one")
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
    app = tmp_path / "app"
    init(app)
    write(app, ".claude/commands/deploie.md", "the application's own\n")
    write(app, "docs/features/f/idees.md", "idea\n")
    commit(app, "app")
    git(app, "remote", "add", "origin", str(remote))
    git(app, "push", "-q", "-u", "origin", "master")
    return root, app, remote


def files_of(app_commit_repo, ref="HEAD"):
    return sorted(git(app_commit_repo, "show", "--name-only", "--format=", ref).split())


# ------------------------------------------------------------------ states

def test_absent_then_up_to_date(repos):
    root, app, remote = repos
    st = chain.state(str(app), str(root))
    assert st["state"] == chain.ABSENT and "chain-version.json" in st["summary"]
    res = chain.install(str(app), str(root))
    head = git(root, "log", "-1", "--format=%h %cs").split()
    assert res["message"] == f"chain: {head[0]} {head[1]}"
    assert res["pushed"] and git(app, "rev-parse", "HEAD") == git(remote, "rev-parse", "master")
    # The chain's files and chain-version.json, nothing else.
    assert files_of(app) == sorted(INSTALLED + [".claude/chain-version.json"])
    assert not (app / "tools").exists() and not (app / "docs" / "process").exists()
    assert not (app / ".claude" / "settings.local.json").exists()
    assert not (app / ".claude" / "skills" / "other").exists()
    assert (app / ".claude/commands/deploie.md").read_text(encoding="utf-8") == "the application's own\n"
    v = json.loads((app / ".claude/chain-version.json").read_text(encoding="utf-8"))
    assert v["commit"] == git(root, "rev-parse", "HEAD").strip()
    assert v["date"] == git(root, "log", "-1", "--format=%cI").strip()
    assert v["files"][".claude/agents/a.md"] == chain.digest(b"agent a\n")
    assert ".claude/commands/deploie.md" not in v["files"]
    st = chain.state(str(app), str(root))
    assert st["state"] == chain.UP_TO_DATE and st["commit"] == head[0]


def test_a_commit_outside_the_chain_leaves_it_up_to_date(repos):
    root, app, _ = repos
    chain.install(str(app), str(root))
    write(root, "tools/cockpit/x.py", "cockpit 2\n")
    commit(root, "cockpit only")
    assert chain.state(str(app), str(root))["state"] == chain.UP_TO_DATE


def test_behind_says_how_many_and_which(repos):
    root, app, _ = repos
    chain.install(str(app), str(root))
    write(root, ".claude/agents/a.md", "agent a, two\n")
    commit(root, "chain two")
    write(root, "tools/cockpit/x.py", "cockpit 2\n")
    commit(root, "cockpit two")
    write(root, ".claude/grids/GRILLE_G.md", "grid two\n")
    commit(root, "chain three")
    st = chain.state(str(app), str(root))
    assert st["state"] == chain.BEHIND and st["behind"] == 2
    assert [s.split(" ", 1)[1] for s in st["subjects"]] == ["chain three", "chain two"]
    assert "en retard de 2 commits" in st["summary"]


def test_modified_in_place_lists_the_files(repos):
    root, app, _ = repos
    chain.install(str(app), str(root))
    write(app, ".claude/agents/b.md", "changed here\n")
    (app / ".claude/scripts/s.py").unlink()
    st = chain.state(str(app), str(root))
    assert st["state"] == chain.MODIFIED
    assert st["modified"] == [".claude/agents/b.md", ".claude/scripts/s.py"]


def test_line_ends_are_not_a_change(repos):
    root, app, _ = repos
    chain.install(str(app), str(root))
    p = app / ".claude/agents/a.md"
    p.write_bytes(p.read_bytes().replace(b"\n", b"\r\n"))
    assert chain.state(str(app), str(root))["state"] == chain.UP_TO_DATE


# ----------------------------------------------------------- install, update

def test_update_writes_removes_and_leaves_the_application_alone(repos):
    root, app, remote = repos
    chain.install(str(app), str(root))
    write(app, ".claude/commands/deploie.md", "the application's own, two\n")
    commit(app, "deploie two")
    write(root, ".claude/agents/a.md", "agent a, two\n")
    (root / ".claude/agents/b.md").unlink()
    write(root, ".claude/agents/c.md", "agent c\n")
    commit(root, "chain two")
    res = chain.install(str(app), str(root))
    assert res["written"] == [".claude/agents/a.md", ".claude/agents/c.md"]
    assert res["removed"] == [".claude/agents/b.md"]
    assert files_of(app) == [".claude/agents/a.md", ".claude/agents/b.md", ".claude/agents/c.md",
                             ".claude/chain-version.json"]
    assert not (app / ".claude/agents/b.md").exists()
    assert (app / ".claude/commands/deploie.md").read_text(encoding="utf-8") == "the application's own, two\n"
    assert git(app, "status", "--porcelain") == ""
    assert git(app, "rev-parse", "HEAD") == git(remote, "rev-parse", "master")
    v = json.loads((app / ".claude/chain-version.json").read_text(encoding="utf-8"))
    assert ".claude/agents/b.md" not in v["files"] and ".claude/agents/c.md" in v["files"]
    assert chain.state(str(app), str(root))["state"] == chain.UP_TO_DATE


def _longpaths(repo):
    p = subprocess.run(["git", "-C", str(repo), "config", "--local", "--get", "core.longpaths"],
                       capture_output=True, text=True)
    return p.stdout.strip() or None


def test_an_install_sets_long_paths_on_windows(repos, monkeypatch):
    """A build in a worktree writes paths deeper than Windows' limit: the
    install sets core.longpaths in the application's own config, so that
    `git worktree remove` holds in every command."""
    root, app, _ = repos
    monkeypatch.setattr(chain, "WINDOWS", True)
    assert _longpaths(app) is None
    chain.install(str(app), str(root))
    assert _longpaths(app) == "true"


def test_an_update_sets_long_paths_on_a_repository_without_it(repos, monkeypatch):
    root, app, _ = repos
    monkeypatch.setattr(chain, "WINDOWS", True)
    chain.install(str(app), str(root))
    git(app, "config", "--local", "--unset", "core.longpaths")
    write(root, ".claude/agents/a.md", "agent a, two\n")
    commit(root, "chain two")
    chain.install(str(app), str(root))
    assert _longpaths(app) == "true"
    # Nothing of the chain changed: the update still sets it.
    git(app, "config", "--local", "--unset", "core.longpaths")
    assert chain.install(str(app), str(root))["app_commit"] is None
    assert _longpaths(app) == "true"


def test_long_paths_left_alone_outside_windows(repos, monkeypatch):
    root, app, _ = repos
    monkeypatch.setattr(chain, "WINDOWS", False)
    chain.install(str(app), str(root))
    assert _longpaths(app) is None


def test_nothing_changed_commits_nothing(repos):
    root, app, _ = repos
    chain.install(str(app), str(root))
    before = git(app, "rev-parse", "HEAD")
    res = chain.install(str(app), str(root))
    assert res["app_commit"] is None and git(app, "rev-parse", "HEAD") == before


def test_the_product_owners_staged_work_stays_out_of_the_commit(repos):
    root, app, _ = repos
    write(app, "docs/features/f/notes.md", "mine\n")
    git(app, "add", "docs/features/f/notes.md")
    chain.install(str(app), str(root))
    assert "docs/features/f/notes.md" not in files_of(app)
    assert git(app, "status", "--porcelain").strip() == "A  docs/features/f/notes.md"


def test_crlf_application(repos, tmp_path):
    root, app, _ = repos
    git(app, "config", "core.autocrlf", "true")
    chain.install(str(app), str(root))
    assert (app / ".claude/agents/a.md").read_bytes() == b"agent a\r\n"
    assert git(app, "status", "--porcelain") == ""
    assert chain.state(str(app), str(root))["state"] == chain.UP_TO_DATE


# ------------------------------------------------------------- it asks first

def test_modified_in_place_asks_before_overwriting(repos):
    root, app, _ = repos
    chain.install(str(app), str(root))
    write(app, ".claude/agents/a.md", "changed here\n")
    commit(app, "changed in place")
    with pytest.raises(chain.NeedsConfirm) as e:
        chain.install(str(app), str(root))
    assert e.value.files == [".claude/agents/a.md"]
    assert (app / ".claude/agents/a.md").read_text(encoding="utf-8") == "changed here\n"
    chain.install(str(app), str(root), confirm=True)
    assert (app / ".claude/agents/a.md").read_text(encoding="utf-8") == "agent a\n"
    assert chain.state(str(app), str(root))["state"] == chain.UP_TO_DATE


def test_a_first_install_asks_before_replacing_what_is_there(repos):
    root, app, _ = repos
    write(app, ".claude/agents/a.md", "an older chain\n")
    write(app, ".claude/agents/b.md", "agent b\n")          # the same: nothing to ask
    commit(app, "older chain")
    write(app, ".claude/grids/GRILLE_G.md", "not committed\n")
    with pytest.raises(chain.NeedsConfirm) as e:
        chain.install(str(app), str(root))
    assert e.value.files == [".claude/agents/a.md", ".claude/grids/GRILLE_G.md"]
    chain.install(str(app), str(root), confirm=True)
    assert chain.state(str(app), str(root))["state"] == chain.UP_TO_DATE


def test_an_applications_own_copy_of_the_skill_is_replaced_only_once_asked(repos):
    """An application installed before the chain shipped the skill holds its
    own copy: the install asks before replacing it, as any differing file
    already there, and never touches the application's other skills."""
    root, app, _ = repos
    skill = ".claude/skills/technical-state-format/SKILL.md"
    git(root, "rm", "-q", "--", skill)
    commit(root, "chain without the skill")
    chain.install(str(app), str(root))
    write(app, skill, "---\nname: technical-state-format\n---\nthe application's own\n")
    write(app, ".claude/skills/mine/SKILL.md", "mine\n")
    commit(app, "own skills")
    write(root, skill, CHAIN_FILES[skill])
    commit(root, "chain ships the skill")
    assert chain.plan(str(app), str(root))["ask"] == [skill]
    with pytest.raises(chain.NeedsConfirm) as e:
        chain.install(str(app), str(root))
    assert e.value.files == [skill]
    assert "the application's own" in (app / skill).read_text(encoding="utf-8")
    chain.install(str(app), str(root), confirm=True)
    assert (app / skill).read_text(encoding="utf-8") == CHAIN_FILES[skill]
    assert (app / ".claude/skills/mine/SKILL.md").read_text(encoding="utf-8") == "mine\n"
    assert chain.state(str(app), str(root))["state"] == chain.UP_TO_DATE


def test_an_applications_copy_identical_to_the_chains_is_not_asked(repos):
    root, app, _ = repos
    skill = ".claude/skills/technical-state-format/SKILL.md"
    write(app, skill, CHAIN_FILES[skill].replace("\n", "\r\n"))     # CRLF reads as LF
    commit(app, "same skill")
    assert chain.plan(str(app), str(root))["ask"] == []
    chain.install(str(app), str(root))
    assert chain.state(str(app), str(root))["state"] == chain.UP_TO_DATE


# ----------------------------------------------------------------- refusals

def test_refused_while_a_managed_file_is_not_committed(repos):
    root, app, _ = repos
    chain.install(str(app), str(root))
    write(app, ".claude/agents/a.md", "uncommitted\n")
    with pytest.raises(chain.InstallError, match="non commitées.*a.md"):
        chain.install(str(app), str(root), confirm=True)
    assert (app / ".claude/agents/a.md").read_text(encoding="utf-8") == "uncommitted\n"


def test_the_applications_own_uncommitted_work_does_not_refuse(repos):
    root, app, _ = repos
    chain.install(str(app), str(root))
    write(app, ".claude/commands/deploie.md", "being edited\n")
    write(root, ".claude/agents/a.md", "agent a, two\n")
    commit(root, "chain two")
    chain.install(str(app), str(root))
    assert git(app, "status", "--porcelain").strip() == "M .claude/commands/deploie.md"


def test_refused_outside_a_repository_and_in_the_chain_itself(repos, tmp_path):
    root, _, _ = repos
    plain = tmp_path / "plain"
    (plain / ".claude").mkdir(parents=True)
    with pytest.raises(chain.InstallError, match="pas un dépôt git"):
        chain.install(str(plain), str(root))
    with pytest.raises(chain.InstallError, match="dépôt de la chaîne"):
        chain.install(str(root), str(root))


def test_an_unreadable_version_file(repos):
    root, app, _ = repos
    write(app, ".claude/chain-version.json", "{ broken")
    assert chain.state(str(app), str(root))["state"] == chain.MODIFIED
    with pytest.raises(chain.InstallError, match="illisible"):
        chain.install(str(app), str(root))


# ----------------------------------------------------------------- the server

def _gitify(app_root, remote):
    init(app_root)
    commit(app_root, "app")
    git(app_root, "remote", "add", "origin", str(remote))
    git(app_root, "push", "-q", "-u", "origin", "master")


def test_server_launch_asks_and_install_refuses_while_a_run_goes(tmp_path, monkeypatch):
    root = tmp_path / "chain"
    init(root)
    for rel, text in CHAIN_FILES.items():
        write(root, rel, text)
    commit(root, "chain one")
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
    monkeypatch.setattr(server, "CHAIN_ROOT", str(root))
    chain._chain_cache.clear()

    async def body(c, app_root, feat, rn):
        _gitify(app_root, remote)
        await open_pair(c, app_root)
        s = await (await c.get("/api/state")).json()
        assert s["chain"]["state"] == chain.ABSENT
        # Not « à jour »: the launch asks first.
        r = await post(c, "/api/run", {"command": "1_lexique", "args": "f"})
        assert r.status == 409 and (await r.json())["chain"]["state"] == chain.ABSENT
        assert not rn.is_running(str(app_root))
        r = await post(c, "/api/run", {"command": "1_lexique", "args": "f", "chain_ok": True})
        assert r.status == 200
        # A run goes: no install.
        r = await post(c, "/api/chain/install", {})
        assert r.status == 409 and "tourne" in (await r.json())["error"]
        await rn.stop_now(str(app_root))
        assert await rn.wait_ended(str(app_root), 10)
        r = await post(c, "/api/chain/install", {})
        j = await r.json()
        assert r.status == 200, j
        assert j["chain"]["state"] == chain.UP_TO_DATE and j["result"]["pushed"]
        # The application's own commands are still listed, beside the chain's.
        s = await (await c.get("/api/state")).json()
        names = {x["name"] for x in s["commands"]}
        assert {"1_x", "deploie", "1_lexique"} <= names
        r = await post(c, "/api/run", {"command": "1_x", "args": "f"})
        assert r.status == 200
    with_client(tmp_path, body, script=script_until_interrupted)


def test_server_install_asks_before_overwriting(tmp_path, monkeypatch):
    root = tmp_path / "chain"
    init(root)
    for rel, text in CHAIN_FILES.items():
        write(root, rel, text)
    commit(root, "chain one")
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
    monkeypatch.setattr(server, "CHAIN_ROOT", str(root))
    chain._chain_cache.clear()

    async def body(c, app_root, feat, rn):
        write(app_root, ".claude/agents/a.md", "an older chain\n")
        _gitify(app_root, remote)
        await open_pair(c, app_root)
        r = await post(c, "/api/chain/install", {})
        j = await r.json()
        assert r.status == 409 and j["overwrite"] == [".claude/agents/a.md"]
        assert (app_root / ".claude/agents/a.md").read_text(encoding="utf-8") == "an older chain\n"
        r = await post(c, "/api/chain/install", {"confirm": True})
        assert r.status == 200 and (await r.json())["chain"]["state"] == chain.UP_TO_DATE
    with_client(tmp_path, body)


# --------------------------------------------- the first commit (1.7)

def test_first_install_on_an_empty_repository_is_its_first_commit(tmp_path, repos):
    root, _, _ = repos
    app = tmp_path / "neuve"
    init(app)
    res = chain.install(str(app), str(root), push=True)
    assert res["app_commit"] and git(app, "rev-list", "--count", "HEAD").strip() == "1"
    assert git(app, "log", "-1", "--format=%s").strip() == res["message"]
    assert files_of(app) == sorted(INSTALLED + [".claude/chain-version.json"])
    # No remote: the commit stands, the push says why.
    assert not res["pushed"] and "push" in res["push_error"]
    assert chain.state(str(app), str(root))["state"] == chain.UP_TO_DATE


def test_first_push_sets_the_upstream(tmp_path, repos):
    root, _, _ = repos
    app = tmp_path / "neuve"
    init(app)
    remote = tmp_path / "neuve.git"
    subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
    git(app, "remote", "add", "origin", str(remote))
    res = chain.install(str(app), str(root), push=True)
    assert res["pushed"], res["push_error"]
    assert git(app, "rev-parse", "--abbrev-ref", "@{u}").strip() == "origin/master"
    assert git(remote, "rev-parse", "master") == git(app, "rev-parse", "HEAD")
    # Every later push is a plain one.
    write(root, ".claude/agents/a.md", "agent a, two\n")
    commit(root, "chain two")
    chain._chain_cache.clear()
    assert chain.install(str(app), str(root), push=True)["pushed"]
    assert git(remote, "rev-parse", "master") == git(app, "rev-parse", "HEAD")


def test_a_first_install_that_failed_before_its_commit_is_done_again(tmp_path, repos, monkeypatch):
    """Its files and chain-version.json are there, uncommitted: with no
    commit yet, nothing counts as installed, and they compare by content."""
    root, _, _ = repos
    app = tmp_path / "neuve"
    init(app)
    real = chain._git

    def no_commit(repo, *args, **kw):
        if args and args[0] == "commit":
            raise chain.InstallError("git commit : simulated")
        return real(repo, *args, **kw)
    monkeypatch.setattr(chain, "_git", no_commit)
    with pytest.raises(chain.InstallError):
        chain.install(str(app), str(root), push=False)
    assert (app / ".claude" / "chain-version.json").exists()
    monkeypatch.setattr(chain, "_git", real)
    res = chain.install(str(app), str(root), push=False)
    assert res["app_commit"] and git(app, "status", "--porcelain").strip() == ""
