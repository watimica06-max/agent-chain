# Asking the Product Owner

The contract for every text the Product Owner reads to decide: a
question of a questions file, and the prose of a blocking file. Every
agent that writes either one reads this format before writing it. This
format is the chain's, and the install brings it.

📌 **Who reads what you write.** 🔴 **She is French, and not
technical.** ⚠️ **She sees one question at a time** — 📌 beside the
passage its second line names, when it names one — ⚠️ **never the
earlier questions files, never the rest of the corpus.** 🔴 **What she
needs to decide is in the question, or she cannot decide.**

## 1. What it governs

| Text | What this format rules |
|---|---|
| **A question** — one `### Q<n>` entry of a questions file | 🔴 **The `Question:` text and the `Options:` items, whole** |
| **A blocking file** | 🔴 **The prose under `## What blocks`, `## Where` and `## To resume`, and its `Options:` items** — see *§4* |

🔴 **The keys never change** — `### Q<n>`, `Question:`, `Options:`,
`Answer:`, `Block:`, `Terms:`, `Entries:`, `Folder:`, `Défaut:`,
`Kind:`, `Occurrences:`, and a blocking file's headings. ⚠️ **They are
what the chain and the cockpit read**, and they stay in English.

📌 **The entry's second line is its agent's** — `Terms:`, `Block:`,
`Entries:` — 📌 **written as that agent's rules say**, and this format
does not touch it.

📌 **`Défaut:` repeats one option verbatim before ` — `**, so it is in
French as the options are. ⚠️ **What follows ` — ` names its source** —
📌 **a quote stays in the language of the text it quotes.**

📌 **`Occurrences:` is not hers to read** — see *§3*. ⚠️ **The rules
below are the question's**, and none of them reaches those lines.

🔴 **Everything else an agent writes keeps its own language** — 📌 the
product file, the technical document, a report, a `## Decision` the
Arbitre writes.

## 2. The rules

🔴 **Each rule says what it prevents.** ⚠️ **A question that breaks one
is a question she cannot decide** — 📌 or one whose answer reaches the
chain meaning something she did not mean.

### Rule 1 — Form only is never asked

🔴 **A form-only matter is not a question.** 📌 **Three kinds, and no
other:**

- **Quotes** — whether a word is written between quotes, 🔴 **when the
  corpus already says, word for word, what the screen shows**
- **Typography** — backticks, bold, capitals, a dash
- **The choice between two words her answers already settled as naming
  one same thing**, 🔴 **when no text shown to the user changes**

⚠️ **Never form-only**: 🔴 **anything shown on screen** · **anything
about what an action does** · **the name of a thing she has not
settled.** 📌 **Whether a text reaches the screen at all is a question
about the screen**, and it is asked.

🔴 **The agent settles a form-only matter itself, the most cautious
way** — see *§5* — ⚠️ **and records it**, so that she can come back to
it.

📌 **Prevents**: a question whose answer changes nothing she can see,
which she can only answer at random — 📌 and an answer given at random
that the chain then reads as a decision.

### Rule 2 — One decision per question

🔴 **A question asks one decision.** 📌 **A second decision is a second
question**, with its own `Options:`.

🔴 **A question that leaves nothing to ask after its answer is not
split further.**

📌 **Prevents**: four decisions in one entry, an answer that settles
one of them, and three left open that the agent reads as settled — 📌
or applies none of, and asks again.

### Rule 3 — French, everyday words

🔴 **The `Question:` text and the options are in French**, 📌 **in the
words she uses about her own application.**

⚠️ **No chain word** — *concept*, *occurrence*, *bloc*, *entrée*,
*sens (a)*, *texte affiché*, *regroupement*, *genre*, *nature*, *lot* —
🔴 **unless the question defines it in the same sentence.**

⚠️ **No `§` number, no count of how many times a word appears, no file
name in the `Question:` text.** 📌 **What an agent needs to apply the
answer goes in its own lines** — see *§3*.

📌 **Prevents**: a question she reads in a language that is not hers,
with words whose chain meaning she does not know — 📌 and an option she
picks for the word she recognises, not for what it decides.

### Rule 4 — Short

🔴 **The `Question:` text: about sixty words at most**, the stake
included.

⚠️ **The places an answer applies to never go in the question** — 📌
**they go in `Occurrences:`**, see *§3*.

📌 **Prevents**: a question whose decision is buried under its
evidence.

### Rule 5 — Self-contained

🔴 **Never name an earlier question or answer by its number.** 📌
**Quote the words that matter, in full**, between « ».

⚠️ **A number means nothing to her**: 📌 the file it points to is put
away once answered, and nothing shows it again — ⚠️ **and the new file
numbers its own questions from `Q1`**, so « Q4 » names two things.

📌 **Prevents**: a question that cannot be decided without opening a
file she never sees.

### Rule 6 — The stake first

🔴 **The `Question:` text opens on one sentence: what the answer
changes for the application's user.** 📌 **When nothing visible
changes, what it changes in the documents the chain writes next** —
*« Le mot retenu sera le seul employé dans toute la description de
l'application. »*

⚠️ **One sentence**, 📌 **never a justification of why the agent
asks.**

📌 **Prevents**: a choice between words she cannot weigh, because
nothing says what either one leads to.

### Rule 7 — It asks

🔴 **The `Question:` text ends on what it asks, a sentence ending in
« ? »** — 📌 **one she can answer by picking an option, or by writing
the text the question says to write.**

⚠️ **Never a statement followed by options** — 📌 **the choice is
never only in the options.**

📌 **Prevents**: an entry she reads as information, with nothing that
says a decision is hers.

### Rule 8 — Options

🔴 **Two to six options, or none.** 📌 **Each one:**

- **one complete choice** — 🔴 **chosen alone, it is the whole
  answer**
- **one decision** — ⚠️ **never two choices joined by « ; »**
- **exclusive of the others** — 📌 two options never both hold
- **one short sentence, in French**
- ⚠️ **never opening on a number and a dot** — 📌 **an option chosen
  becomes the answer word for word**, and `1.` would read as a list

🔴 **A question about a name offers every word she could want** — 📌
**each word the corpus uses for that thing**, ⚠️ **the code identifier
included when the corpus writes one.**

🔴 **Two words that may name one same thing**: 📌 **the options are**
*« Une même chose : X est gardé »* · *« Une même chose : Y est gardé »*
· *« Deux choses différentes »* — 📌 **plus** *« Une même chose : les
deux mots restent »* **when keeping both is possible.** ⚠️ **Never
« une même chose ? » alone**: the name would be a second round.

⚠️ **An option never depends on a text she must add elsewhere** — 📌
*« … donné dans la remarque »*. 🔴 **When the answer needs a word she
must write, the question has no options**, and its last sentence says
what to write.

📌 **Prevents**: the word she wanted missing from the list · an option
that is three choices at once · an option whose meaning lives in a
remark she never wrote.

## 3. A question, whole

    ### Q1
    <the agent's second line>
    Question: <l'enjeu, en une phrase> <ce qu'elle demande, qui finit sur « ? »>
    Options:
    - <un choix complet, en une phrase courte>
    - <un autre>
    Answer:

📌 **An agent's own lines keep their place** — `Folder:`, `Kind:`,
`Défaut:` — as its rules say.

### `Occurrences:` — where the answer applies

🔴 **An agent that applies the answer to places in a text writes them
here, after `Options:`, one line each:**

    Occurrences:
    - <ce sous quoi la ligne est rangée> · §<ref> "<sa phrase, mot pour mot>"
    - <…> · §<ref> "<…>"

📌 **Today the Lexicographe alone writes it** — see its file. ⚠️
**`Défaut:`, when an entry carries both, comes after `Occurrences:`.**

🔴 **Every place, however many** — 📌 **a long list is still one
question**: its length is in `Occurrences:`, never in `Question:`.

⚠️ **The cockpit shows it folded, under « Où dans le texte »**, and
« Expliquer » never reads it.

## 4. A blocking file

| Heading | What it holds, under this format |
|---|---|
| `## What blocks` | 🔴 **The fact, in one sentence, in French, in everyday words** — rule 3 |
| `## Where` | 📌 **The file and the passage, as the agent that resumes needs them** — ⚠️ **the one place a file name and a `§` number belong**; the words around them in French |
| `## To resume` | 🔴 **The stake first, then the decision, asked** — rules 2, 5, 6, 7 |
| `Options:`, closing `## To resume` | 🔴 **Rule 8** |
| `## Decision` | 📌 **Hers, or the Arbitre's** — this format does not rule it |

📌 **A `## To resume` that gives her steps to do by hand**, not a
choice to make, follows its agent's own rules — 🔴 **in French, in
everyday words, still.**

## 5. Settling a form-only matter

🔴 **The most cautious way is the one that changes the least of what
she wrote:**

| The matter | The choice |
|---|---|
| **Two words her answers settled as one thing**, no name chosen | 🔴 **The word her own answers used** — 📌 **else the one the corpus uses most** |
| **Quotes**, the corpus saying word for word what the screen shows | 🔴 **Quotes where the text is shown, none where it is not** — 📌 as the corpus says it |
| **Typography** | 🔴 **As written** — ⚠️ nothing changes |

🔴 **Each choice is recorded where she can find it** — 📌 **the
Lexicographe writes it in `lexique.md`, under `## Tranché sans toi`**:
the words, the choice, the reason, one line each. ⚠️ **She overrules
one by saying so in a later answer**, and the Lexicographe applies it
as an answer.

⚠️ **Any other agent that meets a form-only matter asks nothing and
changes nothing** — 📌 **quotes and words are the Lexicographe's**, and
its next run settles them.
