"""1.18 — the automatic mode's rules (autopilot.py), on a fake host and a
fake clock: each bound alone, then combined — the first reached wins —, each
start mode, the spacing; each always-stop, the two confirmed commands both
ways, no stop on an intermediate step; /8_code one lot per launch, the checks
between lots; waiting for a reset inside the bounds, stopping when it is
beyond them or unknown; both stops; the pushes and the summary. No server,
no Claude."""
import asyncio
from datetime import datetime, timedelta

import pytest

import autopilot as ap
import scan as scan_mod
import usage

T0 = datetime(2026, 10, 10, 22, 0, 0)
MAIN = [d.id for d in scan_mod.MAIN]


class FakeClock:
    def __init__(self, now=T0):
        self.t = now
        self.slept = []

    def now(self):
        return self.t

    async def sleep_until(self, when, wake):
        await asyncio.sleep(0)
        if wake.is_set():
            return False
        self.slept.append(when)
        self.t = max(self.t, when)
        return not wake.is_set()


def run_(cmd, args="f"):
    sid = scan_mod.step_of_command(cmd) or cmd
    return {"next": {"kind": "run", "command": cmd, "args": args, "french": f"Lancer /{cmd} {args}."},
            "chain": "main", "step": sid}


def answer_(cmd="4_grille"):
    return {"next": {"kind": "answer", "what": "questions", "command": cmd, "args": "f",
                     "french": f"Répondre aux questions, puis lancer /{cmd} f."}, "chain": "main", "step": cmd}


def manual_(step="test", text="tester sur l'émulateur, puis décider d'une bug-list ou de /fusion"):
    return {"next": {"kind": "manual", "command": None, "text": text, "french": f"À faire à la main : {text}."},
            "chain": "main", "step": step}


class FakeHost:
    """Each decision in `flow` in turn — the next one once a command ran."""

    def __init__(self, clock, flow, outcomes=None, refuse=None, five=0.10, week=0.10, est=None,
                 minutes_per_run=10, after_reset=0.05, resets_in=timedelta(hours=2)):
        self.clock = clock
        self.flow = list(flow)
        self.outcomes = outcomes or {}
        self.refuse = refuse or {}
        self.limits = self._lim(five, week, resets_in)
        self.after_reset = after_reset
        self.est = est or {}
        self.minutes = minutes_per_run
        self.launched, self.pushes, self.records, self.saved, self.changes = [], [], [], [], []
        self.stop_written = self.stopped_now = 0
        self.refreshed = []
        self.busy_prompt = None
        self.during_run = None            # called while a run goes: a stop from the page

    def _lim(self, five, week, resets_in):
        at = self.clock.now().isoformat()
        r5 = int((self.clock.now() + resets_in).timestamp()) if resets_in else None
        return {"five_hour": {"utilization": five, "resets_at": r5, "measured_at": at},
                "seven_day": {"utilization": week, "resets_at": int((self.clock.now() + timedelta(days=4)).timestamp()),
                              "measured_at": at}}

    def decide(self, app, feature):
        dec = self.flow[min(len(self.launched), len(self.flow) - 1)]
        cur = dec.get("step")
        i = MAIN.index(cur) if cur in MAIN else len(MAIN)
        steps = [{"id": x, "name": ap.step_name("main", x),
                  "state": scan_mod.FAITE if j < i else scan_mod.A_FAIRE} for j, x in enumerate(MAIN)]
        return {"main": steps, "corrections": []}, dec

    def busy(self):
        return self.busy_prompt

    async def wait_idle(self):
        self.busy_prompt = None

    async def refresh_usage(self, force):
        self.refreshed.append(force)
        if force:
            self.limits["five_hour"]["utilization"] = self.after_reset
            self.limits["five_hour"]["resets_at"] = int((self.clock.now() + timedelta(hours=5)).timestamp())

    def levels(self):
        return usage.levels(self.limits, self.thresholds(), now=self.clock.now())

    def thresholds(self):
        return usage.clean_thresholds(None)

    def estimate(self, cmd):
        e = self.est.get(cmd)
        return {"five_hour": {"median": e[0], "n": 3, "scope": "app"},
                "seven_day": {"median": e[1], "n": 3, "scope": "app"}} if e else None

    async def launch(self, app, feature, cmd, args, pid):
        if cmd in self.refuse:
            return None, self.refuse[cmd]
        self.launched.append(f"/{cmd} {args}".rstrip())
        return {"cmd": cmd, "args": args}, None

    async def wait_run(self, r):
        n = len(self.launched)
        if self.during_run:
            await self.during_run(n)
        self.clock.t += timedelta(minutes=self.minutes)
        return {"outcome": self.outcomes.get(n, "terminé"), "prompt": f"/{r['cmd']} {r['args']}".rstrip(),
                "command": r["cmd"], "error": "boom" if self.outcomes.get(n) == "erreur" else ""}

    async def stop_run_now(self, app):
        self.stopped_now += 1

    def write_stop(self, app):
        self.stop_written += 1

    def changed(self, public):
        self.changes.append(public and public["status"])

    def push(self, event, title, body):
        self.pushes.append((event, title, body))

    def record(self, summary):
        self.records.append(summary)

    def spent(self, pid):
        return {"five_hour": {"spent": 7.5, "unknown": 0}, "seven_day": {"spent": 1.0, "unknown": 1}}

    def save(self, record):
        self.saved.append(record and dict(record))


def go(flow, spec=None, clock=None, **kw):
    clock = clock or FakeClock()
    host = FakeHost(clock, flow, **kw)

    async def main():
        pilot = ap.Pilot(host, clock)
        pilot.create(spec or {}, "C:/app", "f", "app")
        await pilot.task
        return pilot
    pilot = asyncio.run(main())
    return pilot, host


UPSTREAM = [run_(c) for c in ("1_lexique", "2_structure", "3_decoupe", "3a_genre", "3b_nature")] + [answer_("4_grille")]


# --------------------------------------------------------------- the flow

def test_it_chains_until_she_is_needed():
    pilot, host = go(UPSTREAM)
    assert host.launched == ["/1_lexique f", "/2_structure f", "/3_decoupe f", "/3a_genre f", "/3b_nature f"]
    s = pilot.last
    assert s["reason_kind"] == ap.NEED and s["reason"].startswith("Des réponses vous attendent")
    assert s["commands"] == 5 and s["lots"] == 0 and s["usage"]["five_hour"]["spent"] == 7.5
    assert host.records == [s] and host.saved[-1] is None
    # Pushed when it starts and when it stops, with the reason.
    assert [p[0] for p in host.pushes] == ["start", "stop"]
    assert "Des réponses vous attendent" in host.pushes[-1][2] and "5 commandes" in host.pushes[-1][2]
    assert "≈ 7,5 % de la fenêtre" in host.pushes[-1][2]


def test_no_stop_on_an_intermediate_step_only_at_the_final_test():
    flow = [run_("6_convertit"), run_("conventions"), run_("batir"), run_("7_lots"), run_("8_code"), run_("8_code"),
            run_("9_controle"), manual_("test")]
    pilot, host = go(flow, {"run_confirmed": True})
    assert host.launched == ["/6_convertit f", "/conventions f", "/batir f", "/7_lots f", "/8_code f", "/8_code f",
                             "/9_controle f"]
    assert pilot.last["reason"].startswith("L'étape de test finale") and pilot.last["lots"] == 2


@pytest.mark.parametrize("dec, kind, said", [
    (answer_(), ap.NEED, "Des réponses vous attendent"),
    (manual_("test"), ap.NEED, "L'étape de test finale"),
    (run_("deploie", ""), ap.NEED, "L'étape de test finale"),
    (manual_("8_code", "écrire bugfix-01/bug-list.md"), ap.NEED, "Une étape pour vous"),
    ({"next": {"kind": "blocked", "french": "L'étape est bloquée : x"}, "chain": "main", "step": "4_grille"}, ap.NEED, "bloquée"),
    ({"next": {"kind": "stop", "text": "le split n'est pas cohérent"}, "chain": "main", "step": None}, ap.ERROR, "La chaîne s'est arrêtée : le split"),
    ({"next": {"kind": "done"}, "chain": "main", "step": None}, ap.DONE, "Toutes les étapes"),
    (run_("fusion"), ap.NEED, "/fusion se lance à la main"),
])
def test_each_step_for_a_person_stops(dec, kind, said):
    pilot, host = go([dec])
    assert host.launched == [] and pilot.last["reason_kind"] == kind and said in pilot.last["reason"]


@pytest.mark.parametrize("cmd", ["9_controle", "diagnostique"])
def test_the_two_confirmed_commands_both_ways(cmd):
    pilot, host = go([run_("8_code"), run_(cmd), answer_()])
    assert host.launched == ["/8_code f"] and pilot.last["reason_kind"] == ap.CONFIRM
    assert f"/{cmd} attend votre confirmation" in pilot.last["reason"]
    pilot, host = go([run_("8_code"), run_(cmd), answer_()], {"run_confirmed": True})
    assert host.launched == ["/8_code f", f"/{cmd} f"] and pilot.last["reason_kind"] == ap.NEED


@pytest.mark.parametrize("refusal", [
    (ap.MACHINE, "État de l'ordinateur : Claude Code n'est pas connecté"),
    (ap.GITHUB, "GitHub : divergé — rien ne se lance avant « Réconcilier »"),
    (ap.USAGE, "Seuil de blocage atteint : Fenêtre de 5 heures à 92 %"),
    (ap.CHAIN, "Chaîne en retard — un programme ne lance rien sur une chaîne pas à jour."),
])
def test_a_refused_launch_stops_with_its_reason(refusal):
    pilot, host = go([run_("1_lexique"), run_("2_structure")], refuse={"2_structure": refusal})
    assert host.launched == ["/1_lexique f"] and (pilot.last["reason_kind"], pilot.last["reason"]) == refusal


@pytest.mark.parametrize("outcome, kind, said", [("erreur", ap.ERROR, "s'est arrêtée sur une erreur : boom"),
                                                  ("interrompu", ap.ERROR, "a été interrompue")])
def test_an_error_stops(outcome, kind, said):
    pilot, host = go(UPSTREAM, outcomes={2: outcome})
    assert host.launched == ["/1_lexique f", "/2_structure f"] and pilot.last["reason_kind"] == kind
    assert said in pilot.last["reason"]


def test_the_blocking_threshold_stops_with_no_override():
    pilot, host = go(UPSTREAM, five=0.93)
    assert host.launched == [] and pilot.last["reason_kind"] == ap.USAGE
    assert "un programme ne passe jamais outre" in pilot.last["reason"]


def test_a_run_launched_by_hand_is_waited_for():
    clock = FakeClock()
    host = FakeHost(clock, UPSTREAM[:2] + [answer_()])
    host.busy_prompt = "/7_lots g"

    async def main():
        pilot = ap.Pilot(host, clock)
        pilot.create({}, "C:/app", "f")
        await pilot.task
        return pilot
    pilot = asyncio.run(main())
    assert ap.ATTEND in host.changes and host.launched == ["/1_lexique f", "/2_structure f"]


# ------------------------------------------------------------- the bounds

LONG = [run_("8_code")] * 30


@pytest.mark.parametrize("bounds, launched, said", [
    ({"commands": 3}, 3, "3 commandes lancées"),
    ({"lots": 2}, 2, "2 lots codés"),
    ({"minutes": 45}, 5, "Durée atteinte (45 min)"),          # 10 min per run: 0, 10, 20, 30, 40
    ({"until": "23:00"}, 6, "Heure de fin atteinte (23 h)"),     # from 22 h
])
def test_each_bound_alone(bounds, launched, said):
    pilot, host = go(LONG, {"bounds": bounds})
    assert len(host.launched) == launched and pilot.last["reason_kind"] == ap.BOUND, pilot.last
    assert said in pilot.last["reason"]


@pytest.mark.parametrize("bounds, launched, said", [
    ({"commands": 3, "lots": 5, "minutes": 120}, 3, "3 commandes"),
    ({"commands": 9, "lots": 2, "minutes": 120}, 2, "2 lots codés"),
    ({"commands": 9, "lots": 8, "minutes": 25}, 3, "Durée atteinte"),
    ({"commands": 9, "lots": 8, "until": "22:15"}, 2, "Heure de fin"),
])
def test_bounds_combined_the_first_reached_wins(bounds, launched, said):
    pilot, host = go(LONG, {"bounds": bounds})
    assert len(host.launched) == launched and said in pilot.last["reason"]


def test_lots_count_only_coded_lots_of_8_code():
    flow = [run_("7_lots"), run_("8_code"), run_("8_code"), run_("8_code"), answer_()]
    pilot, host = go(flow, {"bounds": {"lots": 2}}, outcomes={})
    assert host.launched == ["/7_lots f", "/8_code f", "/8_code f"] and pilot.last["lots"] == 2


def test_8_code_one_lot_per_launch_whatever_the_relay_says():
    pilot, host = go([run_("8_code", "f 3"), run_("8_code", "f 2"), answer_()])
    assert host.launched == ["/8_code f", "/8_code f"]


@pytest.mark.parametrize("w, bound, level, stopped", [("five_hour", 50, 0.55, True), ("seven_day", 30, 0.35, True),
                                                       ("five_hour", 50, 0.45, False)])
def test_a_usage_bound(w, bound, level, stopped):
    kw = {"five": level} if w == "five_hour" else {"week": level}
    pilot, host = go(UPSTREAM, {"bounds": {w: bound}}, **kw)
    if stopped:
        assert host.launched == [] and pilot.last["reason_kind"] == ap.BOUND and f"la borne de {bound} %" in pilot.last["reason"]
    else:
        assert len(host.launched) == 5


@pytest.mark.parametrize("when, launched, said", [
    ("before", ["/1_lexique f", "/2_structure f"], "Arrêt avant « Découper les blocs »"),
    ("after", ["/1_lexique f", "/2_structure f", "/3_decoupe f"], "« Découper les blocs » est faite"),
])
def test_a_step_to_reach(when, launched, said):
    pilot, host = go(UPSTREAM, {"bounds": {"step": {"chain": "main", "id": "3_decoupe", "when": when}}})
    assert host.launched == launched and pilot.last["reason_kind"] == ap.BOUND and said in pilot.last["reason"]


def test_bounds_in_words():
    p = {"spec": ap.clean_spec({"bounds": {"until": "07:00", "lots": 4, "five_hour": 80,
                                           "step": {"chain": "main", "id": "9_controle", "when": "before"}}}),
         "lots": 0, "commands": 0, "end_at": datetime(2026, 10, 11, 7, 0).isoformat(), "started_at": T0.isoformat(),
         "start_at": T0.isoformat()}
    assert ap.bounds_text(p, T0) == ("s'arrête demain à 7 h ou après 4 lots encore ou à 80 % de la fenêtre de 5 heures "
                                     "ou avant « Contrôler la feature »")
    p["lots"] = 3
    assert "après 1 lot encore" in ap.bounds_text(p, datetime(2026, 10, 11, 1, 0))
    assert "s'arrête à 7 h ou" in ap.bounds_text(p, datetime(2026, 10, 11, 1, 0))
    assert ap.bounds_text({**p, "spec": ap.clean_spec({}), "end_at": None}, T0) == "s'arrête quand on a besoin de vous"


# --------------------------------------------------------------- starting

def test_start_now_at_a_time_and_in_a_slot():
    r = ap.resolve(ap.clean_spec({}), T0)
    assert r["start_at"] == T0 and r["end_at"] is None and not r["later"]
    r = ap.resolve(ap.clean_spec({"start": {"mode": "at", "at": "1:30"}}), T0)
    assert r["start_at"] == datetime(2026, 10, 11, 1, 30) and r["later"]
    r = ap.resolve(ap.clean_spec({"start": {"mode": "slot", "from": "01:00", "to": "07:00"}}), T0)
    assert (r["start_at"], r["end_at"]) == (datetime(2026, 10, 11, 1, 0), datetime(2026, 10, 11, 7, 0))
    # Inside the slot already: at once, until its end.
    r = ap.resolve(ap.clean_spec({"start": {"mode": "slot", "from": "21:00", "to": "02:00"}}), T0)
    assert (r["start_at"], r["end_at"]) == (T0, datetime(2026, 10, 11, 2, 0)) and not r["later"]
    # An end time and a slot: the earlier wins.
    r = ap.resolve(ap.clean_spec({"start": {"mode": "slot", "from": "01:00", "to": "07:00"},
                                  "bounds": {"until": "05:00"}}), T0)
    assert r["end_at"] == datetime(2026, 10, 11, 5, 0)


def test_a_later_start_waits_and_says_the_computer_must_stay_awake():
    clock = FakeClock()
    host = FakeHost(clock, UPSTREAM)

    async def main():
        pilot = ap.Pilot(host, clock)
        out = pilot.create({"start": {"mode": "slot", "from": "01:00", "to": "07:00"}}, "C:/app", "f")
        assert out["status"] == ap.PROGRAMME and out["notice"] == ap.LATER
        assert host.saved[-1]["status"] == ap.PROGRAMME        # kept: a cockpit restart finds it
        await pilot.task
        return pilot
    pilot = asyncio.run(main())
    assert clock.slept[0] == datetime(2026, 10, 11, 1, 0)
    assert pilot.last["started_at"] == "2026-10-11T01:00:00" and len(host.launched) == 5


def test_a_slot_end_is_a_bound():
    pilot, host = go(LONG, {"start": {"mode": "slot", "from": "01:00", "to": "02:00"}})
    assert len(host.launched) == 6 and "Heure de fin atteinte (2 h)" in pilot.last["reason"]


def test_spacing_between_commands():
    pilot, host = go(UPSTREAM, {"spacing_min": 15})
    clock_waits = [t for t in pilot.clock.slept]
    assert len(host.launched) == 5 and len(clock_waits) == 5
    assert clock_waits[0] == T0 + timedelta(minutes=10 + 15)
    assert ap.PAUSE in host.changes


def test_spacing_never_runs_past_the_deadline():
    pilot, host = go(LONG, {"spacing_min": 30, "bounds": {"minutes": 50}})
    assert len(host.launched) == 2 and "Durée atteinte" in pilot.last["reason"]
    assert max(pilot.clock.slept) <= T0 + timedelta(minutes=50)


def test_a_bad_spec_is_refused_in_french():
    for bad, said in [({"start": {"mode": "at", "at": "25:00"}}, "heure illisible"),
                      ({"bounds": {"lots": 0}}, "nombre de lots"),
                      ({"bounds": {"step": {"id": "x"}}}, "étape inconnue"),
                      ({"start": {"mode": "slot", "from": "1:00", "to": "1:00"}}, "même heure")]:
        with pytest.raises(ValueError, match=said):
            ap.clean_spec(bad)


def test_one_programme_at_a_time():
    clock = FakeClock()
    host = FakeHost(clock, UPSTREAM)

    async def main():
        pilot = ap.Pilot(host, clock)
        pilot.create({"start": {"mode": "at", "at": "23:30"}}, "C:/app", "f")
        with pytest.raises(ap.Refused, match="déjà actif"):
            pilot.create({}, "C:/app", "f")
        await pilot.stop("apres")
        await pilot.task
        return pilot
    pilot = asyncio.run(main())
    assert pilot.last["reason"] == "Annulé avant son démarrage, à votre demande." and host.launched == []


# --------------------------------------------------------- waiting a reset

def test_waits_for_the_reset_inside_its_bounds_then_measures_and_goes_on():
    pilot, host = go(UPSTREAM, {"bounds": {"until": "06:00"}}, five=0.86, est={"3_decoupe": (6.0, 1.0)},
                     resets_in=timedelta(hours=2))
    reset = T0 + timedelta(minutes=20) + timedelta(hours=2)      # set when the limits were made, at 22 h
    assert host.launched == ["/1_lexique f", "/2_structure f", "/3_decoupe f", "/3a_genre f", "/3b_nature f"]
    resume = T0 + timedelta(hours=2, seconds=ap.RESET_MARGIN_S)
    assert resume in pilot.clock.slept and True in host.refreshed
    wait = [p for p in host.pushes if p[0] == "wait"]
    assert len(wait) == 1 and "reprise demain à 0 h" in wait[0][2] and "86 %" in wait[0][2]
    assert ap.ATTEND in host.changes and reset


def test_stops_when_the_reset_is_beyond_the_bounds():
    pilot, host = go(UPSTREAM, {"bounds": {"until": "23:00"}}, five=0.86, est={"1_lexique": (6.0, 1.0)},
                     resets_in=timedelta(hours=2))
    assert host.launched == [] and pilot.last["reason_kind"] == ap.USAGE
    assert "après la fin du programme (23 h)" in pilot.last["reason"] and "≈ 6 %" in pilot.last["reason"]


def test_stops_when_the_reset_is_unknown():
    pilot, host = go(UPSTREAM, five=0.86, est={"1_lexique": (6.0, 1.0)}, resets_in=None)
    assert host.launched == [] and "sa réinitialisation est inconnue" in pilot.last["reason"]


def test_the_week_never_waits():
    pilot, host = go(UPSTREAM, week=0.88, est={"1_lexique": (1.0, 3.0)})
    assert host.launched == [] and pilot.last["reason"].startswith("Semaine à 88 %")


def test_an_unknown_estimate_does_not_wait():
    pilot, host = go(UPSTREAM, five=0.86)
    assert len(host.launched) == 5


# ---------------------------------------------------------------- stopping

def test_stop_after_the_current_lot_writes_stop_md():
    clock = FakeClock()
    host = FakeHost(clock, LONG)
    box = {}

    async def stop_during(n):
        if n == 2:
            out = await box["pilot"].stop("apres")
            assert out["stop_after"]

    host.during_run = stop_during

    async def main():
        pilot = box["pilot"] = ap.Pilot(host, clock)
        pilot.create({}, "C:/app", "f")
        await pilot.task
        return pilot
    pilot = asyncio.run(main())
    assert host.launched == ["/8_code f", "/8_code f"] and host.stop_written == 1
    assert pilot.last["reason"] == "Arrêté après la commande en cours, à votre demande." and pilot.last["lots"] == 2


def test_stop_after_a_non_code_command_writes_nothing():
    clock = FakeClock()
    host = FakeHost(clock, UPSTREAM)
    box = {}

    async def stop_during(n):
        if n == 1:
            await box["pilot"].stop("apres")
    host.during_run = stop_during

    async def main():
        pilot = box["pilot"] = ap.Pilot(host, clock)
        pilot.create({}, "C:/app", "f")
        await pilot.task
        return pilot
    pilot = asyncio.run(main())
    assert host.launched == ["/1_lexique f"] and host.stop_written == 0


def test_stop_now_interrupts_the_command():
    clock = FakeClock()
    host = FakeHost(clock, UPSTREAM, outcomes={2: "interrompu"})
    box = {}

    async def stop_during(n):
        if n == 2:
            await box["pilot"].stop("maintenant")
    host.during_run = stop_during

    async def main():
        pilot = box["pilot"] = ap.Pilot(host, clock)
        pilot.create({}, "C:/app", "f")
        await pilot.task
        return pilot
    pilot = asyncio.run(main())
    assert host.stopped_now == 1 and host.launched == ["/1_lexique f", "/2_structure f"]
    assert pilot.last["reason"] == "Arrêté maintenant, à votre demande." and pilot.last["reason_kind"] == ap.ASKED
    assert host.pushes[-1][0] == "stop"


def test_restore_a_scheduled_programme_or_sum_up_an_interrupted_one():
    clock = FakeClock()
    host = FakeHost(clock, UPSTREAM)

    async def main():
        pilot = ap.Pilot(host, clock)
        pilot.create({"start": {"mode": "at", "at": "23:00"}}, "C:/app", "f")
        kept = dict(host.saved[-1])
        pilot.task.cancel()
        await asyncio.gather(pilot.task, return_exceptions=True)
        assert host.records == []                       # not summed up: kept for the next cockpit
        again = ap.Pilot(host, clock)
        assert again.restore(kept) is True
        await again.task
        ran = again.last
        third = ap.Pilot(host, clock)
        assert third.restore({**kept, "status": ap.LANCE, "started_at": "2026-10-10T23:00:00"}) is False
        return ran, third.last
    ran, interrupted = asyncio.run(main())
    assert ran["commands"] == 5
    assert interrupted["reason"] == "Le cockpit s'est arrêté pendant le programme."
