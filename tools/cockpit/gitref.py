"""What git says about the repository, read from its files — never by
running git. The scan may run no command (cockpit 1.3, §1.3)."""
import os


def _git_dir(repo: str) -> str | None:
    """`.git` is a folder in a main checkout, a `gitdir:` file in a worktree."""
    p = os.path.join(repo, ".git")
    if os.path.isdir(p):
        return p
    try:
        with open(p, encoding="utf-8") as f:
            line = f.readline().strip()
    except OSError:
        return None
    if line.startswith("gitdir:"):
        d = line[len("gitdir:"):].strip()
        return d if os.path.isabs(d) else os.path.normpath(os.path.join(repo, d))
    return None


def _common_dir(git_dir: str) -> str:
    try:
        with open(os.path.join(git_dir, "commondir"), encoding="utf-8") as f:
            d = f.readline().strip()
        return d if os.path.isabs(d) else os.path.normpath(os.path.join(git_dir, d))
    except OSError:
        return git_dir


def _ref(common: str, git_dir: str, ref: str) -> str | None:
    for base in (git_dir, common):
        try:
            with open(os.path.join(base, *ref.split("/")), encoding="utf-8") as f:
                sha = f.readline().strip()
            if sha:
                return sha
        except OSError:
            pass
    try:
        with open(os.path.join(common, "packed-refs"), encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(" ", 1)
                if len(parts) == 2 and parts[1] == ref:
                    return parts[0]
    except OSError:
        pass
    return None


def head(repo: str) -> str | None:
    """The commit `HEAD` points at, or None when it cannot be read."""
    gd = _git_dir(repo)
    if not gd:
        return None
    try:
        with open(os.path.join(gd, "HEAD"), encoding="utf-8") as f:
            line = f.readline().strip()
    except OSError:
        return None
    if line.startswith("ref:"):
        return _ref(_common_dir(gd), gd, line[len("ref:"):].strip())
    return line or None
