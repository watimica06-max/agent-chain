"""`config.json` — the two folders, the recent pairs, and the last relay
with its `Next:` per working folder, so that reopening shows where things
stood. Local paths: the file is git-ignored."""
import json
import os
import threading
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PATH = os.path.join(HERE, "config.json")
MAX_RECENT = 8


def _key(app: str, work: str) -> str:
    return f"{os.path.normcase(os.path.abspath(app))}|{work}"


class State:
    def __init__(self, path: str = DEFAULT_PATH):
        self.path = path
        self._lock = threading.Lock()
        self.data = {"app_folder": None, "working_folder": None, "recent": [], "relays": {}}
        self.load_error = None
        if os.path.exists(path):
            try:
                with open(path, encoding="utf-8") as f:
                    loaded = json.load(f)
                if isinstance(loaded, dict):
                    self.data.update(loaded)
            except (OSError, ValueError) as e:
                # A broken config is reported, then replaced on next save.
                self.load_error = f"config.json illisible : {e}"

    def _save(self):
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, self.path)

    @property
    def app_folder(self):
        return self.data.get("app_folder")

    @property
    def working_folder(self):
        return self.data.get("working_folder")

    def open_pair(self, app: str, work: str):
        with self._lock:
            self.data["app_folder"] = app
            self.data["working_folder"] = work
            recent = [r for r in self.data.get("recent", [])
                      if not (r.get("app") == app and r.get("work") == work)]
            recent.insert(0, {"app": app, "work": work})
            self.data["recent"] = recent[:MAX_RECENT]
            self._save()

    def forget_pair(self):
        with self._lock:
            self.data["working_folder"] = None
            self._save()

    def set_relay(self, app: str, work: str, command: str, relay: str, nxt: dict,
                  outcome: str = "terminé"):
        with self._lock:
            self.data.setdefault("relays", {})[_key(app, work)] = {
                "command": command,
                "relay": relay,
                "next": nxt,
                "outcome": outcome,
                "at": datetime.now().isoformat(timespec="seconds"),
            }
            self._save()

    def relay(self, app: str, work: str):
        return self.data.get("relays", {}).get(_key(app, work))

    def recent(self):
        return list(self.data.get("recent", []))
