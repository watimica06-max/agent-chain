"""1.12 — two computers and GitHub, in a temporary folder: a bare
repository plays GitHub, two clones play the two computers. Nothing
reaches the real GitHub."""
import os
import subprocess

from test_chain import commit, git, init, write


def bare(path):
    path.mkdir(parents=True, exist_ok=True)
    git(path, "init", "-q", "--bare", "-b", "master")
    return path


def clone_of(remote, dest):
    p = subprocess.run(["git", "clone", "-q", "-c", "core.autocrlf=false", str(remote), str(dest)], capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    git(dest, "config", "user.email", "t@example.com")
    git(dest, "config", "user.name", "T")
    git(dest, "config", "core.autocrlf", "false")
    return dest


def world(tmp_path, files=None):
    """GitHub (`remote`), and computers A and B, both « à jour » on one
    first commit."""
    remote = bare(tmp_path / "github" / "app.git")
    seed = tmp_path / "seed"
    init(seed)
    for rel, text in (files or {"README.md": "app\n", "docs/features/f/idees.md": "# Idées\n"}).items():
        write(seed, rel, text)
    commit(seed, "first")
    git(seed, "remote", "add", "origin", str(remote))
    git(seed, "push", "-q", "-u", "origin", "master")
    a = clone_of(remote, tmp_path / "A")
    b = clone_of(remote, tmp_path / "B")
    return remote, a, b


def change(repo, rel, text, msg=None, push=False):
    write(repo, rel, text)
    sha = commit(repo, msg or f"edit {rel}")
    if push:
        git(repo, "push", "-q")
    return sha


def head(repo):
    return git(repo, "rev-parse", "HEAD").strip()


def offline(repo):
    """GitHub out of reach: nothing answers at the remote's address."""
    git(repo, "remote", "set-url", "origin", "http://127.0.0.1:9/app.git")


def online(repo, remote):
    git(repo, "remote", "set-url", "origin", str(remote))


def app_world(tmp_path, name, commands=("1_lexique", "2_structure", "3_decoupe")):
    """An application on GitHub and on two computers: its commands, a
    feature « f » with an idea file and an open question."""
    files = {f".claude/commands/{c}.md": f'---\ndescription: run {c}\nargument-hint: "<f>"\n---\nbody\n'
             for c in commands}
    files.update({
        "docs/features/f/idees.md": "# Idées\n\nUne application.\n",
        "docs/features/f/questions-lexicographe-01.md":
            "### Q1\nTerms: séance, entraînement\nQuestion: Une séance et un entraînement sont-ils la même chose ?\n"
            "Options:\n- Oui, la même chose.\n- Non, deux choses.\nAnswer:\n\n"
            "### Q2\nTerms: parcours\nQuestion: Un parcours est-il l'itinéraire prévu, ou ce qui a été roulé ?\n"
            "Options:\n- L'itinéraire prévu.\n- Ce qui a été roulé.\nAnswer:\n",
        "README.md": f"{name}\n",
    })
    return world(tmp_path / name, files)
