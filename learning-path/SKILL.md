---
name: learning-path
description: >
  Use when a user wants to learn any technical topic from scratch, continue learning one, or
  maintain an existing learning path. Triggers on: "I want to learn X", "start a learning path for X",
  "I finished module X of course Y", "I finished chapter X of book Y", "create a learning path for X",
  "set up notes for learning X", "I'm studying X", "help me learn X", "I completed X",
  "write a chapter on what I just learned", and also on maintenance asks like "review my learning path",
  "update the learning path", "refresh the path", "is my learning path still current",
  "check the path against the latest release/exam". ALSO fires after any note is taken (a reading note,
  research note, or notebook note added under docs/sources/, or a new book chapter) — reconcile the
  path against what the note revealed and fold in anything new. This skill researches the topic's book
  and course landscape, creates a structured learning path, auto-generates a topic-specific book writing
  skill, writes a technical book chapter by chapter as the user progresses, keeps the path in sync as new
  notes land, and periodically re-verifies the path against current certifications, runtime/package
  versions, and course catalogs. Works for any topic: LangChain, Databricks, Python, MLOps, Kubernetes,
  system design, etc.
---

# Learning Path Skill

A five-phase workflow for learning any technical topic, building a knowledge book as you go, and keeping the path current: **Phase 1** researches the landscape and scaffolds the notes site, **Phase 2** writes the topic-based learning path, **Phase 3** writes a book chapter each time a topic is finished, **Phase 4** reviews and refreshes an existing path against current sources, and **Phase 5** reconciles the path against each new note as it lands.

## Phase Detection

Before doing anything, check the topic's state:

```
topic slug = derive from user's message (e.g. "ai agents" → "ai-agents", "databricks" → "databricks")
notes root = C:\opt\learn\<topic-slug>\notes
```

| State | Action |
|---|---|
| `notes\` missing OR `docs\learning-path.md` missing | Run Phase 1 then Phase 2 |
| `learning-path.md` exists + user says "I finished X" / "write the chapter for X" | Run Phase 3 |
| `learning-path.md` exists + user wants to review / update / refresh / verify currency | Run Phase 4 |
| `learning-path.md` exists + a new note was just taken (reading/research/notebook note or book chapter) | Run Phase 5 |
| `learning-path.md` exists + a plain status check | Show learning path + book progress summary |

When the request is ambiguous between "show me where I am" and "check the path is still current", prefer Phase 4 — a real review is more useful than a summary, and Phase 4 ends with the summary anyway.

**Phase 4 vs Phase 5.** Phase 4 is a heavy, scheduled re-verification against *external* sources (re-fetches cert pages, runtime notes, catalogs). Phase 5 is a light, event-driven reconcile against *one new note* — no vendor fetch. A note landing triggers Phase 5, not Phase 4.

---

## Fetching vendor pages (Phases 1 and 4)

Research depends on reading certification exam guides, training catalogs, and release notes — and most of these (databricks.com, vendor academies) are JavaScript-rendered. `WebFetch` paraphrases such pages and silently drops the exact facts that matter (question counts, domain weights, version dates), or returns a login/challenge shell. Do not trust it for vendor marketing/training/cert pages.

Use the project's `scripts/fetch_page.py` (Playwright driving system Chrome) instead — it renders the page and saves verbatim text to `cache/web/<slug>.txt`, which you then Read:

```
python scripts/fetch_page.py "<url>" --slug <slug> --timeout 45000
```

If it errors with `ModuleNotFoundError: No module named 'playwright'`, run `pip install playwright` once (no separate browser download — it uses the installed Chrome). `cache/` is gitignored scratch. `WebSearch` is fine for discovery (finding which pages exist); switch to `fetch_page.py` to read the page that holds the actual numbers.

---

## Phase 1 — Research & Scaffold

Read `references/phase1-research.md` for full instructions.

**Summary:**
1. Research topic taxonomy — derive all topics from certification exams, university syllabi, job descriptions, and course curricula; classify each topic as Beginner / Intermediate / Advanced / Expert
2. Research top books (fetch full TOCs); note which topics each book covers
3. Research courses — official academies, university MOOCs (Coursera/edX), Udemy, YouTube, interactive platforms (DataCamp, Kaggle); note topics covered, hours, hands-on vs lecture
4. Research certifications — fetch official exam guides; record topics, weights, fees, and which level they validate
5. Validate current stable version against official docs
6. Scaffold `C:\opt\learn\<topic-slug>\notes\` (Zensical site, Docker)
7. Auto-generate `~/.claude/skills/<topic>-book/SKILL.md` with full chapter arc from taxonomy

Phase 1 flows directly into Phase 2.

---

## Phase 2 — Learning Path

Read `references/phase2-path.md` for full instructions.

**Summary:**
1. Organise topics into four levels: Beginner / Intermediate / Advanced / Expert
2. For each topic write: what it is (1 sentence), why you need it (1 sentence), a **"How to learn it"** list (video first → interactive exercise → depth reading → reference docs), and a concrete milestone
3. Place certifications as level checkpoints (not as topics)
4. Do NOT organise by resource/book/course — topics are the primary unit; resources serve the topics
5. Every "How to learn it" section must cite **both a book chapter and a specific official docs page** — not the docs root, and not two resources of the same kind. Where no book genuinely covers the topic (recent features), add an explicit "No book covers this" callout naming what to use instead, rather than citing a book that does not. Verify every docs URL before writing it — pages get renamed between releases

---

## Phase 3 — Book Chapter Writing

Read `references/phase3-book.md` for full instructions.

**Notes** (written by `book-pdf-notes`) are source-faithful — one per book/article/course. **Book chapters** (written here) are topic-driven syntheses — one per learning-path topic, blending all sources the user has read on that topic.

**Summary:**
1. Trigger: user says "I finished topic X" or "write the chapter for X"
2. Identify the topic code and chapter number from the topic-book skill's arc table
3. Gather all notes already written for this topic (grep notes directory)
4. Web-search for current best practices and pitfalls not yet in the notes
5. Produce a synthesis plan — how to blend sources; note conflicts and different framings
6. Write one book chapter that blends all sources; chapter follows the learning-path topic's scope exactly
7. Fit the chapter's structure to the topic — free format guided by a few invariants, not a fixed 8-section template
8. Sync: book index, `zensical.toml`, glossary

---

## Phase 4 — Review & Refresh

Read `references/phase4-review.md` for full instructions.

**Summary:** Re-verify an existing path against current reality and sync it. Volatile facts (cert
question counts / domain weights / fees, current runtime & package versions, course catalog
names and links) drift; this phase catches that.

1. Re-fetch the volatile sources with `fetch_page.py` — cert exam pages, runtime/release notes, training catalog
2. Diff each fetched fact against what the path claims; correct mismatches
3. Sync topic `⬜`/`✅` status with what the user has actually completed (book chapters present)
4. Fold any new breaking changes / renames / new features into the relevant topic as a callout
5. Update the header `Last updated` line (with a one-line changelog of what this pass verified/changed) and the `Sources consulted` list
6. Report what changed vs. what was verified-and-unchanged; offer to commit

---

## Phase 5 — Note-Triggered Path Sync

**Trigger:** a new note just landed — a reading/research/notebook note, or a new book chapter — in
whichever notes/chapters dirs this project actually uses (modern: `docs/sources/` + `docs/book/`; older
projects vary, e.g. spark uses `docs/books/` + `docs/spark-book/` — detect the layout per the
**Canonical project layout** section, don't assume). The note skills (`book-pdf-notes`,
`notebook-notes`, `research-notes`, `<topic>-book`) own writing the note; this phase runs **right
after**, as the last step, to keep the path honest. If you wrote the note in this session, run Phase 5
before signing off. If the user says "I took a note on X" after the fact, run Phase 5 against that note.

This is a **lightweight** reconcile, not a Phase 4 review — do **not** re-fetch vendor pages. Diff only
the new note against `docs/learning-path.md`. Four checks:

1. **New topic / subtopic.** Does the note cover a concept the path doesn't list at all? → add it under
   the right level (Beginner / Intermediate / Advanced / Expert) with the standard fields (what / why /
   how to learn it / milestone). If it's a sub-point of an existing topic, fold it into that topic's
   scope instead of creating a new one.
2. **New version / rename / deprecation.** Does the note surface a version bump, product rename, or
   deprecated tool the path still states the old way? → correct the path and add a dated callout on the
   affected topic.
3. **New resource.** Does the note come from a book / course / article not yet credited in any topic's
   "How to learn it"? → add it there (keeping the book-and-docs requirement intact).
4. **Completion.** Does the note (or its book chapter) mean a topic is now effectively done? → flip
   `⬜` → `✅` and update book progress.
5. **Staleness.** Did checks 1–3 add material to a topic whose chapter is already written? → that
   chapter is now behind the path, so flip it `✅` → `🔄` (needs revisiting) rather than leaving a
   ✅ that claims it is current. Mark all three places together: the topic heading here, the chapter
   row in the book index, and a dated banner in the chapter file saying what drifted. State whether
   the chapter is **wrong** (a false claim — a changed default, a stale version requirement) or
   merely **incomplete**; only the first misleads a reader, and it decides what to fix first.

**If at least one check fires:** make the edit, bump the header `Last updated` line with a one-line
changelog (e.g. `2026-06-21 — Phase 5: added "Liquid Clustering" subtopic to B5 from Ch2 notes`), and
tell the user exactly what changed in the path.

**If nothing is new:** do **not** touch the file. Say "Path already covers this — no change," and stop.
Most notes on already-planned topics will land here; that's expected, not a failure.

Keep it cheap: this runs on every note, so it must stay a quick diff, never a research pass.

---

## Topic Slug Derivation

Convert the user's topic to a lowercase kebab-case slug:

| User says | Slug | Notes root |
|---|---|---|
| "ai agents" | `ai-agents` | `C:\opt\learn\ai-agents\notes` |
| "databricks" | `databricks` | `C:\opt\learn\databricks\notes` |
| "LangChain" | `langchain` | `C:\opt\learn\langchain\notes` |
| "MLOps" | `mlops` | `C:\opt\learn\mlops\notes` |

---

## Canonical project layout

Phases 1, 3, and 4 all read and write inside `C:\opt\learn\<slug>\notes\`. Use these paths so the
phases agree — Phase 1 creates them, Phase 3 reads/writes them, Phase 4 syncs them:

| Path | Holds | Written by |
|---|---|---|
| `docs/learning-path.md` | the learning path | Phase 2 / Phase 4 |
| `docs/book/` | synthesized book chapters (`ch<NN>-<slug>.md` + `index.md`) | Phase 3 / `<topic>-book` skill |
| `docs/sources/` | source-faithful reading notes, one dir per book/course | note skills (`book-pdf-notes`, etc.) |
| `docs/research-cache/` | verified API/version facts captured during research | Phase 3 / Phase 4 |
| `docs/reference/glossary.md` | glossary terms | Phase 3 |
| `cache/web/` | `fetch_page.py` output (gitignored scratch) | Phases 1, 4 |

> **Older projects vary.** The earliest sites use `docs/<topic>-book/` for chapters and `docs/books/`
> for reading notes (e.g. the Spark notes). Don't rename an existing project to match this table —
> detect the layout that's actually there (list `docs/`) and use it. The table is the default for
> *new* scaffolds and the tie-breaker when a path is ambiguous.

---

## After Every Phase 3 Run

Before confirming, run the coverage audit (`references/phase3-book.md` Step 5c): re-check every cited note against the written chapter, point by point, not just for false claims but for dropped content. Grounded and complete are different properties — check both.

Always end with:
- Confirmation of what was written / blended
- Coverage audit result (gaps found + fixed, or clean)
- Current chapter count and book progress
- What's next in the learning path
