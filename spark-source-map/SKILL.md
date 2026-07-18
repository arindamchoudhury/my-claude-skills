---
name: spark-source-map
description: >
  Use when mining the Apache Spark source to drive the personal Spark book at
  C:\opt\learn\spark\notes. Triggers on: "generate the config catalog", "refresh
  the spark configs", "trace B7", "trace the joins topic", "sweep core", "sweep
  sql/catalyst", "map the joins code paths", "what configs relate to <topic>",
  "update the source coverage matrix", or any request to build/refresh the
  source-derived config catalog, per-topic traces, source sweeps, or the
  topic-coverage matrix under docs/reference/spark-source-map/. Three engines:
  a deterministic Python config parser (whole repo), a topic-first LLM tracer
  (one learning-path topic at a time), and a source-first LLM sweeper (one
  subsystem at a time for gap discovery). Spark source is at C:\opt\learn\spark\spark.
---

# Spark Source Map — Skill

Hybrid pipeline for mining Apache Spark source to drive the spark-book.

- **Topic traces** (`trace <topic-code>`) — start from a learning-path topic, find the backing source, configs, and code paths. Topic pages live at `docs/reference/spark-source-map/topics/<code>.md`.
- **Source sweeps** (`sweep <subsystem>`) — scan a subsystem for concepts not yet covered by any topic. Sweep pages live at `docs/reference/spark-source-map/sweeps/<slug>.md`. Generates proposals auto-appended to `learning-path.md`.
- **Config catalog** (`gen configs`) — deterministic whole-repo config parser. Used as a lookup by both engines.

The learning path is never assumed complete — sweeps expand it by surfacing unknown unknowns.

---

- Design spec: `C:\opt\learn\spark\notes\docs\superpowers\specs\2026-06-06-spark-source-map-design.md`
- Spark source: `C:\opt\learn\spark\spark` (verify Spark facts here, not the web)
- Artifacts: `C:\opt\learn\spark\notes\docs\reference\spark-source-map\`
- Tools: `C:\opt\learn\spark\notes\tools\spark_source_map\`
- Requires: `python`, `pyyaml` (`pip install pyyaml`); tests need `pytest`.

> **Version caveat (check every run):** the local checkout may be on `master`
> (`spark_version: 5.0.0-SNAPSHOT` in the catalog), while the book targets Spark 4.1.x.
> To target 4.1.x, `git -C C:\opt\learn\spark\spark checkout v4.1.x` before `gen configs`.
> The catalog `meta.spark_version` always records what was actually parsed.

## Four verbs

### `gen configs` — refresh the whole-repo config catalog (deterministic, cheap)

1. Run from the notes repo root:
   ```
   python tools/spark_source_map/gen_configs.py \
     --source C:/opt/learn/spark/spark \
     --out-dir docs/reference/spark-source-map/configs
   ```
2. Read the printed summary: `spark <version>: <N> configs, <U> unparsed`.
   - **Floor check:** N should be > 1000. A sharp drop means a parser regression — run
     `python -m pytest tools/spark_source_map/test_gen_configs.py` and fix before committing.
   - If `U > ~5`, open `catalog.yaml` `unparsed:` and check they are genuinely hard
     (nested string interpolation, indirect constant refs). Never hand-edit `catalog.yaml`.
3. Run `coverage` (below) so the sweep-status table picks up new config counts.
4. Wire `configs/index.md` into `zensical.toml` nav if not already present; commit.

This regenerates `configs/catalog.yaml` (source of truth) and `configs/index.md` (rendered,
grouped by subsystem → prefix, GitHub-linked). Re-runnable per Spark version in seconds.

---

### `trace <topic-code>` — topic-first trace (LLM, on-demand)

For each learning-path topic (B7, I4, A11, …), find the source code, configs, and key classes
that back it. One topic per run.

1. **Pre-flight:** look up the topic in `docs/learning-path.md` to get its title and level.
   Confirm which repo(s) are relevant (most topics: `C:\opt\learn\spark\spark`; Delta Lake
   topics: check the local Delta repo; Dagster/Unity Catalog: note they require network access
   or local clones).
2. **Config slice:** grep `configs/catalog.yaml` for keyword matches (e.g. for B7 "joins":
   `autoBroadcastJoin`, `join.prefer`, `adaptive` — take the relevant slice).
3. **Dispatch a tracer subagent** (see "Topic tracer subagent brief"). Give it: the topic code,
   title, and description from `learning-path.md`; the config slice; the Spark source path.
4. **Write** `docs/reference/spark-source-map/topics/<code>.md` using the topic page contract
   below. `<code>` is the topic code in lowercase (e.g. `B7` → `b7.md`).

   **Trace the whole subsystem, not one path through it.** The stopping condition is *the
   subsystem is mapped* — never *the page has enough material*. Following the happy path from the
   user-facing call to the terminal action produces a page that reads complete while omitting the
   layers where most real failures live. Before writing, walk every layer the data crosses and
   confirm you have anchors in each:

   | Layer | Ask |
   |---|---|
   | **Registration / lookup** | How does a name (`"parquet"`, a strategy, a function) become a class? `ServiceLoader`, registries, config-driven overrides |
   | **Discovery / planning** | What runs on the driver before any task? Listing, inference, pruning, plan rewrites — and what makes it slow |
   | **Splitting / distribution** | What decides the unit of parallelism, and by what formula? |
   | **Per-record execution** | The actual parse/compute path on the executor, including codegen vs interpreted |
   | **Error and edge paths** | Malformed input, missing files, retries, fallbacks. Which failures are *silent* |
   | **Termination / commit** | How does the operation finish, and what are its atomicity guarantees? |
   | **Alternative APIs** | V1 vs V2, classic vs Connect, the deprecated form the books still teach |

   Not every topic has all seven, but you must have *asked* about each. Two heuristics: a config in
   the slice you cannot tie to an anchor means an unmapped layer; and any behaviour that fails
   silently deserves an anchor precisely because nothing else will surface it.
5. **Reconcile the learning-path topic — always, every trace.** A trace that only produces a topic
   page is half-finished: the path is what the user actually reads when deciding what to study, and
   it will not mention the trace unless you put it there. Open `docs/learning-path.md` at this
   topic and update, in this order:

   - **"Learn it with" — the important one.** Add the trace as the last entry, after the books and
     docs, with one line on what reading it buys:

     ```markdown
     N. **Source trace — [<CODE> in the source map](reference/spark-source-map/topics/<code>.md)** —
        <what it shows: the code path, which plan node each verb produces, where the failure modes live>
     ```

     Then add any **official docs page the trace proved the topic needs**. A trace surfaces these
     reliably: every config in the trace's table has a docs page, and every layer in the code path
     (commit protocol, parse modes, catalog, scheduling) usually does too. If the topic cites one
     docs page while the trace lists twenty configs across five subsystems, the topic is
     under-served — fix it here. The book-and-docs rule still applies: both, always.
   - **Scope line ("What it is").** If the trace showed the scope is wrong or has drifted — a second
     implementation exists, a default flipped, the API split in two — correct it. This is the most
     common silent staleness in a path.
   - **Milestone.** Strengthen it with something the trace makes checkable: name the function that
     enforces a behaviour, predict which of two paths runs, explain a value the source determines.
   - **Callouts.** Any behaviour the trace found that the cited books get *wrong* deserves an
     `!!! warning`; new surface they simply lack gets an `!!! info` or `!!! note`.

   State in your final summary what changed in the path, not just in the trace.
6. **Mark the chapter 🔄 if the trace changed anything.** A trace that opens a chapter gap, or a
   learning-path edit that adds material the chapter does not cover, leaves the written chapter
   stale — and a chapter still showing ✅ is a claim that it is current. Whenever the "Not in
   spark-book" section is non-empty, or you add a topic resource/callout covering something the
   chapter omits, flip **all three** places together:
   - `docs/spark-book/index.md` — the status cell, ✅ → 🔄
   - the chapter file — a dated `> 🔄 **Needs revisiting — …**` banner under the header block,
     saying what specifically drifted and linking the trace
   - `docs/learning-path.md` — the topic heading, `### ✅ <code>` → `### 🔄 <code>`, and the
     "Carrying 🔄" summary line

   Distinguish **wrong** from **incomplete** in the banner, and say which this is. A chapter with
   a false claim (a changed default, a dropped version requirement) must be cleared before the
   chapter is trusted; one merely missing new surface is safe to read as-is. Collapsing the two
   into "needs update" loses the only distinction that decides what to fix first.
7. **Regenerate the matrix:** `python tools/spark_source_map/gen_coverage.py`
8. **Wire** the new topic page into `zensical.toml` nav under `Spark Source Map → Topic traces`;
   commit the topic page, the updated `index.md`, the learning-path edits from step 5, and any
   🔄 status changes from step 6 — one commit, so the path and the trace never disagree in history.

> **Re-tracing an existing topic.** Most traces after the first are refreshes against a newer
> Spark. Do not just bump the tag in the GitHub links — `file:line` anchors drift heavily between
> releases (26 of 33 moved for B3 between 4.1.2 and 4.2.0), and a stale anchor still renders
> perfectly on GitHub while pointing at the wrong code. Re-verify every anchor against the local
> checkout and confirm the content at each new line, then record `spark_version`, `traced_at`, and
> a refresh-log table in the topic page.

---

### `sweep <subsystem>` — source-first discovery sweep (LLM, on-demand)

For each Spark subsystem, scan all major concepts and identify which have no learning-path topic.
One subsystem per run. This expands the learning path with things you didn't know to include.

**Available subsystems** (from `groups.yaml`; config counts from catalog at v4.1.2):

| Subsystem | Configs | Groups |
|---|---|---|
| `sql/catalyst` | 656 | analysis, optimizer, planner, expressions, types-parser |
| `core` | 533 | rdd-layer, execution-engine, shuffle-memory, storage-serializer, infra |
| `resource-managers/kubernetes` | 81 | driver-executor, auth-networking |
| `resource-managers/yarn` | 59 | am-executor |
| `streaming` | 28 | structured-streaming, dstream |
| `sql/connect` | 14 | client-server, declarative-pipelines |
| `sql/hive` | 11 | hive-metastore |
| `connector/kafka-0-10` | 8 | consumer |
| `connector/kafka-0-10-sql` | 8 | source-sink |
| `connector/profiler` | 7 | async-profiler |

Sweep in book-priority order: `sql/catalyst` and `sql/core` first (highest config density, most
relevant to the book). For large subsystems pick one group per run.

Sweeps already done: `core — rdd-layer` (partial).

1. **Pre-flight:** confirm `configs/catalog.yaml` exists and note its `meta.spark_version`.
2. **Scope check.** Big subsystems (`sql/catalyst`, `sql/core`) are too large for one pass.
   Enumerate the candidate concepts (from `groups.yaml` scope field + package layout), then ask
   the user to pick a group. A single-group run sets `status: partial`.
3. **Config slice:** extract all configs whose `subsystem` matches from `catalog.yaml`.
4. **Dispatch a sweeper subagent** (see "Sweeper subagent brief"). Give it: the subsystem path,
   the config slice, `docs/learning-path.md` (for existing topic codes), and `groups.yaml`
   (for group scope definitions).
5. **Write** `docs/reference/spark-source-map/sweeps/<slug>.md` using the sweep page contract
   below. `<slug>` is the subsystem with `/` → `-` (e.g. `sql/core` → `sql-core`).

   **Sweep the subsystem, not the concepts you already recognise.** The stopping condition is
   *the group's scope is covered* — never *the page has enough concepts*. A sweep exists to find
   unknown unknowns, so the concept you cannot name yet is the one that justifies the run. Two
   completeness dimensions, and a sweep needs both:

   - **Breadth — did you visit everything in scope?** Walk the packages named in the group's
     `scope` field and list the classes; a package you never opened is a concept you cannot have
     found. Every config in the slice must tie to a concept — one that doesn't means an unvisited
     area, and that check is mechanical, so run it before writing.
   - **Depth — for each concept, the same layers a trace demands.** Do not stop at the entry point
     and the happy path. For each concept ask: registration/lookup, discovery/planning,
     splitting/distribution, per-record execution, **error and edge paths** (especially anything
     that fails *silently*), termination/commit and its guarantees, and alternative APIs (V1 vs V2,
     classic vs Connect). A concept recorded as an entry point and one class is a placeholder, not
     a mapped concept.

   Record what you *chose not to* cover. A sweep that silently omits half its scope is worse than
   one marked `status: partial` with the remainder named — the first looks finished.
6. **Reconcile every learning-path topic the sweep touched — always.** A sweep maps concepts to
   topic codes, so it tells you exactly which topics to revisit; the generator only handles the
   *new* ones. Two jobs:

   - **Existing topics** (any concept whose `topics:` list is non-empty). For each, add to its
     **"Learn it with"** a sweep entry — `**Source sweep — [<subsystem> sweep](reference/spark-source-map/sweeps/<slug>.md)**` — plus any official docs page the sweep proved the topic
     needs, and correct the scope line if the sweep showed it has drifted. Same book-and-docs rule
     as a trace. A concept that maps to a topic but reveals something the topic never mentions is a
     path gap, not just a source finding.
   - **Proposed topics** (`propose:` blocks, auto-appended by `gen_coverage.py`). The generator
     writes a stub with a placeholder resource list. **Never leave it as generated** — a stub whose
     only entry is "Spark-docs — see official documentation" and whose milestone is `TBD` fails the
     book-and-docs rule and reads as noise. Fill in `what` / `why`, cite a real book chapter or an
     explicit "No book covers this" callout, cite the specific docs page, and write a concrete
     milestone.

   Then flip any written chapter the sweep left behind to 🔄, per the trace verb's step 6.
7. **Regenerate the matrix:** `python tools/spark_source_map/gen_coverage.py`
   This auto-appends any `propose:` blocks to `learning-path.md`. Pass `--no-write-proposals` to skip.
8. **Wire** the new sweep page into `zensical.toml` nav under `Spark Source Map → Sweeps`;
   commit the sweep page, the learning-path edits from step 6, and any 🔄 status changes together.

---

### `coverage` — regenerate the landing page + matrix (deterministic, cheap)

```
python tools/spark_source_map/gen_coverage.py
```

Rebuilds `docs/reference/spark-source-map/index.md` from:
- `learning-path.md` (the 40 topics)
- `spark-book/index.md` (topic → chapter mapping)
- `configs/catalog.yaml` (subsystem config counts)
- `topics/*.md` (topic-first traces — drives coverage matrix)
- `sweeps/*.md` (source-first sweeps — drives gap discovery and sweep-status table)

Also auto-appends `propose:` blocks from sweep gaps to `learning-path.md` (pass
`--no-write-proposals` to skip). Run after any trace, sweep, or `gen configs`, or whenever
the learning path changes. Never hand-edit `index.md`.

---

## Knowledge pipeline (read before tracing)

There are three tiers — understanding them is required for the "Chapter notes" section:

1. **Learning path** (`docs/learning-path.md`) — advises which external books to read for each topic (Rioux Ch X, LS2e Ch Y, etc.). Does not represent the synthesis.
2. **Book notes** (`docs/books/<slug>/chapters/`) — raw notes taken while reading each external book.
3. **Spark book** (`docs/spark-book/ch<NN>-*.md`) — the synthesized personal book. This is the *output* of all learning. The spark-book `index.md` maps each topic code to its chapter(s).

The "Chapter notes" section in a topic trace is a **gap analysis against the spark-book**: what did the source reveal that the spark-book already has, and what does the spark-book still need? It is never a comparison against external books (Rioux, LS2e, SDG) — those feed into the spark-book but are not the synthesis target.

---

## Topic page contract

The topic tracer writes Markdown with this front matter — `gen_coverage.py` reads it:

```markdown
---
topic: B7
title: "Joins: Types and Mechanics"
status: complete          # or: partial
chapter: 10               # chapter from spark-book/index.md (optional)
repos: [apache/spark]     # source repos consulted
configs:
  - spark.sql.autoBroadcastJoinThreshold
  - spark.sql.join.preferSortMergeJoin
  - spark.sql.adaptive.enabled
sources:
  - subsystem: sql/catalyst
    concepts: [JoinSelection]
  - subsystem: sql/core
    concepts: [SortMergeJoinExec, BroadcastHashJoinExec]
---

## What it is
One paragraph — the concept, not the code.

## Code path
`Dataset.join` → `Analyzer (ResolveJoin)` → `JoinSelection` → `BroadcastHashJoinExec` / `SortMergeJoinExec`

## Key source locations

- [JoinSelection.scala:42](https://github.com/apache/spark/blob/v4.1.2/sql/core/src/main/scala/org/apache/spark/sql/execution/JoinSelection.scala#L42) — strategy selection
- [SortMergeJoinExec.scala:89](https://github.com/apache/spark/blob/v4.1.2/sql/core/src/main/scala/org/apache/spark/sql/execution/joins/SortMergeJoinExec.scala#L89) — execution

## Relevant configs

| Config | Default | Effect |
|---|---|---|
| `spark.sql.autoBroadcastJoinThreshold` | 10MB | Threshold for broadcast hash join |

## Chapter notes

Gap analysis against the spark-book chapter(s) for this topic.
Read `docs/spark-book/index.md` to find which chapter(s) map to this topic code,
then read those chapter files. Produce two sections:

### Already in spark-book ✅
Bullet list of what the source trace confirms is already covered. Be specific —
name the section or concept in the spark-book that covers it.

### Not in spark-book — needs addition ❌
Bullet list of what the source trace found that is NOT yet in the spark-book.
For each gap: one sentence naming the missing concept and why it matters.
These are the additions that should be made to the spark-book chapter.
```

## Sweep page contract

The sweeper writes Markdown with this front matter — `gen_coverage.py` reads it:

```markdown
---
subsystem: sql/core
spark_version: "4.1.2"    # copy from catalog meta
swept_at: 2026-06-06       # date this sweep was run (ISO 8601)
group: joins-and-agg       # optional; set when sweeping a large subsystem in parts
all_groups: [joins-and-agg, streaming-integration, connector-v2]  # all planned groups; only on first page
status: complete            # or: partial
concepts:
  - name: joins
    topics: [B7, A3]        # learning-path codes this concept backs; [] = discovery gap
  - name: aqe
    topics: [A2]
  - name: vectorized-reader
    topics: []              # gap: no topic yet — add propose: block
    propose:
      code: A12             # next unused code for this level (check learning-path.md)
      level: Advanced       # Beginner | Intermediate | Advanced | Expert
      title: "Vectorized Reads and Columnar Execution"
      what: "One sentence: what this concept is."
      why: "One sentence: why a practitioner needs to understand it."
---

## Joins
**What it is:** one paragraph.
**Code path:** `Dataset.join` → Analyzer (ResolveJoin) → `JoinSelection` → `SortMergeJoinExec` / `BroadcastHashJoinExec`
**Anchor files:** [JoinSelection.scala](https://github.com/apache/spark/blob/v4.1.2/...)
**Configs:** `spark.sql.autoBroadcastJoinThreshold`, `spark.sql.join.preferSortMergeJoin`
**Maps to topics:** B7 (Joins), A3 (Join Strategies)
```

## Topic tracer subagent brief

Dispatch a `feature-dev:code-explorer` (or general-purpose) subagent, read-only, with:

> Trace learning-path topic **`<code>` — `<title>`** in Apache Spark at
> `C:\opt\learn\spark\spark`.
>
> For this topic: identify the key source classes and their entry points, trace the
> analysis/planning/execution path, and annotate each class with `file:line` anchors.
> Pull relevant configs from the supplied catalog slice.
>
> **Map the whole subsystem, not one path through it.** You are done when the subsystem is
> mapped, not when you have enough material for a page — those are different, and the second
> produces a page that reads complete while omitting the layers where real failures live.
> Walk every layer the data crosses and report anchors for each that applies:
> registration/lookup (how a name becomes a class), discovery/planning (what runs on the
> driver first, and what makes it slow), splitting (what sets the unit of parallelism, by
> what formula), per-record execution, **error and edge paths** (malformed input, missing
> files, retries, fallbacks — especially anything that fails *silently*), termination/commit
> (including atomicity guarantees), and alternative APIs (V1 vs V2, classic vs Connect).
>
> Two checks before you return: every config in the supplied slice should tie to an anchor,
> or you have found an unmapped layer; and any silent-failure behaviour needs an anchor
> precisely because nothing else will surface it.
>
> **Chapter notes — gap analysis against the spark-book:**
> Read `docs/spark-book/index.md` to find which spark-book chapter(s) map to topic code
> `<code>`. Then read those chapter file(s). Produce a gap analysis with two subsections:
> - **Already in spark-book ✅** — what the source trace confirms is already covered;
>   be specific about the section or concept in the spark-book.
> - **Not in spark-book — needs addition ❌** — what the source trace found that is NOT
>   yet in the spark-book; one sentence per gap naming the concept and why it matters.
> The spark-book is the synthesis *output*, not a source to compare against. Never write
> "the Rioux book covers X" — the gap analysis is always against the spark-book.
>
> Return the topic page in the exact front-matter contract above (fields: `topic`, `title`,
> `status`, `chapter`, `repos`, `configs`, `sources`), followed by the prose sections:
> "What it is", "Code path", "Key source locations", "Relevant configs", "Chapter notes".
>
> **Be source-faithful:** if you cannot confidently trace a path, say so — never invent one.
> For partial traces, set `status: partial` and note which parts are missing.

## Sweeper subagent brief

Dispatch a `feature-dev:code-explorer` (or general-purpose) subagent, read-only, with:

> Sweep the **`<subsystem>`** subsystem of Apache Spark at `C:\opt\learn\spark\spark`.
>
> For each major concept in scope (see supplied groups.yaml scope field): identify the
> entry point, the analysis/planning path, and the physical execution classes — with
> `file:line` anchors. Pull the relevant configs from the supplied catalog slice. Map each
> concept to learning-path topic codes (B/I/A/E) from the supplied `learning-path.md`;
> mark `[]` when a concept backs no topic (a discovery gap).
>
> **Cover the subsystem, not the concepts you recognise.** The point of a sweep is unknown
> unknowns, so a concept you cannot name yet is exactly the one worth reporting. Include the
> error/fallback paths and the commit or termination logic, not just the success path — and
> treat any config in the slice you cannot tie to a concept as evidence of something you have
> not found yet.
>
> For every gap concept, add a `propose:` block with: the next unused topic code for the
> appropriate level (check the highest existing code in that level first), a `level`
> (Beginner/Intermediate/Advanced/Expert), a concise `title`, a one-sentence `what`, and a
> one-sentence `why`. These proposals will be appended to `learning-path.md` automatically.
>
> Return the sweep page in the exact front-matter contract above.
> **Be source-faithful:** if you cannot confidently trace a path, say so — never invent one.

## Conventions (project memory)

- Blank line before every bullet list (Zensical won't render otherwise).
- Mermaid for diagrams, never ASCII art.
- **Callouts are admonitions.** Use `!!! note` / `!!! warning` / `!!! info` (with a quoted title and
  a 4-space-indented body) for every note, caveat, or aside — in topic pages, sweep pages, chapters,
  and the learning path alike. Pick the type by what the reader must do: `warning` for something
  that will bite them, `info` for a naming or behaviour clarification, `note` for additive context.
  - **One exception:** directly after a bullet list, a bare `!!!` block does not render — put the
    admonition before the list, separate it with a paragraph, or fall back to a `>` blockquote there.
  - Chapter *metadata* headers (`> *Learning-path topic: …*`) stay blockquotes; they are a header
    block, not a callout.
- Every new **page** must be added to `zensical.toml` nav. Data files (`catalog.yaml`) and
  `.gitkeep` are not pages — leave them out of nav.
- Verify all Spark facts against the **local source**, not the web.
- Never hand-edit generated files (`catalog.yaml`, `configs/index.md`, `index.md`) — re-run
  the generator. Topic and sweep pages are authored; their front matter feeds `gen_coverage.py`.

## Tests

```
python -m pytest tools/spark_source_map/test_gen_configs.py
```

Covers the config parser (type/default/version/doc extraction, constant-key resolution,
dynamic-key flagging) plus a real-source floor assertion (`entry_count > 1000`, known configs
present). Run after any change to `gen_configs.py`.
