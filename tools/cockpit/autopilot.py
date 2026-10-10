"""Le pilote automatique — cockpit 1.18.

A « programme » runs the step the cockpit proposes (decide.py), command
after command, until something needs the Product Owner or a bound is
reached. One at a time, in one application, on this computer.

Decided by the Product Owner (10 October): every setting adjustable; every
command chains, upstream to code, while no person is needed; the permission
mode stays « auto »; bounds combine freely and **the first reached stops the
programme**; a start now, at a time, or within a slot; a spacing between
commands; /9_controle and /diagnostique stop to ask unless a setting lets
them run; no stop for an intermediate test — the programme stops at the
final test step.

The programme is pure logic over a `host` — the server, or a fake in the
tests — and a `clock`, real or fake:

- host.decide(app, feature) → (scan, decision), decide.py's;
- host.busy() → the prompt of a run going that is not the programme's, or None;
- await host.wait_idle(); await host.refresh_usage(force);
- host.levels() → usage.levels; host.thresholds(); host.estimate(command);
- await host.launch(app, feature, command, args, programme_id) →
  (run, None) or (None, (kind, text));
- await host.wait_run(run) → the run's snapshot once it ended;
- await host.stop_run_now(app); host.write_stop(app) — stop.md, /8_code's;
- host.changed(public); host.push(event, title, body);
- host.record(summary); host.spent(programme_id) → usage spent per window;
- host.save(record) — the active programme, kept in config.json.
"""
import asyncio
import json
import uuid
from datetime import datetime, timedelta

import decide as decide_mod
import scan as scan_mod
import usage as usage_mod

# Statuses of a programme.
PROGRAMME, LANCE, PAUSE, ATTEND, FINI = "programmé", "en cours", "pause", "attend", "arrêté"
# /9_controle and /diagnostique: confirmed by hand today — a programme stops
# to ask before them, unless `run_confirmed`.
CONFIRMED = {"9_controle": "/9_controle", "diagnostique": "/diagnostique"}
# The final test step, and what comes after it: never a programme's.
TEST_COMMANDS = {"deploie"}
FUSION_COMMANDS = {"fusion", "fusion_compare", "fusion_applique"}
# After a reset, how long before measuring again: the window has turned.
RESET_MARGIN_S = 90
WINDOWS = usage_mod.WINDOWS
LATER = "L'ordinateur doit rester allumé et réveillé jusque-là."

# Why a programme stopped, by kind.
NEED, BOUND, USAGE, ERROR, MACHINE, GITHUB, CHAIN, CONFIRM, DONE, ASKED, BUSY = (
    "besoin", "borne", "consommation", "erreur", "ordinateur", "github", "chaîne", "confirmation", "fini",
    "demandé", "occupé")

PRESETS = [
    {"id": "besoin", "name": "Maintenant, jusqu'à ce qu'on ait besoin de moi",
     "spec": {"start": {"mode": "now"}, "bounds": {}}},
    {"id": "nuit", "name": "Cette nuit, 1 h – 7 h",
     "spec": {"start": {"mode": "slot", "from": "01:00", "to": "07:00"}, "bounds": {}}},
    {"id": "deux-heures", "name": "Pendant 2 heures",
     "spec": {"start": {"mode": "now"}, "bounds": {"minutes": 120}}},
]


class Refused(Exception):
    pass


# ------------------------------------------------------------------ the spec

def parse_hm(text):
    """« 7:00 », « 07:30 », « 7 h », « 7h30 » → (hour, minute)."""
    t = str(text or "").strip().lower().replace("h", ":").replace(" ", "")
    if t.endswith(":"):
        t += "00"
    try:
        h, m = (t.split(":") + ["0"])[:2]
        h, m = int(h), int(m or 0)
    except ValueError:
        raise ValueError(f"heure illisible : « {text} »")
    if not (0 <= h <= 23 and 0 <= m <= 59):
        raise ValueError(f"heure illisible : « {text} »")
    return h, m


def next_at(after, hm, inclusive=True):
    """The first moment at `hm` from `after` on — today or tomorrow."""
    h, m = hm
    t = after.replace(hour=h, minute=m, second=0, microsecond=0)
    if t < after or (not inclusive and t == after):
        t += timedelta(days=1)
    return t


def _int(v, what, lo, hi):
    if v is None or v is False or (isinstance(v, str) and not v.strip()):
        return None
    try:
        n = int(round(float(v)))
    except (TypeError, ValueError):
        raise ValueError(f"{what} : nombre illisible « {v} »")
    if not lo <= n <= hi:
        raise ValueError(f"{what} : de {lo} à {hi}")
    return n


def clean_spec(raw):
    """The programme as the form sends it, checked: what is missing takes
    its default, what is wrong is refused in French (ValueError)."""
    raw = raw if isinstance(raw, dict) else {}
    st = raw.get("start") if isinstance(raw.get("start"), dict) else {}
    mode = st.get("mode") or "now"
    start = {"mode": mode}
    if mode == "at":
        start["at"] = "%02d:%02d" % parse_hm(st.get("at"))
    elif mode == "slot":
        a, b = parse_hm(st.get("from")), parse_hm(st.get("to"))
        if a == b:
            raise ValueError("le créneau commence et finit à la même heure")
        start.update({"from": "%02d:%02d" % a, "to": "%02d:%02d" % b})
    elif mode != "now":
        raise ValueError(f"démarrage inconnu : {mode}")
    b = raw.get("bounds") if isinstance(raw.get("bounds"), dict) else {}
    bounds = {}
    if b.get("until"):
        bounds["until"] = "%02d:%02d" % parse_hm(b["until"])
    for k, what, lo, hi in (("minutes", "durée (minutes)", 1, 7 * 24 * 60), ("lots", "nombre de lots", 1, 999),
                            ("commands", "nombre de commandes", 1, 999),
                            ("five_hour", "fenêtre de 5 heures (%)", 1, 100), ("seven_day", "semaine (%)", 1, 100)):
        n = _int(b.get(k), what, lo, hi)
        if n is not None:
            bounds[k] = n
    step = b.get("step")
    if isinstance(step, dict) and step.get("id"):
        when = step.get("when") or "before"
        if when not in ("before", "after"):
            raise ValueError("étape à atteindre : « avant » ou « après »")
        chain = step.get("chain") or "main"
        if chain not in ("main", "correction"):
            raise ValueError("étape à atteindre : la chaîne principale ou la correction")
        ids = [s.id for s in (scan_mod.MAIN if chain == "main" else scan_mod.CORRECTION)]
        if step["id"] not in ids:
            raise ValueError(f"étape inconnue : {step['id']}")
        bounds["step"] = {"chain": chain, "id": step["id"], "when": when}
    spacing = _int(raw.get("spacing_min"), "espacement (minutes)", 0, 24 * 60) or 0
    name = str(raw.get("name") or "").strip()[:80]
    return {"name": name, "start": start, "bounds": bounds, "spacing_min": spacing,
            "run_confirmed": bool(raw.get("run_confirmed"))}


def resolve(spec, now):
    """The spec's times, as moments: when it starts, and the end time its
    `until` and its slot give — the earlier of the two. `later`: it starts
    after now."""
    st = spec["start"]
    end = None
    if st["mode"] == "now":
        start = now
    elif st["mode"] == "at":
        start = next_at(now, parse_hm(st["at"]))
    else:
        a, b = parse_hm(st["from"]), parse_hm(st["to"])
        # Inside the slot now: it starts at once, and ends at the slot's end.
        begun = next_at(now, a) - timedelta(days=1)
        begun_end = next_at(begun, b, inclusive=False)
        if begun <= now < begun_end:
            start, end = now, begun_end
        else:
            start = next_at(now, a)
            end = next_at(start, b, inclusive=False)
    if spec["bounds"].get("until"):
        u = next_at(start, parse_hm(spec["bounds"]["until"]), inclusive=False)
        end = min(end, u) if end else u
    return {"start_at": start, "end_at": end, "later": start > now + timedelta(seconds=30)}


# ------------------------------------------------------------------- words

def hm(t):
    """« 7 h », « 7 h 30 »."""
    return f"{t.hour} h" + (f" {t.minute:02d}" if t.minute else "")


def hm_text(t, now=None):
    """« à 7 h », « demain à 7 h », « le 12/10 à 7 h »."""
    if now is not None and t.date() != now.date():
        day = "demain" if t.date() == (now + timedelta(days=1)).date() else t.strftime("le %d/%m")
        return f"{day} à {hm(t)}"
    return f"à {hm(t)}"


def plural(n, one, many):
    return f"{n} {one if n == 1 else many}"


def step_name(chain, sid):
    for d in (scan_mod.MAIN if chain == "main" else scan_mod.CORRECTION):
        if d.id == sid:
            return d.name
    return sid


def bounds_text(p, now):
    """The bounds still ahead, in words: « s'arrête à 7 h ou après 4 lots
    encore ». Its stops for her are always there: said when nothing else is."""
    b = p["spec"]["bounds"]
    parts = []
    dl = deadline(p)
    if dl:
        parts.append(hm_text(dl, now))
    if b.get("lots"):
        left = max(0, b["lots"] - p["lots"])
        parts.append(f"après {plural(left, 'lot', 'lots')} encore")
    if b.get("commands"):
        left = max(0, b["commands"] - p["commands"])
        parts.append(f"après {plural(left, 'commande', 'commandes')} encore")
    if b.get("five_hour"):
        parts.append(f"à {b['five_hour']} % de la fenêtre de 5 heures")
    if b.get("seven_day"):
        parts.append(f"à {b['seven_day']} % de la semaine")
    if b.get("step"):
        s = b["step"]
        name = step_name(s["chain"], s["id"])
        where = "" if s["chain"] == "main" else " de la correction"
        parts.append(f"avant « {name} »{where}" if s["when"] == "before" else f"une fois « {name} »{where} faite")
    if not parts:
        return "s'arrête quand on a besoin de vous"
    return "s'arrête " + " ou ".join(parts)


def deadline(p):
    """The earliest time bound: the end time, or the start plus the duration."""
    out = []
    if p.get("end_at"):
        out.append(datetime.fromisoformat(p["end_at"]))
    m = p["spec"]["bounds"].get("minutes")
    if m:
        base = datetime.fromisoformat(p["started_at"] or p["start_at"])
        out.append(base + timedelta(minutes=m))
    return min(out) if out else None


def spec_text(spec, now=None):
    """A saved programme, in one line."""
    st = spec["start"]
    first = {"now": "maintenant", "at": f"à {st.get('at', '')}",
             "slot": f"de {st.get('from', '')} à {st.get('to', '')}"}[st["mode"]]
    p = {"spec": spec, "lots": 0, "commands": 0, "end_at": None, "started_at": None,
         "start_at": (now or datetime.now()).isoformat()}
    b = bounds_text(p, now)
    if spec["bounds"].get("until"):
        b = b.replace("s'arrête ", f"s'arrête à {spec['bounds']['until']} ou ", 1) \
            if b != "s'arrête quand on a besoin de vous" else f"s'arrête à {spec['bounds']['until']}"
    if spec["bounds"].get("minutes"):
        b = b.replace(hm_text(deadline(p), now), f"après {spec['bounds']['minutes']} min")
    return f"Démarre {first}, {b}."


# ------------------------------------------------------------------- clock

class Clock:
    """The real time. `sleep_until` wakes early, returning False, when
    `wake` is set; it checks the wall clock every 30 s — a computer that
    slept is caught up with."""

    def now(self):
        return datetime.now()

    async def sleep_until(self, when, wake):
        while True:
            left = (when - datetime.now()).total_seconds()
            if left <= 0:
                return True
            try:
                await asyncio.wait_for(wake.wait(), min(left, 30.0))
                return False
            except asyncio.TimeoutError:
                continue


# ----------------------------------------------------------------- the pilot

class Pilot:
    def __init__(self, host, clock=None):
        self.host = host
        self.clock = clock or Clock()
        self.p = None              # the programme going, scheduled or waiting
        self.task = None
        self.last = None           # the last summary
        self.wake = None
        # Each change of the programme counted: a page that got a newer one
        # through the stream never goes back to an older one (1.19).
        self.rev = 0

    # ------------------------------------------------------------- reading

    def active(self):
        return self.p is not None and self.p["status"] != FINI

    def public(self):
        if not self.p:
            return None
        now = self.clock.now()
        out = {k: v for k, v in self.p.items() if k not in ("run_obj",)}
        out["bounds_text"] = bounds_text(self.p, now)
        out["rev"] = self.rev
        out["notice"] = LATER if self.p["status"] == PROGRAMME and self.p.get("later") else ""
        dl = deadline(self.p)
        out["deadline"] = dl.isoformat(timespec="seconds") if dl else None
        return out

    # ------------------------------------------------------------ creating

    def create(self, spec, app, feature, app_name=""):
        if self.active():
            raise Refused(f"un programme est déjà actif dans « {self.p.get('app_name') or self.p['app']} »")
        spec = clean_spec(spec)
        now = self.clock.now()
        r = resolve(spec, now)
        if r["end_at"] and r["end_at"] <= r["start_at"]:
            raise Refused("l'heure de fin vient avant le démarrage")
        self.p = {
            "id": "prog-" + uuid.uuid4().hex[:10], "name": spec["name"], "spec": spec,
            "app": app, "app_name": app_name, "feature": feature,
            "created_at": now.isoformat(timespec="seconds"),
            "start_at": r["start_at"].isoformat(timespec="seconds"),
            "end_at": r["end_at"].isoformat(timespec="seconds") if r["end_at"] else None,
            "later": r["later"], "started_at": None, "status": PROGRAMME,
            "doing": "", "waiting": None, "run": None, "commands": 0, "lots": 0, "prompts": [],
            "stop_after": False, "stop_now": False, "reason": None, "reason_kind": None, "ended_at": None,
        }
        self._start_task()
        return self.public()

    def restore(self, record):
        """A programme kept in config.json when the cockpit stopped: one not
        started yet goes on; one that ran is summed up as interrupted."""
        if record.get("status") == PROGRAMME and not record.get("started_at"):
            self.p = dict(record)
            self._start_task()
            return True
        self.p = dict(record)
        self._finish(ERROR, "Le cockpit s'est arrêté pendant le programme.", push=False)
        return False

    def _start_task(self):
        self.wake = asyncio.Event()
        self.task = asyncio.get_running_loop().create_task(self._drive())
        self._changed()

    # ------------------------------------------------------------ stopping

    async def stop(self, how):
        """`apres`: after the command going — after its lot for /8_code,
        stop.md written where it reads it; `maintenant`: the command
        interrupted. A programme not running a command stops at once."""
        if not self.active():
            raise Refused("aucun programme actif")
        p = self.p
        if how == "maintenant":
            p["stop_now"] = True
            self.wake.set()
            if p["status"] == LANCE and p.get("run"):
                await self.host.stop_run_now(p["app"])
        else:
            p["stop_after"] = True
            p["stop_mid_run"] = bool(p["status"] == LANCE and p.get("run"))
            if p["status"] == LANCE and p.get("run"):
                if (p["run"] or {}).get("command") == "8_code":
                    try:
                        self.host.write_stop(p["app"])
                    except Exception as e:      # said, the programme stops all the same
                        p["doing"] += f" — stop.md non écrit : {e}"
            else:
                self.wake.set()
        self._changed()
        return self.public()

    # ------------------------------------------------------------- driving

    def _changed(self):
        self.rev += 1
        if self.p and self.p["status"] != FINI:
            self.host.save(self.p)
        self.host.changed(self.public())

    def _set(self, status, doing, waiting=None):
        self.p.update(status=status, doing=doing, waiting=waiting)
        self._changed()

    def _asked(self):
        p = self.p
        if p["stop_now"]:
            return (ASKED, "Arrêté maintenant, à votre demande.")
        if p["stop_after"]:
            return (ASKED, "Arrêté après la commande en cours, à votre demande." if p.get("stop_mid_run")
                    else "Arrêté à votre demande.")
        return None

    async def _sleep(self, until):
        """Until `until` or the deadline, whichever comes first; False when
        woken by a stop."""
        dl = deadline(self.p) if self.p["started_at"] else None
        target = min(until, dl) if dl else until
        return await self.clock.sleep_until(target, self.wake)

    async def _drive(self):
        try:
            p = self.p
            start = datetime.fromisoformat(p["start_at"])
            if start > self.clock.now():
                self._set(PROGRAMME, f"Démarre {hm_text(start, self.clock.now())}.")
                if not await self.clock.sleep_until(start, self.wake):
                    return self._finish(ASKED, "Annulé avant son démarrage, à votre demande.")
            p["started_at"] = self.clock.now().isoformat(timespec="seconds")
            self._set(LANCE, "Démarre.")
            self.host.push("start", f"{self._app()} — pilote automatique lancé",
                           f"{p['name'] or 'Programme'} : {bounds_text(p, self.clock.now())}.")
            while True:
                why = self._asked() or self._bounds()
                if why:
                    return self._finish(*why)
                other = self.host.busy()
                if other:
                    self._set(ATTEND, f"Attend la fin de {other}, lancée à la main.", {"what": "run", "prompt": other})
                    await self._idle_or_wake()
                    continue
                await self.host.refresh_usage(False)
                sc, dec = self.host.decide(p["app"], p["feature"])
                why, cmd, args = self._choose(sc, dec)
                if why:
                    return self._finish(*why)
                why = self._usage(cmd)
                if isinstance(why, datetime):
                    if not await self._wait_reset(why):
                        return self._finish(*self._asked() or self._bounds() or (ASKED, "Arrêté."))
                    continue
                if why:
                    return self._finish(*why)
                self._set(LANCE, f"Lance /{cmd} {args}".rstrip() + ".")
                run, refused = await self.host.launch(p["app"], p["feature"], cmd, args, p["id"])
                if refused:
                    return self._finish(*refused)
                p["run"] = {"command": cmd, "prompt": f"/{cmd} {args}".rstrip(),
                            "started_at": self.clock.now().isoformat(timespec="seconds")}
                self._set(LANCE, f"/{cmd} {args}".rstrip() + " tourne.")
                snap = await self.host.wait_run(run)
                p["run"] = None
                p["commands"] += 1
                p["prompts"].append(snap.get("prompt") or f"/{cmd} {args}".rstrip())
                outcome = snap.get("outcome")
                if cmd == "8_code" and outcome == "terminé":
                    p["lots"] += 1
                self._changed()
                if p["stop_now"] or outcome == "interrompu":
                    return self._finish(ASKED if p["stop_now"] else ERROR,
                                        "Arrêté maintenant, à votre demande." if p["stop_now"]
                                        else f"{snap.get('prompt')} a été interrompue.")
                if outcome != "terminé":
                    return self._finish(ERROR, f"{snap.get('prompt')} s'est arrêtée sur une erreur : "
                                               f"{snap.get('error') or 'erreur'}.")
                if p["stop_after"]:
                    return self._finish(*self._asked())
                gap = p["spec"]["spacing_min"]
                if gap and not self._bounds():
                    until = self.clock.now() + timedelta(minutes=gap)
                    self._set(PAUSE, f"Pause de {gap} min entre deux commandes, jusqu'à {hm(until)}.",
                              {"what": "pause", "until": until.isoformat(timespec="seconds")})
                    await self._sleep(until)
        except asyncio.CancelledError:
            # Not started yet: kept as it is — the server keeps it in config.json.
            if self.p and self.p["status"] not in (FINI, PROGRAMME):
                self._finish(ASKED, "Le cockpit s'arrête.", push=False)
            raise
        except Exception as e:          # never silent: the programme stops and says why
            if self.p and self.p["status"] != FINI:
                self._finish(ERROR, f"Erreur du pilote : {type(e).__name__}: {e}")

    def _app(self):
        return self.p.get("app_name") or self.p["app"]

    async def _idle_or_wake(self):
        idle = asyncio.ensure_future(self.host.wait_idle())
        woke = asyncio.ensure_future(self.wake.wait())
        await asyncio.wait({idle, woke}, return_when=asyncio.FIRST_COMPLETED)
        for t in (idle, woke):
            if not t.done():
                t.cancel()

    # ------------------------------------------------------------- the rules

    def _bounds(self):
        p, now = self.p, self.clock.now()
        b = p["spec"]["bounds"]
        if p.get("end_at") and now >= datetime.fromisoformat(p["end_at"]):
            return (BOUND, f"Heure de fin atteinte ({hm(datetime.fromisoformat(p['end_at']))}).")
        if b.get("minutes") and p["started_at"] and \
                now >= datetime.fromisoformat(p["started_at"]) + timedelta(minutes=b["minutes"]):
            return (BOUND, f"Durée atteinte ({b['minutes']} min).")
        if b.get("commands") and p["commands"] >= b["commands"]:
            return (BOUND, f"{plural(b['commands'], 'commande lancée', 'commandes lancées')} : la borne est atteinte.")
        if b.get("lots") and p["lots"] >= b["lots"]:
            return (BOUND, f"{plural(b['lots'], 'lot codé', 'lots codés')} : la borne est atteinte.")
        return None

    def _choose(self, sc, dec):
        """(stop, command, args) from the decision: a step for a person, the
        final test, the fusion, a confirmed command, the step to reach — a
        stop; otherwise the command, /8_code one lot at a time."""
        p = self.p
        n = dec.get("next") or {}
        kind = n.get("kind")
        chain, sid = dec.get("chain") or "main", dec.get("step")
        said = n.get("french") or n.get("raw") or ""
        reached = self._step_bound(sc, chain, sid, kind)
        if reached:
            return reached, None, None
        if kind == "answer":
            return (NEED, f"Des réponses vous attendent : {said}"), None, None
        if kind == "manual":
            if sid == "test" or not n.get("command") and "tester" in (n.get("text") or ""):
                return (NEED, "L'étape de test finale : à vous de tester l'application. " + said), None, None
            return (NEED, f"Une étape pour vous : {said}"), None, None
        if kind == "done":
            return (DONE, "Toutes les étapes de la chaîne sont faites."), None, None
        if kind == "stop":
            return (ERROR, f"La chaîne s'est arrêtée : {n.get('text') or said}"), None, None
        if kind != "run" or not n.get("command"):
            return (NEED, said or "Le cockpit ne sait pas quelle commande vient ensuite."), None, None
        cmd = n["command"]
        if cmd in TEST_COMMANDS:
            return (NEED, "L'étape de test finale : à vous de tester l'application."), None, None
        if cmd in FUSION_COMMANDS:
            return (NEED, f"/{cmd} se lance à la main, après votre test."), None, None
        if cmd in CONFIRMED and not p["spec"]["run_confirmed"]:
            return (CONFIRM, f"{CONFIRMED[cmd]} attend votre confirmation : elle se lance à la main, ou "
                             "le programme la laisse tourner si son réglage le dit."), None, None
        args = (n.get("args") or p["feature"]).strip()
        if cmd == "8_code":
            args = args.split()[0]          # one lot per launch
        return None, cmd, args

    def _step_bound(self, sc, chain, sid, kind):
        b = self.p["spec"]["bounds"].get("step")
        if not b:
            return None
        if b["chain"] == "main":
            want, steps = "main", sc.get("main") or []
        else:
            hb = next((c for c in sc.get("corrections") or [] if c.get("highest")), None)
            if not hb:
                return None
            want, steps = hb["name"], hb["steps"]
        ids = [s["id"] for s in steps]
        if b["id"] not in ids:
            return None
        i = ids.index(b["id"])
        name = steps[i].get("name") or step_name(b["chain"], b["id"])
        past = chain == want and sid in ids and ids.index(sid) > i
        if b["when"] == "after":
            if steps[i].get("state") == scan_mod.FAITE or past or (kind == "done" and chain == want):
                return (BOUND, f"« {name} » est faite : l'étape à atteindre est atteinte.")
            return None
        if (chain == want and sid == b["id"] and kind in ("run", "answer", "manual")) or past:
            return (BOUND, f"Arrêt avant « {name} », comme demandé.")
        return None

    def _usage(self, cmd):
        """None to go on; a stop; or the moment to wait for — the 5-hour
        window's reset, within the programme's bounds."""
        b = self.p["spec"]["bounds"]
        lv = self.host.levels()
        th = self.host.thresholds()
        for w in WINDOWS:
            x = lv.get(w) or {}
            if b.get(w) and x.get("pct") is not None and x.get("level") not in ("reset", "inconnu") \
                    and x["pct"] >= b[w]:
                return (BOUND, f"{usage_mod.WINDOW_NAMES[w]} à {usage_mod.fmt_pct(x['pct'])} : la borne de "
                               f"{b[w]} % est atteinte.")
        blocked = usage_mod.blocking(lv)
        if blocked:
            return (USAGE, f"Seuil de blocage atteint : {usage_mod.block_text(blocked)} — un programme ne "
                           "passe jamais outre.")
        est = self.host.estimate(cmd) or {}
        for w in WINDOWS:
            x = lv.get(w) or {}
            e = (est.get(w) or {}).get("median")
            if e is None or x.get("pct") is None or x.get("level") in ("reset", "inconnu"):
                continue
            block = th[w]["block"]
            if x["pct"] + e < block:
                continue
            said = (f"{usage_mod.WINDOW_NAMES[w]} à {usage_mod.fmt_pct(x['pct'])}, et /{cmd} en prend "
                    f"≈ {usage_mod.fmt_pct(e)} : le seuil de blocage ({block} %) serait passé")
            if w != "five_hour":
                return (USAGE, said + ".")
            if not x.get("resets_at"):
                return (USAGE, said + ", et sa réinitialisation est inconnue.")
            reset = datetime.fromtimestamp(x["resets_at"])
            resume = reset + timedelta(seconds=RESET_MARGIN_S)
            dl = deadline(self.p)
            if dl and resume >= dl:
                return (USAGE, said + f" ; elle se réinitialise {hm_text(reset, self.clock.now())}, après la "
                                      f"fin du programme ({hm(dl)}).")
            return resume
        return None

    async def _wait_reset(self, resume):
        p = self.p
        lv = self.host.levels().get("five_hour") or {}
        reset = resume - timedelta(seconds=RESET_MARGIN_S)
        self._set(ATTEND, f"Attend la réinitialisation de la fenêtre de 5 heures, {hm_text(reset, self.clock.now())}.",
                  {"what": "reset", "until": resume.isoformat(timespec="seconds"),
                   "reset_at": reset.isoformat(timespec="seconds")})
        self.host.push("wait", f"{self._app()} — le pilote attend la réinitialisation",
                       f"Fenêtre de 5 heures à {usage_mod.fmt_pct(lv.get('pct') or 0)} : reprise "
                       f"{hm_text(reset, self.clock.now())}.")
        if not await self._sleep(resume):
            return False
        await self.host.refresh_usage(True)
        return True

    # -------------------------------------------------------------- ending

    def _finish(self, kind, reason, push=True):
        p = self.p
        p.update(status=FINI, reason=reason, reason_kind=kind, run=None, waiting=None,
                 ended_at=self.clock.now().isoformat(timespec="seconds"), doing="")
        spent = {}
        try:
            spent = self.host.spent(p["id"]) or {}
        except Exception:
            pass
        self.last = {k: p.get(k) for k in ("id", "name", "app", "app_name", "feature", "spec", "created_at",
                                           "started_at", "ended_at", "commands", "lots", "prompts", "reason",
                                           "reason_kind")}
        self.last["usage"] = spent
        try:
            self.host.record(self.last)
        except Exception as e:
            print(f"Pilote automatique : résumé non enregistré ({e})", flush=True)
        self.host.save(None)
        if push:
            self.host.push("stop", f"{self._app()} — pilote automatique arrêté",
                           f"{reason} {summary_counts(self.last)}")
        print(f"Pilote automatique — {p['name'] or p['id']} arrêté : {reason} {summary_counts(self.last)}", flush=True)
        self.rev += 1
        self.host.changed(self.public())
        return self.last


def summary_counts(s):
    out = f"{plural(s.get('commands') or 0, 'commande', 'commandes')}, {plural(s.get('lots') or 0, 'lot codé', 'lots codés')}"
    u = s.get("usage") or {}
    parts = []
    for w, name in (("five_hour", "de la fenêtre"), ("seven_day", "de la semaine")):
        x = u.get(w) or {}
        if x.get("spent") is not None:
            parts.append(f"≈ {usage_mod.fmt_pct(x['spent'])} {name}")
    if parts:
        out += ", " + " et ".join(parts)
    return f"— {out}."


def spec_json(spec):
    return json.dumps(spec, ensure_ascii=False, sort_keys=True)
