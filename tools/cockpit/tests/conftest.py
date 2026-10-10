import os
import shutil
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

FIX = os.path.join(HERE, "fixtures")


def fixture_path(*parts):
    return os.path.join(FIX, *parts)


@pytest.fixture
def place(tmp_path):
    """Copy a fixture to `tmp_path/<dest>` and return the new path."""
    def _place(src, dest):
        target = tmp_path / dest
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(fixture_path(*src.split("/")), target)
        return str(target)
    return _place


@pytest.fixture(scope="session", autouse=True)
def _templates(tmp_path_factory):
    """The scratch repositories built once per run (copies.py): built in
    this worker's temporary folder, published in the run's. None may
    change: each test starts from a clean copy."""
    import copies
    copies.ROOT = str(tmp_path_factory.mktemp("modeles"))
    # Under xdist each worker's basetemp is <the run's basetemp>/popen-gwN: the run's own folder is shared.
    base = tmp_path_factory.getbasetemp()
    shared = (base.parent if os.environ.get("PYTEST_XDIST_WORKER") else base) / "modeles-partages"
    shared.mkdir(exist_ok=True)
    copies.SHARED = str(shared)
    yield
    changed = copies.changed()
    assert not changed, f"un modèle a été modifié par un test — il ne se copie plus propre : {changed}"


@pytest.fixture(scope="module")
def browser():
    """Microsoft Edge, headless, through Playwright: one per test file.
    Each test opens its own context — no cookie, storage or service worker
    carried from one test to the next. Skipped when Playwright or Edge is
    missing. Not one per session: while it is open, Playwright's sync API
    holds an event loop on this thread, and the next file's
    `asyncio.run()` would refuse to start."""
    pytest.importorskip("playwright")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        try:
            b = p.chromium.launch(channel="msedge")
        except Exception as e:                      # no Edge on this machine
            pytest.skip(f"Edge indisponible : {e}")
        yield b
        b.close()


BROWSER_FIXTURES = {"browser", "edge"}


def pytest_collection_modifyitems(config, items):
    """A test that drives the headless browser is marked `navigateur`: the
    quick suite leaves it out (`-m "not navigateur"`)."""
    for item in items:
        if BROWSER_FIXTURES & set(getattr(item, "fixturenames", ())):
            item.add_marker(pytest.mark.navigateur)


@pytest.fixture(autouse=True)
def _logs_in_tmp(tmp_path_factory, monkeypatch):
    """The raw run logs of a test never land in tools/cockpit/logs/."""
    import runner
    monkeypatch.setattr(runner, "LOG_DIR", str(tmp_path_factory.mktemp("logs")))


@pytest.fixture(autouse=True)
def _no_sync_at_start(monkeypatch):
    """1.12: the cockpit fetches agent-chain's own clone, and pulls it, when
    it starts — never in a test, which would touch this repository. A test
    turns it on with a scratch CHAIN_ROOT of its own."""
    import server
    monkeypatch.setattr(server, "SYNC_CHAIN_AT_START", False)
    monkeypatch.setattr(server, "SYNC_APPS_AT_START", False)
    # 1.14: nor when the home screen opens.
    monkeypatch.setattr(server, "SYNC_CHAIN_ON_HOME", False)


@pytest.fixture(autouse=True)
def _no_java_home(monkeypatch):
    """1.5: the diagnostic checks the Java of JAVA_HOME when it is set. A
    test sets it itself, never this machine's."""
    monkeypatch.delenv("JAVA_HOME", raising=False)


def pytest_configure(config):
    config.addinivalue_line("markers", "real_chain: the chain's state is computed, not stubbed « à jour »")
    config.addinivalue_line("markers", "navigateur: drives the headless browser — left out of the quick suite")


@pytest.fixture(autouse=True)
def _chain_up_to_date(request, monkeypatch):
    """§20: a launch asks first when the application's chain is not « à
    jour ». A test's application is a folder with no chain installed: its
    state is « à jour » unless the test is marked `real_chain`."""
    if request.node.get_closest_marker("real_chain"):
        return
    import server
    monkeypatch.setattr(server, "chain_state", lambda app: {
        "state": "à jour", "summary": "Chaîne à jour — test", "commit": "0000000", "date": "2026-10-06",
        "chain_commit": "0000000", "chain_date": "2026-10-06", "behind": None, "subjects": [], "modified": []})


@pytest.fixture(autouse=True)
def revealed(monkeypatch):
    """1.9.1: a log link opens its folder on this computer. In a test it
    is recorded here, never opened: [(path, select)]."""
    import server
    calls = []
    monkeypatch.setattr(server, "REVEAL", lambda path, select=False: calls.append((path, select)))
    return calls


@pytest.fixture(autouse=True)
def _creations_in_tmp(tmp_path_factory, monkeypatch):
    """1.9.1: a test never creates an application outside its temporary
    folder, whatever the timing. The default parent of « Nouvelle
    application » is a temporary folder; a creation aimed anywhere else is
    refused before its first step, and fails the test."""
    import create
    base = os.path.normcase(os.path.abspath(str(tmp_path_factory.getbasetemp())))
    parent = tmp_path_factory.mktemp("parent-par-defaut")
    monkeypatch.setattr(create, "default_parent", lambda: str(parent))
    outside = []
    real = create.Creation.run

    def run(self):
        p = os.path.normcase(os.path.abspath(self.path))
        try:
            inside = os.path.commonpath([p, base]) == base
        except ValueError:                          # another drive
            inside = False
        if not inside:
            outside.append(self.path)
            raise AssertionError(f"création hors du dossier temporaire du test : {self.path}")
        return real(self)
    monkeypatch.setattr(create.Creation, "run", run)
    yield
    assert not outside, f"une création visait un dossier hors du dossier temporaire : {outside}"


@pytest.fixture(autouse=True)
def fake_machine(monkeypatch):
    """1.16: « État de l'ordinateur » never probes this computer in a test —
    every probe sees the all-good fake computer (machinefakes.py), which a
    test changes for its case. No check at start, no restart of its own, no
    registry read."""
    import installs
    import machinefakes
    import server
    monkeypatch.setattr(server, "MACHINE_AT_START", False)
    monkeypatch.setattr(server, "AUTO_RESTART", False)
    monkeypatch.setattr(installs, "REGISTRY", lambda: {})
    return machinefakes.install(monkeypatch)


@pytest.fixture(autouse=True)
def _no_real_diagnostic(monkeypatch):
    """1.4.5: the cockpit runs the diagnostic on its own when none is stored.
    In a test it is always a fake, all ✓, unless the test passes its own."""
    import diagnostic
    import server
    from test_mode_diagnostic import ALL_GOOD, fake_exec
    monkeypatch.setattr(server, "DIAG_RUNNER", lambda app: diagnostic.run_diagnostic(app, fake_exec(ALL_GOOD)))
    # 1.8: scrcpy and the emulator, never this machine's.
    monkeypatch.setattr(diagnostic, "FIND", lambda tool: None)
