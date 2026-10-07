"""« Déploiement » — TECHNICAL_V1 §23 (1.8). Build the active application and
put it where it runs, without Claude, then watch it run.

- The profile (`deploy_profile.py`) lists the targets; each target's
  adapter (`adapters/`) says where it can go, what it can do there, and how.
- A deploy is a job of the server, in a worker thread, like a run: closing
  the page does not stop it. Per target, its build once, then on each
  destination chosen its deploy, then its launch. Each step ✓ or ✗ with its
  duration; a failure keeps the end of its output; the full output goes to
  `logs/deploy-<time>.log`. One deploy at a time, whatever the application.
- « Journal » follows one destination at a time; the crashes its adapter's
  rules find are listed, and the page told as they come.
"""
import os
import re
import subprocess
import threading
import time
import uuid
from datetime import datetime

import apps as apps_mod
import deploy_profile
from adapters import ADAPTERS
from adapters.base import ActionError, run_shell

BUILD_TIMEOUT = 1800
TODO, GOING, DONE, FAILED, SKIPPED = "à faire", "en cours", "fait", "échec", "sans objet"


class DeployError(Exception):
    """A deploy that cannot start, said in French."""


def app_key(app):
    return os.path.normcase(os.path.abspath(app))


class DeviceStore:
    """The names and addresses the Product Owner gave her devices, in
    config.json, by the device's own key — never in the application."""

    def __init__(self, state):
        self.state = state

    def get(self, key):
        return self.state.deploy_devices().get(key)

    def all(self):
        return self.state.deploy_devices()

    def set(self, key, **fields):
        self.state.set_deploy_device(key, **fields)

    def forget(self, key):
        self.state.forget_deploy_device(key)


class Hub:
    """What an adapter reaches of the server."""

    def __init__(self, devices, on_crash):
        self.devices = devices
        self._on_crash = on_crash

    def crash(self, dest, target, c):
        self._on_crash(dest, target, c)


def head_of(app):
    """The main checkout's commit, and what git sees changed and not
    committed — said before a deploy."""
    def git(*args):
        try:
            p = subprocess.run(["git", "-C", app, "-c", "core.quotepath=off", *args], capture_output=True,
                               timeout=20, stdin=subprocess.DEVNULL)
        except (OSError, subprocess.SubprocessError):
            return None
        return p.stdout.decode("utf-8", "replace").strip() if p.returncode == 0 else None
    files = git("status", "--porcelain")
    lines = [x[3:] for x in (files or "").splitlines() if x.strip()]
    return {"commit": git("rev-parse", "--short", "HEAD"), "subject": git("log", "-1", "--format=%s"),
            "date": git("log", "-1", "--format=%cd", "--date=format:%Y-%m-%d %H:%M"),
            "dirty": apps_mod.uncommitted(app), "dirty_files": lines[:8]}


class Job:
    """One deploy: its steps, run one after the other in a worker thread."""

    def __init__(self, app, app_name, plan, log_dir, head, on_change):
        self.id = uuid.uuid4().hex[:10]
        self.app, self.app_name, self.head = app, app_name, head
        self.on_change = on_change
        self.started_at = datetime.now().isoformat(timespec="seconds")
        self.ended_at = ""
        self.status = GOING
        os.makedirs(log_dir, exist_ok=True)
        stamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        self.log_path = os.path.join(log_dir, f"deploy-{stamp}-{self.id[:4]}.log")
        self.steps = []
        for item in plan:
            t, adapter = item["target"], item["adapter"]
            if t.get("build"):
                self._add(t, None, "build", "Construire", None, t["build"])
            for d in item["dests"]:
                for st in adapter.deploy_steps(t, d, app):
                    self._add(t, d, st.kind, st.label, st.run, None)

    def _add(self, t, d, kind, label, run, command):
        self.steps.append({"n": len(self.steps) + 1, "target": t["name"], "type": t["type"],
                           "dest": d["id"] if d else None, "dest_name": d["name"] if d else "",
                           "kind": kind, "label": label, "command": command, "status": TODO,
                           "started_at": "", "duration_s": None, "detail": "", "tail": [], "_run": run})

    def record(self):
        return {"id": self.id, "app": self.app, "app_name": self.app_name, "head": self.head,
                "started_at": self.started_at, "ended_at": self.ended_at, "status": self.status,
                "log_path": self.log_path, "going": self.status == GOING,
                "steps": [{k: v for k, v in s.items() if k != "_run"} for s in self.steps]}

    def run(self):
        failed_build, failed_dest = set(), set()
        with open(self.log_path, "a", encoding="utf-8") as log:
            def write(line):
                log.write(line + "\n")
                log.flush()
            write(f"# Déploiement de {self.app_name} ({self.app}) — {self.started_at}")
            if self.head:
                write(f"# commit {self.head.get('commit')} « {self.head.get('subject')} »"
                      + (f", {self.head['dirty']} fichier(s) non commité(s)" if self.head.get("dirty") else ""))
            for s in self.steps:
                where = f" sur {s['dest_name']}" if s["dest"] else ""
                if s["target"] in failed_build:
                    s.update(status=SKIPPED, detail="le build a échoué")
                    continue
                if s["kind"] == "launch" and (s["target"], s["dest"]) in failed_dest:
                    s.update(status=SKIPPED, detail="l'installation a échoué")
                    continue
                s.update(status=GOING, started_at=datetime.now().isoformat(timespec="seconds"))
                self.on_change(self)
                write(f"\n=== {s['n']}. {s['target']} — {s['label']}{where} ===")
                t0 = time.monotonic()
                try:
                    if s["kind"] == "build":
                        write(f"$ {s['command']}")
                        r = run_shell(s["command"], self.app, write, timeout=BUILD_TIMEOUT)
                        ok = r.code == 0 and not r.timed_out
                        said = f"délai dépassé ({BUILD_TIMEOUT // 60} min)" if r.timed_out else f"code {r.code}"
                        tail = r.tail
                    else:
                        ok, said, tail = s["_run"](write)
                except ActionError as e:
                    ok, said, tail = False, str(e), []
                except Exception as e:          # said, never raised out of the thread
                    ok, said, tail = False, f"{type(e).__name__} : {e}", []
                s["duration_s"] = round(time.monotonic() - t0, 1)
                s["status"] = DONE if ok else FAILED
                s["detail"] = said
                s["tail"] = [] if ok else tail[-25:]
                write(f"--- {'✓' if ok else '✗'} {said} ({s['duration_s']} s)")
                if not ok:
                    if s["kind"] == "build":
                        failed_build.add(s["target"])
                    else:
                        failed_dest.add((s["target"], s["dest"]))
                self.on_change(self)
            self.status = FAILED if any(s["status"] == FAILED for s in self.steps) else DONE
            self.ended_at = datetime.now().isoformat(timespec="seconds")
            write(f"\n# Fin : {self.status} — {self.ended_at}")

    def summary(self):
        n_fail = sum(1 for s in self.steps if s["status"] == FAILED)
        if not n_fail:
            return f"{len(self.steps)} étape(s), toutes réussies"
        first = next(s for s in self.steps if s["status"] == FAILED)
        return (f"{n_fail} étape(s) en échec — d'abord {first['target']} : {first['label'].lower()}"
                + (f" sur {first['dest_name']}" if first["dest"] else "") + f" ({first['detail']})")


class Deployer:
    def __init__(self, state, log_dir, emit=None):
        self.state = state
        self.log_dir = log_dir
        self.emit = emit or (lambda kind, data: None)
        self.hub = Hub(DeviceStore(state), self._crash)
        self.adapters = {t: cls(self.hub) for t, cls in ADAPTERS.items()}
        self.job = None
        self.last = {}                 # app key -> the last job's record
        self.journals = {}             # key -> handle (stream, stop)
        self._lock = threading.Lock()

    # ---------------------------------------------------------- reading

    def describe(self):
        return {"frame": deploy_profile.frame_fields(), "adapters": [a.describe() for a in self.adapters.values()]}

    def profile(self, app):
        return deploy_profile.load(app)

    def targets(self, app, typ=None):
        p = deploy_profile.load(app)
        ok = [t for i, t in enumerate(p["targets"]) if i not in p["errors"]["targets"] and t.get("type") in self.adapters]
        return [t for t in ok if typ is None or t["type"] == typ]

    def destinations(self, app):
        """Every adapter's destinations, grouped by adapter — each with the
        profile's targets that go there."""
        targets = self.targets(app)
        groups = []
        for typ, a in self.adapters.items():
            mine = [t for t in targets if t["type"] == typ]
            try:
                dests = a.destinations(mine, app)
            except ActionError as e:
                dests = []
                notes = [str(e)]
            else:
                notes = []
            for d in dests:
                d["type"] = typ
                d["targets"] = [t["name"] for t in mine if a.accepts(t, d)]
            try:
                panels = a.panels(mine, app)
            except ActionError as e:
                panels, notes = [], notes + [str(e)]
            groups.append({"type": typ, "label": a.LABEL, "targets": [t["name"] for t in mine],
                           "destinations": dests, "panels": panels, "notes": notes})
        return {"groups": groups, "at": datetime.now().isoformat(timespec="seconds")}

    def find_dest(self, app, typ, dest_id):
        a = self.adapters.get(typ)
        if not a:
            raise ActionError(f"type inconnu : {typ}")
        for d in a.destinations(self.targets(app, typ), app):
            if d["id"] == dest_id:
                d["type"] = typ
                return a, d
        raise ActionError("cette destination n'est plus là")

    # ------------------------------------------------------------ deploy

    def going(self):
        return self.job if self.job and self.job.status == GOING else None

    def going_in(self, app):
        j = self.going()
        return j if j and app_key(j.app) == app_key(app) else None

    def job_for(self, app):
        j = self.job
        if j and app_key(j.app) == app_key(app):
            return j.record()
        return self.last.get(app_key(app))

    def start(self, app, app_name, choice, head=None):
        """Starts a deploy of the targets and destinations chosen ({target
        name: [destination ids]}). Raises DeployError when it cannot."""
        if self.going():
            raise DeployError(f"un déploiement est en cours ({self.job.app_name}) : un seul à la fois")
        prof = deploy_profile.load(app)
        if not prof["exists"]:
            raise DeployError("cette application n'a pas de profil de déploiement : Déploiement → Profil")
        if deploy_profile.has_errors(prof["errors"]):
            raise DeployError("le profil de déploiement a des erreurs : Déploiement → Profil")
        by_name = {t["name"]: t for t in prof["targets"]}
        plan = []
        for name, ids in (choice or {}).items():
            ids = [x for x in (ids or []) if x]
            if not ids:
                continue
            t = by_name.get(name)
            if not t:
                raise DeployError(f"cible inconnue : {name}")
            a = self.adapters[t["type"]]
            offered = {d["id"]: d for d in a.destinations([t], app)}
            dests = []
            for i in ids:
                d = offered.get(i)
                if not d:
                    raise DeployError(f"« {name} » : une destination n'est plus là — rafraîchir")
                if not d["connected"]:
                    raise DeployError(f"« {name} » : « {d['name']} » n'est pas connecté ({d['state']})")
                if not a.accepts(t, d):
                    raise DeployError(f"« {name} » ne va pas sur « {d['name']} »")
                dests.append(d)
            plan.append({"target": t, "adapter": a, "dests": dests})
        # The profile's order, not the click order.
        order = [t["name"] for t in prof["targets"]]
        plan.sort(key=lambda x: order.index(x["target"]["name"]))
        if not plan:
            raise DeployError("aucune cible choisie, ou aucune destination pour elle")
        job = Job(app, app_name, plan, self.log_dir, head, self._changed)
        self.job = job
        threading.Thread(target=self._run, args=(job,), daemon=True).start()
        return job

    def _run(self, job):
        try:
            job.run()
        except Exception as e:          # said, never raised out of the thread
            job.status = FAILED
            job.ended_at = datetime.now().isoformat(timespec="seconds")
            job.error = f"{type(e).__name__} : {e}"
        self.last[app_key(job.app)] = job.record()
        try:
            print(f"Déploiement {job.app_name} : {job.status} — {job.summary()} — {job.log_path}", flush=True)
        except (OSError, ValueError):       # a console that cannot write it: the log has it
            pass
        self.emit("deploy_ended", {"app": job.app, "app_name": job.app_name, "status": job.status,
                                   "summary": job.summary(), "log_path": job.log_path})

    def _changed(self, job):
        self.emit("deploy_step", {"app": job.app, "id": job.id})

    # ----------------------------------------------------------- actions

    def act(self, app, typ, action_id, dest_id, args):
        a = self.adapters.get(typ)
        if not a:
            raise ActionError(f"type inconnu : {typ}")
        return a.act(action_id, dest_id or "", args or {}, app, self.targets(app, typ))

    def image(self, app, typ, action_id, dest_id, args):
        a = self.adapters.get(typ)
        if not a:
            raise ActionError(f"type inconnu : {typ}")
        return a.image(action_id, dest_id, args or {})

    # ----------------------------------------------------------- journal

    def _jkey(self, app, dest_id, target):
        return f"{app_key(app)}|{dest_id}|{target or ''}"

    def _target_for(self, app, typ, dest, name):
        a = self.adapters[typ]
        mine = self.targets(app, typ)
        if name:
            t = next((x for x in mine if x["name"] == name), None)
            if not t:
                raise ActionError(f"cible inconnue : {name}")
            return t
        return next((x for x in mine if a.accepts(x, dest)), None)

    def journal(self, app, typ, dest_id, target=None, after=0, reopen=False):
        """The destination's log since line `after`. Opening one stops the
        log followed before it: one destination at a time."""
        key = self._jkey(app, dest_id, target)
        with self._lock:
            h = self.journals.get(key)
            if h is not None and reopen:
                h.stop()
                self.journals.pop(key, None)
                h = None
        if h is None:
            a, dest = self.find_dest(app, typ, dest_id)
            if not dest.get("connected"):
                raise ActionError(f"« {dest['name']} » n'est pas connecté")
            t = self._target_for(app, typ, dest, target)
            with self._lock:
                for k, other in list(self.journals.items()):
                    other.stop()
                    self.journals.pop(k, None)
            h = a.journal(t, dest, app)
            h.dest_name, h.target = dest["name"], (t or {}).get("name")
            with self._lock:
                self.journals[key] = h
        out = h.stream.since(int(after or 0))
        out.update(key=key, dest_name=getattr(h, "dest_name", ""), target=getattr(h, "target", None))
        return out

    def journal_save(self, app, dest_id, target=None):
        h = self.journals.get(self._jkey(app, dest_id, target))
        if h is None:
            raise ActionError("ce journal n'est pas ouvert")
        os.makedirs(self.log_dir, exist_ok=True)
        name = re.sub(r"[^\w-]+", "_", (h.dest_name or "journal"), flags=re.UNICODE).strip("_") or "journal"
        path = os.path.join(self.log_dir, f"journal-{name}-{datetime.now().strftime('%Y-%m-%d-%H%M%S')}.log")
        with open(path, "w", encoding="utf-8") as f:
            f.write(h.stream.text())
        return path

    def _crash(self, dest, target, c):
        self.emit("deploy_crash", {"dest": dest.get("id"), "dest_name": dest.get("name"),
                                   "target": (target or {}).get("name"), "title": c["title"], "at": c["at"],
                                   "rule": c["rule"]})

    def stop_all(self):
        for h in list(self.journals.values()):
            try:
                h.stop()
            except Exception:
                pass
        self.journals.clear()
        for a in self.adapters.values():
            try:
                a.stop_all()
            except Exception:
                pass
