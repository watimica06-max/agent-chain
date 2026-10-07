---
name: technical-state-format
description: How to write an entry in docs/CURRENT_TECHNICAL_STATE.md — what earns a place, what to remove, the domain/subject structure, where a trap goes. Load before writing to that file, never write to it without.
---

# Writing `CURRENT_TECHNICAL_STATE.md`

It exists so an agent does not **rebuild what already exists** or **fall
into a known trap**. An entry earns its place only if it is **not
quickly findable in the code** AND **not knowing it would cause a
mistake**.

**Write an entry when your lot created or removed:**
- a service, a component or a mechanism another lot could otherwise
  rebuild
- a table, a route, a chain of calls one component drives, a deletion
  cascade
- a trap (*"a lookup by day must use a range — the stored value carries
  a time of day"*)
- a dead state (*"`<Type>.<field>` has no writer"*)

**Do NOT write**: a narrative of what you changed, anything a single
grep would answer, or a coding convention (that is
`TECHNICAL_CONVENTIONS.md`).

🔴 **Remove what your lot made false.** A deleted service's entry
**disappears** — it does not become "removed by lot-NN". A changed
behaviour is **rewritten**, not appended to. Without this the file only
ever grows.

**Describe the state, never the change:**
- ✅ *"`RetryPolicy` waits twice as long after each failure, up to five
  attempts."*
- ❌ *"lot-NN deleted all three mechanisms and replaced them with…"*
- **No lot number in the body.**
- **Rewrite if any of these appear**: a past-tense verb, a lot number,
  "replaced by", "no longer", "used to". They are the signature of a
  narrative.

**Where the entry goes.** Agents search one way — *"what must I know
about X?"* The format serves that and nothing else:

- **Two heading levels only**: `## Domain`, then `### Subject`. 📌 **A
  domain is a kind of thing the project holds** — schema, services,
  routes, synchronisation, access, what the platform provides, what is
  left to verify: examples, not a fixed list. 🔴 **Two domains are
  fixed, by name**: `## Traps — general` and `## Dead state` — see
  below.
- 🔴 **The subject heading is the code identifier, verbatim** —
  `### RetryPolicy`, never `### The retry policy`. That string is what
  an agent greps.
- 🔴 **The one-line summary after the dash carries the answer.** In the
  common case the agent greps the heading and stops there. Make that
  line self-sufficient.
- **Body: four lines maximum, wrapped at ~80 characters.** Longer means
  you are describing a change, not a state.
- **Tables only for genuinely tabular data** — a few words per cell. A
  row needing a paragraph becomes its own `###` entry: multi-line table
  content produces lines `Read` cannot open and `grep` truncates.

    ### RetryPolicy — doubles the wait after each failure, five attempts

    `<the file that holds it>`. Pure, no I/O. The first wait is
    `<the constant that holds it>`; attempts counted from 1, the fifth
    failure is final (no sixth attempt). The clock is passed in — never
    read inside.

**Where a trap goes depends on whether it can be grepped:**
- **Owned by one subject** → put it under that subject, heading leading
  with the same identifier, then ⚠️:
  `### RetryPolicy ⚠️ the wait is never reset on success`. One grep on
  the subject returns entry and trap together.
- **General, or owned by several** → `## Traps — general`. Agents read
  that section whole, because you cannot grep for a rule you don't know
  applies to you. When in doubt, put it here.
- `## Dead state` — what exists but is wired to nothing. Also read
  whole: you cannot grep for something you don't know is dead.
