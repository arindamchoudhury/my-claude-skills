---
name: spark-book
description: >
  Use when writing a chapter in the personal Apache Spark / PySpark book at
  C:\opt\learn\spark\notes\docs\spark-book\. Triggers on: "write the chapter for X",
  "I finished topic B3", "I just learned about window functions", "add a chapter on joins",
  "write the spark book chapter for structured streaming", any reference to a learning-path
  topic code (B1–B12, I1–I53, A1–A60, E1–E60), or any request to add, draft, review, or
  extend a chapter in the Spark personal book. The book lives at the site
  C:\opt\learn\spark\notes and is built with Zensical.
---

# Spark / PySpark Personal Book — Writing Skill

## What this skill is for

Writing the personal Spark/PySpark book at `C:\opt\learn\spark\notes\docs\spark-book\`.

Each chapter corresponds to one topic from the learning path (`docs/learning-path-v2.md`). As the user masters a topic (via books, MOOCs, or hands-on work), they trigger this skill to write the chapter. The book is their synthesis — not notes from a single source, but their own explanation of the topic in their own words, verified against current Spark 4.x docs.

The book structure mirrors the learning path exactly:

```
Part 1 — Beginner     (Chapters 01–09)
Part 2 — Intermediate (Chapters 10–19)
Part 3 — Advanced     (Chapters 20–29)
Part 4 — Expert       (Chapters 30–38)
```

---

## Chapter arc — read it from the repo, not from here

**Ground truth is `docs/spark-book/index.md`**, whose table lists every chapter with its
status, number, v2 topic code, title and link; `zensical.toml`'s nav is the second check.
This skill used to carry its own arc table and it drifted twice — the book's real numbering
does not match a naive topic-code order (RDDs are Ch 05, UDFs are Ch 13), and the learning
path was renumbered wholesale when v2 replaced v1. Do not reconstruct the mapping from
memory or from topic codes.

Before writing, read that index and take from it:

- the next free chapter number,
- the slug convention (`ch<NN>-<slug>.md`, slug derived from the title),
- whether a chapter for this topic already exists (extend it rather than adding a second),
- which chapters are 🔄 and might be better work than a new one.

Topic codes are **v2 codes** from `docs/learning-path-v2.md` (185 topics: B1–B12, I1–I53,
A1–A60, E1–E60). `docs/learning-path.md` is v1 — deprecated and frozen; its codes mean
different topics, and the v1 → v2 crosswalk lives at the end of v2.

## File locations

| File | Purpose |
|---|---|
| `docs/spark-book/index.md` | Book progress table — one row per chapter |
| `docs/spark-book/ch<NN>-<slug>.md` | Chapter file (e.g. `ch11-window-functions.md`) |

Chapter numbers are always **two-digit zero-padded** (`ch01`, `ch11`, `ch38`).

---

## Workflow (follow in order every time)

### Step 1 — Identify the chapter

From the user's message, determine:
- Which learning-path topic code was completed (B1–B12, I1–I53, A1–A60, E1–E60 in v2)
- The chapter number and slug from the arc table above
- Whether the chapter file already exists (read it if so — this may be an update, not a new chapter)

### Step 2 — Research before writing

**Always web-search before writing.** Never rely solely on training data for API behaviour, version specifics, or best practices.

Run at least two searches:
```
"PySpark <topic> Spark 4.1 <year>"
"<topic> best practices PySpark 2025 2026"
```

Also check:
- `docs/research-cache/spark-api-versions.md` — API versions, function additions, config defaults
- `docs/research-cache/spark-source-internals-v412.md` — source-verified execution internals (QueryExecution, WholeStageCodegenExec, FileScanRDD, UnsafeRow, stage types)
- The relevant official docs page (see Code Standards below for URLs)

**Verifying against Spark v4.1.2 source:** Use the local checkout at `C:\opt\learn\spark\spark`. Read or grep files directly — do not rely on web search for source-level facts. Examples:

```powershell
# Find a config default
grep -r "maxFailures" "C:\opt\learn\spark\spark\core\src\main\scala\org\apache\spark\internal\config"

# Read a specific class
cat "C:\opt\learn\spark\spark\sql\core\src\main\scala\org\apache\spark\sql\execution\QueryExecution.scala"
```

Save any new verified facts to the appropriate cache file above.

### Step 3 — Write the chapter

Fit the chapter to the topic — there is no fixed section list. See **Chapter Form** below. File goes to `docs/spark-book/ch<NN>-<slug>.md`.

Rules:
- Write from first principles, in your own voice — not as a summary of a specific book
- Open by establishing why the topic matters, anchored in a concrete real-world scenario
- Every code block must be complete and runnable (all imports included)
- Build from minimal → complete — one new idea per example
- Where the chapter includes pitfalls, draw them from real bugs (book notes, web research, or verified behaviour) — never invented

### Step 4 — Sync site files

After writing the chapter, update all of these:

1. **`docs/spark-book/index.md`** — flip the chapter row from ⬜ to ✅, fill in the date

   **Status marks are a claim, so keep them honest.** ✅ means written *and current*. 🔄 means
   written but needing revisiting — use it whenever the chapter no longer matches reality:
   a newer Spark changed a default the chapter states, a source trace opened gaps, or the
   learning-path topic gained material the chapter does not cover. When you flip to 🔄, do all
   three together or the marks disagree:
   - the status cell in `docs/spark-book/index.md`
   - a dated `> 🔄 **Needs revisiting — …**` banner under the chapter's header block, naming
     what specifically drifted
   - the topic heading in `docs/learning-path-v2.md` (`#### ✅ <code>` → `#### 🔄 <code>`) and the
     "Carrying 🔄" summary line

   Say in the banner whether the chapter is **wrong** (a false claim — a changed default, a
   stale version requirement) or merely **incomplete** (missing new surface). Only the first
   kind misleads a reader, and that is what decides which chapter to fix first.
2. **`zensical.toml`** — add the chapter entry under the `"Spark Book"` nav group:
   ```toml
   { "Ch NN. Title" = "spark-book/ch<NN>-<slug>.md" }
   ```
3. **`docs/reference/glossary.md`** — append any new terms the chapter introduces (with source `Spark Book Ch NN`)
4. **`docs/topics/index.md`** — add any new cross-cutting topics to the backlog if they aren't already there

### Step 4b — Write the lab, if this topic has one

Twelve topics are earmarked for a hands-on lab — a Jupyter notebook run against the
local stack, where running the thing teaches what reading it cannot. **A lab is written
with its chapter, not in a batch.** The list and the notebook contract are in
`C:/opt/learn/spark/notes/docs/superpowers/specs/2026-08-12-spark-labs-design.md`; the
step-by-step recipe (notebook shape, how to run it, how to wire it into the site) is
`docs/superpowers/plans/2026-08-12-spark-labs.md`, Tasks 3-5.

Labs are earmarked for: **B10**, **I28**/**I29**, **I24**, **A18**/**A19**, **A15**/**A16**,
**I25**, **A11**/**A12**, **I37**/**A39**, **I10**/**I50**, **A32**/**A34**, **A59**/**A60**,
**E29**/**A51**. If the chapter you just wrote is not one of these, skip this step.

If it is one of these:

1. Write `workspace/notebooks/labs/NN-<slug>.ipynb` in the stack repo
   (`C:/opt/learn/spark/spark-delta-unitycatalog`), following the five-part shape in the
   plan: header stating what you will observe · setup via `_labkit.session()` · data via
   `_labkit.fetch()` · predict-then-run body · teardown.
2. **Run it top to bottom** and correct every "roughly N" in the prose to match what you
   observed. Numbers that contradict the output are worse than no numbers. Notebooks carry
   **no assertions** — this is a design decision recorded in the spec.
3. Add a row to `docs/labs.md` (create it from the plan's Task 4 if it does not exist yet,
   and add the nav entry) and a `**Lab**` line to the topic in `docs/learning-path-v2.md`.
4. Run `python tools/check_labs.py` if it exists; commit the notebook in the stack repo and
   the site changes in the notes repo.

**Runtime facts** (learned, do not rediscover): the Windows host has no PySpark — run
notebooks inside the `dagster-user-code` container, which mounts `workspace/` at
`/workspace`. Prefix docker commands from Git Bash with `MSYS_NO_PATHCONV=1`. The Spark
Connect service needs `docker compose up -d` from the stack repo root.

### Step 5 — Confirm to user

```
✓ Chapter NN: "<Title>" → docs/spark-book/ch<NN>-<slug>.md
  Learning-path topic: <code> (<level>)
  New glossary terms: N
  Next topic in learning path: <code> — <title>

Book progress: N / 38 chapters
```

---

## Chapter Form

**There is no fixed section template.** The right structure depends on the topic. A setup chapter, an API-family chapter, an architecture/internals chapter, and a tuning chapter each take a different shape — forcing them all through the same headings produces padded chapters where half the sections are filler. Fit the chapter to its topic.

### Fixed header (every chapter)

Start every chapter file with the title and metadata blockquote, then a one-paragraph hook:

```markdown
# Chapter NN — <Title>

> *Learning-path topic: <code> (<Beginner / Intermediate / Advanced / Expert>)*
> *Written: YYYY-MM-DD · Spark 4.1.x / Python 3.10+*

One paragraph: what this chapter is about and why the topic matters.
```

### Invariants — every chapter, no exceptions

- Opens by establishing why the topic matters — the problem it solves or the capability it unlocks. The reader knows within the first screen why they're here.
- Teaches toward the learning-path milestone for this topic. When done, the reader can do what the milestone names.
- All code is current (Spark 4.1.x / Python 3.10+), complete, and runnable — see Code Standards below.
- Prose is built from short sentences — one idea per sentence, not long clause-stacked ones. Easier to read and to revise.
- Ends pointing forward — the closing lines connect to the next topic or to what this chapter unlocks.
- **Callouts are admonitions, never blockquotes.** Every note, caveat, version difference, or aside uses `!!! note` / `!!! warning` / `!!! info` with a quoted title and a 4-space-indented body:

  ```markdown
  !!! warning "ANSI mode changes what a bad cast does"
      Spark 4.x raises instead of returning null. Book examples that relied on
      a null result will now fail the job.
  ```

  Choose the type by what the reader must do about it: `warning` for something that will bite them, `info` for a naming or behaviour clarification, `note` for additive context. One carve-out: the chapter's metadata header (`> *Learning-path topic: …*`) stays a blockquote, because it is a header block rather than a callout. Admonitions otherwise render anywhere, including directly after a list — an earlier version of this file claimed they did not, which was a misdiagnosis of a missing `admonition` markdown extension in `zensical.toml` (fixed 2026-07-18). If an `!!!` block renders as literal text, check that extension before rewriting content.

### Toolkit — use the elements the topic needs, in the order that serves it

- **Learning outcomes** up front (3–5 bullets) — valuable for dense topics; skip for short ones
- **A motivating problem** — a concrete scenario that breaks or becomes painful without this topic
- **Core concept / mental model** prose — the WHY behind the mechanism, not just the WHAT; an analogy or comparison table where it helps
- **Worked examples**, minimal → complete, one new idea each
- **Mermaid diagrams** where a picture beats prose — architecture, data flow, partitioning, shuffle
- **A reference table** where the topic is API-shaped — a family of functions, config keys, frame types
- **A semantics / edge-case section** where correctness is subtle — ANSI overflow, null handling, watermarks, frame defaults
- **Common pitfalls** (3–5) drawn from real bugs — book notes, web research, verified behaviour; never invented
- **Performance notes** where the topic has cost implications
- **Exercises** — recall / apply / extend
- **Summary** — key takeaways; last bullet points to what the next chapter builds on
- **References** — official PySpark docs page + any sources consulted

### Match the shape to the topic

- **Setup / environment** → mostly procedure + verification; heavy on "what can go wrong"; few or no exercises.
- **API family** (e.g. DataFrame transformations, column functions) → organised around a reference table plus one tight example per important operation.
- **Architecture / internals** (e.g. Catalyst, Tungsten, the DAG scheduler) → prose and Mermaid diagrams lead; code is illustrative, not the point.
- **Concept** (e.g. window functions, joins) → problem → mental model → examples → semantics → pitfalls.
- **Tuning / operations** (e.g. skew, AQE, partitioning) → symptom → diagnosis → fix, with Spark UI walkthroughs and before/after metrics.

Let the topic pick the structure. A chapter that needs only four of these elements should have only four — don't manufacture a "Pitfalls" or "Exercises" section just to fill a slot.

---

## Code Standards

These apply to every code block in every chapter. No exceptions.

### Mandatory imports and aliases

```python
import pyspark.sql.functions as F   # always F, never aliased differently
import pyspark.sql.types as T        # always T
from pyspark.sql import SparkSession
from pyspark.sql.window import Window  # for window function chapters
from typing import Iterator, Tuple     # for pandas UDF chapters
import pandas as pd                    # for pandas UDF chapters
```

**Never** use `from pyspark.sql.functions import *`. **Never** use bare names like `col(...)` or `sum(...)` — always `F.col(...)`, `F.sum(...)`.

### SparkSession for standalone examples

```python
spark = SparkSession.builder \
    .appName("ch<NN>-<slug>") \
    .getOrCreate()
```

For local stack examples, use:
```python
spark = SparkSession.builder \
    .appName("ch<NN>-<slug>") \
    .config("spark.sql.catalog.unity", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()
```

### Version comment

Add to the first code block in every chapter:
```python
# Apache Spark 4.1.x / PySpark 4.1.x · Python 3.10+ · Delta Lake 4.x
```

### Completeness rules

- **Never truncate** with `# ... rest of code` or `# etc`
- Every example is **copy-paste runnable** — all imports at top, `SparkSession` created if needed
- Show **actual output** inline as comments where helpful:
  ```python
  result.show(3)
  # +------+----+-------+
  # |  col1|col2|  col3 |
  # +------+----+-------+
  # |   ... |  ... | ... |
  # +------+----+-------+
  ```
- For ANSI mode (Spark 4.x default), use `try_cast()` / `F.col("x").try_cast(T.IntegerType())` for nullable conversions — **not** `cast()` when overflow is possible

### Local stack references

When examples involve Delta Lake or Unity Catalog, use the local stack namespace:
```python
# writing to local Unity Catalog
df.write.format("delta").saveAsTable("unity.default.<table_name>")

# reading back
df = spark.read.table("unity.default.<table_name>")
```

---

## Diagram Standards

**Always use Mermaid for diagrams.** Never use ASCII art (`─`, `│`, `▶`, `└`, `├`, etc.) for diagrams, flowcharts, or sequence illustrations. Mermaid renders natively in the Zensical site; ASCII art does not.

```markdown
```mermaid
flowchart TD
    A["Node A"] --> B["Node B"]
```
```

Use the appropriate Mermaid diagram type for the content:

| Content | Diagram type |
|---|---|
| Component relationships, data flow, execution pipeline | `flowchart TD` or `flowchart LR` |
| Sequences and protocol exchanges | `sequenceDiagram` |
| State machines | `stateDiagram-v2` |
| Entity relationships | `erDiagram` |
| Timelines / Gantt | `gantt` |

Node labels may contain newlines using `\n` inside the label string.

---

## Key Patterns (include at least one per relevant chapter)

**Lazy evaluation chain** (B1, B2, B3)
```python
result = (
    spark.read.parquet("path/")
    .filter(F.col("year") == "2024")
    .withColumn("temp_c", (F.col("temp") - 32) * 5 / 9)
    .groupBy("stn", "mo")
    .agg(F.avg("temp_c").alias("avg_temp_c"))
)
result.show()  # action triggers execution
```

**groupBy + multi-agg** (B6)
```python
result = df.groupBy("category").agg(
    F.count("*").alias("n"),
    F.avg("value").alias("avg_value"),
    F.sum(F.when(F.col("flag") == 1, 1).otherwise(0)).alias("n_flagged"),
)
```

**Window function** (I2, A5)
```python
w = Window.partitionBy("stn", "year").orderBy("dt_num")
df = df.withColumn("prev_temp", F.lag("temp").over(w)) \
       .withColumn("rolling_avg", F.avg("temp").over(
           w.rowsBetween(-6, 0)   # 7-day trailing average
       ))
```

**pandas UDF — cold start model** (I3, A5)
```python
@F.pandas_udf(T.DoubleType())
def score(features: Iterator[pd.Series]) -> Iterator[pd.Series]:
    import joblib
    model = joblib.load("/mnt/models/model.pkl")   # once per partition
    for batch in features:
        yield pd.Series(model.predict(batch.values.reshape(-1, 1)))
```

**MERGE INTO for upserts** (I9, A6)
```python
from delta.tables import DeltaTable
target = DeltaTable.forName(spark, "unity.default.silver_gsod")
target.alias("t").merge(
    source=updates.alias("s"),
    condition="t.stn = s.stn AND t.dt = s.dt",
).whenMatchedUpdateAll() \
 .whenNotMatchedInsertAll() \
 .execute()
```

**Streaming to Delta** (A7)
```python
query = (
    spark.readStream.format("parquet").schema(schema).load("ingest/")
    .writeStream.format("delta")
    .outputMode("append")
    .option("checkpointLocation", "checkpoints/bronze")
    .toTable("unity.default.bronze_gsod")
)
```

---

## Anti-patterns (never write these in the book)

- `from pyspark.sql.functions import col, sum, avg` — name collisions with Python builtins; always use `F.`
- `df.toPandas()` on a large DataFrame — collects entire dataset to driver; only safe after aggregation
- Calling `df.count()` in a loop or hot path — triggers a full job each time
- `df.repartition(1)` before writing to disk on large data — creates one massive task and one file
- Mutable Python state inside a UDF (e.g., appending to a list defined outside the function) — executors are separate processes; shared state doesn't work
- `cache()` without an explicit `unpersist()` later — leaks memory across jobs
- Using `PandasUDFType.GROUPED_AGG` — deprecated Spark 2.x syntax; use type hints
- `Window.orderBy("col")` on an aggregate function without thinking about the default growing frame — will silently compute a running aggregate instead of a partition-wide aggregate
- `inferSchema=True` in production pipelines — reads data twice and may infer wrong types on sparse columns

---

## Ecosystem Reference

| Technology | Version | Notes |
|---|---|---|
| Apache Spark | 4.1.2 (May 2026) | ANSI mode on by default; Spark Connect default in 4.x |
| PySpark | 4.1.x | Use `from pyspark.sql import SparkSession`; classic mode for standalone scripts |
| Delta Lake OSS | 4.x | `io.delta:delta-spark_2.13:4.x`; `from delta.tables import DeltaTable` |
| Unity Catalog OSS | Local stack | Three-level namespace: `unity.default.<table>` |
| Python | 3.10+ | Type hints required for pandas UDFs since Spark 3.0 |
| pandas | ≥ 2.2.0 | Minimum for Spark 4.1 |
| PyArrow | Latest stable | Required for pandas UDFs; zero-copy Arrow serialisation |
| Dagster | Latest stable | `dagster-pyspark` for Spark integration |

**Verified research facts (do not re-search):**

| Fact | Value | Source |
|---|---|---|
| Spark origin paper | *"Spark: Cluster Computing with Working Sets"* — Zaharia et al., **2010**, HotCloud (USENIX) | Ch01 reference |
| RDD origin paper | *"Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing"* — Zaharia et al., **2012**, NSDI (USENIX) — Best Paper Award | Ch03 reference |
| Spark Connect is opt-in in 4.x | Classic mode is default for both `pyspark` shell and `spark-submit`; opt in via `SPARK_REMOTE`, `--remote`, or `spark.api.mode=connect` | Verified against Spark 4.1.2 docs |
| `spark.task.maxFailures` default | **4** — confirmed in `core/src/main/scala/org/apache/spark/internal/config/package.scala` v4.1.2 | Source-verified |
| KubernetesSchedulerBackend class name | `KubernetesClusterSchedulerBackend` (not `KubernetesSchedulerBackend`) | Source-verified |
| Celeborn JAR for Spark 4.x | `celeborn-client-spark-4-shaded_*.jar` (not spark-3) | Maven Central |
| JDK requirement for Spark 4.x | Java **17 or 21** (not "17+") | Spark 4.1.2 docs |
| `QueryExecution.toRdd` | `new SQLExecutionRDD(executedPlan.execute(), conf)` — `RDD[InternalRow]` is the scheduling shell | v4.1.2 source |
| `WholeStageCodegenExec.doExecute()` | Gets leaf RDDs via `inputRDDs()`, wraps with `mapPartitionsWithIndex { evaluator.eval() }` — Tungsten runs INSIDE the RDD partition | v4.1.2 source |
| `FileScanRDD` | `extends RDD[InternalRow]` — real RDD, not bypassed; ends with `asInstanceOf[Iterator[InternalRow]] // This is an erasure hack.` | v4.1.2 source |
| `UnsafeRow` default memory | **On-heap** by default; `sun.misc.Unsafe` is the write API, not the allocator; off-heap requires `spark.memory.offHeap.enabled=true` | v4.1.2 source |
| `GenericInternalRow` appears | Only when codegen disabled (`spark.sql.codegen.wholeStage=false`), during Catalyst planning, or in tests — never in normal Tungsten execution | v4.1.2 source |
| `spark.sql.codegen.fallback` | Default `true` — silent fallback to interpreted execution with `GenericInternalRow` on codegen compile failure | v4.1.2 source |
| `ShuffleMapTask.runTask()` | Returns `MapStatus` (not void) — shuffle file location metadata sent to driver; user data goes to local disk only | v4.1.2 source |
| `ResultStage` partial execution | May run on subset of partitions — `first()` runs on 1 partition, `lookup(key)` runs on 1 partition | v4.1.2 source (`ResultStage.scala` Scaladoc) |
| Uniffle Spark 4.x support | **Unverified** — official client guide only documents Spark 2 and 3 JARs; use Celeborn for Spark 4.x | v4.1.2 check |

Full research cache:
- `docs/research-cache/spark-api-versions.md` — API versions and config defaults
- `docs/research-cache/spark-source-internals-v412.md` — execution internals, stage types, memory model

**Official doc URLs to consult per chapter:**
- PySpark API: `https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/`
- SQL functions: `https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions/`
- Structured Streaming: `https://spark.apache.org/docs/latest/streaming/index.html`
- MLlib: `https://spark.apache.org/docs/latest/ml-guide.html`
- Delta Lake: `https://docs.delta.io/latest/`
- Dagster: `https://docs.dagster.io/`

---

## Triggering phrase examples

The skill activates on any of these patterns:

| User says | Chapter |
|---|---|
| "I finished B3" | Ch 03 — DataFrame Basics |
| "write the chapter on window functions" | Ch 11 — Window Functions |
| "I just learned about joins" | Ch 07 — Joins |
| "add the structured streaming chapter" | Ch 26 — Streaming Fundamentals |
| "I completed A2" | Ch 21 — AQE |
| "write a chapter for Delta Lake advanced" | Ch 25 — Delta Lake Advanced |
| "I'm done with the medallion architecture topic" | Ch 18 — Medallion Architecture |
| "write the spark book chapter for I7" | Ch 16 — Spark UI |
