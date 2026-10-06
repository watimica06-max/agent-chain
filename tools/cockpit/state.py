"""`config.json` — the applications the Product Owner works on, the active
one, the recent pairs, the permission mode and the history of runs. Local
paths: the file is git-ignored.

Since 1.3 the working folder is the feature alone: its `bugfix-NN/` live
under « Correction ». A 1.2 value `feature/bugfix-NN` reads as `feature`.

1.5.1: `ignored`, the folders of `docs/features/` the cockpit never shows —
the earlier chain's, whose files no current command produces. The Product
Owner edits it in Paramètres → Dossiers.

1.6 — several applications (TECHNICAL_V1 §21). `apps` is the list, each
entry with:
- `name`, shown in the page — the folder's name until she renames it;
- `folder`;
- `ignored`, its ignored folders;
- `last_feature`, the feature it opens on;
- `relays`, the last relay of each of its features, with its `Next:` and the
  `HEAD` it left — the latest of them is the application's last relay;
- `diagnostic`, the environment diagnostic of its own stack.
`active` is the folder of the application every screen works on. A config
written before 1.6 is migrated in place at the first load, nothing lost: its
application becomes the first entry, with its relays, its ignored folders
and its diagnostic. `history` stays one list, its keys `folder|feature`,
kept to MAX_HISTORY entries per application."""
import json
import os
import threading
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PATH = os.path.join(HERE, "config.json")
MAX_RECENT = 8
MAX_HISTORY = 30
MODES = ("auto", "manuel")


def app_key(app: str) -> str:
    return os.path.normcase(os.path.abspath(app))


_app_key = app_key


def _key(app: str, work: str) -> str:
    return f"{_app_key(app)}|{work}"


def default_name(folder: str) -> str:
    return os.path.basename(os.path.normpath(folder)) or folder


def _clean_names(names):
    clean = []
    for n in names or []:
        n = (n if isinstance(n, str) else "").strip().strip("/")
        if n and "/" not in n and "\\" not in n and n not in (".", "..") and n not in clean:
            clean.append(n)
    return clean


def migrate(loaded: dict) -> dict:
    """A config written before 1.6 — one `app_folder`, `relays` keyed
    `folder|feature`, `ignored` as a list or keyed by folder, one
    `diagnostic` — as the list of applications. Every application the old
    file names gets its entry; the one open comes first."""
    out = {k: v for k, v in loaded.items()
           if k not in ("app_folder", "working_folder", "relays", "ignored", "diagnostic")}
    apps, by_key = [], {}

    def entry(folder):
        k = _app_key(folder)
        if k not in by_key:
            by_key[k] = {"name": default_name(folder), "folder": folder, "ignored": [],
                         "last_feature": None, "relays": {}, "diagnostic": None}
            apps.append(by_key[k])
        return by_key[k]

    open_app = loaded.get("app_folder")
    if isinstance(open_app, str) and open_app:
        e = entry(open_app)
        w = loaded.get("working_folder")
        e["last_feature"] = w.split("/")[0] if isinstance(w, str) and w else None
    for r in loaded.get("recent") or []:
        if isinstance(r, dict) and isinstance(r.get("app"), str) and r["app"]:
            e = entry(r["app"])
            if e["last_feature"] is None and r.get("work"):
                e["last_feature"] = r["work"].split("/")[0]
    # Relay keys are the folder as normcase wrote it: matched to an entry
    # when one has that key, an entry of their own otherwise.
    for k, relay in (loaded.get("relays") or {}).items():
        folder, _, work = k.partition("|")
        if folder and work:
            entry(folder)["relays"][work.split("/")[0]] = relay
    ig = loaded.get("ignored")
    if isinstance(ig, list) and isinstance(open_app, str) and open_app:
        entry(open_app)["ignored"] = _clean_names(ig)
    elif isinstance(ig, dict):
        for folder, names in ig.items():
            if isinstance(names, list):
                entry(folder)["ignored"] = _clean_names(names)
    diag = loaded.get("diagnostic")
    if isinstance(diag, dict):
        owner = diag.get("app") or open_app
        if isinstance(owner, str) and owner:
            entry(owner)["diagnostic"] = diag
    out["apps"] = apps
    out["active"] = by_key[_app_key(open_app)]["folder"] if isinstance(open_app, str) and open_app else None
    return out


class State:
    def __init__(self, path: str = DEFAULT_PATH):
        self.path = path
        self._lock = threading.Lock()
        self.data = {"apps": [], "active": None, "recent": [], "mode": "auto", "history": []}
        self.load_error = None
        self.migrated = False
        # Relays of a run that has just ended, trusted without a check until
        # the next scan trigger (§2.2). In memory only: a restart is an opening.
        self._fresh = set()
        self._logged = set()
        if os.path.exists(path):
            try:
                with open(path, encoding="utf-8") as f:
                    loaded = json.load(f)
                if isinstance(loaded, dict):
                    if "apps" not in loaded:
                        loaded = migrate(loaded)
                        self.migrated = True
                    self.data.update(loaded)
            except (OSError, ValueError) as e:
                # A broken config is reported, then replaced on next save.
                self.load_error = f"config.json illisible : {e}"
        apps = self.data.get("apps")
        self.data["apps"] = [a for a in apps if isinstance(a, dict) and a.get("folder")] if isinstance(apps, list) else []
        for a in self.data["apps"]:
            a.setdefault("name", default_name(a["folder"]))
            a["ignored"] = _clean_names(a.get("ignored"))
            a.setdefault("last_feature", None)
            if not isinstance(a.get("relays"), dict):
                a["relays"] = {}
            a.setdefault("diagnostic", None)
        if self.data.get("active") and not self._entry(self.data["active"]):
            self.data["active"] = None
        if self.migrated:
            with self._lock:
                self._save()

    def _save(self):
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, self.path)

    # ------------------------------------------------------- applications

    def _entry(self, app, create=False):
        if not app:
            return None
        k = _app_key(app)
        for a in self.data["apps"]:
            if _app_key(a["folder"]) == k:
                return a
        if not create:
            return None
        a = {"name": default_name(app), "folder": app, "ignored": [],
             "last_feature": None, "relays": {}, "diagnostic": None}
        self.data["apps"].append(a)
        return a

    def apps(self):
        """The list, in its order: copies, never the stored entries."""
        return [{"name": a["name"], "folder": a["folder"], "ignored": list(a["ignored"]),
                 "last_feature": a["last_feature"]} for a in self.data["apps"]]

    def app(self, folder):
        a = self._entry(folder)
        return dict(a) if a else None

    def name_of(self, folder):
        a = self._entry(folder)
        return a["name"] if a else (default_name(folder) if folder else "")

    def has_app(self, folder) -> bool:
        return self._entry(folder) is not None

    def add_app(self, folder, name=None):
        """Adds the application to the list — config.json alone, nothing is
        written in the folder. Already there: its entry, unchanged."""
        with self._lock:
            had = self._entry(folder)
            a = self._entry(folder, create=True)
            if not had and name and name.strip():
                a["name"] = name.strip()
            self._save()
            return dict(a), not had

    def rename_app(self, folder, name):
        name = (name or "").strip()
        if not name:
            raise ValueError("un nom vide")
        if len(name) > 60:
            raise ValueError("un nom de 60 caractères au plus")
        with self._lock:
            a = self._entry(folder)
            if not a:
                raise KeyError(folder)
            a["name"] = name
            self._save()
            return dict(a)

    def remove_app(self, folder):
        """Takes the application out of the list — its name, its ignored
        folders, its relays, its diagnostic. The folder is never touched.
        The active one removed, none is active."""
        with self._lock:
            a = self._entry(folder)
            if not a:
                raise KeyError(folder)
            self.data["apps"].remove(a)
            if self.data.get("active") and _app_key(self.data["active"]) == _app_key(folder):
                self.data["active"] = None
            self.data["recent"] = [r for r in self.data.get("recent", [])
                                   if not (r.get("app") and _app_key(r["app"]) == _app_key(folder))]
            self._save()
            return dict(a)

    def activate(self, folder):
        """Makes the application the active one, on its last feature."""
        with self._lock:
            a = self._entry(folder)
            if not a:
                raise KeyError(folder)
            self.data["active"] = a["folder"]
            self._save()
            return dict(a)

    # ------------------------------------------------------ the open pair

    @property
    def app_folder(self):
        a = self._entry(self.data.get("active"))
        return a["folder"] if a else None

    @property
    def app_name(self):
        return self.name_of(self.app_folder) if self.app_folder else None

    @property
    def working_folder(self):
        a = self._entry(self.data.get("active"))
        w = a.get("last_feature") if a else None
        return w.split("/")[0] if w else w

    def open_pair(self, app: str, work: str):
        """Opens `work` of `app`, which joins the list when it is not there."""
        with self._lock:
            a = self._entry(app, create=True)
            a["last_feature"] = work
            self.data["active"] = a["folder"]
            recent = [r for r in self.data.get("recent", [])
                      if not (r.get("app") == app and r.get("work") == work)]
            recent.insert(0, {"app": app, "work": work})
            self.data["recent"] = recent[:MAX_RECENT]
            self._save()

    def forget_pair(self):
        """No application active — each keeps its last feature."""
        with self._lock:
            self.data["active"] = None
            self._save()

    # ------------------------------------------------------------- relays

    def set_relay(self, app: str, work: str, command: str, relay: str, nxt: dict,
                  outcome: str = "terminé", head: str | None = None, log_path: str = "",
                  fresh: bool = True):
        with self._lock:
            self._entry(app, create=True)["relays"][work.split("/")[0]] = {
                "command": command,
                "relay": relay,
                "next": nxt,
                "outcome": outcome,
                "at": datetime.now().isoformat(timespec="seconds"),
                "head": head,
                "log_path": log_path,
            }
            if fresh:
                self._fresh.add(_key(app, work))
            else:
                self._fresh.discard(_key(app, work))
            self._save()

    def is_fresh(self, app: str, work: str) -> bool:
        return _key(app, work) in self._fresh

    def clear_fresh(self, app: str, work: str):
        self._fresh.discard(_key(app, work))

    def first_log(self, token) -> bool:
        """True the first time `token` is seen: a dropped `Next:` is logged
        once, not on every refresh of the page."""
        if token in self._logged:
            return False
        self._logged.add(token)
        return True

    def relay(self, app: str, work: str):
        a = self._entry(app)
        return a["relays"].get(work.split("/")[0]) if a and work else None

    def last_relay(self, app):
        """The application's last relay, whatever its feature: (feature, relay)."""
        a = self._entry(app)
        if not a or not a["relays"]:
            return None, None
        f, r = max(a["relays"].items(), key=lambda kv: (kv[1] or {}).get("at") or "")
        return f, r

    # --------------------------------------------------------------- mode

    @property
    def mode(self):
        """The permission mode of the next run: « auto » unless set otherwise."""
        m = self.data.get("mode")
        return m if m in MODES else "auto"

    def set_mode(self, mode: str):
        if mode not in MODES:
            raise ValueError(f"mode inconnu : {mode}")
        with self._lock:
            self.data["mode"] = mode
            self._save()

    # --------------------------------------------------------- diagnostic

    def diagnostic(self, app=None):
        """The application's own diagnostic — the active one's by default."""
        a = self._entry(app or self.app_folder)
        return a.get("diagnostic") if a else None

    def set_diagnostic(self, result: dict, app=None):
        with self._lock:
            a = self._entry(app or (result or {}).get("app") or self.app_folder, create=True)
            if a is None:
                raise ValueError("un diagnostic appartient à une application")
            a["diagnostic"] = result
            self._save()

    # ------------------------------------------------------------ history

    def add_history(self, app: str, work: str, entry: dict):
        with self._lock:
            hist = self.data.setdefault("history", [])
            hist.insert(0, {"key": _key(app, work), **entry})
            # MAX_HISTORY per application: one busy application never pushes
            # another's out.
            prefix, n, keep = _app_key(app) + "|", 0, []
            for h in hist:
                if (h.get("key") or "").startswith(prefix):
                    n += 1
                    if n > MAX_HISTORY:
                        continue
                keep.append(h)
            self.data["history"] = keep
            self._save()

    def all_history(self):
        return [dict(h) for h in self.data.get("history", [])]

    def history(self, app: str, work: str, n: int = 5):
        k = _key(app, work)
        return [{a: b for a, b in h.items() if a != "key"}
                for h in self.data.get("history", []) if h.get("key") == k][:n]

    def app_history(self, app: str, n: int = 1):
        """The application's last runs, any feature, each with its feature."""
        prefix = _app_key(app) + "|"
        return [{**{a: b for a, b in h.items() if a != "key"}, "feature": h["key"][len(prefix):]}
                for h in self.data.get("history", []) if (h.get("key") or "").startswith(prefix)][:n]

    # ------------------------------------------------------------ ignored

    def ignored_for(self, app):
        """The feature folders of `app` never shown (1.5.1), names under its
        `docs/features/`; none for an application never set (1.6)."""
        a = self._entry(app)
        return list(a["ignored"]) if a else []

    def ignored_by_app(self):
        """{folder key: names} of every application listed."""
        return {_app_key(a["folder"]): list(a["ignored"]) for a in self.data["apps"]}

    @property
    def ignored(self):
        """Those of the application open."""
        return self.ignored_for(self.app_folder)

    def set_ignored(self, names, app=None):
        """Stores the list of `app`, the application open by default,
        cleaned: one name per folder, never a path. The feature open, once
        ignored, is closed."""
        app = app or self.app_folder
        if not app:
            raise ValueError("aucune application")
        clean = _clean_names(names)
        with self._lock:
            a = self._entry(app, create=True)
            a["ignored"] = clean
            if (a.get("last_feature") or "").split("/")[0] in clean:
                a["last_feature"] = None
            self._save()
        return clean

    def is_ignored(self, work, app=None):
        return bool(work) and work.split("/")[0] in self.ignored_for(app or self.app_folder)

    def recent(self):
        out, seen = [], set()
        for r in self.data.get("recent", []):
            pair = (r.get("app"), (r.get("work") or "").split("/")[0])
            if pair[1] and pair not in seen and pair[1] not in self.ignored_for(pair[0]):
                seen.add(pair)
                out.append({"app": pair[0], "work": pair[1]})
        return out
