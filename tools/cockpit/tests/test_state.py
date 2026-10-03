import json

from state import State


def test_pairs_relays_and_reopen(tmp_path):
    path = str(tmp_path / "config.json")
    s = State(path)
    assert s.app_folder is None
    s.open_pair("C:/Dev/app", "f")
    s.open_pair("C:/Dev/app", "f/bugfix-02")
    s.open_pair("C:/Dev/app", "f")
    s.set_relay("C:/Dev/app", "f", "/1_lexique f", "…\nNext: done", {"kind": "done"})
    again = State(path)
    assert again.app_folder == "C:/Dev/app" and again.working_folder == "f"
    assert [r["work"] for r in again.recent()] == ["f", "f/bugfix-02"]
    assert again.relay("C:/Dev/app", "f")["next"] == {"kind": "done"}
    assert again.relay("C:/Dev/app", "f/bugfix-02") is None


def test_broken_config_is_reported_not_fatal(tmp_path):
    path = tmp_path / "config.json"
    path.write_text("{ broken", encoding="utf-8")
    s = State(str(path))
    assert s.load_error and s.app_folder is None
    s.open_pair("a", "b")
    assert json.loads(path.read_text(encoding="utf-8"))["working_folder"] == "b"
