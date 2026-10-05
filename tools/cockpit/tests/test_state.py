import json

from state import State


def test_pairs_relays_and_reopen(tmp_path):
    path = str(tmp_path / "config.json")
    s = State(path)
    assert s.app_folder is None
    s.open_pair("C:/Dev/app", "f")
    s.open_pair("C:/Dev/app", "f/bugfix-02")
    s.open_pair("C:/Dev/app", "f")
    s.set_relay("C:/Dev/app", "f", "/1_lexique f", "...\nNext: done", {"kind": "done"},
                head="abc123", log_path="logs/x.jsonl")
    assert s.is_fresh("C:/Dev/app", "f")                 # just ended: trusted (§2.2)
    s.clear_fresh("C:/Dev/app", "f")
    assert not s.is_fresh("C:/Dev/app", "f")
    again = State(path)
    assert again.app_folder == "C:/Dev/app" and again.working_folder == "f"
    # 1.3: a working folder is a feature; a 1.2 « f/bugfix-02 » reads as « f ».
    assert [r["work"] for r in again.recent()] == ["f"]
    relay = again.relay("C:/Dev/app", "f")
    assert relay["next"] == {"kind": "done"} and relay["head"] == "abc123" and relay["log_path"] == "logs/x.jsonl"
    assert not again.is_fresh("C:/Dev/app", "f")          # a restart is an opening: checked
    again.data["working_folder"] = "f/bugfix-02"
    assert again.working_folder == "f"


def test_broken_config_is_reported_not_fatal(tmp_path):
    path = tmp_path / "config.json"
    path.write_text("{ broken", encoding="utf-8")
    s = State(str(path))
    assert s.load_error and s.app_folder is None
    s.open_pair("a", "b")
    assert json.loads(path.read_text(encoding="utf-8"))["working_folder"] == "b"
