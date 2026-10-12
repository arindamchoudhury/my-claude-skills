---
name: postgres-book
description: >
  Use when writing, drafting, reviewing, or extending a chapter in the personal Database Systems /
  PostgreSQL book at C:\opt\learn\postgres\notes\docs\book\. Triggers on: "write the chapter for X",
  "I finished topic B3", "I finished I15", "I just learned about MVCC / B-trees / WAL / EXPLAIN /
  isolation levels", "add a chapter on partitioning", "write the postgres book chapter for
  replication", any reference to a learning-path topic code (B1–B13, I1–I17, A1–A15, E1–E9), or any
  request to add/draft/review/extend a chapter in the PostgreSQL personal book. Also fires on
  database-systems or PostgreSQL concept learning ("I learned about HOT updates", "add a chapter on
  hash joins", "explain vacuum freezing for the book").
---

# PostgreSQL & Database Systems Book: Chapter Writing

Synthesized chapters, one per learning-path topic, at `C:\opt\learn\postgres\notes\docs\book\`.
A chapter blends **every source the user has read** on that topic (reading notes in `docs/sources/`,
plus current web best-practices) into one explained treatment aligned to the learning-path milestone.

This skill is invoked by **Phase 3** of the `learning-path` skill. Read
`learning-path/references/phase3-book.md` for the full workflow (gather notes → web-search current
practices → synthesis plan → write → sync index/glossary). This file supplies the **chapter arc**,
**invariants**, **toolkit**, and **PostgreSQL-specific standards**.

**The book has two halves that must stay welded together.** Every chapter owes the reader both the
vendor-neutral mechanism (what a B+Tree *is*, what serializability *means*) and the PostgreSQL
realization (what `pageinspect` shows, what `EXPLAIN` prints, which GUC controls it). A chapter that
is all theory is a textbook summary; a chapter that is all `psql` output is a blog post. Neither is
this book.

---

## Chapter arc

One chapter per learning-path topic, numbered sequentially across all four levels.
File name: `ch<NN>-<slug>.md`.

**The chapter list is deliberately not duplicated here.** It lives in `docs/book/index.md`,
generated from `docs/learning-path.md` by `scripts/sync_book_index.py`. Read that file to get the
number and title for the topic you are about to write.

```bash
python scripts/sync_book_index.py     # regenerate; --check fails without writing, for CI
```

A hardcoded table used to live in this section and went stale: the 2026-09-01 feature-matrix audit
added seven topics (B11-B13, I17, A14, A15, E9) and shifted every Intermediate, Advanced and
Expert number by three or more. A stale table here mis-numbers a chapter *before* it is written,
which is the expensive moment to be wrong.

Rules the numbering follows:

- Numbers run in learning-path order across all four levels. As of 2026-09-01 that is **54
  topics**: B1-B13 -> 1-13, I1-I17 -> 14-30, A1-A15 -> 31-45, E1-E9 -> 46-54.
- **A written chapter's number never changes.** The filename is the permanent identifier and
  published links point at it. If inserting a topic would renumber a written chapter,
  `sync_book_index.py` refuses to rewrite and reports the conflict rather than orphaning links.
- Every chapter header **must** declare its topic on its own line:

  ```markdown
  > **Learning-path topic:** [The relational model & relational algebra](../learning-path.md#b1-the-relational-model-relational-algebra)
  ```

  The link text is the topic **title**; the sync script reads the topic code from the anchor
  (`#b1-…`). A chapter file without this line is an error.
- **Never show a topic code (B1, I10, A2, …) anywhere in a chapter**: not in prose, tables,
  admonitions, See-also or What's next. Readers navigate by chapter number; codes are learning-path
  bookkeeping. Refer to every chapter as **"Chapter N"** (number from `docs/book/index.md`), with
  its title where it helps:
  - **Written chapter** → link the file, with a section anchor when pointing at a section:
    `[Chapter 2, section 2 "Cluster, database, table"](ch02-running-your-own-cluster.md#2-cluster-database-table)`.
  - **Unwritten chapter** → same "Chapter N" text, linked to its learning-path topic (no file yet):
    `[Chapter 23](../learning-path.md#i10-reading-explain-plans)`. Switch the link to the file once
    that chapter exists.
  - Chapter numbers are safe to print: written ones never change, and `sync_book_index.py` refuses
    to renumber them. If a path insert shifts *unwritten* numbers, grep the chapters for
    `learning-path.md#` links and update their "Chapter N" text.
  - Mermaid node ids like `A1[…]` are not topic codes and are fine.

---

## Chapter invariants (every chapter, no exceptions)

**These are contracts, not a shape.** Nothing below dictates section order or section titles. See
"Chapter shapes" for how the arc is chosen. A chapter that satisfies all six and looks unlike every
other chapter in the book is correct.

1. **Nothing is used before it is explained.** A reader must never meet a term, an object, a command
   or a mechanism that the chapter leans on before the chapter, or an earlier chapter, has named
   it. **This is a book, not a notebook.** Whatever a section takes for granted, something before it
   must have supplied.

   Every chapter states its exit contract up front, as
   `## What you should be able to do by the end`: 4-6 concrete, checkable abilities derived from
   the learning-path **Milestone**, written as things the reader *does* ("point at the file on disk
   holding a table's data, finding the path with a catalog query"), not things they know about.
   That list is the one fixed opening; everything after it is chosen by topic.

   The failure this rule exists to prevent: a chapter opens by posing a problem, and the problem
   silently assumes four things the chapter has not introduced, so the reader carries four unnamed
   objects until section 5 rescues them. Diagnosed on 2026-09-05 in ch02, whose opening posed
   "which cluster am I talking to?" while deferring cluster, `initdb`, start/stop and connect.
   The fix was to supply the machinery first, for *that* chapter. It is not a template.
2. **Both halves.** The vendor-neutral mechanism *and* the PostgreSQL realization. Say explicitly
   where PostgreSQL diverges from the textbook design and why (e.g. no undo pass in recovery,
   because MVCC keeps old versions in the heap).
3. **Teach toward the milestone.** The learning-path topic's **Milestone** sentence is the chapter's
   exit criterion. A reader who finishes the chapter must be able to do exactly that.
4. **Runnable against PostgreSQL 18.** Every SQL block runs as written on a stock PG 18 cluster.
   Show the setup (`CREATE TABLE`, data generation) when the reader needs it to reproduce.
5. **Every body callout is a Material admonition**, never a `>` blockquote. See "Callout
   formatting" below.
6. **End pointing forward.** Close with what the next chapter builds on this one, by chapter number
   and title, never by topic code.

---

## Chapter shapes (choose one; do not default)

**The arc is fit to the topic, and the topic decides.** Before writing, ask what actually brings a
reader to this material and what they already hold. Then pick, or build, the shape that serves
that. The shapes below are the common answers, not a menu you must pick from.

| Shape | Fits a topic where… | Arc |
| --- | --- | --- |
| **Problem-first** | the reader arrives already burned by a slow query, a wrong result or an outage | the failure, felt and reproduced → why it happens → the mechanism → the fix |
| **Orientation-first** | the reader arrives with nothing built and no grievance | what the thing is, end to end at the keyboard → each part in depth → the failure modes |
| **Mechanism-first** | the value is the idea itself, and applications follow from it | the model from first principles → what it buys → where PostgreSQL implements it |
| **Surface-first** | the topic is a body of syntax or an API the reader must become fluent in | the shape of the construct → semantics and edge cases → where it goes wrong |
| **Decision-first** | the topic is a choice between options with real trade-offs | the decision and what rides on it → the axes → each option against them → how to pick |

Two corollaries:

- **A "The problem" section is one option, never an obligation.** Write it when a reader genuinely
  arrives with that problem. Retrofitting a grievance onto an orientation topic invents a motivation
  the reader does not have, and costs a section.
- **Navigation is separate from motivation.** A long chapter (say 8+ sections) owes the reader a map
  of which section answers what. That map does not need a problem to hang on: it can be a short
  lead-in, a table, or the tail of the opening section.

Section titles, numbering depth and whether sections are numbered at all are likewise the chapter's
own call. What every chapter owes is invariant 1: nothing used before it is explained.

---

## Toolkit (draw on what the topic needs, NOT a fixed template)

Having chosen a shape, fill it from these. Nothing here is required and nothing here is ordered. A
theory chapter (I8, A3), a SQL-surface chapter (B4, I1), an internals chapter (I5, I15, E3) and an
operations chapter (A6, A8, E7) draw very different subsets:

- A motivating problem: a slow query, a corrupted result, an outage. Optional: use it when the
  reader really arrives with that problem (see "Chapter shapes"), not as a fixed opening
- Core-concept prose with the mechanism explained from first principles
- Worked examples with real `psql` output
- Mermaid diagrams (page layouts, B+Tree splits, plan trees, replication topologies, state machines)
- Reference tables (lock conflict matrix, isolation-level anomaly grid, index-type capability grid)
- Semantics & edge cases (NULL behaviour, tie handling, boundary conditions)
- Pitfalls: what goes wrong in production and what it looks like in the logs
- Performance notes with measured numbers
- Exercises that map to the milestone
- Summary and references

---

## PostgreSQL code standards

- **Target PostgreSQL 18.** State the version any time behaviour is version-dependent, and say what
  the previous behaviour was, because the reader will meet PG 14–17 clusters in the wild.
- **`psql` sessions**: show the prompt and the real output, trimmed for width. Use `\x` for wide
  result sets rather than truncating columns silently.
- **`EXPLAIN`**: always `EXPLAIN (ANALYZE, BUFFERS)` when making a performance claim; add `SETTINGS`
  when a non-default GUC is in play. Never quote a plan without saying what the settings were.
- **Identifiers**: `snake_case`, plural table names, singular column names. Explicit schema
  qualification when `search_path` matters to the point being made.
- **Explicit over implicit**: write `INNER JOIN` not `JOIN`, `STORED`/`VIRTUAL` on generated columns,
  `ON DELETE` actions on every foreign key in an example.
- **Data generation**: prefer `generate_series` so examples are reproducible without a fixture dump.
- **Multi-session demos** (locking, isolation, MVCC): label the sessions and show interleaving
  explicitly: a table with a "Session 1 / Session 2 / time" layout, not two code blocks in a row.
- **Lab clusters come from the repository's `docker-compose.yml`**, service `lab`, started with
  `docker compose --profile lab up -d lab`, entered with `docker compose exec lab psql -U postgres`,
  and torn down with `docker compose rm -sf lab`, never a bare `docker compose down`, which acts on
  the whole project and stops the documentation site container too.
  It initializes with `--locale-provider=builtin --builtin-locale=C.UTF-8 --lc-collate=C
  --lc-ctype=C --encoding=UTF8`, which is what makes captured output reproducible: byte-order
  sorting cannot drift when the base image's collation library changes, because the builtin provider
  is PostgreSQL's own code. Unlike libc's `C` it also leaves `upper()`/`lower()` Unicode-aware, and
  the two `--lc-*` flags stop the image's `LANG` leaking into `datcollate`/`datctype`. **Never write a
  bare `docker run` in a chapter from B3 onward.** Chapters 1 and 2 are the deliberate exceptions:
  B2 needs a cluster whose locale was inherited by accident in order to teach what that costs. When
  an example needs different collation behaviour, ask for it per query or per column with `COLLATE`
  rather than changing the cluster; if it genuinely needs a second cluster, build one in the example
  and say why.

---

## Measured claims (numbers the chapter asserts)

Any number the chapter states (a timing, a row count, a size, a speedup) must come from a run the
author actually did, on stated hardware and version, with the query and setup shown. Record the
method inline (one line is enough: `PG 18.6, 8-core/32 GB, 10 M rows, shared_buffers=8GB`).

Never carry a benchmark number forward from a book or blog post as if it were measured here. If a
source's number is worth citing, attribute it and say what it was measured on.

If a claim cannot be measured (an architectural assertion, a design rationale), state it as reasoning
and cite the docs or source, not as a number.

---

## Version-gated facts

PostgreSQL changes defaults between majors, and every book in the resources table is behind PG 18.
When a chapter states a default, a GUC value, a syntax form or a capability:

1. Verify it against the [PG 18 docs](https://www.postgresql.org/docs/18/) at writing time.
2. If it changed within the last three majors, add a version callout naming the old behaviour.
3. Record the verified fact in `docs/research-cache/version-facts.md` so later chapters reuse it.

Known traps to flag whenever they come up:

| Fact | Changed in | Trap |
|---|---|---|
| Generated columns default to `VIRTUAL` | PG 18 | Books (PG ≤17) describe `STORED` as the only form |
| Asynchronous I/O (`io_method`, `io_workers`) | PG 18 | No book coverage at all |
| B-tree skip scan on multicolumn indexes | PG 18 | Changes leading-column advice |
| `pg_upgrade` carries statistics forward | PG 18 | The traditional post-upgrade `ANALYZE` cliff is gone |
| `EXPLAIN ANALYZE` output changed three ways: automatic `BUFFERS`, **fractional** `actual rows`, `Index Searches: N` | PG 18 | Every plan quoted in a pre-18 book looks different from what the reader gets; `actual rows=2.29 loops=7` reads as a bug unless you know it is a per-loop average |
| CTEs inlined unless `MATERIALIZED` | PG 12 | Pre-12 advice calls CTEs an unconditional fence |
| Hash aggregation can spill to disk | PG 13 | Pre-13 advice says hash agg never spills |
| `hash_mem_multiplier` | PG 13 | Hash nodes no longer bounded by plain `work_mem` |
| `UNIQUE NULLS NOT DISTINCT` | PG 15 | Older advice says NULLs always defeat `UNIQUE` |
| `CREATE`-on-`public` no longer granted to `PUBLIC` | PG 15 | Older tutorials assume it is |
| `MERGE` | PG 15 (+`RETURNING` in PG 17) | LP2e covers `MERGE` without `RETURNING` |
| `pg_stat_io` | PG 16 | I/O tuning advice predating it points at cruder views |
| SQL/JSON (`JSON_TABLE`, `JSON_VALUE`, …) | PG 16–17 | LP2e covers only the operator style |
| Logical replication slots preserved by `pg_upgrade` | PG 17 | Changes the near-zero-downtime upgrade story |

---

## Self-containment

A chapter must stand alone. A reader arriving from a search engine at chapter 25 should not need
chapters 1–24 open. Restate the two or three prerequisite facts in a sentence each and cross-link
(`[[ch18-index-theory]]`) rather than assuming.

Cross-links use wikilink syntax `[[ch<NN>-<slug>]]`; `serve.py` resolves them against `docs/`.

---

## Hands-on: inline first, lab second

**Teach every concept at the keyboard, where it is introduced.** A reader must not have to hold five
new ideas in their head until an end-of-chapter lab lets them try any of them. The moment a chapter
explains a mechanism, it shows the command that makes it visible and the output it produces.

So a chapter carries hands-on material in **two distinct places, with different jobs**:

| | Inline hands-on | `## Lab` at the end |
| --- | --- | --- |
| **Where** | in the body, immediately after each concept | one section, before the summary |
| **Job** | *learn* the concept: see it happen once | *strengthen* it: combine, vary, break, diagnose |
| **Shape** | short: one command, its real output, one sentence on what to notice | multi-step scenario with setup and teardown |
| **Reader state** | meeting the idea for the first time | has read the whole chapter |

**Inline hands-on rules:**

- Put the command **next to the sentence it proves**, never several pages later.
- Keep it small: a `psql` snippet with real output, not a scenario. If it needs a schema and three
  tables, it belongs in the lab.
- Show the output. A command without its output teaches nothing to a reader who is not typing along.
- Say what to look at in the output; do not leave the reader to guess which line matters.
- Prefer something with an immediately visible result over something that requires belief.

**The end-of-chapter `## Lab` then reinforces rather than introduces.** By the time the reader
reaches it they have already run every individual command inline; the lab's job is to make them
*use* those commands together on a problem, and it should include at least one step where something
goes wrong and they diagnose it. A lab that is the reader's first contact with the chapter's
commands is a defect. Move that material inline and rebuild the lab on top of it.

Lab structure stays as before:

- **Setup**: a `docker run` or `psql` block that creates the schema and data from nothing
- **Steps**: numbered, each with the command and what to observe
- **Expected output**: enough to know it worked
- **Teardown**: `DROP` the objects; labs must not accumulate state across chapters

Labs for internals topics should use `pageinspect`, `pg_buffercache`, `pg_visibility` or
`pg_stat_statements` where they make the mechanism visible. Say which extension is needed and how
to install it.

---

## Callout formatting (mandatory)

Every note, definition, aside, tip, warning, and version-gate in a chapter **body** is a Material
admonition:

```markdown
!!! note "Title"
    Body indented four spaces.

!!! warning "This bites in production"
    Body.
```

Types by what the reader must do: `warning` for something that will bite them (a changed default, a
book that is now wrong), `danger` for data loss, `info` for a naming or behaviour clarification,
`tip` for a technique, `note` for additive context.

`>` blockquotes are reserved for the **chapter-header front-matter** only (source + summary +
see-also). A `>` in the body is a defect: convert it on sight. Never indent an admonition into a
list item.

---

## Sentences without em dashes (mandatory)

Book text carries no em dash (`—`). The user set this rule on 2026-10-12, after a chapter sentence
that put three examples between its subject and its verb could not be read at first pass.

Build the sentence so that it does not need one:

| Where the dash would have gone | Write instead |
| --- | --- |
| An aside in the middle of a sentence | Two sentences. Finish the main statement, then give the aside its own. |
| Examples that interrupt the sentence | The examples at the end: "A value of the type used anywhere else is never checked against them, whether it is a function argument, a return value, or a column in another table." |
| A reason or a consequence after the statement | A colon, or a full stop and a new sentence. |
| A short qualifier | Commas or parentheses. |
| A label and its description, in a list item or a table cell | A colon after the label. |
| A chapter number with its title | `Chapter N: Title`, in link text and in the page title. |
| A lead-in label such as Hands-on or Step 3 | `**Hands-on: do this.**` and `**Step 3: do this.**` |
| A lab step heading that names its outcome | `### 1. Do this (*outcome 1*)` |
| A table cell with nothing to say | The word `none` or `never`. |

This covers everything a reader sees in a chapter: body text, headings, admonition titles and
bodies, list items, table cells, link text and the front-matter block. A spaced hyphen (` - `) or a
double hyphen (`--`) standing in for the dash is the same defect. The en dash in a range
(`PG 14–17`) is a different character and stays.

If an em dash is inside captured program output or a verbatim quotation, it stays as captured.

`docs/book/` was swept on 2026-10-12 and holds no em dash, so any one found there is new.

Check the whole book. Every file must print `0`:

```bash
grep -c '—' docs/book/*.md
```

---

## Current versions (verified 2026-08-29; see docs/research-cache/version-facts.md)

| Component | Version | Note |
|---|---|---|
| PostgreSQL | **18.6** (2026-08-13) | Current stable; PG 19 in Beta 3, GA expected Sep/Oct 2026 |
| Supported majors | 14 – 18 | Five-year window; PG 13 is EOL |
| pgvector | check release notes at writing time | Moves fast; HNSW since 0.5.0 |
| CloudNativePG | 1.25+ | The version the EDB cert targets |

Re-verify before writing any chapter that states a version-dependent fact.

---

## Key patterns every chapter should reinforce where relevant

1. **Measure, then change.** No tuning claim without a before/after `EXPLAIN (ANALYZE, BUFFERS)`.
2. **The estimate is the bug.** When a plan is bad, check the row estimate before blaming the index.
3. **Correctness before speed.** Isolation level, constraints and NULL semantics come before tuning;
   a fast wrong answer is worse than a slow right one.
4. **The database enforces invariants; the application does not.** Constraints, foreign keys and RLS
   over application-layer checks.
5. **Physical follows logical.** Design the schema, then index it, never the reverse.
6. **Every durability setting is a trade.** Name what is being traded away (`synchronous_commit`,
   `fsync`, async replication) rather than calling a setting "faster".
7. **Locks are the production failure mode.** Any DDL or migration example says which lock level it
   takes and for how long.

---

## Anti-patterns to never write

- `SELECT *` in an example that is about performance
- A performance claim with no plan, no version and no hardware
- `EXPLAIN` without `ANALYZE` used to argue about actual time
- Advising query hints (PostgreSQL has none) instead of statistics, cost parameters or rewrites
- Recommending `enable_seqscan = off` or friends as a production fix rather than a diagnostic
- `VACUUM FULL` presented as routine maintenance (it takes `ACCESS EXCLUSIVE` and rewrites the table)
- Treating `REPEATABLE READ` as serializable, or `SERIALIZABLE` as free
- Trusting a book's stated default without checking it against PG 18
- Reproducing more than a short attributed quote from any source; synthesize in your own words
- Leaving a `>` blockquote in the chapter body
- An em dash in chapter text, or a spaced or double hyphen standing in for one

---

## After writing a chapter

1. Regenerate `docs/book/index.md`: `python scripts/sync_book_index.py`. It picks up the new
   chapter from its `**Learning-path topic:**` header line and updates the status and the
   progress count. Do **not** hand-edit that file; it is generated.
2. Update `docs/learning-path.md`: flip the topic heading `⬜` → `✅`.
3. Add the chapter to `zensical.toml` nav under `Book`.
4. Append new terms to `docs/reference/glossary.md` with the chapter link.
5. Record any newly verified version facts in `docs/research-cache/version-facts.md`.
6. Run the Phase 3 coverage audit (`learning-path/references/phase3-book.md` Step 5c): re-check
   every cited note against the written chapter for dropped content, not just false claims.
7. Run Phase 5 of the `learning-path` skill to reconcile the path against what the chapter revealed.
8. Expand acronyms: `python scripts/expand_acronyms.py --check`, **after any edit to a chapter,
   the learning path or a source note, not only after a new chapter**. It covers `docs/book/`,
   `docs/learning-path.md` and `docs/sources/`. If it fails, run it without `--check`, read the
   diff (expansions plus paragraphs re-flowed to 100 columns) and stage the result. Nothing else
   runs this check (there is no git hook, by choice), so this step is the only gate. It was
   missing until 2026-10-01, and the check failed unnoticed for two weeks.
9. Check that the book holds no em dash, **after any edit to a chapter**: the command and the rule
   are in "Sentences without em dashes". Nothing else runs this check.
10. Verify the site builds: `.venv\Scripts\python -m zensical build`. Expect only the two
    known `sources/dombrovskaya/` intra-page anchor warnings; anything else is yours.
11. Verify no dead links: `.venv\Scripts\python scripts/check_links.py site`. The build only
    sees markdown links, so wikilinks that resolve to the `/sources/<slug>/` fallback ship as
    silent 404s unless this runs.
