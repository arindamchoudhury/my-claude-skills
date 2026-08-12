# Topic traces — the `trace` verb

> Reference for the `spark-source-map` skill. Load it when running a `trace <topic-code>`.
> Read `SKILL.md` first — it holds the design intent and the autonomy contract that govern
> everything here.

## Knowledge pipeline (read before tracing)

There are three tiers — understanding them is required for the "Chapter notes" section:

1. **Learning path** (`docs/learning-path-v2.md`) — advises which external books to read for each topic (Rioux Ch X, LS2e Ch Y, etc.). Does not represent the synthesis.
2. **Book notes** (`docs/books/<slug>/chapters/`) — raw notes taken while reading each external book.
3. **Spark book** (`docs/spark-book/ch<NN>-*.md`) — the synthesized personal book. This is the *output* of all learning. The spark-book `index.md` maps each topic code to its chapter(s).

The "Chapter notes" section in a topic trace is a **gap analysis against the spark-book**: what did the source reveal that the spark-book already has, and what does the spark-book still need? It is never a comparison against external books (Rioux, LS2e, SDG) — those feed into the spark-book but are not the synthesis target.

---

---

### `trace <topic-code>` — topic-first trace (LLM, on-demand)

For each learning-path topic (B7, I4, A11, …), find the source code, configs, and key classes
that back it. One topic per run.

1. **Pre-flight:** look up the topic in `docs/learning-path-v2.md` to get its title and level.
   Confirm which repo(s) are relevant (most topics: `C:\opt\learn\spark\repos\spark`; Delta Lake
   topics: check the local Delta repo; Dagster/Unity Catalog: note they require network access
   or local clones).
2. **Config slice:** grep `configs/catalog.yaml` for keyword matches (e.g. for B7 "joins":
   `autoBroadcastJoin`, `join.prefer`, `adaptive` — take the relevant slice).
3. **Run the tracer brief** ("Topic tracer subagent brief", at the end of this file) — inline, or dispatched to a
   read-only subagent if the harness allows agent calls and the user asked for one. Give it: the topic code,
   title, and description from `learning-path-v2.md`; the config slice; the Spark source path.
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
   it will not mention the trace unless you put it there. Open `docs/learning-path-v2.md` at this
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
   - `docs/learning-path-v2.md` — the topic heading, `#### ✅ <code>` → `#### 🔄 <code>`, and the
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

---

## Topic tracer subagent brief

**This is the trace checklist.** Work it inline yourself, or dispatch it to a read-only
`feature-dev:code-explorer` / general-purpose subagent **when the harness permits unprompted agent
calls and the user asked for one** — several harnesses forbid that, and the brief is written to be
followed either way. Whichever you do, say which in the summary. The brief:

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
