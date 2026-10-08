"""1.12 — always agreeing with GitHub: each state of §1, offline included;
§2's launch rules; §3's rejected push; §4's reconciliation, clean and
conflicting; §5's commit of the answers, then the next command's own commit
step finding nothing; §7's clone and long paths. Bare repositories play
GitHub, in temporary folders; nothing reaches the real GitHub."""
import os
import re
import subprocess

import pytest

import sync
from syncworld import change, clone_of, head, offline, online, world
from test_chain import git, write

CHAIN = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


# ------------------------------------------------------------ §1 the states

def test_up_to_date(tmp_path):
    _, a, _ = world(tmp_path)
    st = sync.compute(str(a))
    assert st["state"] == sync.UP_TO_DATE and st["fetched"] and st["uncommitted"] == 0
    assert st["upstream"] == "origin/master"


def test_behind(tmp_path):
    _, a, b = world(tmp_path)
    change(b, "x.md", "x\n", push=True)
    change(b, "y.md", "y\n", push=True)
    st = sync.compute(str(a))
    assert st["state"] == sync.BEHIND and st["behind"] == 2 and st["ahead"] == 0
    assert "GitHub a 2 commits" in st["summary"]


def test_ahead(tmp_path):
    _, a, _ = world(tmp_path)
    change(a, "x.md", "x\n")
    st = sync.compute(str(a))
    assert st["state"] == sync.AHEAD and st["ahead"] == 1


def test_diverged(tmp_path):
    _, a, b = world(tmp_path)
    change(b, "x.md", "x\n", push=True)
    change(a, "y.md", "y\n")
    st = sync.compute(str(a))
    assert st["state"] == sync.DIVERGED and (st["ahead"], st["behind"]) == (1, 1)


def test_offline(tmp_path):
    _, a, _ = world(tmp_path)
    offline(a)
    st = sync.compute(str(a))
    assert st["state"] == sync.OFFLINE and not st["fetched"]
    assert "injoignable" in st["summary"]


def test_uncommitted_counted(tmp_path):
    _, a, _ = world(tmp_path)
    write(a, "README.md", "changed\n")
    write(a, "new.md", "new\n")
    assert sync.compute(str(a))["uncommitted"] == 2


def test_no_remote_and_no_repository(tmp_path):
    from test_chain import init
    r = tmp_path / "local"
    init(r)
    write(r, "a.md", "a\n")
    git(r, "add", "-A")
    git(r, "commit", "-q", "-m", "a")
    assert sync.compute(str(r))["state"] == sync.NO_REMOTE
    (tmp_path / "plain").mkdir()
    st = sync.compute(str(tmp_path / "plain"))
    assert st["state"] is None and st["detail"] == "pas un dépôt git"


def test_branch_not_on_github_yet_is_not_sent(tmp_path):
    """A first commit never pushed: no upstream, the remote has no branch."""
    from syncworld import bare
    from test_chain import init
    remote = bare(tmp_path / "gh.git")
    r = tmp_path / "new"
    init(r)
    write(r, "a.md", "a\n")
    git(r, "add", "-A")
    git(r, "commit", "-q", "-m", "a")
    git(r, "remote", "add", "origin", str(remote))
    st = sync.compute(str(r))
    assert st["state"] == sync.AHEAD and st["ahead"] == 1
    assert sync.push(str(r))["ok"]
    assert sync.compute(str(r))["state"] == sync.UP_TO_DATE


def test_env_never_prompts():
    e = sync.env()
    assert e["GIT_TERMINAL_PROMPT"] == "0" and e["GCM_INTERACTIVE"] == "never"


# ------------------------------------------------------------ §2 before a launch

def test_behind_pulled_then_launched(tmp_path):
    _, a, b = world(tmp_path)
    sha = change(b, "x.md", "x\n", push=True)
    book = sync.Book()
    res = sync.before_launch(book, str(a))
    assert res["ok"] and head(a) == sha
    assert res["sync"]["state"] == sync.UP_TO_DATE and "récupéré" in res["notice"]
    # Fast-forward only: no merge commit.
    assert git(a, "rev-list", "--merges", "--count", "HEAD").strip() == "0"


def test_behind_with_overlapping_uncommitted_file_refused(tmp_path):
    _, a, b = world(tmp_path)
    change(b, "docs/features/f/idees.md", "# Idées\nB\n", push=True)
    write(a, "docs/features/f/idees.md", "# Idées\nA, pas commité\n")
    before = head(a)
    res = sync.before_launch(sync.Book(), str(a))
    assert not res["ok"] and res["files"] == ["docs/features/f/idees.md"]
    assert "docs/features/f/idees.md" in res["error"]
    assert head(a) == before
    assert (a / "docs/features/f/idees.md").read_text(encoding="utf-8") == "# Idées\nA, pas commité\n"


def test_behind_with_unrelated_uncommitted_file_pulled(tmp_path):
    _, a, b = world(tmp_path)
    sha = change(b, "x.md", "x\n", push=True)
    write(a, "README.md", "local\n")
    res = sync.before_launch(sync.Book(), str(a))
    assert res["ok"] and head(a) == sha
    assert (a / "README.md").read_text() == "local\n"


def test_diverged_refused(tmp_path):
    _, a, b = world(tmp_path)
    change(b, "x.md", "x\n", push=True)
    mine = change(a, "y.md", "y\n")
    res = sync.before_launch(sync.Book(), str(a))
    assert not res["ok"] and res["reconcile"] and "Réconcilier" in res["error"]
    assert head(a) == mine


def test_offline_launched_with_notice(tmp_path):
    _, a, _ = world(tmp_path)
    offline(a)
    res = sync.before_launch(sync.Book(), str(a))
    assert res["ok"] and "injoignable" in res["notice"]


def test_ahead_pushed_then_launched(tmp_path):
    remote, a, _ = world(tmp_path)
    sha = change(a, "x.md", "x\n")
    res = sync.before_launch(sync.Book(), str(a))
    assert res["ok"] and git(remote, "rev-parse", "master").strip() == sha
    assert res["sync"]["state"] == sync.UP_TO_DATE


# ------------------------------------------------------------ §3 push

def test_rejected_push_shows_new_state(tmp_path):
    _, a, b = world(tmp_path)
    change(a, "y.md", "y\n")
    # A's last fetch saw nothing; B pushes meanwhile.
    assert sync.compute(str(a))["state"] == sync.AHEAD
    change(b, "x.md", "x\n", push=True)
    p = sync.push(str(a))
    assert not p["ok"] and p["rejected"] and "refusé" in p["message"]
    assert sync.compute(str(a))["state"] == sync.DIVERGED


def test_push_sends(tmp_path):
    remote, a, _ = world(tmp_path)
    sha = change(a, "y.md", "y\n")
    assert sync.push(str(a))["ok"]
    assert git(remote, "rev-parse", "master").strip() == sha


def test_credentials_said_never_prompted(tmp_path):
    """A server asking for a login: git, with prompts off, gives up — and
    the message says why, in French."""
    import threading
    from http.server import BaseHTTPRequestHandler, HTTPServer

    class Auth(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="GitHub"')
            self.end_headers()

        def log_message(self, *a):
            pass

    srv = HTTPServer(("127.0.0.1", 0), Auth)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        _, a, _ = world(tmp_path)
        git(a, "remote", "set-url", "origin", f"http://127.0.0.1:{srv.server_port}/app.git")
        # No credential helper of this computer: nothing stored, nothing to ask.
        git(a, "config", "credential.helper", "")
        st = sync.compute(str(a))
        assert st["state"] == sync.OFFLINE and st["credentials"]
        assert st["detail"] == sync.CREDENTIALS_TEXT
        change(a, "y.md", "y\n")
        p = sync.push(str(a))
        assert not p["ok"] and p["credentials"] and "identifiant" in p["message"]
    finally:
        srv.shutdown()


# ------------------------------------------------------------ §4 Réconcilier

def test_reconcile_clean(tmp_path):
    remote, a, b = world(tmp_path)
    theirs = change(b, "x.md", "x\n", push=True)
    change(a, "y.md", "y\n")
    res = sync.reconcile(str(a))
    assert res["ok"] and res["pushed"]
    assert git(a, "merge-base", "--is-ancestor", theirs, "HEAD") == ""
    assert git(remote, "rev-parse", "master").strip() == head(a)
    assert git(a, "rev-list", "--merges", "--count", "HEAD").strip() == "0"
    assert sync.compute(str(a))["state"] == sync.UP_TO_DATE


def test_reconcile_conflict_aborted_clone_unchanged(tmp_path):
    remote, a, b = world(tmp_path)
    change(b, "README.md", "B\n", push=True)
    mine = change(a, "README.md", "A\n")
    status = git(a, "status", "--porcelain")
    res = sync.reconcile(str(a))
    assert not res["ok"] and res["conflicts"] == ["README.md"]
    assert "Claude Code" in res["message"] and "README.md" in res["message"]
    assert head(a) == mine and git(a, "status", "--porcelain") == status
    assert (a / "README.md").read_text() == "A\n"
    assert not os.path.exists(a / ".git" / "rebase-merge") and not os.path.exists(a / ".git" / "rebase-apply")
    assert sync.compute(str(a))["state"] == sync.DIVERGED


def test_reconcile_refused_with_uncommitted_files(tmp_path):
    _, a, b = world(tmp_path)
    change(b, "x.md", "x\n", push=True)
    mine = change(a, "y.md", "y\n")
    write(a, "docs/features/f/idees.md", "# Idées\nréponse\n")
    res = sync.reconcile(str(a))
    assert not res["ok"] and res["files"] == ["docs/features/f/idees.md"]
    assert head(a) == mine


def test_reconcile_refused_when_untracked_file_would_be_overwritten(tmp_path):
    _, a, b = world(tmp_path)
    change(b, "x.md", "x de B\n", push=True)
    change(a, "y.md", "y\n")
    write(a, "x.md", "x d'ici, jamais commité\n")
    res = sync.reconcile(str(a))
    assert not res["ok"] and res["files"] == ["x.md"]
    assert (a / "x.md").read_text(encoding="utf-8") == "x d'ici, jamais commité\n"


def test_reconcile_only_diverged(tmp_path):
    _, a, _ = world(tmp_path)
    res = sync.reconcile(str(a))
    assert not res["ok"] and "rien à réconcilier" in res["message"]


# ------------------------------------------------------------ §5 the answers

ANSWER_STEP = re.compile(r'git add docs/features/<name>/ && git commit -m "([^"]+)"')


def command_steps():
    """Each command of the chain whose pre-invocation step commits the
    feature folder: (name, message, the text that follows the step)."""
    out = []
    folder = os.path.join(CHAIN, ".claude", "commands")
    for name in sorted(os.listdir(folder)):
        text = open(os.path.join(folder, name), encoding="utf-8").read()
        m = ANSWER_STEP.search(text)
        if m:
            out.append((name, m.group(1), text[m.end():m.end() + 1200]))
    return out


def test_every_commit_step_carries_on_when_nothing_is_left():
    """The commands that commit the feature folder before their worktree
    each say that nothing to commit is normal, and carry on — before the
    next step, the worktree."""
    steps = command_steps()
    assert {n for n, _, _ in steps} >= {"1_lexique.md", "2_structure.md", "3_decoupe.md", "3a_genre.md",
                                         "3b_nature.md", "4_grille.md", "6_convertit.md", "7_lots.md",
                                         "8_code.md", "9_controle.md", "batir.md", "conventions.md",
                                         "diagnostique.md", "fusion.md", "fusion_applique.md", "fusion_compare.md"}
    for name, _, after in steps:
        carry = after.find("Nothing to commit is a normal outcome")
        worktree = after.find("git worktree add")
        assert carry != -1 and "carry on" in after[carry:carry + 80], name
        assert worktree == -1 or carry < worktree, name
        before = after[:carry]
        assert "stop" not in before.lower(), (name, before)


def play_commit_step(repo, feature, message):
    """The command's own step, as its file writes it, in a shell — then
    the next step, the worktree from local HEAD."""
    step = f'git add docs/features/{feature}/ && git commit -m "{message}"'
    p = subprocess.run(["bash", "-c", step], cwd=str(repo), capture_output=True, text=True,
                       env=dict(os.environ, GIT_TERMINAL_PROMPT="0"))
    wt = repo / ".claude" / "worktrees" / feature
    w = subprocess.run(["git", "worktree", "add", "-q", str(wt), "HEAD"], cwd=str(repo), capture_output=True,
                       text=True)
    return p, w, wt


@pytest.mark.parametrize("message", sorted({m for _, m, _ in command_steps()}))
def test_answers_sent_then_next_command_finds_nothing_and_goes_on(tmp_path, message):
    remote, a, _ = world(tmp_path)
    write(a, "docs/features/f/questions-lexicographe-01.md", "### Q1\nQuestion: ?\nAnswer: oui\n")
    write(a, "README.md", "outside the feature folder\n")
    assert sync.answers_pending(str(a), "f") == 1
    sha = sync.commit_answers(str(a), "f")
    assert sha and git(a, "log", "-1", "--format=%s").strip() == sync.ANSWERS_MESSAGE
    assert git(a, "show", "--name-only", "--format=", "HEAD").split() == ["docs/features/f/questions-lexicographe-01.md"]
    assert sync.answers_pending(str(a), "f") == 0
    # What lies outside the feature folder stays uncommitted, as the command leaves it.
    assert " M README.md" in git(a, "status", "--porcelain")
    assert sync.push(str(a))["ok"] and git(remote, "rev-parse", "master").strip() == head(a)
    # The next command's own commit step: nothing left — git says so, and the
    # command carries on to its worktree, which holds the answer.
    p, w, wt = play_commit_step(a, "f", message)
    # Git's words for it: « nothing to commit », or — README.md stays
    # modified outside the folder — « no changes added to commit ».
    assert p.returncode == 1 and re.search(r"nothing to commit|no changes added to commit", p.stdout + p.stderr)
    assert w.returncode == 0, w.stderr
    assert (wt / "docs/features/f/questions-lexicographe-01.md").read_text() == "### Q1\nQuestion: ?\nAnswer: oui\n"
    assert git(wt, "rev-parse", "HEAD").strip() == sha_full(a)
    git(a, "worktree", "remove", "--force", str(wt))


def sha_full(repo):
    return head(repo)


def test_commit_answers_nothing(tmp_path):
    _, a, _ = world(tmp_path)
    assert sync.commit_answers(str(a), "f") is None


# ------------------------------------------------------------ §7 a second computer

def test_clone_sets_long_paths(tmp_path):
    remote, _, _ = world(tmp_path)
    dest = tmp_path / "second" / "app"
    dest.parent.mkdir()
    res = sync.clone(str(remote), str(dest))
    assert res["ok"], res
    assert (dest / "README.md").exists()
    assert sync.long_paths(str(dest)) is True
    assert sync.compute(str(dest))["state"] == sync.UP_TO_DATE


def test_long_paths_set_and_read(tmp_path):
    _, a, _ = world(tmp_path)
    git(a, "config", "--local", "--unset-all", "core.longpaths") if sync.long_paths(str(a)) is not None else None
    assert sync.long_paths(str(a)) is None
    sync.set_long_paths(str(a))
    assert sync.long_paths(str(a)) is True


def test_repo_name():
    assert sync.repo_name("https://github.com/vous/mon-app.git") == "mon-app"
    assert sync.repo_name("git@github.com:vous/belivo.git") == "belivo"
    assert sync.repo_name("C:\\gh\\app.git") == "app"
