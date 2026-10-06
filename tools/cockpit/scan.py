"""Where a feature stands — cockpit 1.3, §1.

Reads the files only: no Claude call, no git command, no write. Each step's
state comes from its own command's tests, `.claude/commands/<cmd>.md`;
every rule carries the id `scan_rules.md` lists it under, with the lines
it comes from. A step no rule can place is « inconnu », never guessed.

States: faite · t'attend · en cours · bloquée · à faire · inconnu.
"""
import os
import re
import time
from dataclasses import dataclass, field, asdict

import blocking
import questions
import textfile

FAITE, ATTEND, EN_COURS, BLOQUEE, A_FAIRE, INCONNU = (
    "faite", "t'attend", "en cours", "bloquée", "à faire", "inconnu")

BUGFIX = re.compile(r"^bugfix-(\d+)$")
ROOT_Q = re.compile(r"^questions-([A-Za-z0-9_]+(?:-[A-Za-z][A-Za-z0-9_]*)*)-(\d+)\.md$")
Q_HEAD = re.compile(r"^### Q")
ANSWER_EMPTY = re.compile(r"^Answer:\s*$")
DEFAUT = re.compile(r"^Défaut:")
MARKER_NEW = re.compile(r"^### .*NEW")
MARKER_MOD = re.compile(r"^### .*MODIFIED")
NATURES = ["model", "persistence", "calculation", "transition", "external exchange",
           "synchronisation", "presentation", "access"]
GENRE_FILES = ["comportements", "transverses", "directives", "references", "hors-perimetre", "recette"]
# The turn order of the agents that leave their questions file at the root
# (cmd/3_decoupe.md:66-69, cmd/3a_genre.md:72-75, cmd/3b_nature.md:~67,
# cmd/4_grille.md:266-269 each file every root file before writing).
# The agent's own file, or a later one, at the root: the step ran on this
# turn. An earlier one: it has not.
AFTER_DEC = {"qualifieur", "classeur", "sondeur", "existant"}
AFTER_GEN = {"qualifieur", "classeur", "sondeur", "existant"}
AFTER_NAT = {"classeur", "sondeur", "existant"}
BEFORE_DEC = {"lexicographe", "redacteur"}
BEFORE_GEN = {"lexicographe", "redacteur"}
BEFORE_NAT = {"lexicographe", "redacteur", "qualifieur"}


# ---------------------------------------------------------------- steps

@dataclass
class StepDef:
    id: str
    command: str | None      # the command its button launches
    name: str                # in plain French
    commands: tuple = ()     # every command that belongs to the step


MAIN = [
    StepDef("1_lexique", "1_lexique", "Fixer le vocabulaire"),
    StepDef("2_structure", "2_structure", "Structurer la fiche produit"),
    StepDef("3_decoupe", "3_decoupe", "Découper les blocs"),
    StepDef("3a_genre", "3a_genre", "Donner un genre aux blocs"),
    StepDef("3b_nature", "3b_nature", "Donner une nature aux blocs"),
    StepDef("4_grille", "4_grille", "Passer la grille de cadrage"),
    StepDef("5_reclasse", "5_reclasse", "Reclasser par genre et par nature"),
    StepDef("6_convertit", "6_convertit", "Convertir en document technique"),
    StepDef("conventions", "conventions", "Établir les conventions"),
    StepDef("7_lots", "7_lots", "Découper en lots"),
    StepDef("8_code", "8_code", "Coder les lots"),
    StepDef("9_controle", "9_controle", "Contrôler la feature"),
    StepDef("test", "deploie", "Tester sur l'émulateur", ("deploie",)),
    StepDef("fusion", "fusion", "Fusionner dans le global", ("fusion", "fusion_compare", "fusion_applique")),
]
CORRECTION = [
    StepDef("diagnostique", "diagnostique", "Diagnostiquer les écarts"),
    StepDef("7_lots", "7_lots", "Découper en lots"),
    StepDef("8_code", "8_code", "Coder les lots"),
    StepDef("9_controle", "9_controle", "Contrôler la correction"),
]
for _s in MAIN + CORRECTION:
    if not _s.commands:
        _s.commands = (_s.command,)

# §1.2 — commands whose own text puts a test after a git action, a write or
# an agent: clicking them in the wrong state is not harmless, so the flow
# always asks. The reasons are scan_rules.md's « Préconditions » table.
# /2_structure left the list in 1.4.3: its three stops after the filing
# (2_structure.md:110-120, :135-139, :167-169) leave only the lexicographe's
# empty questions file filed (:89-93), a state the next command reads
# correctly — nothing a confirmation would protect.
CONFIRM = {
    "9_controle": "elle commite et crée le worktree (9_controle.md:104, :110) avant le contrôle de la carte des lots "
                  "(:225-228), qui lit ce que la phase 1 écrit : sur cet arrêt, elle commite, fusionne et pousse "
                  "tracabilite-full.md avant de refermer son worktree (:449-451)",
    "diagnostique": "elle commite et crée le worktree (diagnostique.md:86, :96) avant de retenir la phase 2 "
                    "(:142-147) : quand la phase 1 n'émet rien, elle referme son worktree (:184-186) mais laisse "
                    "commité et poussé ce qui attendait dans le dossier",
}

# Every rule the scan applies, with the lines it comes from. scan_rules.md
# is the same table, for the Product Owner; a test keeps the two together
# and checks that each cited line still says what the rule reads in it.
RULES = {
    "G-ATT": "« À qui est une réponse » : la commande nommée après « answer …, then run »",
    "G-AMONT": "6_convertit.md:35-38 · 2_structure.md:248-255",
    "G-AVAL": "§1.3 de la demande : « nothing upstream changed it since »",
    "G-BUGFIX": "7_lots.md:18-19 · 8_code.md:25-26 · 9_controle.md:20-21 · 9_controle.md:512-513",
    "G-WT": "1_lexique.md:138-140 — git worktree add .claude/worktrees/<name>, dans chaque commande à agent",
    "G-ERR": "TECHNICAL_V1 §8.1 : un fichier illisible est une erreur, jamais un fichier sans question",
    "G-RUN": "le run en cours du cockpit",
    "G-HEAD": "§2 : HEAD a bougé depuis le relais, hors run du cockpit",
    "X-FAITE": "§2 : la sortie de X existe",
    "X-BLOQUEE": "§2 : X est bloquée",
    "X-AMONT": "§2 : une étape avant X t'attend",
    "OWN-Q": "1_lexique.md:77-78",
    "OWN-LEX": "1_lexique.md:41",
    "OWN-RED1": "2_structure.md:81",
    "OWN-RE3": "fusion.md:57",
    "OWN-DEC": "3_decoupe.md:39",
    "OWN-GEN": "3a_genre.md:39",
    "OWN-NAT": "3b_nature.md:38",
    "OWN-GRI": "4_grille.md:47-61",
    "OWN-TEC": "6_convertit.md:468 · 6_convertit.md:470",
    "OWN-CNV": "6_convertit.md:56",
    "OWN-ARC": "conventions.md:82",
    "OWN-ARB": "conventions.md:78",
    "OWN-AR3": "8_code.md:327-333",
    "OWN-CAD": "7_lots.md:212",
    "OWN-RED": "7_lots.md:379-380",
    "OWN-COD": "8_code.md:333-334 · 8_code.md:752",
    "OWN-FUS": "fusion.md:60",
    "OWN-FUB": "fusion.md:57",
    "OWN-DIA": "diagnostique.md:233 · diagnostique.md:243",
    "OWN-?": "aucune commande ne nomme ce fichier",
    "LEX-1": "1_lexique.md:93-104",
    "LEX-2": "1_lexique.md:56",
    "LEX-3": "1_lexique.md:57",
    "LEX-4": "1_lexique.md:58",
    "LEX-5": "1_lexique.md:60",
    "LEX-6": "1_lexique.md:63 · 1_lexique.md:121-122",
    "LEX-7": "1_lexique.md:59",
    "LEX-8": "1_lexique.md:61",
    "LEX-9": "1_lexique.md:62",
    "STR-1": "2_structure.md:63-72",
    "STR-2": "2_structure.md:82",
    "STR-3": "2_structure.md:115",
    "STR-4": "2_structure.md:114",
    "STR-5": "2_structure.md:116",
    "STR-6": "2_structure.md:118",
    "STR-7": "2_structure.md:119",
    "STR-8": "2_structure.md:120",
    "STR-9": "2_structure.md:120",
    "DEC-0": "3_decoupe.md:39-40",
    "DEC-1": "3_decoupe.md:51-55",
    "DEC-2": "3_decoupe.md:57-61",
    "DEC-3": "3_decoupe.md:47-49",
    "DEC-4": "3_decoupe.md:87-90 · 3_decoupe.md:113-115",
    "DEC-5": "3_decoupe.md:66-69 · 3a_genre.md:72-75 · 3b_nature.md:71-75 · 4_grille.md:266-269",
    "DEC-6": "3_decoupe.md:66-69",
    "DEC-7": "3_decoupe.md:66-69 · agents/redacteur.md:275",
    "DEC-9": "aucune règle : le fichier d'un agent hors du tour",
    "GEN-1": "3a_genre.md:49-53",
    "GEN-2": "3a_genre.md:55-58",
    "GEN-3": "3a_genre.md:109-115 · 2_structure.md:119",
    "GEN-4": "3a_genre.md:127-130",
    "GEN-5": "3b_nature.md:71-75 · 4_grille.md:266-269 · agents/qualifieur.md:3",
    "GEN-6": "3_decoupe.md:66-69",
    "GEN-7": "3_decoupe.md:66-69",
    "GEN-8": "3a_genre.md:114",
    "GEN-9": "aucune règle : le fichier d'un agent hors du tour",
    "GEN-10": "3a_genre.md:117-120 · 3a_genre.md:40",
    "NAT-1": "3b_nature.md:48-51",
    "NAT-2": "3b_nature.md:54-57",
    "NAT-3": "3b_nature.md:113 · 2_structure.md:119",
    "NAT-4": "3b_nature.md:129-130",
    "NAT-5": "4_grille.md:266-269 · agents/classeur.md:3",
    "NAT-6": "3a_genre.md:72-75",
    "NAT-7": "3_decoupe.md:66-69",
    "NAT-8": "3b_nature.md:113-115",
    "NAT-9": "aucune règle : le fichier d'un agent hors du tour",
    "NAT-10": "3b_nature.md:118 · 3b_nature.md:38-40",
    "GRI-0": "4_grille.md:126-132 · 2_structure.md:119",
    "GRI-1": "4_grille.md:81-85",
    "GRI-2": "4_grille.md:94-98",
    "GRI-4": "5_reclasse.md:50-68 · 4_grille.md:356-357",
    "GRI-5": "4_grille.md:134-140",
    "GRI-6": "4_grille.md:193-201",
    "REC-1": "5_reclasse.md:50-68",
    "REC-2": "5_reclasse.md:74-76",
    "REC-3": "5_reclasse.md:78-81",
    "REC-4": "5_reclasse.md:86-90",
    "REC-5": "6_convertit.md:41-46",
    "REC-6": "5_reclasse.md:136-139 · 5_reclasse.md:149-152",
    "REC-7": "5_reclasse.md:119-139 · 5_reclasse.md:158",
    "CNV-2": "6_convertit.md:41-46",
    "CNV-3": "6_convertit.md:62-66",
    "CNV-4": "6_convertit.md:85-95",
    "CNV-5": "6_convertit.md:114-118",
    "CNV-6": "6_convertit.md:119",
    "CON-1": "conventions.md:63-64",
    "CON-2": "conventions.md:79",
    "CON-3": "conventions.md:80",
    "CON-4": "conventions.md:83",
    "CON-5": "conventions.md:84",
    "CON-6": "conventions.md:85",
    "CON-7": "conventions.md:86-88",
    "LOT-1": "7_lots.md:22-23 · 7_lots.md:58-66",
    "LOT-2": "7_lots.md:72-78",
    "LOT-3": "7_lots.md:207",
    "LOT-4": "7_lots.md:143",
    "LOT-5": "7_lots.md:140",
    "LOT-6": "7_lots.md:241-250",
    "LOT-7": "7_lots.md:208",
    "LOT-8": "8_code.md:92-93 · 7_lots.md:142",
    "LOT-9": "7_lots.md:141",
    "COD-1": "8_code.md:80-83",
    "COD-2": "8_code.md:92-100",
    "COD-3": "8_code.md:297-299",
    "COD-5": "8_code.md:85-87",
    "COD-6": "8_code.md:80-83",
    "CTL-1": "9_controle.md:75-77",
    "CTL-3": "9_controle.md:488-495 · 9_controle.md:509-510",
    "CTL-4": "9_controle.md:488-495",
    "TST-1": "fusion.md:59",
    "TST-2": "9_controle.md:509-513",
    "TST-3": "9_controle.md:512-513",
    "TST-4": "9_controle.md:509-513",
    "FUS-1": "fusion.md:56",
    "FUS-2": "fusion.md:59",
    "FUS-3": "fusion.md:61-66",
    "DIA-1": "diagnostique.md:21-25",
    "DIA-2": "diagnostique.md:75-77 · diagnostique.md:228",
    "DIA-3": "diagnostique.md:60-67",
}


@dataclass
class Why:
    rule: str
    text: str
    files: list = field(default_factory=list)
    cite: str = ""

    def __post_init__(self):
        self.cite = self.cite or RULES.get(self.rule, "")


@dataclass
class Step:
    id: str
    command: str | None
    name: str
    state: str = INCONNU
    why: list = field(default_factory=list)
    lots: dict | None = None
    waiting: list = field(default_factory=list)   # ids of the open entries it owns
    confirm: str | None = None
    note: str | None = None

    def to_dict(self):
        return asdict(self)


# ------------------------------------------------------------ the folder

class Folder:
    """A cached, read-only view of one feature or bug-fix folder."""

    def __init__(self, path, feature_path=None):
        self.path = path
        self.feature = feature_path or path
        self._lines = {}
        try:
            self.names = sorted(os.listdir(path))
        except OSError:
            self.names = []

    def p(self, *rel):
        return os.path.join(self.path, *rel)

    def rel(self, path):
        return os.path.relpath(path, self.feature).replace(os.sep, "/")

    def has(self, *rel):
        return os.path.exists(self.p(*rel))

    def lines(self, path):
        if path not in self._lines:
            try:
                self._lines[path] = textfile.load(path).lines
            except textfile.UnreadableFile:
                self._lines[path] = None
        return self._lines[path] or []

    def readable(self, path):
        self.lines(path)
        return self._lines.get(path) is not None

    def root_questions(self):
        """(agent, number, path) of every `questions-<agent>-NN.md` at the root."""
        out = []
        for n in self.names:
            m = ROOT_Q.match(n)
            if m and os.path.isfile(self.p(n)):
                out.append((m.group(1), int(m.group(2)), self.p(n)))
        return out

    def highest(self, agent):
        """The highest `questions-<agent>-NN.md`, at the root or filed under
        `questions/<agent>/` — the place both are globbed (cmd/4_grille.md:196-199)."""
        best = None
        for d in (self.path, self.p("questions", agent)):
            try:
                names = os.listdir(d)
            except OSError:
                continue
            for n in names:
                m = ROOT_Q.match(n)
                if m and m.group(1) == agent:
                    k = int(m.group(2))
                    if best is None or k > best[0]:
                        best = (k, os.path.join(d, n), d == self.path)
        return best      # (number, path, at_root) or None

    def highest_filed(self, agent):
        """The highest `questions-<agent>-NN.md` under `questions/<agent>/`
        alone (cmd/3a_genre.md:94-98)."""
        h = None
        try:
            names = os.listdir(self.p("questions", agent))
        except OSError:
            return None
        for n in names:
            m = ROOT_Q.match(n)
            if m and m.group(1) == agent and (h is None or int(m.group(2)) > h[0]):
                h = (int(m.group(2)), self.p("questions", agent, n))
        return h

    def holds_q(self, path):
        return any(Q_HEAD.match(l) for l in self.lines(path))

    def desc(self):
        return self.lines(self.p("desc-produit.md")) if self.has("desc-produit.md") else []


def unanswered(lines):
    """`^Answer:\\s*$` with no `Défaut:` above it in the same entry — the
    test of cmd/1_lexique.md:77-83."""
    out, cur, has_def, empty = [], None, False, False
    for l in lines + ["### Q-end"]:
        if Q_HEAD.match(l):
            if cur is not None and empty and not has_def:
                out.append(cur)
            cur, has_def, empty = l, False, False
        elif DEFAUT.match(l):
            has_def = True
        elif ANSWER_EMPTY.match(l):
            empty = True
    return out


def markers(lines):
    return [l for l in lines if MARKER_NEW.match(l) or MARKER_MOD.match(l)]


def behaviours_without_nature(lines):
    """`grep -B1 '^Nature:$'` kept to `Genre: comportement` (cmd/4_grille.md:94-98)."""
    return [lines[i - 2] if i >= 2 else "" for i, l in enumerate(lines)
            if l == "Nature:" and i >= 1 and lines[i - 1] == "Genre: comportement"]


def stale_natures(lines):
    """A `Nature: <x>` under a genre other than `comportement` (cmd/3b_nature.md:~118)."""
    return [i for i, l in enumerate(lines) if l.startswith("Nature: ") and i >= 1
            and lines[i - 1].startswith("Genre:") and lines[i - 1] != "Genre: comportement"]


def blocks(lines):
    """Each `### B` block, from its line to the next heading of any level
    (cmd/5_reclasse.md:136-137)."""
    out, cur = [], None
    for l in lines:
        if l.startswith("#"):
            if cur is not None:
                out.append(cur)
                cur = None
            if l.startswith("### B"):
                cur = [l]
            continue
        if cur is not None:
            cur.append(l.rstrip())
    if cur is not None:
        out.append(cur)
    norm = []
    for b in out:
        while b and not b[-1].strip():
            b = b[:-1]
        norm.append("\n".join(b))
    return norm


def section(lines, title):
    """Lines under `## <title>` up to the next `## `."""
    out, inside = [], False
    for l in lines:
        if l.startswith("## "):
            if inside:
                break
            inside = l[3:].strip() == title
            continue
        if inside:
            out.append(l)
    return out


def decision_filled(lines):
    """Every `## Decision` filled, by `grep -A2` (cmd/2_structure.md:151-153)."""
    idx = [i for i, l in enumerate(lines) if l == "## Decision"]
    return bool(idx) and not any(blocking.decision_empty_a2(lines, i) for i in idx)


def invocation_of(lines):
    for i, l in enumerate(lines):
        if l.strip() == "## Invocation":
            for nxt in lines[i + 1:]:
                if nxt.strip():
                    m = re.search(r"\d", nxt)
                    return int(m.group(0)) if m else None
    return None


# --------------------------------------------------------- open entries

def owner(rel, kind, lines):
    """The step an open entry belongs to: the command named after it in
    « answer …, then run X » (scan_rules.md, « À qui est une réponse »)."""
    name = rel.split("/")[-1]
    parts = rel.split("/")
    if kind == "technique":
        return "6_convertit", "OWN-TEC"
    if kind == "questions":
        m = ROOT_Q.match(name)
        agent = m.group(1) if m else ""
        if agent == "architecte":
            return "conventions", "OWN-ARC"
        if agent == "fusionneur":
            return "fusion", "OWN-FUS"
        return "1_lexique", "OWN-Q"
    # blocking files
    if kind == "redecoupage":
        return "7_lots", "OWN-RED"
    agent = blocking.agent_of(name) if name.startswith("blocked_") else ""
    if parts[0] == "cadrage-produit" or agent in ("existant", "assembleur"):
        return "4_grille", "OWN-GRI"
    if parts[0] == "convertisseur":
        return "6_convertit", "OWN-CNV"
    if parts[0] == "investigation" or agent == "diagnostiqueur":
        return "diagnostique", "OWN-DIA"
    if parts[0] == "code":
        if agent == "cadreur":
            return "7_lots", "OWN-CAD"
        return "8_code", "OWN-COD"
    if agent == "lexicographe":
        return "1_lexique", "OWN-LEX"
    if agent == "redacteur":
        return ("fusion", "OWN-RE3") if invocation_of(lines) == 3 else ("2_structure", "OWN-RED1")
    if agent == "decoupeur":
        return "2_structure", "OWN-DEC"
    if agent == "qualifieur":
        return "3a_genre", "OWN-GEN"
    if agent == "classeur":
        return "3b_nature", "OWN-NAT"
    if agent == "architecte":
        return ("8_code", "OWN-AR3") if invocation_of(lines) == 3 else ("conventions", "OWN-ARB")
    if agent == "fusionneur":
        return "fusion", "OWN-FUB"
    return None, "OWN-?"


@dataclass
class Open:
    id: str
    rel: str          # relative to the feature folder
    kind: str         # questions, technique, blocking, redecoupage
    step: str | None
    rule: str
    label: str


def open_entries(folder: Folder, work_dir: str, prefix: str = ""):
    """The entries the Product Owner still has to answer, by the commands'
    own tests, and the files that could not be read. The same parsers as the
    « À répondre » form."""
    out, errors = [], []
    qs, qerr = questions.scan(work_dir)
    for q in qs:
        if not q.open:
            continue
        rel = prefix + q.rel
        step, rule = owner(q.rel, q.kind, [])
        out.append(Open(q.id if not prefix else q.id.replace("q:", "q:" + prefix, 1),
                        rel, q.kind, step, rule, f"{rel} · Q{q.number}"))
    bs, notices, redec = blocking.scan(work_dir)
    for b in bs:
        rel = prefix + b.rel
        step, rule = owner(b.rel, "blocking", folder.lines(b.file))
        out.append(Open(b.id if not prefix else b.id.replace("b:", "b:" + prefix, 1),
                        rel, "blocking", step, rule,
                        rel + (f" · Blocking {b.number}" if b.number is not None else "")))
    if redec:
        out.append(Open(redec.id if not prefix else redec.id.replace("r:", "r:" + prefix, 1),
                        prefix + redec.rel, "redecoupage", "7_lots", "OWN-RED",
                        prefix + redec.rel))
    for e in list(qerr) + [n for n in notices if n.level == "error"]:
        rel = e.rel
        kind = "technique" if rel.startswith("convertisseur/technique-") else (
            "questions" if rel.split("/")[-1].startswith("questions-") else "blocking")
        step, rule = owner(rel, kind, folder.lines(e.file))
        errors.append({"rel": prefix + rel, "message": e.message, "step": step})
    return out, errors


# ------------------------------------------------------------ the scan

class Scan:
    def __init__(self, app, feature):
        self.app = app
        self.feature = feature
        self.fpath = os.path.join(app, "docs", "features", feature)
        self.F = Folder(self.fpath)
        self.bugfixes = sorted((n for n in self.F.names if BUGFIX.match(n)
                                and os.path.isdir(self.F.p(n))),
                               key=lambda n: int(BUGFIX.match(n).group(1)))

    # -- helpers on the feature folder -----------------------------------
    def root_files(self, folder=None):
        """Root questions files other than the architecte's — the root « as
        if it were not there » (cmd/1_lexique.md:68-71)."""
        F = folder or self.F
        return [(a, n, p) for (a, n, p) in F.root_questions() if a != "architecte"]

    def clarification(self):
        return any("Clarification needed" in l for l in self.F.desc())

    def root_q_files(self):
        return [self.F.rel(p) for (a, n, p) in self.root_files() if self.F.holds_q(p)]

    def sondeur_anywhere(self):
        return self.F.highest("sondeur") is not None

    def grid_closed(self):
        """cmd/5_reclasse.md:51-70 — the highest sondeur and existant files
        each present and holding no `### Q`, and no marker on a heading."""
        s, e = self.F.highest("sondeur"), self.F.highest("existant")
        ok = s and e and not self.F.holds_q(s[1]) and not self.F.holds_q(e[1]) and not markers(self.F.desc())
        files = [self.F.rel(x[1]) for x in (s, e) if x]
        return bool(ok), files

    def token(self, later):
        """The root files that hold no `### Q`, split by whether their agent
        writes after the step (`later`) or before it."""
        agents = {a for (a, n, p) in self.root_files() if not self.F.holds_q(p)}
        files = [self.F.rel(p) for (a, n, p) in self.root_files() if not self.F.holds_q(p)]
        return agents, files

    # -- the main chain ---------------------------------------------------
    def eval_main(self, opens):
        F = self.F
        steps = []
        cut = F.has("code", "decoupage.md")
        for d in MAIN:
            s = Step(d.id, d.command, d.name, confirm=CONFIRM.get(d.command))
            mine = [o for o in opens if o.step == d.id and not o.rel.startswith("bugfix-")]
            if mine:
                s.state = ATTEND
                s.waiting = [o.id for o in mine]
                s.why.append(Why("G-ATT", f"{len(mine)} réponse(s) attendue(s) qui reviennent à cette étape.",
                                 sorted({o.rel for o in mine})))
            elif cut and d.id in UPSTREAM:
                s.state = FAITE
                s.why.append(Why("G-AMONT", "Le découpage en lots existe : un changement du produit appartient "
                                 "désormais à un nouveau cycle.", ["code/decoupage.md"]))
            else:
                getattr(self, "m_" + d.id)(s)
            steps.append(s)
        return steps

    def m_1_lexique(self, s):
        F = self.F
        has_desc = F.has("desc-produit.md")
        L = [(a, n, p) for (a, n, p) in self.root_files() if a == "lexicographe"]
        O = [(a, n, p) for (a, n, p) in self.root_files() if a != "lexicographe"]
        rel = lambda xs: [F.rel(p) for (_, _, p) in xs]
        if len(O) >= 2 or len(L) >= 2:
            return self.set(s, BLOQUEE, "LEX-6", "Plusieurs fichiers de questions à la racine : un rangement a échoué.", rel(O + L))
        if not O:
            if not L:
                if has_desc:
                    return self.set(s, FAITE, "LEX-1", "desc-produit.md existe : le vocabulaire est fixé, la fiche est écrite.", ["desc-produit.md"])
                return self.set(s, A_FAIRE, "LEX-2", "Aucun fichier de questions à la racine : invocation 1, le balayage.", ["idees.md"])
            if not F.holds_q(L[0][2]):
                return self.set(s, FAITE, "LEX-3", "Le fichier du lexicographe à la racine ne pose aucune question : la boucle est finie.", rel(L))
            if has_desc:
                return self.set(s, FAITE, "LEX-1", "desc-produit.md existe : les invocations 1 et 2 s'arrêtent.", ["desc-produit.md"])
            return self.set(s, A_FAIRE, "LEX-4", "Le fichier du lexicographe est répondu : invocation 2, l'application des réponses.", rel(L))
        if not L:
            if F.holds_q(O[0][2]):
                return self.set(s, A_FAIRE, "LEX-5", "Un fichier répondu d'un autre agent attend : invocation 3, la veille.", rel(O))
            return self.set(s, FAITE, "LEX-7", "Le fichier d'un autre agent ne pose aucune question : rien à veiller.", rel(O))
        if not F.holds_q(L[0][2]):
            return self.set(s, FAITE, "LEX-8", "La veille n'a rien demandé : rien à corriger.", rel(L + O))
        return self.set(s, A_FAIRE, "LEX-9", "La veille a posé des questions, répondues : invocation 4, la correction.", rel(L + O))

    def m_2_structure(self, s):
        F = self.F
        L = [(a, n, p) for (a, n, p) in self.root_files() if a == "lexicographe"]
        if L and F.holds_q(L[0][2]):
            return self.set(s, A_FAIRE, "STR-1", "Le fichier du lexicographe à la racine tient encore des questions : /1_lexique d'abord.", [F.rel(L[0][2])])
        bred = F.p("blocked_redacteur.md")
        if os.path.isfile(bred) and invocation_of(F.lines(bred)) != 3 and decision_filled(F.lines(bred)):
            return self.set(s, A_FAIRE, "STR-2", "blocked_redacteur.md a sa décision : le Rédacteur l'applique.", ["blocked_redacteur.md"])
        R = [(a, n, p) for (a, n, p) in self.root_files() if not (a == "lexicographe" and not F.holds_q(p))]
        if len(R) > 1:
            return self.set(s, BLOQUEE, "STR-3", "Plus d'un fichier de questions à la racine : un rangement a échoué.", [F.rel(p) for (_, _, p) in R])
        if R and F.holds_q(R[0][2]):
            return self.set(s, A_FAIRE, "STR-4", "Un fichier de questions répondu attend d'être intégré (invocation 2).", [F.rel(R[0][2])])
        for name in ("blocked_decoupeur.md", "blocked_qualifieur.md", "blocked_classeur.md"):
            p = F.p(name)
            if os.path.isfile(p) and decision_filled(F.lines(p)):
                return self.set(s, A_FAIRE, "STR-5", f"{name} a toutes ses décisions : la réécriture est au Rédacteur.", [name])
        if R:
            return self.set(s, FAITE, "STR-6", "Le fichier de questions à la racine ne pose rien : rien à intégrer.", [F.rel(R[0][2])])
        if not F.has("desc-produit.md"):
            return self.set(s, A_FAIRE, "STR-7", "Ni fichier de questions ni desc-produit.md : invocation 1, la structuration.", ["idees.md"])
        if self.clarification():
            return self.set(s, BLOQUEE, "STR-8", "« Clarification needed » reste dans desc-produit.md sans fichier de questions pour le lever.", ["desc-produit.md"])
        return self.set(s, FAITE, "STR-9", "desc-produit.md existe et rien n'attend d'intégration.", ["desc-produit.md"])

    def _upstream_guards(self, s, prefix):
        """The guards 3_decoupe, 3a_genre and 3b_nature share: the flag, and
        a root file holding questions."""
        if self.clarification():
            return self.set(s, A_FAIRE, prefix + "-1", "« Clarification needed » dans desc-produit.md : /2_structure d'abord.", ["desc-produit.md"])
        held = self.root_q_files()
        if held:
            return self.set(s, A_FAIRE, prefix + "-2", "Un fichier de questions à la racine attend une réponse ou une intégration : la commande s'arrêterait.", held)
        return None

    def m_3_decoupe(self, s):
        F = self.F
        if F.has("blocked_decoupeur.md"):
            return self.set(s, A_FAIRE, "DEC-0", "blocked_decoupeur.md est à /2_structure, qui doit passer d'abord.", ["blocked_decoupeur.md"])
        if self._upstream_guards(s, "DEC"):
            return s
        if not F.has("desc-produit.md"):
            return self.set(s, A_FAIRE, "DEC-3", "desc-produit.md absent : /2_structure n'a pas tourné.", [])
        mk = markers(F.desc())
        if self.sondeur_anywhere() and not mk:
            return self.set(s, FAITE, "DEC-4", "La grille a tourné et aucun bloc ne porte NEW ni MODIFIED : rien à découper.", ["desc-produit.md"])
        return self._turn(s, "DEC", AFTER_DEC, BEFORE_DEC, "le découpeur")

    def _turn(self, s, prefix, later, before, who):
        """Where the turn stands, from the one file the root holds: each
        command of the turn files every root file before its agent writes
        its own there (scan_rules.md, « Le tour »)."""
        agents, files = self.token(later)
        if agents & later:
            return self.set(s, FAITE, prefix + "-5", f"Un fichier écrit après {who} est à la racine : il a tourné sur ce tour.", files)
        if agents & before:
            return self.set(s, A_FAIRE, prefix + "-6", f"Le fichier à la racine précède {who} : il n'a pas encore tourné sur ce tour.", files)
        if not agents:
            if prefix == "DEC":
                return self.set(s, FAITE, prefix + "-7", "La racine est vide : /3_decoupe a rangé le fichier du Rédacteur, il a tourné.", [])
            return self.set(s, A_FAIRE, prefix + "-7", f"La racine est vide : /3_decoupe a tourné, pas encore {who}.", [])
        return self.set(s, INCONNU, prefix + "-9", "Le fichier à la racine ne dit pas où en est le tour.", files)

    def m_3a_genre(self, s):
        lines = self.F.desc()
        empty = sum(1 for l in lines if l == "Genre:")
        return self._classify(s, "GEN", "qualifieur", "blocked_qualifieur.md", empty,
                              f"{empty} bloc(s) sans genre.",
                              "Aucun Genre: vide, aucun MODIFIED, aucune réponse à appliquer : rien à qualifier.",
                              AFTER_GEN, BEFORE_GEN, "le qualifieur")

    def m_3b_nature(self, s):
        lines = self.F.desc()
        empty = len(behaviours_without_nature(lines)) + len(stale_natures(lines))
        return self._classify(s, "NAT", "classeur", "blocked_classeur.md", empty,
                              f"{empty} bloc(s) dont la nature est à donner ou à vider.",
                              "Chaque comportement a sa nature, aucun MODIFIED, aucune réponse à appliquer : rien à classer.",
                              AFTER_NAT, BEFORE_NAT, "le classeur")

    def _classify(self, s, prefix, agent, blocked, empty, empty_text, none_text, after, before, who):
        """3a_genre and 3b_nature: the same three triggers — an empty line,
        a MODIFIED block, the answered file filed last turn — and the same
        « do not invoke » when none fires (3a_genre.md:107-130,
        3b_nature.md:~105-130)."""
        F = self.F
        if self._upstream_guards(s, prefix):
            return s
        if not F.has("desc-produit.md"):
            return self.set(s, A_FAIRE, prefix + "-3", "desc-produit.md absent : /2_structure n'a pas tourné.", [])
        if empty:
            return self.set(s, A_FAIRE, prefix + "-8", empty_text, ["desc-produit.md"])
        mod = [l for l in F.desc() if MARKER_MOD.match(l)]
        h = F.highest_filed(agent)
        answered = bool(h) and F.holds_q(h[1])
        filled = F.has(blocked)
        if not mod and not answered and not filled:
            return self.set(s, FAITE, prefix + "-4", none_text, ["desc-produit.md"])
        agents, files = self.token(after)
        if agents & after:
            return self.set(s, FAITE, prefix + "-5", f"Un fichier écrit par {who} ou après lui est à la racine : il a tourné sur ce tour.", files)
        if answered or filled:
            files = ([F.rel(h[1])] if answered else []) + ([blocked] if filled else [])
            return self.set(s, A_FAIRE, prefix + "-10", f"Des réponses ou une décision attendent {who}.", files)
        return self._turn(s, prefix, after, before, who)

    def m_4_grille(self, s):
        F = self.F
        if not F.has("desc-produit.md"):
            return self.set(s, A_FAIRE, "GRI-0", "desc-produit.md absent.", [])
        if self.clarification():
            return self.set(s, A_FAIRE, "GRI-1", "« Clarification needed » dans desc-produit.md : /2_structure d'abord.", ["desc-produit.md"])
        lines = F.desc()
        if behaviours_without_nature(lines):
            return self.set(s, A_FAIRE, "GRI-2", "Un comportement n'a pas de nature : /3b_nature d'abord.", ["desc-produit.md"])
        closed, files = self.grid_closed()
        if closed:
            return self.set(s, FAITE, "GRI-4", "La grille est close : derniers fichiers sondeur et existant vides, aucun marqueur.", files + ["desc-produit.md"])
        if not self.sondeur_anywhere() and not any(l == "Genre: comportement" for l in lines):
            return self.set(s, BLOQUEE, "GRI-5", "Aucun bloc de comportement : rien que la grille puisse sonder.", ["desc-produit.md"])
        return self.set(s, A_FAIRE, "GRI-6", "La grille n'est pas close.", files + ["desc-produit.md"])

    def m_5_reclasse(self, s):
        F = self.F
        closed, files = self.grid_closed()
        if not closed:
            return self.set(s, A_FAIRE, "REC-1", "La grille n'est pas close : /4_grille d'abord.", files)
        lines = F.desc()
        if any(l == "Genre:" for l in lines):
            return self.set(s, A_FAIRE, "REC-2", "Un bloc n'a pas de genre : /3a_genre d'abord.", ["desc-produit.md"])
        if behaviours_without_nature(lines):
            return self.set(s, A_FAIRE, "REC-3", "Un comportement n'a pas de nature : /3b_nature d'abord.", ["desc-produit.md"])
        held = self.root_q_files()
        if held:
            return self.set(s, A_FAIRE, "REC-4", "Un fichier de questions à la racine attend : la commande s'arrêterait.", held)
        views = [F.p("par-genre", g + ".md") for g in GENRE_FILES]
        if not all(os.path.isfile(v) for v in views) or not F.has("desc-par-nature.md"):
            return self.set(s, A_FAIRE, "REC-5", "Les vues par genre ou par nature n'existent pas.", ["par-genre/", "desc-par-nature.md"])
        mine = sorted(blocks(lines))
        theirs = sorted(b for v in views for b in blocks(F.lines(v)))
        if mine != theirs:
            return self.set(s, A_FAIRE, "REC-6", "Les vues par genre ne recopient plus desc-produit.md : un bloc a changé depuis.", ["desc-produit.md", "par-genre/"])
        return self.set(s, FAITE, "REC-7", "Les vues par genre recopient chaque bloc de desc-produit.md, et desc-par-nature.md existe.", ["par-genre/", "desc-par-nature.md"])

    def m_6_convertit(self, s):
        F = self.F
        if not F.has("par-genre") or not F.has("desc-par-nature.md"):
            return self.set(s, A_FAIRE, "CNV-2", "par-genre/ ou desc-par-nature.md absent : /5_reclasse d'abord.", [])
        held = self.root_q_files()
        if held:
            return self.set(s, A_FAIRE, "CNV-3", "Un fichier de questions à la racine attend : la commande s'arrêterait.", held)
        dpn = F.lines(F.p("desc-par-nature.md"))
        runs, files = [], []
        for nat in NATURES:
            n = nat.replace(" ", "-")
            part = section(dpn, nat)
            has_block = any(l.startswith("### B") for l in part)
            base = F.p("convertisseur", n)
            own = [base + ".md", base + "-input.md", base + "-notes.md"]
            if not has_block:
                if any(os.path.isfile(x) for x in own):
                    runs.append(f"{nat} (ses fichiers sont à supprimer)")
                continue
            inp = base + "-input.md"
            same = os.path.isfile(inp) and _norm(part) == _norm(F.lines(inp))
            tech = F.p("convertisseur", f"technique-{n}.md")
            tech_lines = F.lines(tech) if os.path.isfile(tech) else []
            tech_answered = bool(tech_lines) and any(Q_HEAD.match(l) for l in tech_lines) and not any(ANSWER_EMPTY.match(l) for l in tech_lines)
            md = base + ".md"
            assumed = not os.path.isfile(md) or any("<<ASSUMED" in l for l in F.lines(md))
            blk = F.p("convertisseur", f"blocked_{n}.md")
            if not same:
                runs.append(nat)
                files.append(F.rel(inp))
            elif tech_answered:
                runs.append(nat)
                files.append(F.rel(tech))
            elif assumed and not any(ANSWER_EMPTY.match(l) for l in tech_lines):
                runs.append(nat)
                files.append(F.rel(md))
            elif os.path.isfile(blk) and decision_filled(F.lines(blk)):
                runs.append(nat)
                files.append(F.rel(blk))
        if runs:
            return self.set(s, A_FAIRE, "CNV-4", "Des natures sont à (ré)écrire : " + ", ".join(runs) + ".", files or ["desc-par-nature.md"])
        spec = F.lines(F.p("spec-technique.md")) if F.has("spec-technique.md") else []
        first = next((l.strip() for l in spec if l.strip()), "")
        tt = F.p("convertisseur", "technique-transversal.md")
        bt = F.p("convertisseur", "blocked_transversal.md")
        stands = (spec and first == "# Preamble" and not any("<<ASSUMED" in l for l in spec)
                  and not any("[B" in l for l in spec) and F.has("tracabilite.md")
                  and (not os.path.isfile(tt) or any(ANSWER_EMPTY.match(l) for l in F.lines(tt)))
                  and not (os.path.isfile(bt) and decision_filled(F.lines(bt))))
        if stands:
            return self.set(s, FAITE, "CNV-5", "Aucune nature à écrire et le document tient : préambule, aucun <<ASSUMED ni [B, tracabilite.md présent.", ["spec-technique.md", "tracabilite.md"])
        return self.set(s, A_FAIRE, "CNV-6", "Le document est à assembler de nouveau autour de ce qui tient.", ["spec-technique.md"])

    def m_conventions(self, s):
        F = self.F
        if not F.has("spec-technique.md"):
            return self.set(s, A_FAIRE, "CON-1", "spec-technique.md absent : la conversion n'est pas arrivée là.", [])
        b = F.p("blocked_architecte.md")
        if os.path.isfile(b) and invocation_of(F.lines(b)) != 3:
            return self.set(s, A_FAIRE, "CON-2", "blocked_architecte.md a sa décision : l'Architecte l'applique.", ["blocked_architecte.md"])
        req = pending_requests(F)
        if req:
            return self.set(s, A_FAIRE, "CON-3", "Une demande à l'Architecte attend son verdict (invocation 3).", req)
        arch = [(n, p) for (a, n, p) in F.root_questions() if a == "architecte" and F.holds_q(p)]
        if arch:
            return self.set(s, A_FAIRE, "CON-4", "Un fichier de questions de l'Architecte répondu attend d'être intégré.", [F.rel(arch[-1][1])])
        if not os.path.isfile(os.path.join(self.app, "docs", "TECHNICAL_CONVENTIONS.md")):
            return self.set(s, A_FAIRE, "CON-5", "docs/TECHNICAL_CONVENTIONS.md n'existe pas : invocation 1.", [])
        if not F.has("couverture.md"):
            return self.set(s, A_FAIRE, "CON-6", "Pas de couverture.md : la feature n'a pas été parcourue (invocation 4).", [])
        return self.set(s, FAITE, "CON-7", "Les conventions existent et couverture.md est là.", ["couverture.md"])

    def m_7_lots(self, s, W=None, doc="spec-technique.md"):
        W = W or self.F
        r = lambda *x: self.F.rel(W.p(*x))
        if not W.has(doc):
            return self.set(s, A_FAIRE, "LOT-1", f"{doc} absent : rien à découper encore.", [])
        if doc == "spec-technique.md" and not any(l.startswith("### §") for l in W.lines(W.p(doc))):
            return self.set(s, FAITE, "LOT-2", "spec-technique.md ne porte aucune entrée ### § : rien à construire, /fusion ensuite.", [r(doc)])
        if W.has("code", "blocked_verificateur.md"):
            return self.set(s, BLOQUEE, "LOT-3", "code/blocked_verificateur.md : une entrée manquait au Vérificateur ; l'étape d'avant doit repasser.", [r("code", "blocked_verificateur.md")])
        if W.has("code", "redecoupage.md"):
            return self.set(s, A_FAIRE, "LOT-4", "code/redecoupage.md : le codage a renvoyé le découpage.", [r("code", "redecoupage.md")])
        if W.has("code", "blocked_cadreur.md"):
            return self.set(s, A_FAIRE, "LOT-5", "code/blocked_cadreur.md a sa décision : le Cadreur l'applique.", [r("code", "blocked_cadreur.md")])
        if not (W.has("code", "decoupage.md") and W.has("code", "sequence.md")):
            return self.set(s, A_FAIRE, "LOT-9", "Pas encore de découpage.", [])
        seq = W.lines(W.p("code", "sequence.md"))
        if any(l.strip() for l in section(seq, "Defects")):
            return self.set(s, A_FAIRE, "LOT-8", "code/sequence.md porte des défauts : le découpage est à corriger.", [r("code", "sequence.md")])
        req = pending_requests(W)
        if req:
            return self.set(s, A_FAIRE, "LOT-6", "Le découpage tient, mais une demande à l'Architecte attend son verdict.", [self.F.rel(W.p(x)) for x in req])
        return self.set(s, FAITE, "LOT-7", "Le découpage tient : code/sequence.md, ## Defects vide.", [r("code", "decoupage.md"), r("code", "sequence.md")])

    def m_8_code(self, s, W=None):
        W = W or self.F
        r = lambda *x: self.F.rel(W.p(*x))
        if not W.has("code", "sequence.md"):
            return self.set(s, A_FAIRE, "COD-1", "Pas de code/sequence.md : /7_lots d'abord.", [])
        seq = W.lines(W.p("code", "sequence.md"))
        if any(l.strip() for l in section(seq, "Defects")) or W.has("code", "blocked_verificateur.md"):
            return self.set(s, A_FAIRE, "COD-2", "Le découpage n'a jamais été corrigé : /7_lots d'abord.", [r("code", "sequence.md")])
        order = re.findall(r"\blot-[A-Za-z0-9]+\b", "\n".join(section(seq, "Order")))
        done, failed = 0, []
        for lot in order:
            v = W.p("code", lot, "verdict.md")
            vl = W.lines(v) if os.path.isfile(v) else []
            if first_after(vl, "## Status").startswith("PASS"):
                done += 1
            elif vl:
                try:
                    att = int(re.match(r"\d+", first_after(vl, "## Attempts") or "1").group(0))
                except (AttributeError, ValueError):
                    att = 1
                if att >= 3:
                    failed.append(lot)
        s.lots = {"pass": done, "total": len(order)}
        if failed:
            return self.set(s, BLOQUEE, "COD-3", f"{failed[0]} a échoué trois fois : le lot est au Product Owner.", [r("code", failed[0], "verdict.md")])
        if order and done == len(order):
            return self.set(s, FAITE, "COD-5", f"{done} / {len(order)} lots en PASS.", [r("code", "sequence.md")])
        return self.set(s, A_FAIRE, "COD-6", f"{done} / {len(order)} lots en PASS.", [r("code", "sequence.md")])

    def m_9_controle(self, s, W=None):
        W = W or self.F
        F = self.F
        if not F.has("desc-produit.md"):
            return self.set(s, A_FAIRE, "CTL-1", "desc-produit.md absent : rien à confronter encore.", [])
        # 9_controle.md:488-495 — the four files a run writes.
        four = [F.rel(W.p("code", "recette-ordonnee.md")), F.rel(W.p("code", "decisions-produit.md")), "registre-questions.md"]
        have = [x for x in four if os.path.isfile(os.path.join(self.fpath, *x.split("/")))]
        reports = [n for n in (os.listdir(F.p("code")) if F.has("code") else []) if re.match(r"^rapport-controle.*\.md$", n)]
        if len(have) == 3 and reports:
            return self.set(s, FAITE, "CTL-3", "Les quatre fichiers d'un contrôle sont là.", have + ["code/" + sorted(reports)[-1]])
        return self.set(s, A_FAIRE, "CTL-4", "Les quatre fichiers d'un contrôle ne sont pas tous là.", have + (["code/" + sorted(reports)[-1]] if reports else []))

    def m_test(self, s):
        if self.F.has("rapport-fusion.md"):
            return self.set(s, FAITE, "TST-1", "La fusion est faite.", ["rapport-fusion.md"])
        if self.bugfixes:
            hb = self.bugfixes[-1]
            if self._correction_done(hb):
                return self.set(s, A_FAIRE, "TST-2", f"La correction {hb} est contrôlée : à tester, puis décider d'une bug-list ou de /fusion.", [f"{hb}/code/recette-ordonnee.md"])
            return self.set(s, FAITE, "TST-3", f"{hb}/bug-list.md existe : le test a eu lieu et une correction est ouverte.", [f"{hb}/bug-list.md"])
        return self.set(s, A_FAIRE, "TST-4", "Après le contrôle : tester, puis décider d'une bug-list ou de /fusion.", ["code/recette-ordonnee.md"])

    def m_fusion(self, s):
        if not self.F.has("desc-produit.md"):
            return self.set(s, A_FAIRE, "FUS-1", "desc-produit.md absent : rien à fusionner encore.", [])
        if self.F.has("rapport-fusion.md"):
            return self.set(s, FAITE, "FUS-2", "rapport-fusion.md existe : la fusion est faite.", ["rapport-fusion.md"])
        return self.set(s, A_FAIRE, "FUS-3", "Pas de rapport-fusion.md.", [])

    # -- the correction chain ---------------------------------------------
    def _correction_done(self, name):
        steps = self.eval_correction(name, [])
        return all(st.state == FAITE for st in steps)

    def eval_correction(self, name, opens):
        W = Folder(self.F.p(name), self.fpath)
        out = []
        for d in CORRECTION:
            s = Step(d.id, d.command, d.name, confirm=CONFIRM.get(d.command))
            mine = [o for o in opens if o.step == d.id and o.rel.startswith(name + "/")]
            if mine:
                s.state = ATTEND
                s.waiting = [o.id for o in mine]
                s.why.append(Why("G-ATT", f"{len(mine)} réponse(s) attendue(s) qui reviennent à cette étape.",
                                 sorted({o.rel for o in mine})))
            elif d.id == "diagnostique":
                self.c_diagnostique(s, W, name)
            elif d.id == "7_lots":
                self.m_7_lots(s, W, "desc-bug.md")
            elif d.id == "8_code":
                self.m_8_code(s, W)
            else:
                self.m_9_controle(s, W)
            if d.id == "8_code" and s.lots is None:
                tmp = Step("x", None, "")
                self.m_8_code(tmp, W)
                s.lots = tmp.lots
            out.append(s)
        return out

    def c_diagnostique(self, s, W, name):
        if not W.has("bug-list.md"):
            return self.set(s, A_FAIRE, "DIA-1", "bug-list.md absent : à écrire.", [])
        if not any(l.strip() for l in W.lines(W.p("bug-list.md"))):
            return self.set(s, A_FAIRE, "DIA-1", "bug-list.md est encore vide : les écarts sont à écrire.", [f"{name}/bug-list.md"])
        if W.has("desc-bug.md"):
            return self.set(s, FAITE, "DIA-2", "desc-bug.md existe : le diagnostic est fait.", [f"{name}/desc-bug.md"])
        return self.set(s, A_FAIRE, "DIA-3", "bug-list.md est écrit, pas encore de desc-bug.md.", [f"{name}/bug-list.md"])

    # -- shared ------------------------------------------------------------
    @staticmethod
    def set(s, state, rule, text, files):
        s.state = state
        s.why.append(Why(rule, text, list(files)))
        return s


UPSTREAM = ("1_lexique", "2_structure", "3_decoupe", "3a_genre", "3b_nature",
            "4_grille", "5_reclasse", "6_convertit")


def _norm(lines):
    return "\n".join(l.rstrip() for l in lines).strip()


def first_after(lines, heading):
    for i, l in enumerate(lines):
        if l.strip() == heading:
            for n in lines[i + 1:]:
                if n.strip():
                    return n.strip() if not n.startswith("#") else ""
    return ""


def pending_requests(W: Folder):
    """A request in `architecte/` with an empty `## Verdict`, or none at all
    (cmd/conventions.md:80, cmd/7_lots.md:229-234). A file holding several
    `# Request N` is read request by request."""
    out = []
    d = W.p("architecte")
    if not os.path.isdir(d):
        return out
    for n in sorted(os.listdir(d)):
        p = os.path.join(d, n)
        if not n.endswith(".md") or not os.path.isfile(p):
            continue
        lines = W.lines(p)
        starts = [i for i, l in enumerate(lines) if re.match(r"^# Request \d+", l)] or [0]
        for k, a in enumerate(starts):
            b = starts[k + 1] if k + 1 < len(starts) else len(lines)
            part = lines[a:b]
            idx = [i for i, l in enumerate(part) if l.strip() == "## Verdict"]
            if not idx or blocking.decision_empty_a2(part, idx[-1]):
                out.append(W.rel(p))
                break
    return out


# ---------------------------------------------------------------- entry

def step_of_command(command):
    for d in MAIN + CORRECTION:
        if command in d.commands:
            return d.id
    return None


def run_scan(app, feature, run=None):
    """The whole picture of one feature: the main chain, every correction
    chain, the open entries, the alerts. `run` is the runner's snapshot of
    the run going, if any."""
    t0 = time.perf_counter()
    sc = Scan(app, feature)
    opens, errors = open_entries(sc.F, sc.fpath)
    hb = sc.bugfixes[-1] if sc.bugfixes else None
    old_opens = []
    for name in sc.bugfixes:
        o, e = open_entries(Folder(sc.F.p(name), sc.fpath), sc.F.p(name), prefix=name + "/")
        if name == hb:
            opens += o
            errors += e
        else:
            # Older correction cycles: read for their own flow, never answered
            # here — the commands look at the highest alone (cmd/7_lots.md:19-21).
            old_opens.extend(o)
    main = sc.eval_main(opens)
    corrections = []
    for name in reversed(sc.bugfixes):
        o = opens if name == hb else old_opens
        corrections.append({"name": name, "highest": name == hb, "steps": sc.eval_correction(name, o)})

    # Superseded by a correction cycle: the commands' working folder is the
    # highest bugfix-NN/ (cmd/7_lots.md:19-21, 8_code.md:26-28, 9_controle.md:20-22),
    # and a bug-list is what follows a control (9_controle.md:511-513).
    if hb:
        for s in main:
            if s.id in ("7_lots", "8_code", "9_controle") and s.state in (A_FAIRE, INCONNU):
                s.state = FAITE
                s.why.append(Why("G-BUGFIX", f"Une correction est ouverte ({hb}) : la feature a été contrôlée, "
                                 f"et cette commande agit désormais sur {hb}.", [f"{hb}/bug-list.md"]))
            if s.id in ("7_lots", "8_code", "9_controle"):
                s.note = f"Agit sur {hb}, la correction la plus haute."

    # Downstream of a step not done, a step's own output is stale (§1.3,
    # « nothing upstream changed it since »). Past the split, the upstream
    # no longer reaches the code (cmd/6_convertit.md:35-38).
    cut = sc.F.has("code", "decoupage.md")
    _downgrade(main, stop_at="conventions" if cut else None)
    for c in corrections:
        _downgrade(c["steps"])

    alerts = []
    _running(main, corrections, run, feature)
    wt = os.path.join(app, ".claude", "worktrees", feature)
    if os.path.isdir(wt) and not (run and run.get("status") != "ended"):
        alerts.append({"rule": "G-WT", "text": f"Un worktree est resté : .claude/worktrees/{feature}. "
                       "Toute commande de la feature le recréerait et échouerait.", "files": [f".claude/worktrees/{feature}"]})
        for chain in [main] + [c["steps"] for c in corrections if c["highest"]]:
            _block_first(chain, Why("G-WT", "Un worktree est resté sur .claude/worktrees/" + feature + " : la commande échouerait à le recréer.",
                                    [f".claude/worktrees/{feature}"]))
    for e in errors:
        alerts.append({"rule": "G-ERR", "text": f"Fichier illisible : {e['rel']} — {e['message']}", "files": [e["rel"]]})
        target = corrections[0]["steps"] if hb and e["rel"].startswith(f"{hb}/") else main
        for s in target:
            if s.id == e["step"] and s.state != EN_COURS:
                s.state = BLOQUEE
                s.why.append(Why("G-ERR", f"{e['rel']} ne se lit pas : {e['message']}", [e["rel"]]))

    main_prop = proposal(main, "main")
    corr = corrections[0] if corrections else None
    corr_prop = proposal(corr["steps"], corr["name"]) if corr else None
    took = (time.perf_counter() - t0) * 1000
    unknown_owner = [o.rel for o in opens if o.step is None]
    return {
        "feature": feature,
        "main": [s.to_dict() for s in main],
        "corrections": [{"name": c["name"], "highest": c["highest"],
                         "steps": [s.to_dict() for s in c["steps"]],
                         "proposal": proposal(c["steps"], c["name"])} for c in corrections],
        "main_proposal": main_prop,
        "proposal": _overall(main_prop, corr_prop, corr),
        "opens": [asdict(o) for o in opens],
        "alerts": alerts,
        "unknown_owner": unknown_owner,
        "took_ms": round(took, 1),
    }


def _downgrade(steps, stop_at=None):
    behind = None
    for s in steps:
        if stop_at and s.id == stop_at:
            behind = None
        if behind and s.state == FAITE and not any(w.rule == "G-AMONT" for w in s.why):
            s.state = A_FAIRE
            s.why.append(Why("G-AVAL", f"Sortie présente, mais « {behind.name} » en amont n'est pas faite : elle est à refaire après.", []))
        if s.state != FAITE and behind is None:
            behind = s


def _running(main, corrections, run, feature):
    if not run or run.get("status") == "ended" or (run.get("work") or feature).split("/")[0] != feature:
        return
    sid = step_of_command(run.get("command"))
    if not sid:
        return
    hb = next((c for c in corrections if c["highest"]), None)
    in_corr = hb and (sid == "diagnostique" or sid in ("7_lots", "8_code", "9_controle"))
    chain = hb["steps"] if in_corr else main
    for s in chain:
        if s.id == sid:
            s.state = EN_COURS
            s.why.append(Why("G-RUN", f"{run.get('prompt')} tourne depuis {(run.get('started_at') or '')[11:16]}.", []))


def _block_first(chain, why):
    for s in chain:
        if s.state == EN_COURS:
            return
        if s.state != FAITE:
            s.state = BLOQUEE
            s.why.append(why)
            return


def proposal(steps, chain):
    """§1.4 — the first step, in chain order, not done. It is proposed when
    it is « t'attend » or « à faire »; a blocked or unknown step is shown and
    never stepped over."""
    for s in steps:
        if s.state == FAITE:
            continue
        return {"chain": chain, "step": s.id, "command": s.command, "name": s.name, "state": s.state,
                "proposable": s.state in (ATTEND, A_FAIRE)}
    return {"chain": chain, "step": None, "command": None, "name": None, "state": FAITE, "proposable": False}


def _overall(main_prop, corr_prop, corr):
    """The dashboard's proposal: the highest correction cycle while it is
    open — the commands act on it — else the main chain."""
    if corr and corr_prop and corr_prop["step"] is not None:
        return corr_prop
    return main_prop
