#!/usr/bin/env python3
"""
Balanced grouping with minimal cumulative reading.

Problem
-------
N blocks, each mapped to 0..k lots. Each lot is one fiche to read.
A group must read every lot touched by any of its blocks.
If a lot is touched by g different groups, that fiche is read g times.

    total reads = sum over lots of (number of groups touching it)
                = L + sum over lots of (lambda - 1)      [lambda-1 metric]

Goal: partition the blocks into G groups of similar size while keeping
total reads as close to L as possible (L = number of distinct lots).

Method
------
0. Model as a bipartite graph blocks x lots.
1. ATOMS   : connected components (union-find). Two blocks sharing a lot,
             directly or by chaining, are inseparable at zero cost.
2. BOUND   : total reads = L exactly iff every group is a union of atoms.
             That is the optimum; nothing can do better.
3. CAPACITY: with G groups, capacity = ceil(N / G).
             Zero-cost solution exists iff max atom size <= capacity,
             i.e. G <= N / max_atom_size.
4. PACK    : first-fit-decreasing of atoms into G bins. Balance metric is
             either block count or fiche count (reading workload).
5. SPLIT   : only if G exceeds the bound. Duplicate the cheapest lot that
             breaks the oversized atom (+1 read each). Greedy, repeatable.

Usage
-----
    python grouper.py <file> [--groups N] [--balance blocks|fiches]

Input format: one block per line, "ID  label  lot-01, lot-02"
Any line without a lot reference is ignored. Blocks with no lot are kept
as free fillers.
"""

import re
import sys
from collections import Counter, defaultdict


# ---------------------------------------------------------------- parsing
def parse(path):
    """Return [(block_id, [lot, ...]), ...]."""
    rows = []
    for line in open(path, encoding="utf-8"):
        m = re.match(r"\s*([A-Z]+\d+)\s+(.*)$", line)
        if not m:
            continue
        bid, tail = m.groups()
        rows.append((bid, re.findall(r"lot-\d+", tail)))
    return rows


# ------------------------------------------------------------- union-find
class UnionFind:
    def __init__(self):
        self.parent = {}

    def find(self, x):
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[ra] = rb


def atoms(rows, duplicated=frozenset()):
    """Connected components of the bipartite graph.

    Lots listed in `duplicated` are ignored as connectors: they are read by
    every group that needs them, so they no longer bind blocks together.
    Returns [(blocks, lots), ...] sorted by decreasing block count.
    """
    uf = UnionFind()
    for bid, lots in rows:
        uf.find(bid)
        for lot in lots:
            if lot not in duplicated:
                uf.union(bid, lot)

    groups = defaultdict(list)
    for bid, _ in rows:
        groups[uf.find(bid)].append(bid)

    lots_of = {bid: lots for bid, lots in rows}
    out = []
    for blocks in groups.values():
        lots = sorted({l for b in blocks for l in lots_of[b]},
                      key=lambda x: int(x.split("-")[1]))
        out.append((blocks, lots))
    return sorted(out, key=lambda a: (-len(a[0]), a[0][0]))


# --------------------------------------------------------------- packing
def pack(atom_list, n_groups, n_blocks, balance="blocks"):
    """First-fit-decreasing into n_groups bins. None if infeasible."""
    base, extra = divmod(n_blocks, n_groups)
    caps = [base + 1] * extra + [base] * (n_groups - extra)

    key = (lambda a: len(a[0])) if balance == "blocks" else (lambda a: len(a[1]))
    ordered = sorted(atom_list, key=lambda a: (-key(a), -len(a[0])))

    bins = [[] for _ in range(n_groups)]
    load = [0] * n_groups
    for atom in ordered:
        size = len(atom[0])
        candidates = [i for i in range(n_groups) if load[i] + size <= caps[i]]
        if not candidates:
            return None
        # tightest fit first, then lightest reading load
        best = min(candidates,
                   key=lambda i: (caps[i] - load[i] - size,
                                  sum(len(a[1]) for a in bins[i])))
        bins[best].append(atom)
        load[best] += size
    return bins


# ---------------------------------------------------------------- cutting
def cut_to_fit(rows, capacity, duplicated=None):
    """Duplicate lots until every atom fits in `capacity` blocks.

    Each duplication costs +1 read. Picks the lot giving the most balanced
    break of the largest oversized atom.
    """
    duplicated = set(duplicated or ())
    while True:
        current = atoms(rows, duplicated)
        oversized = [a for a in current if len(a[0]) > capacity]
        if not oversized:
            return current, duplicated

        target = oversized[0]
        members = set(target[0])
        best, best_score = None, None
        for lot in target[1]:
            pieces = [a for a in atoms(rows, duplicated | {lot})
                      if set(a[0]) & members]
            # smallest resulting piece first, then fewest pieces (least churn)
            score = (max(len(a[0]) for a in pieces), len(pieces))
            if best_score is None or score < best_score:
                best, best_score = lot, score
        if best is None:
            raise RuntimeError(f"atom {sorted(members)} has no lot to cut")
        if best_score[0] >= len(members):
            # no single cut breaks it (blocks bound by several shared lots):
            # duplicate the least-used lot and keep going
            counts = Counter(l for b, lots in rows if b in members for l in lots)
            best = min((l for l in target[1] if l not in duplicated),
                       key=lambda l: (counts[l], l), default=None)
            if best is None:
                raise RuntimeError(f"atom {sorted(members)} is indivisible")
        duplicated.add(best)


# ----------------------------------------------------------------- report
def report(rows, n_groups=None, balance="blocks"):
    n_blocks = len(rows)
    all_lots = {l for _, lots in rows for l in lots}
    base = atoms(rows)
    largest = max(len(a[0]) for a in base)
    g_max = n_blocks // largest

    print(f"blocks {n_blocks} | distinct lots {len(all_lots)} | "
          f"incidences {sum(len(l) for _, l in rows)} "
          f"({sum(len(l) for _, l in rows) / n_blocks:.2f} per block)")
    print(f"atoms {len(base)} | largest atom {largest} blocks")
    print(f"floor on reads {len(all_lots)} fiches "
          f"| zero-cost up to {g_max} groups "
          f"(group size >= {largest})")

    for n in ([n_groups] if n_groups else range(2, g_max + 1)):
        capacity = -(-n_blocks // n)
        atom_list, duplicated = (base, set())
        if largest > capacity:
            atom_list, duplicated = cut_to_fit(rows, capacity)
        bins = pack(atom_list, n, n_blocks, balance)
        if bins is None and n_blocks // n >= 1:
            # only one bin may hold the ceiling: re-cut to the floor capacity
            atom_list, duplicated = cut_to_fit(rows, n_blocks // n, duplicated)
            bins = pack(atom_list, n, n_blocks, balance)
        if bins is None:
            print(f"\n=== {n} groups: infeasible with this packing ===")
            continue

        reads = sum(len({l for a in b for l in a[1]}) for b in bins)
        sizes = [sum(len(a[0]) for a in b) for b in bins]
        loads = [len({l for a in b for l in a[1]}) for b in bins]
        print(f"\n=== {n} groups | blocks {min(sizes)}-{max(sizes)} "
              f"| fiches per group {min(loads)}-{max(loads)} "
              f"| total reads {reads} (+{reads - len(all_lots)}) ===")
        for i, b in enumerate(bins, 1):
            lots = sorted({l for a in b for l in a[1]},
                          key=lambda x: int(x.split("-")[1]))
            body = " | ".join("+".join(a[0]) for a in b)
            print(f"G{i} [{sum(len(a[0]) for a in b)} blocks, "
                  f"{len(lots)} fiches] {body}")
            print(f"     {', '.join(lots)}")
        if duplicated:
            print(f"     duplicated lots: {', '.join(sorted(duplicated))}")


def _cli():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    path = args[0]
    n = int(args[args.index("--groups") + 1]) if "--groups" in args else None
    bal = args[args.index("--balance") + 1] if "--balance" in args else "blocks"
    if "--auto" in args:
        w = float(args[args.index("--weight") + 1]) if "--weight" in args else 0.6
        auto(parse(path), w_load=w)
    elif "--budget" in args:
        budget_report(parse(path), float(args[args.index("--budget") + 1]))
    else:
        report(parse(path), n, bal)



# ------------------------------------------------- context-budget packing
FICHE_WEIGHT = 3.67    # one fiche, in block-equivalents of context
BLOCK_WEIGHT = 1.0
AGENT_OVERHEAD = 14.0  # fixed cost of spinning up one agent (prompt, tooling)


def load(atoms_in_bin):
    """Context load of one group, in block-equivalents.

    The agent overhead is paid once per group, so it inflates the per-group
    context AND makes the number of groups a direct cost:
        total = AGENT_OVERHEAD * G + FICHE_WEIGHT * reads + BLOCK_WEIGHT * N
    """
    fiches = len({l for a in atoms_in_bin for l in a[1]})
    blocks = sum(len(a[0]) for a in atoms_in_bin)
    return AGENT_OVERHEAD + FICHE_WEIGHT * fiches + BLOCK_WEIGHT * blocks


def pack_by_budget(atom_list, budget):
    """First-fit-decreasing on FICHE weight. Bins hold at most `budget`
    fiches. Atoms are lot-disjoint, so a bin's fiche load is the plain sum
    of its atoms' fiche counts. Returns the bins.
    """
    ordered = sorted(atom_list, key=lambda a: -load([a]))
    bins = []
    for atom in ordered:
        best = None
        for i, b in enumerate(bins):
            if load(b + [atom]) <= budget and (
                    best is None or load(b) > load(bins[best])):
                best = i
        if best is None:
            bins.append([atom])
        else:
            bins[best].append(atom)
    return bins


def budget_report(rows, budget):
    n_blocks = len(rows)
    all_lots = {l for _, lots in rows for l in lots}
    atom_list, duplicated = atoms(rows), set()
    heaviest = max(load([a]) for a in atom_list)

    while heaviest > budget:
        # an atom alone busts the context: duplicate the lot whose removal
        # leaves the lightest pieces (+1 read each time)
        target = max(atom_list, key=lambda a: load([a]))
        members = set(target[0])
        best, best_score = None, None
        for lot in target[1]:
            if lot in duplicated:
                continue
            pieces = [a for a in atoms(rows, duplicated | {lot})
                      if set(a[0]) & members]
            score = (max(load([a]) for a in pieces), len(pieces))
            if best_score is None or score < best_score:
                best, best_score = lot, score
        if best is None or best_score[0] >= load([target]):
            raise RuntimeError(
                f"budget {budget} unreachable: {sorted(members)} needs "
                f"{len(target[1])} fiches and cannot be lightened")
        duplicated.add(best)
        atom_list = atoms(rows, duplicated)
        heaviest = max(load([a]) for a in atom_list)

    bins = rebalance(pack_by_budget(atom_list, budget), budget)
    reads = sum(len({l for a in b for l in a[1]}) for b in bins)
    print(f"\n=== budget {budget} block-equivalents/group -> {len(bins)} groups "
          f"| total reads {reads} (+{reads - len(all_lots)}) ===")
    for i, b in enumerate(sorted(bins, key=lambda b: -load(b)), 1):
        lots = sorted({l for a in b for l in a[1]}, key=lambda x: int(x.split("-")[1]))
        blocks = sum(len(a[0]) for a in b)
        print(f"G{i} [load {load(b):.1f} = {len(lots)}f + {blocks}b] "
              + " | ".join("+".join(a[0]) for a in b))
        print(f"     {', '.join(lots) if lots else '(no fiche)'}")
    if duplicated:
        print(f"     duplicated: {', '.join(sorted(duplicated))}")
    return len(bins), reads

# ------------------------------------------------------- automatic budget
def auto(rows, w_load=0.6, step=0.5, verbose=True):
    """Sweep every feasible budget, keep the Pareto-optimal ones on
    (max context load, total reads), and return the best under the
    lexicographic rule: lowest max load first, fewest reads to break ties.

    Total tokens = FICHE_WEIGHT * reads + BLOCK_WEIGHT * N, so criterion 2
    reduces to minimising reads.
    """
    import io
    import contextlib

    atom_list = atoms(rows)
    floor_load = max(load([a]) for a in atom_list)
    ceiling = load(atom_list)          # everything in a single group
    points = []
    budget = 1.0
    while budget <= ceiling + step:
        # fine steps where the atoms are, coarse steps above
        step = 0.5 if budget < floor_load + 2 else 2.0
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                n_groups, reads = budget_report(rows, budget)
            loads = [float(l.split("load ")[1].split(" =")[0])
                     for l in buf.getvalue().splitlines()
                     if l.startswith("G") and "load " in l]
            points.append((budget, n_groups, reads, max(loads)))
        except RuntimeError:
            pass
        budget += step

    def _tok(p):
        return AGENT_OVERHEAD * p[1] + FICHE_WEIGHT * p[2] + BLOCK_WEIGHT * len(rows)

    pareto = [p for p in points
              if not any((q[3] <= p[3] and _tok(q) < _tok(p))
                         or (q[3] < p[3] and _tok(q) <= _tok(p))
                         for q in points)]

    # Scalarisation: each criterion is scored as its relative excess over the
    # best value reachable on the frontier, so the two are in the same unit
    # (% above floor). Min-max scaling is deliberately avoided: it would erase
    # the fact that reads vary far less, in relative terms, than max load.
    floor_max = min(p[3] for p in pareto)


    n = len(rows)

    def tokens(p):
        return AGENT_OVERHEAD * p[1] + FICHE_WEIGHT * p[2] + BLOCK_WEIGHT * n

    floor_tokens = min(tokens(q) for q in pareto)

    def score(p):
        return (w_load * (p[3] / floor_max - 1)
                + (1 - w_load) * (tokens(p) / floor_tokens - 1))

    best = min(pareto, key=score)

    if verbose:
        print(f"weights: context {w_load:.2f} / reads {1 - w_load:.2f}")
        print("budget groups reads maxload tokens  +load%  +reads%  score")
        for p in pareto:
            b, g, r, m = p
            mark = " <-- selected" if p == best else ""
            print(f"{b:6.1f} {g:6} {r:5} {m:7.1f} "
                  f"{AGENT_OVERHEAD * g + FICHE_WEIGHT * r + BLOCK_WEIGHT * n:6.0f} "
                  f"{(m / floor_max - 1) * 100:6.1f} "
                  f"{(tokens(p) / floor_tokens - 1) * 100:8.1f} "
                  f"{score(p) * 100:6.2f}{mark}")
        budget_report(rows, best[0])
    return best

# --------------------------------------------------- post-packing cleanup
def bin_reads(b):
    return len({l for a in b for l in a[1]})


def quality(bins):
    """Lexicographic quality of a packing, lower is better:
    total reads, then max load, then spread (sum of squared loads).
    Reads come first because two pieces of a cut atom sharing a duplicated
    lot cost one read instead of two when they sit in the same bin.
    """
    loads = [load(b) for b in bins if b]
    return (sum(bin_reads(b) for b in bins),
            max(loads) if loads else 0.0,
            sum(l * l for l in loads))


def rebalance(bins, budget, max_rounds=50):
    """Local search on top of first-fit-decreasing: single-atom moves then
    pairwise swaps, keeping every bin under budget. Fixes the FFD tail
    (a nearly empty last bin) and reunites split atoms when it can.
    """
    bins = [list(b) for b in bins]
    for _ in range(max_rounds):
        improved = False

        for i in range(len(bins)):
            for atom in list(bins[i]):
                for j in range(len(bins)):
                    if i == j or atom not in bins[i]:
                        continue
                    if load(bins[j] + [atom]) > budget:
                        continue
                    before = quality(bins)
                    bins[i].remove(atom)
                    bins[j].append(atom)
                    if quality(bins) < before:
                        improved = True
                    else:
                        bins[j].remove(atom)
                        bins[i].append(atom)

        for i in range(len(bins)):
            for j in range(i + 1, len(bins)):
                for a in list(bins[i]):
                    for b in list(bins[j]):
                        # a or b may have moved in an earlier accepted swap:
                        # operating on a stale pair duplicates atoms
                        if not any(x is a for x in bins[i]):
                            break
                        if not any(x is b for x in bins[j]):
                            continue
                        rest_i = [x for x in bins[i] if x is not a]
                        rest_j = [x for x in bins[j] if x is not b]
                        if (load(rest_i + [b]) > budget
                                or load(rest_j + [a]) > budget):
                            continue
                        before = quality(bins)
                        bins[i] = rest_i + [b]
                        bins[j] = rest_j + [a]
                        if quality(bins) < before:
                            improved = True
                        else:
                            bins[i] = rest_i + [a]
                            bins[j] = rest_j + [b]

        if not improved:
            break

    out = [b for b in bins if b]
    placed = [a for b in out for a in b]
    assert len(placed) == sum(len(b) for b in bins), "atom lost or duplicated"
    return out


if __name__ == "__main__":
    _cli()
