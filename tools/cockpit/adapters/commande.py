"""The `commande` adapter (1.8): any target whose deploy is a command run on
this computer — a web server, a desktop program, a script.

- One destination: « cet ordinateur ».
- Deploy: the run command, from the application's root. A command that keeps
  running (a server) is the target's process: « Arrêter » stops it, with
  everything it started; deployed again, it is stopped and started anew. One
  that ends (a script) is waited for, and its exit code is its result.
- Its log is the command's output, kept across its restarts. A URL, when the
  target gives one, gets « Ouvrir » while the command runs.
- No screenshot, no mirror: not declared.
"""
import collections
import os
import threading
import time
from datetime import datetime

from .base import (ActionError, Adapter, CrashRule, LogStream, Step, action, field_spec, kill_tree,
                   shell_popen)

# A command that keeps running and ends within this many seconds has failed.
STARTUP_GRACE = 3.0
SCRIPT_TIMEOUT = 3600
DEST_ID = "commande:local"


def _key(app, name):
    return (os.path.normcase(os.path.abspath(app)), name)


class Process:
    """A target's command started on this computer, and its output."""

    def __init__(self, stream):
        self.stream = stream
        self.popen = None
        self.started_at = ""
        self.ended_code = None
        self.reader = None
        self.step_out = None          # the deploy step reading it, while it does
        self.stopping = False         # stopped from the cockpit: its end is said by the stop
        self.tail = collections.deque(maxlen=40)

    @property
    def running(self):
        return self.popen is not None and self.popen.poll() is None

    def _read(self, popen):
        for line in popen.stdout:
            line = line.rstrip("\r\n")
            self.tail.append(line)
            self.stream.add(line)
            out = self.step_out
            if out:
                out(line)
        code = popen.wait()
        if popen is self.popen:
            self.ended_code = code
            if self.stopping:
                return
            self.stream.live = False
            self.stream.add(f"— la commande s'est terminée : code {code} —", marker=True)


class CommandeAdapter(Adapter):
    TYPE = "commande"
    LABEL = "Commande sur cet ordinateur"
    DEPLOY_LABEL = "Lancer"
    FIELDS = [
        field_spec("run", "Commande de lancement", required=True, placeholder="python -m http.server 8000",
                   help="Lancée depuis la racine de l'application. Sa sortie est le journal de la cible."),
        field_spec("keeps_running", "Elle continue de tourner", "bool", default=False,
                   help="Coché : un serveur, un programme — « Arrêter » l'arrête, et un nouveau déploiement le relance. "
                        "Décoché : un script, attendu jusqu'à sa fin ; son code de sortie dit s'il a réussi."),
        field_spec("url", "Adresse à ouvrir", placeholder="http://127.0.0.1:8000/",
                   help="Facultative : « Ouvrir » l'ouvre dans le navigateur une fois la commande lancée."),
    ]
    CRASHES = [
        CrashRule("Traceback Python", r"^Traceback \(most recent call last\):",
                  r"^(\s|[A-Za-z_][\w.]*(Error|Exception|Exit|Interrupt|Warning)\b)",
                  r"^[A-Za-z_][\w.]*(Error|Exception|Exit|Interrupt)\b"),
        # A line opening on an error, and what follows it — a stack (indented),
        # a Python traceback, « Caused by » — up to the exception's own line:
        # socketserver's « Exception occurred … » and its traceback are one crash.
        CrashRule("Error / Exception", r"^[\w.$]*(Error|Exception)\b",
                  r"^(\s+\S|Traceback \(most recent call last\):|Caused by|[A-Za-z_][\w.]*(Error|Exception):)",
                  r"^[A-Za-z_][\w.]*(Error|Exception)(: |$)"),
    ]

    def __init__(self, hub):
        super().__init__(hub)
        self.procs = {}
        self._lock = threading.Lock()

    def check(self, target):
        errors = super().check(target)
        url = (target.get("url") or "").strip()
        if url and "url" not in errors and not url.lower().startswith(("http://", "https://")):
            errors["url"] = "une adresse en http:// ou https://"
        return errors

    def proc(self, app, target):
        """The target's process record, its log kept across restarts."""
        k = _key(app, target["name"])
        with self._lock:
            p = self.procs.get(k)
            if p is None:
                dest = self.dest_of()
                p = self.procs[k] = Process(LogStream(self.CRASHES, lambda c: self.hub.crash(dest, target, c)))
            return p

    @staticmethod
    def dest_of():
        return {"id": DEST_ID, "name": "cet ordinateur", "kind": "ordinateur"}

    # ------------------------------------------------------- destinations

    def destinations(self, targets, app):
        facts, acts = [], [action("journal", "Journal", "journal")]
        for t in targets:
            p = self.procs.get(_key(app, t["name"]))
            if p and p.running:
                state = f"en marche depuis {p.started_at[11:16]} (pid {p.popen.pid})"
                acts.append(action("stop", f"Arrêter « {t['name']} »", args={"target": t["name"]}, primary=True))
                if (t.get("url") or "").strip():
                    acts.append(action("open", f"Ouvrir « {t['name']} »", "link", url=t["url"].strip(),
                                       title=t["url"].strip()))
            elif p and p.popen is not None:
                state = "arrêtée" if p.stopping or p.ended_code is None else f"terminée (code {p.ended_code})"
            else:
                state = "pas lancée depuis l'ouverture du cockpit"
            facts.append([t["name"], state])
        if not targets:
            facts.append(["Cibles", "aucune cible de ce type dans le profil"])
        return [{**self.dest_of(), "form": "computer", "state": "device", "connected": True, "named": True,
                 "facts": facts, "note": "", "actions": acts}]

    # -------------------------------------------------------------- deploy

    def deploy_steps(self, target, dest, app):
        label = "Lancer" if target.get("keeps_running") else "Exécuter"
        return [Step("deploy", label, lambda out: self._run(target, app, out))]

    def _run(self, target, app, out):
        p = self.proc(app, target)
        if p.running:
            out(f"— déjà en marche (pid {p.popen.pid}) : arrêtée pour être relancée —")
            self._stop(p, "relancée")
        cmd = target["run"]
        out(f"$ {cmd}")
        p.stream.add(f"— {datetime.now().strftime('%H:%M:%S')} · $ {cmd} —", marker=True)
        p.step_out, p.ended_code, p.stopping = out, None, False
        p.tail.clear()
        try:
            popen = shell_popen(cmd, app)
        except OSError as e:
            p.step_out = None
            return False, f"ne démarre pas : {e}", []
        p.popen, p.started_at = popen, datetime.now().isoformat(timespec="seconds")
        p.stream.live, p.stream.ended = True, ""
        p.reader = threading.Thread(target=p._read, args=(popen,), daemon=True)
        p.reader.start()
        try:
            if target.get("keeps_running"):
                deadline = time.monotonic() + STARTUP_GRACE
                while time.monotonic() < deadline and popen.poll() is None:
                    time.sleep(0.1)
                if popen.poll() is not None:
                    p.reader.join(5)
                    return False, f"elle s'est arrêtée aussitôt : code {popen.returncode}", list(p.tail)
                url = (target.get("url") or "").strip()
                return True, f"en marche (pid {popen.pid})" + (f" — {url}" if url else ""), []
            try:
                code = popen.wait(SCRIPT_TIMEOUT)
            except Exception:
                kill_tree(popen)
                return False, f"délai dépassé ({SCRIPT_TIMEOUT // 60} min)", list(p.tail)
            p.reader.join(10)
            return code == 0, f"code {code}", list(p.tail)
        finally:
            p.step_out = None

    def _stop(self, p, why="arrêtée"):
        popen = p.popen
        if popen is None or popen.poll() is not None:
            return False
        p.stopping = True
        kill_tree(popen)
        if p.reader:
            p.reader.join(5)
        p.stream.live, p.stream.ended = False, why
        p.stream.add(f"— {why} depuis le cockpit —", marker=True)
        return True

    # ------------------------------------------------------------- journal

    def journal(self, target, dest, app):
        if not target:
            raise ActionError("aucune cible « commande » dans le profil")
        p = self.proc(app, target)
        if p.popen is None and not p.stream.n:
            p.stream.add(f"— « {target['name']} » n'a pas été lancée depuis l'ouverture du cockpit : "
                         "« Déployer » la lance, et sa sortie s'écrit ici —", marker=True)
        return Followed(p.stream)

    # ------------------------------------------------------------- actions

    def act(self, action_id, dest_id, args, app, targets):
        t = next((x for x in targets if x["name"] == args.get("target")), None)
        if action_id == "stop":
            if not t:
                raise ActionError("cible inconnue")
            p = self.procs.get(_key(app, t["name"]))
            if not p or not self._stop(p):
                raise ActionError(f"« {t['name']} » ne tourne pas")
            return {"message": f"« {t['name']} » arrêtée."}
        raise ActionError(f"action inconnue : {action_id}")

    def running(self, app):
        return [name for (a, name), p in self.procs.items() if a == _key(app, "")[0] and p.running]

    def stop_all(self):
        for p in list(self.procs.values()):
            self._stop(p, "arrêtée avec le cockpit")


class Followed:
    """The handle of a process's log: the process goes on when the page
    follows another destination."""

    def __init__(self, stream):
        self.stream = stream

    def stop(self):
        pass
