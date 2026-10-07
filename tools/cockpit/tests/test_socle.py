""".claude/scripts/socle.py — the scaffolding of a new application, on
scratch repositories: what it writes, what it commits, its refusal, its
report. The script is the chain's own, copied where an install puts it."""
import os
import shutil
import subprocess
import sys

import pytest

from test_chain import commit, git, init, write

CHAIN = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SCRIPT = os.path.join(CHAIN, ".claude", "scripts", "socle.py")


def place(repo):
    target = repo / ".claude" / "scripts" / "socle.py"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SCRIPT, target)
    return target


def run(repo, *args):
    p = subprocess.run([sys.executable, str(repo / ".claude" / "scripts" / "socle.py"), *args],
                       capture_output=True, text=True, encoding="utf-8")
    return p.returncode, p.stdout, p.stderr


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "neuve"
    init(r)
    place(r)
    commit(r, "chain: 0000000 2026-10-06")
    return r


def test_a_new_application(repo, tmp_path):
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
    git(repo, "remote", "add", "origin", str(remote))
    rc, out, err = run(repo)
    assert rc == 0, err
    assert (repo / "docs" / "PRODUIT_GLOBAL.md").read_bytes() == b"# Application\n"
    assert (repo / "docs" / "CURRENT_TECHNICAL_STATE.md").read_bytes() == b"# Technical state\n"
    assert (repo / "docs" / "features").is_dir() and not os.listdir(repo / "docs" / "features")
    assert (repo / ".gitignore").read_text(encoding="utf-8").splitlines() == [
        "docs/features/*/stop.md", "docs/features/*/stop1.md", ".claude/worktrees/", ".claude/settings.local.json"]
    assert not (repo / "docs" / "TECHNICAL_CONVENTIONS.md").exists()
    # One commit, those files alone; nothing pushed.
    assert git(repo, "log", "-1", "--format=%s").strip() == "chore: scaffolding for the chain"
    assert sorted(git(repo, "show", "--name-only", "--format=", "HEAD").split()) == [
        ".gitignore", "docs/CURRENT_TECHNICAL_STATE.md", "docs/PRODUIT_GLOBAL.md"]
    assert git(repo, "status", "--porcelain").strip() == ""
    assert subprocess.run(["git", "-C", str(remote), "rev-parse", "-q", "--verify", "master"],
                          capture_output=True).returncode != 0
    # Nothing left to provide: the chain ships the skill and the format,
    # /conventions writes the conventions.
    assert "À fournir" not in out and out.startswith("Commité « chore: scaffolding for the chain »")


def test_refused_when_the_global_exists(repo):
    write(repo, "docs/PRODUIT_GLOBAL.md", "# Application\n\n## Séances\n")
    commit(repo, "global")
    head = git(repo, "rev-parse", "HEAD")
    rc, out, err = run(repo)
    assert rc == 2 and "docs/PRODUIT_GLOBAL.md existe déjà" in err
    assert (repo / "docs" / "PRODUIT_GLOBAL.md").read_text(encoding="utf-8") == "# Application\n\n## Séances\n"
    assert not (repo / "docs" / "CURRENT_TECHNICAL_STATE.md").exists() and not (repo / ".gitignore").exists()
    assert git(repo, "rev-parse", "HEAD") == head


def test_gitignore_lines_appended_never_rewritten(repo):
    (repo / ".gitignore").write_bytes(b"build/\r\n.claude/worktrees/")
    commit(repo, "ignore")
    assert run(repo)[0] == 0
    assert (repo / ".gitignore").read_bytes() == (b"build/\r\n.claude/worktrees/\r\ndocs/features/*/stop.md\r\n"
                                                  b"docs/features/*/stop1.md\r\n.claude/settings.local.json\r\n")


def test_what_the_owner_staged_stays_out(repo):
    write(repo, "notes.md", "mine\n")
    git(repo, "add", "notes.md")
    assert run(repo)[0] == 0
    assert "notes.md" not in git(repo, "show", "--name-only", "--format=", "HEAD")
    assert git(repo, "diff", "--cached", "--name-only").split() == ["notes.md"]


def test_an_argument_is_refused_and_writes_nothing(repo):
    """`--list` went with PROVIDE: any argument is refused."""
    rc, out, err = run(repo, "--list")
    assert rc == 1 and "usage" in err
    assert not (repo / "docs").exists()


def test_no_identity_writes_nothing(repo, monkeypatch, tmp_path):
    """Who commits is asked before anything is written: a commit that fails
    would leave the global, and the next run refused."""
    env = dict(os.environ, GIT_CONFIG_GLOBAL=str(tmp_path / "none"), GIT_CONFIG_NOSYSTEM="1",
               GIT_AUTHOR_NAME="", GIT_COMMITTER_NAME="", EMAIL="")
    git(repo, "config", "--unset", "user.name")
    git(repo, "config", "--unset", "user.email")
    p = subprocess.run([sys.executable, str(repo / ".claude" / "scripts" / "socle.py")], capture_output=True,
                       text=True, encoding="utf-8", env=env)
    assert p.returncode == 1 and "git var" in p.stderr
    assert not (repo / "docs").exists()


def test_no_provide_list_any_more():
    """PROVIDE went: its two readers were the cockpit's « À fournir avant le
    code » card and the creation's summary, which went with it."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("socle", SCRIPT)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    assert not hasattr(m, "PROVIDE") and not hasattr(m, "missing")


def test_a_technical_state_already_there_is_kept(repo):
    write(repo, "docs/CURRENT_TECHNICAL_STATE.md", "# Technical state\n\n## Traps — general\n")
    commit(repo, "state")
    assert run(repo)[0] == 0
    assert "Traps" in (repo / "docs" / "CURRENT_TECHNICAL_STATE.md").read_text(encoding="utf-8")
    assert sorted(git(repo, "show", "--name-only", "--format=", "HEAD").split()) == [".gitignore", "docs/PRODUIT_GLOBAL.md"]


def test_long_paths_set_on_windows(repo, monkeypatch):
    """socle.py sets core.longpaths in the new application's own config, on
    Windows — the install does too, at every install and update."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("socle_placed", str(repo / ".claude" / "scripts" / "socle.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    monkeypatch.setattr(m, "WINDOWS", True)
    m.scaffold(str(repo))
    assert git(repo, "config", "--local", "--get", "core.longpaths").strip() == "true"
    assert "core.longpaths" not in git(repo, "show", "--name-only", "--format=", "HEAD")
