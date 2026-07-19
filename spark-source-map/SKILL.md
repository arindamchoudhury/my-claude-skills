---
name: spark-source-map
description: >
  Use when mining the Apache Spark source to drive the personal Spark book at
  C:\opt\learn\spark\notes. Triggers on: "generate the config catalog", "refresh
  the spark configs", "trace B7", "trace the joins topic", "sweep core", "sweep
  sql/catalyst", "map the joins code paths", "what configs relate to <topic>",
  "update the source coverage matrix", "regroup core", "add a group for X",
  "what isn't covered by any group", "check the carving", "groups.yaml is
  stale", "Spark 4.3 is out", "bump the source map to the new Spark", or any
  request to build/refresh the source-derived config catalog, per-topic traces,
  source sweeps, the group carving in groups.yaml, or the topic-coverage matrix
  under docs/reference/spark-source-map/. Also fires when a Spark release lands
  and the map must be re-verified against it. Three engines: a deterministic
  Python config parser (whole repo), a topic-first LLM tracer (one learning-path
  topic at a time), and a source-first LLM sweeper (one subsystem at a time for
  gap discovery), plus checker-driven maintenance of the hand-authored
  groups.yaml. Spark source is at C:\opt\learn\spark\repos\spark.
---

# Spark Source Map — Skill

Hybrid pipeline for mining Apache Spark source to drive the spark-book.

- **Topic traces** (`trace <topic-code>`) — start from a learning-path topic, find the backing source, configs, and code paths. Topic pages live at `docs/reference/spark-source-map/topics/<code>.md`.
- **Source sweeps** (`sweep <subsystem>`) — scan a subsystem for concepts not yet covered by any topic. Sweep pages live at `docs/reference/spark-source-map/sweeps/<slug>.md`. Generates proposals auto-appended to `learning-path.md`.
- **Config catalog** (`gen configs`) — deterministic whole-repo config parser. Used as a lookup by both engines.

The learning path is never assumed complete — sweeps expand it by surfacing unknown unknowns.

---

- Design spec: `C:\opt\learn\spark\notes\docs\superpowers\specs\2026-06-06-spark-source-map-design.md`
- Spark source: `C:\opt\learn\spark\repos\spark` (verify Spark facts here, not the web)
- Artifacts: `C:\opt\learn\spark\notes\docs\reference\spark-source-map\`
- Tools: `C:\opt\learn\spark\notes\tools\spark_source_map\`
- Requires: `python`, `pyyaml` (`pip install pyyaml`); tests need `pytest`.

> **Version caveat (check every run):** the checkout is on `v4.2.0` and the catalog was
> parsed from it (`meta.spark_version: 4.2.0`, 1558 configs, 2026-07-18). The checkout may
> drift to `master` (`spark_version: 5.0.0-SNAPSHOT`); to pin a release,
> `git -C C:\opt\learn\spark\repos\spark checkout v4.2.0` before `gen configs`.
> The catalog `meta.spark_version` always records what was actually parsed — trust it over
> this line, and over the config counts in the subsystem table below.

## Six verbs

## Autonomy contract

A verb is a whole job, not a step. Run it to completion: every command, every checker fixed to
green, every document the change invalidated updated, committed. The user asked for the outcome,
not a plan.

**Ask only when one of these is true.** Each is observable — check it, don't estimate your
confidence:

1. **The change alters the learning path's taxonomy** — adding, retitling, renumbering or
   reordering a topic, or deciding a topic is worth studying. That is the user's curriculum.
   (Filling in a `propose:` block the generator already appended is *not* this: finish it.)
2. **Two options are defensible and the source cannot decide between them** — which group owns
   a package, whether a package is plumbing or worth a group, which of several topics a concept
   backs. Bring the options with file counts and a recommendation.
3. **A fix requires inventing a fact** — a checker names a class that exists nowhere in the
   checkout, a config has no discoverable default, a trace cannot follow a path. Say what you
   could not verify rather than writing a plausible guess.
4. **The action reaches outside the repo or is hard to undo** — push, force-push, deleting a page
   with content in it, rewriting history, touching anything outside `C:\opt\learn\spark`.

**Proceed without asking in every other case.** Specifically, these are not doubt:

- The next command in the verb is determined → run it.
- A checker named a specific fix (`add the module to `modules:``, `fix the name`) → apply it.
- A doc, table or nav entry now disagrees with the change → sync it.
- The commit is repo-local and inside the verb's scope → commit it.
- You are unsure whether the user wants the *whole* verb → they asked for the verb; do all of it.

**Report, don't ask, when something surprised you.** A wrong scope, a false positive in your own
check, a regression you caused — fix it, then say plainly what it was in the summary. Discovering
you were wrong is not a reason to stop and ask; it is a reason to correct and disclose.

Two failure modes to avoid, both of which read as helpful:

- **Handing back a checklist.** "Here are the commands to run" is a half-done verb. Run them.
- **Asking to confirm the obvious.** "Shall I regenerate index.md?" — the verb says to. Do it.

### `gen configs` — refresh the whole-repo config catalog (deterministic, cheap)

1. Run from the notes repo root:
   ```
   python tools/spark_source_map/gen_configs.py \
     --source C:/opt/learn/spark/repos/spark \
     --out-dir docs/reference/spark-source-map/configs
   ```
2. Read the printed summary: `spark <version>: <N> configs, <U> unparsed`.
   - **Floor check:** N should be > 1000. A sharp drop means a parser regression — run
     `python -m pytest tools/spark_source_map/test_gen_configs.py` and fix before committing.
   - If `U > ~5`, open `catalog.yaml` `unparsed:` and check they are genuinely hard
     (nested string interpolation, indirect constant refs). Never hand-edit `catalog.yaml`.
3. **Check for drift** — a new Spark release is the moment hand-authored scopes go stale:
   ```
   python tools/spark_source_map/check_drift.py
   ```
   Exits 1 and names the offenders. It verifies `groups.yaml`'s `_meta.spark_version` against
   the catalog, that every subsystem is a real module, and that every class and package named
   in a group `scope` still exists **inside that group's modules**. When a class has moved
   modules (Spark 4.x did this repeatedly — `StorageLevel` → `common/utils`, `DataType` →
   `sql/api`), either add the owning module to that group's `modules:` list or fix the name;
   then bump `_meta.spark_version` / `_meta.verified_at`. Warnings about sweep/topic pages
   recorded against an older Spark are advisory — they flag anchor drift, not a blocker.

   Then run the inverse check — what exists that no scope names:
   ```
   python tools/spark_source_map/check_drift.py --coverage
   ```
   A package no group claims can never be swept, so its concepts can never surface as
   proposals; the gap conceals itself. Advisory, never fails: `util/`, `errors/`, `test/`
   and `dsl/` are plumbing that rightly has no group. Judge each — don't auto-add.

   The same report flags **two groups claiming the identical package path** — both sweeps
   would walk the same code. Parent/child is fine and is not flagged (`execution/` vs
   `execution/joins/`). When the sharing is deliberate, set `shared_scope: true` on each
   group involved; `resource-managers/kubernetes` splits `k8s/` by theme this way.
4. Run `coverage` (below) so the sweep-status table picks up new config counts.
5. Wire `configs/index.md` into `zensical.toml` nav if not already present; commit.

This regenerates `configs/catalog.yaml` (source of truth) and `configs/index.md` (rendered,
grouped by subsystem → prefix, GitHub-linked). Re-runnable per Spark version in seconds.

---

### `trace <topic-code>` — topic-first trace (LLM, on-demand)

For each learning-path topic (B7, I4, A11, …), find the source code, configs, and key classes
that back it. One topic per run.

1. **Pre-flight:** look up the topic in `docs/learning-path.md` to get its title and level.
   Confirm which repo(s) are relevant (most topics: `C:\opt\learn\spark\repos\spark`; Delta Lake
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

### `sweep <subsystem> [<group>]` — source-first discovery sweep (LLM, on-demand)

Scan a subsystem for major concepts and identify which have no learning-path topic. **One group
per run** — this expands the learning path with things you didn't know to include.

Both invocations are valid:

- `sweep core execution-engine` — sweep that group directly.
- `sweep core` — no group named; run the scope check in step 2 and ask the user to pick one.

To see what groups a subsystem has, and which are already done:

```
python tools/spark_source_map/gen_coverage.py --list-groups <subsystem>
```

Prints each group's topics, scope, swept status, Spark version, and page filename; omit the
subsystem for all of them. Read-only. Use it in pre-flight rather than reading `groups.yaml`
by hand — it is the only view that also shows what has already been swept.

**Available subsystems** (from `groups.yaml`):

| Subsystem | Groups |
|---|---|
| `sql/catalyst` | analysis, optimizer, planner, expressions, types-parser, framework |
| `sql/core` | query-execution, joins-exec, adaptive, datasources, agg-window-exchange, python-arrow, streaming-exec, classic-api, sql-scripting |
| `core` | rdd-layer, execution-engine, shuffle-memory, storage-serializer, infra, rpc-resources, api-bridge |
| `sql/pipelines` | graph, autocdc, pipeline-runtime |
| `sql/connect` | client-server, declarative-pipelines |
| `resource-managers/kubernetes` | driver-executor, auth-networking |
| `resource-managers/yarn` | am-executor |
| `sql/hive` | hive-metastore |
| `streaming` | dstream |
| `connector/kafka-0-10` | consumer |
| `connector/kafka-0-10-sql` | source-sink |
| `connector/profiler` | async-profiler |

**Config counts deliberately live only in `index.md`.** The sweep-status table there is generated
from `catalog.yaml` on every `coverage` run, so it is always right; a copy here would be a second
number to maintain and would silently rot at the next release (this table carried v4.1.2 counts
well past the 4.2.0 catalog refresh). Read counts there, not here.

`sql/core` and `sql/pipelines` register no configs of their own — nearly every SQL config is
declared in catalyst's `SQLConf.scala` — but they hold the physical execution for most of the
book's topics and are the highest-value sweeps.

!!! warning "Structured Streaming is not in the `streaming` subsystem"

    The `streaming` module is DStream only. Structured Streaming executes in `sql/core`
    (`execution/streaming/runtime/`) and is covered by the `sql/core — streaming-exec` group.

Sweep in book-priority order: `sql/catalyst` and `sql/core` first (highest config density, most
relevant to the book). For large subsystems pick one group per run.

Sweeps already done: `core — rdd-layer` (`status: complete`; the other four `core` groups are
still pending). Check the sweep-status table in `index.md` rather than trusting this line.

1. **Pre-flight:** confirm `configs/catalog.yaml` exists and note its `meta.spark_version`. Run
   `gen_coverage.py --list-groups <subsystem>` to see the groups and which are already swept.
2. **Scope check.** If the user named a group, confirm it exists in that listing and go. If not,
   show the groups with their scopes and ask which to sweep — never pick silently, and never
   attempt the whole subsystem. A run covering one group of several sets `status: partial`
   *for the subsystem*; the page's own `status:` describes whether that group's scope was
   fully covered.
3. **Config slice:** extract all configs whose `subsystem` matches from `catalog.yaml`.
4. **Dispatch a sweeper subagent** (see "Sweeper subagent brief"). Give it: the subsystem path,
   the config slice, `docs/learning-path.md` (for existing topic codes), and `groups.yaml`
   (for group scope definitions).
5. **Write** `docs/reference/spark-source-map/sweeps/<slug>.md` using the sweep page contract
   below. `<slug>` is the subsystem with `/` → `-`, then `-<group>` when the run covered one
   group (e.g. `core` + group `rdd-layer` → `core-rdd-layer.md`; `sql/catalyst` + `optimizer`
   → `sql-catalyst-optimizer.md`). **One page per group — never merge groups into one file.**
   `gen_coverage.py` keys the sweep-status table on `(subsystem, group)` and `group:` is a
   scalar, so a file holding two groups reports only one and the other stays `⬜ pending`.
   Filenames are otherwise meaningless to the generator — it globs `sweeps/*.md` and reads
   front matter — but they must be unique, hence the group suffix.

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

### `regroup <subsystem>` — recarve groups.yaml (hand-authored, checker-verified)

Triggers: "regroup core", "add a group for X", "groups.yaml is missing Y", "check the carving",
"what isn't covered by any group".

`groups.yaml` is hand-authored — no generator writes it, so nothing notices when its scopes
drift from the source or when a new package has no owner. A package no group claims can never
be swept, so the gap conceals itself.

1. **Survey.** `check_drift.py --coverage` for unclaimed packages and identical-path collisions;
   `gen_coverage.py --list-groups <subsystem>` for the current carving and what is already swept.
2. **Propose, then ask.** What deserves a group is editorial — it changes the sweep plan and the
   learning path. Bring a concrete proposal (new groups, extended scopes, with file counts and
   the topics each would back) and let the user choose. Note which unclaimed packages are
   plumbing you deliberately excluded (`util/`, `errors/`, `test/`, `dsl/`).
3. **Edit, avoiding the two YAML traps.** Numbers ascend within a subsystem; inserting after a
   `scope:` line orphans the following `description:` onto the new group, which `yaml.safe_load`
   accepts silently. Insert after `description:`, then verify with a duplicate-key-aware parse
   (the snippet is in the repo README, "Editing groups.yaml").
4. **Name real classes** — `WholeStageCodegenExec`, not "Whole-Stage CodeGen". A name is what
   makes a scope checkable. Then run `check_drift.py` and expect to be wrong: when a class
   legitimately lives in another module, add it to that group's `modules:` list rather than
   vaguening the scope. Loop until it exits 0.
5. **Re-run `--coverage`** to confirm the gap closed and no identical-path collision appeared.
   Declare deliberate sharing with `shared_scope: true`.
6. **Bump `_meta`** (`spark_version`, `verified_at`) and record *why* in `_meta.note` — nothing
   else captures the reasoning.
7. **Regenerate and sync.** `gen_coverage.py`, then update the group tables in the repo README
   and in this file — both are hand-copied and drift the moment a group is added.
8. **Commit** `groups.yaml` with the regenerated `index.md` and the doc updates, one commit.

---

### `new spark release <version>` — full release runbook

Triggers: "Spark 4.3 is out", "update to the new Spark", "bump the source map to <version>".

Run the seven-step runbook in the repo README ("When a new Spark version ships"), in order:
move the checkout to the tag; `gen_configs.py` plus the parser tests, checking the >1000 floor;
`check_drift.py` and fix every scope it names; `gen_coverage.py`; identify which topic and sweep
pages need re-tracing (**re-verify anchors against the checkout — never bump the tag in a URL**,
line numbers drift heavily and a stale anchor still renders fine on GitHub); reconcile
`learning-path.md`'s header, `spark-book/index.md` statuses and chapter version lines; commit
together.

Re-tracing pages is a `trace` run each, one topic per run — propose the list and let the user
pick, rather than doing all of them unasked.

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
spark_version: "4.2.0"    # the Spark the anchors were verified against
# version_pinned: "<reason>"   # set ONLY when an older spark_version is deliberate
#   rather than stale — e.g. Iceberg and Delta ship no Spark 4.2 module, so those
#   traces pin to 4.1. check_drift.py stops flagging the page as drifted.
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
# All planned groups for this subsystem, copied from groups.yaml in that order.
# Repeat it identically on EVERY page for the subsystem — gen_coverage.py takes the
# list from whichever page sorts first alphabetically, so a page that omits it or
# carries a stale list silently drops rows from the sweep-status table.
all_groups: [joins-and-agg, streaming-integration, connector-v2]
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
> `C:\opt\learn\spark\repos\spark`.
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

> Sweep the **`<subsystem>`** subsystem of Apache Spark at `C:\opt\learn\spark\repos\spark`.
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
  - Admonitions render correctly **anywhere**, including directly after a bullet or numbered list.
    An earlier version of this file claimed otherwise; that was a misdiagnosis of a missing
    `admonition` markdown extension in `zensical.toml`, fixed 2026-07-18. If an `!!!` block ever
    renders as literal text again, check the extension is still enabled before rewriting content.
  - Chapter *metadata* headers (`> *Learning-path topic: …*`) stay blockquotes; they are a header
    block, not a callout.
- Every new **page** must be added to `zensical.toml` nav. Data files (`catalog.yaml`) and
  `.gitkeep` are not pages — leave them out of nav.
- Verify all Spark facts against the **local source**, not the web.
- Never hand-edit generated files (`catalog.yaml`, `configs/index.md`, `index.md`) — re-run
  the generator. Topic and sweep pages are authored; their front matter feeds `gen_coverage.py`.
- **`groups.yaml` is hand-authored**, despite sitting beside two generated files. No tool writes
  it — `gen_configs.py` and `gen_coverage.py` only read it. Editing it directly is the *only* way
  to change it, and no generator run will notice when its scopes drift from the source. Its
  `_meta.spark_version` / `verified_at` record when the scopes were last walked against a
  checkout; re-verify and bump them whenever you re-point the catalog at a new Spark release,
  since nothing else will catch a stale scope. Group `scope` fields are package *hints* for a
  human or a sweeper subagent — not resolvable paths, so a literal path check will throw false
  positives.

## Tests

```
python -m pytest tools/spark_source_map/test_gen_configs.py
```

Covers the config parser (type/default/version/doc extraction, constant-key resolution,
dynamic-key flagging) plus a real-source floor assertion (`entry_count > 1000`, known configs
present). Run after any change to `gen_configs.py`.
