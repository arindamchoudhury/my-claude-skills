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
5. **Regenerate the matrix:** `python tools/spark_source_map/gen_coverage.py`
6. **Wire** the new topic page into `zensical.toml` nav under `Spark Source Map → Topic traces`;
   commit both the topic page and the updated `index.md`.

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
6. **Regenerate the matrix:** `python tools/spark_source_map/gen_coverage.py`
   This auto-appends any `propose:` blocks to `learning-path.md`. Review new stubs; edit
   `what`/`why`/`learn it with` as needed. Pass `--no-write-proposals` to skip.
7. **Wire** the new sweep page into `zensical.toml` nav under `Spark Source Map → Sweeps`;
   commit both the sweep page and any `learning-path.md` additions.

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
What the chapter covers vs what the source reveals beyond it.
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
- Blockquotes (`>`) instead of bare `!!!` admonitions after a list.
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
