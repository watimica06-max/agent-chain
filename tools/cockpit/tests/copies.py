"""Scratch repositories built once, copied for every test. A world of git
repositories costs a few dozen git processes; it is built once per test
run in a template folder no test ever sees, then copied into each test's
own temporary folder. Every absolute path of the template inside the
repositories' git files — a remote's address — is rewritten to the
copy's: a test pushes to its own bare repository, never to the template.

Under xdist, a worker builds a template in its own folder, then publishes
it into the run's shared folder in one rename: a template there is whole,
and never written again. Two workers building the same one at once both
build it; the first rename wins, the other copies from it. Every worker
checks at its end that none it used has changed (conftest.py)."""
import hashlib
import os
import pickle
import shutil
from pathlib import Path

ROOT = None          # set by conftest.py: this worker's own folder, where a template is built
SHARED = None        # set by conftest.py: the run's folder, where a built template is published
VALUE = "valeur-du-modele.pickle"
MARK = Path("@modele")
_BUILT = {}


def _forms(path):
    s = os.path.abspath(str(path))
    # How git writes a local path in its config: backslashes doubled. Then as given, then with slashes.
    return [s.replace("\\", "\\\\"), s, s.replace("\\", "/")]


def _moved(value, tpl, dest):
    if isinstance(value, Path):
        try:
            return dest / value.relative_to(tpl)
        except ValueError:
            return value
    if isinstance(value, tuple):
        return tuple(_moved(v, tpl, dest) for v in value)
    if isinstance(value, list):
        return [_moved(v, tpl, dest) for v in value]
    if isinstance(value, dict):
        return {k: _moved(v, tpl, dest) for k, v in value.items()}
    return value


def _git_files(root):
    """Every file of every git folder under `root`, objects aside: a
    working tree's `.git`, a bare repository's own files."""
    for here, dirs, files in os.walk(root):
        if "objects" in dirs and "refs" in dirs and "HEAD" in files:      # a git folder, bare or not
            dirs.remove("objects")
            for d in list(dirs):
                for sub, _, fs in os.walk(os.path.join(here, d)):
                    for f in fs:
                        yield os.path.join(sub, f)
                dirs.remove(d)
            for f in files:
                yield os.path.join(here, f)


def _fingerprint(tpl):
    return {f: (st.st_size, st.st_mtime_ns) for f in _git_files(tpl) for st in [os.stat(f)]}


def changed():
    """The templates whose git files changed since this worker took them
    — a test that wrote into one. conftest.py fails the session on any."""
    return [str(tpl) for tpl, _, _, fp in _BUILT.values() if _fingerprint(tpl) != fp]


def _template(key, build):
    """The template for `key`: published by this worker or another, or
    built here and published. Returns (folder, where it was built, value
    with its paths under MARK)."""
    name = hashlib.sha1(repr(key).encode("utf-8")).hexdigest()[:16]
    shared = Path(SHARED) / name
    if not shared.is_dir():
        built = Path(ROOT) / name
        value = build(built)
        (built / VALUE).write_bytes(pickle.dumps((str(built), _moved(value, built, MARK))))
        try:
            os.rename(built, shared)
        except FileExistsError:          # another worker published it first: the same, theirs
            pass
        except OSError:                  # held for a moment (an antivirus): this worker keeps its own
            shared = built
    origin, value = pickle.loads((shared / VALUE).read_bytes())
    return shared, origin, value


def built_once(key, dest, build):
    """`build(root)` writes its repositories under `root` and returns what
    the caller needs — paths under `root`, alone or in tuples, lists or
    dicts. Built once per run under `key`; each call copies the template
    into `dest` and returns the same value, its paths under `dest`."""
    assert ROOT is not None and SHARED is not None, "copies.ROOT and copies.SHARED are set by conftest.py"
    if key not in _BUILT:
        tpl, origin, value = _template(key, build)
        _BUILT[key] = (tpl, origin, value, _fingerprint(tpl))
    tpl, origin, value, _ = _BUILT[key]
    dest = Path(dest)
    shutil.copytree(tpl, dest, dirs_exist_ok=True, ignore=shutil.ignore_patterns(VALUE))
    old = [f.encode("utf-8") for f in _forms(origin)]
    new = [f.encode("utf-8") for f in _forms(dest)]
    for f in _git_files(dest):
        b = Path(f).read_bytes()
        if any(o in b for o in old):
            for o, n in zip(old, new):
                b = b.replace(o, n)
            os.chmod(f, 0o644)
            Path(f).write_bytes(b)
    return _moved(value, MARK, dest)
