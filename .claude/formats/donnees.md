# External data — `donnees/` and its index, `donnees.md`

The contract between the Product Owner, who brings a file the chain
cannot invent, and the agents that read it. Whoever writes an index
reads this format: the Product Owner, by hand or through the cockpit.
Every agent that reads an index, or a file an index names, finds it by
the name this format gives. This format is the chain's, and the install
brings it.

## 1. Two kinds, two folders

🔴 **The kind of a file is its folder's** — ⚠️ **never a field of the
index.** A file moved from one folder to the other changes kind.

| Kind | What it is | Folder |
|---|---|---|
| **Reference data** | A real instance of something the code must read or understand, whose structure is decided outside the application — an export of another service, a site's data, what a device sends, a file or a text the user brings. 📌 **The specification and the tests are written from it; it is never shipped.** | `docs/features/<feature>/donnees/` — the feature's |
| **Embedded data** | A file the application itself uses when it runs — a set of images, a table it ships. 📌 **It is shipped, copied into the module that uses it.** | `docs/donnees/` — the application's |

🔴 **A reference instance is copied unaltered** — 📌 **as the other
system delivers it**, never retyped, trimmed or tidied by hand. ⚠️ **An
instance put back in shape by hand describes the hand, not the
system.**

## 2. The index — `donnees.md`

🔴 **One index in each `donnees/` folder, named `donnees.md`**: 📌
`docs/features/<feature>/donnees/donnees.md`, `docs/donnees/donnees.md`.

🔴 **It opens on its title, `# Données`, then one entry per file, five
lines each:**

    # Données

    ## releve-2026-09-14.csv
    What: a statement of operations, as the service the feature imports from exports it
    Source: exported from that service's account page, by the Product Owner
    Date: 2026-09-14
    Private: yes

| Line | What it holds |
|---|---|
| `## <name>` | 🔴 **The file's name, exactly as on disk**, relative to the folder — 📌 `images/fleche.svg` for a file in a subfolder |
| `What:` | What the file is, in one line |
| `Source:` | Where it comes from — the service, the site, the device, the person |
| `Date:` | The date the instance was taken, `YYYY-MM-DD` |
| `Private:` | `yes` or `no` — see below |

🔴 **Every line written, in that order** — ⚠️ **an absent line and a
forgotten one read the same.** 📌 **An index with no entry is its
title alone**, or no index at all: the folder holds nothing the chain
knows of.

**`Private: yes`** — 📌 **the file holds personal or confidential
data.** 🔴 **An agent reads it like any other, and never copies a value
from it into a document the chain writes** — the product file, the
technical document, a sheet, a question, a report: ⚠️ **it describes
the file's shape, and names the file.** 📌 **The copies a lot makes of
it — into a test folder, into a resource folder — are files, not
documents**, and stay in the repository as the file itself does.

Example, an embedded entry:

    ## images/fleche.svg
    What: the arrow shown beside each item of a list
    Source: drawn by the Product Owner
    Date: 2026-10-01
    Private: no

## 3. Who writes, who reads

🔴 **The Product Owner writes the index** — 📌 **by hand, or with the
cockpit's help.** ⚠️ **No agent writes in a `donnees/` folder, the
index included.**

🔴 **An agent reads the index, and the files it names — never the
folder.** ⚠️ **No listing, no glob of a `donnees/` folder**: 📌 **a file
the index does not name does not exist for the chain**, and one the
index names is found by that name alone.

🔴 **Each agent's instructions say which index it reads and which
files**, by name — ⚠️ **this format says how they are shaped, not who
opens them.**

📌 **An entry whose file is not on disk is a missing input** — 🔴 **the
reading agent treats it as its instructions treat one.**

## 4. How a document cites a file

🔴 **By its path from the repository's root** — 📌 the index's folder,
then the entry's `## <name>`:

    docs/features/<feature>/donnees/releve-2026-09-14.csv
    docs/donnees/images/fleche.svg

📌 **The path carries the kind** — ⚠️ **the reader never asks which
index a cited file belongs to.**

## 5. The question that asks for a file — `Folder:`

🔴 **A question whose answer is a file carries one more line, `Folder:`,
naming the folder the file goes to** — 📌 its path from the
repository's root, ending on `/`:

    ### Q4
    Block: B7
    Folder: docs/features/<feature>/donnees/
    Question: <what is missing, stated directly>
    Answer:

📌 **It is a `Key: value` line, between `Block:` and `Question:`** —
the questions file's own shape (`docs/app/TECHNICAL_V1.md` §8.1 of the
chain's repository). 🔴 **Its value is one of the two folders of §1,
the feature's name written out, nothing else.** ⚠️ **Never on a
question whose answer is text**: 📌 **it is what tells the cockpit to
offer « Joindre un fichier »**, and where to save what is joined.

🔴 **The answer names the file, as the index names it** — 📌 the file
saved in the folder, its entry written in the index, its name written
in `Answer:`. ⚠️ **An answer saying there is no such file is an answer
too** — 📌 text, and the block says so.
