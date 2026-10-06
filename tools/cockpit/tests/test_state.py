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
    again.data["apps"][0]["last_feature"] = "f/bugfix-02"
    assert again.working_folder == "f"


def test_broken_config_is_reported_not_fatal(tmp_path):
    path = tmp_path / "config.json"
    path.write_text("{ broken", encoding="utf-8")
    s = State(str(path))
    assert s.load_error and s.app_folder is None
    s.open_pair("a", "b")
    # 1.6: the feature is the application's own, in the list.
    saved = json.loads(path.read_text(encoding="utf-8"))
    assert saved["active"] == "a" and saved["apps"][0]["last_feature"] == "b"


def test_ignored_folders_per_application_edited_and_never_recent(tmp_path):
    # 1.6: kept per application; a new one has none.
    path = tmp_path / "config.json"
    path.write_text(json.dumps({"app_folder": "C:/Dev/app", "working_folder": "premiere-app",
                                "recent": [{"app": "C:/Dev/app", "work": "premiere-app"},
                                           {"app": "C:/Dev/app", "work": "premiere-app-3"},
                                           {"app": "C:/Dev/other", "work": "premiere-app"}]}), encoding="utf-8")
    s = State(str(path))
    assert s.ignored == [] and s.ignored_for("C:/Dev/other") == []
    # Edited: one name per folder, never a path; the feature open, once ignored, is closed.
    assert s.set_ignored(["premiere-app", " premiere-app-2/ ", "a/b", "..", "premiere-app"]) == \
        ["premiere-app", "premiere-app-2"]
    assert s.working_folder is None
    assert s.is_ignored("premiere-app/bugfix-06") and not s.is_ignored("premiere-app-3")
    assert not s.is_ignored("premiere-app", "C:/Dev/other")
    assert [(r["app"], r["work"]) for r in s.recent()] == [("C:/Dev/app", "premiere-app-3"),
                                                          ("C:/Dev/other", "premiere-app")]
    again = State(str(path))
    assert again.ignored_for("C:/Dev/app") == ["premiere-app", "premiere-app-2"]
    assert again.ignored_for("C:/Dev/other") == []
    again.set_ignored([], "C:/Dev/app")
    assert State(str(path)).ignored_for("C:/Dev/app") == []


def test_a_one_application_list_belongs_to_the_application_open(tmp_path):
    # 1.5.1 wrote one list, when the cockpit knew one application.
    path = tmp_path / "config.json"
    path.write_text(json.dumps({"app_folder": "C:/Dev/app", "ignored": ["premiere-app", "premiere-app-2"]}),
                    encoding="utf-8")
    s = State(str(path))
    assert s.ignored_for("C:/Dev/app") == ["premiere-app", "premiere-app-2"]
    assert s.ignored_for("C:/Dev/other") == []
