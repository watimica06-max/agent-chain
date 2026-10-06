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
def _no_real_diagnostic(monkeypatch):
    """1.4.5: the cockpit runs the diagnostic on its own when none is stored.
    In a test it is always a fake, all ✓, unless the test passes its own."""
    import diagnostic
    import server
    from test_mode_diagnostic import ALL_GOOD, fake_exec
    monkeypatch.setattr(server, "DIAG_RUNNER", lambda app: diagnostic.run_diagnostic(app, fake_exec(ALL_GOOD)))
