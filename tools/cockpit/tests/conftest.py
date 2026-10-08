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


@pytest.fixture(autouse=True)
def _no_java_home(monkeypatch):
    """1.5: the diagnostic checks the Java of JAVA_HOME when it is set. A
    test sets it itself, never this machine's."""
    monkeypatch.delenv("JAVA_HOME", raising=False)


def pytest_configure(config):
    config.addinivalue_line("markers", "real_chain: the chain's state is computed, not stubbed « à jour »")


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
def _no_real_diagnostic(monkeypatch):
    """1.4.5: the cockpit runs the diagnostic on its own when none is stored.
    In a test it is always a fake, all ✓, unless the test passes its own."""
    import diagnostic
    import server
    from test_mode_diagnostic import ALL_GOOD, fake_exec
    monkeypatch.setattr(server, "DIAG_RUNNER", lambda app: diagnostic.run_diagnostic(app, fake_exec(ALL_GOOD)))
    # 1.8: scrcpy and the emulator, never this machine's.
    monkeypatch.setattr(diagnostic, "FIND", lambda tool: None)
