---
name: databricks-book
description: Use when writing a chapter in the personal Databricks Data Engineering book at C:\opt\learn\databricks\notes\docs\book\. Triggers on: "write the chapter for X", "I finished topic B3", "I just learned about Delta Lake", "add a chapter on DLT", "write the databricks book chapter for streaming", any reference to a learning-path topic code (B1–B7, I1–I8, A1–A7, E1–E6), or any request to add, draft, review, or extend a chapter in the Databricks personal book.
---

# Databricks Book Skill

Write chapters for the personal Databricks Data Engineering book at `C:\opt\learn\databricks\notes\docs\book\`.

## Book location

```
C:\opt\learn\databricks\notes\docs\book\
  index.md          ← chapter registry (update ⬜ → ✅ when done)
  ch01-databricks-platform-workspace.md
  ch02-spark-architecture-databricks.md
  ch03-pyspark-dataframe-api.md
  ch04-spark-sql-relational-entities.md
  ch05-delta-lake-fundamentals.md
  ch06-data-ingestion-basics.md
  ch07-medallion-architecture.md
  ch08-auto-loader-incremental-ingestion.md
  ch09-structured-streaming.md
  ch10-lakeflow-spark-declarative-pipelines.md
  ch11-cdc-apply-changes.md
  ch12-delta-lake-advanced.md
  ch13-lakeflow-jobs-orchestration.md
  ch14-unity-catalog-governance.md
  ch15-databricks-sql-analytics.md
  ch16-spark-performance-tuning.md
  ch17-liquid-clustering-storage.md
  ch18-lakeflow-connect-enterprise-ingestion.md
  ch19-data-privacy-pii-compliance.md
  ch20-databricks-asset-bundles-cicd.md
  ch21-production-pipeline-observability.md
  ch22-lakehouse-federation-delta-sharing.md
  ch23-photon-cluster-cost.md
  ch24-advanced-streaming-patterns.md
  ch25-devops-testing-deployment.md
  ch26-cost-management-finops.md
  ch27-end-to-end-lakehouse-architecture.md
  ch28-databricks-sdk-automation.md
```

## Chapter Arc

### Beginner (Ch 01–07)

| Code | Chapter | Chapter file |
|---|---|---|
| B1 | Ch 01 — Databricks Platform & Workspace | ch01-databricks-platform-workspace.md |
| B2 | Ch 02 — Apache Spark Architecture on Databricks | ch02-spark-architecture-databricks.md |
| B3 | Ch 03 — PySpark DataFrame API Fundamentals | ch03-pyspark-dataframe-api.md |
| B4 | Ch 04 — Spark SQL & Relational Entities | ch04-spark-sql-relational-entities.md |
| B5 | Ch 05 — Delta Lake Fundamentals | ch05-delta-lake-fundamentals.md |
| B6 | Ch 06 — Data Ingestion Basics | ch06-data-ingestion-basics.md |
| B7 | Ch 07 — Medallion Architecture | ch07-medallion-architecture.md |

### Intermediate (Ch 08–15)

| Code | Chapter | Chapter file |
|---|---|---|
| I1 | Ch 08 — Auto Loader & Incremental Ingestion | ch08-auto-loader-incremental-ingestion.md |
| I2 | Ch 09 — Structured Streaming with Spark | ch09-structured-streaming.md |
| I3 | Ch 10 — Lakeflow Spark Declarative Pipelines | ch10-lakeflow-spark-declarative-pipelines.md |
| I4 | Ch 11 — Change Data Capture with APPLY CHANGES | ch11-cdc-apply-changes.md |
| I5 | Ch 12 — Delta Lake Advanced Operations | ch12-delta-lake-advanced.md |
| I6 | Ch 13 — Lakeflow Jobs & Workflow Orchestration | ch13-lakeflow-jobs-orchestration.md |
| I7 | Ch 14 — Unity Catalog & Data Governance | ch14-unity-catalog-governance.md |
| I8 | Ch 15 — Databricks SQL & Analytics | ch15-databricks-sql-analytics.md |

### Advanced (Ch 16–22)

| Code | Chapter | Chapter file |
|---|---|---|
| A1 | Ch 16 — Spark Performance Tuning & the Spark UI | ch16-spark-performance-tuning.md |
| A2 | Ch 17 — Liquid Clustering & Storage Optimization | ch17-liquid-clustering-storage.md |
| A3 | Ch 18 — Lakeflow Connect & Enterprise Ingestion | ch18-lakeflow-connect-enterprise-ingestion.md |
| A4 | Ch 19 — Data Privacy, PII & Compliance | ch19-data-privacy-pii-compliance.md |
| A5 | Ch 20 — Declarative Automation Bundles (DABs) & CI/CD | ch20-databricks-asset-bundles-cicd.md |
| A6 | Ch 21 — Production Pipeline Operations & Observability | ch21-production-pipeline-observability.md |
| A7 | Ch 22 — Lakehouse Federation & OpenSharing | ch22-lakehouse-federation-delta-sharing.md |

### Expert (Ch 23–28)

| Code | Chapter | Chapter file |
|---|---|---|
| E1 | Ch 23 — Photon Engine & Cluster Cost Optimization | ch23-photon-cluster-cost.md |
| E2 | Ch 24 — Advanced Streaming Patterns | ch24-advanced-streaming-patterns.md |
| E3 | Ch 25 — DevOps: Testing & Multi-Environment Deployment | ch25-devops-testing-deployment.md |
| E4 | Ch 26 — Cost Management & FinOps on Databricks | ch26-cost-management-finops.md |
| E5 | Ch 27 — End-to-End Lakehouse Architecture Design | ch27-end-to-end-lakehouse-architecture.md |
| E6 | Ch 28 — Databricks SDK & API Automation | ch28-databricks-sdk-automation.md |

---

## How to write a chapter

### Trigger

User says "I finished topic X" or "write the chapter for X" (where X is a topic code like B1, I3, A5 or a topic name).

### Step-by-step process

1. **Identify the chapter** — find the topic code in the arc table above; get the chapter number and file path.

2. **Gather notes** — grep `C:\opt\learn\databricks\notes\docs\` for any notes files already written on this topic. The user may have used `book-pdf-notes` or `research-notes` to take notes from their learning resources.

3. **Web-search for current state** — always search for:
   - `"<topic> Databricks 2025 2026 best practices"`
   - `"<topic> Databricks pitfalls common mistakes"`
   - Any version-specific changes since the book resources were published
   Never rely only on the notes; current Databricks moves fast.

4. **Synthesis plan** — briefly note how sources agree/disagree and what the chapter will emphasise. Do not show this to the user; it's internal scaffolding.

5. **Write the chapter** — see invariants and toolkit below.

6. **Sync** — after writing:
   - Update `docs/book/index.md`: flip the chapter row from ⬜ to ✅
   - Update `docs/learning-path.md`: flip the topic heading from `### ⬜ <Code>` to `### ✅ <Code>`
   - Add new terms to `docs/reference/glossary.md`
   - Add the chapter to `zensical.toml` nav under the Book section

---

## Chapter invariants

Every chapter must satisfy these — regardless of shape:

1. **Motivate the topic** — open with why this topic matters in production (a concrete failure mode or business impact, not "this topic is important").
2. **Teach toward the milestone** — the chapter's scope exactly matches the learning-path milestone for this topic; don't go wider.
3. **Current runnable code** — all code examples use DBR 18 / Spark 4.1 imports and APIs. Flag anything that changed from a prior version.
4. **End pointing forward** — the final paragraph connects this topic to what comes next in the learning path.
5. **Short sentences over overloaded ones** — one idea per sentence, not long clause-stacked ones; easier to read and to revise.

---

## Chapter toolkit

Draw from these elements — not all chapters need all of them. Chapter structure adapts to the topic type.

- **Learning outcomes** — 3–5 bullet "after this chapter you will..." (useful for dense topics)
- **Motivating problem** — a concrete scenario that creates the need for this topic
- **Core-concept prose** — explanation-first paragraphs before code
- **Worked examples** — step-by-step walkthroughs with code and expected output
- **Mermaid diagrams** — for architecture, flow, or decision trees (use ```` ```mermaid ```` blocks)
- **Reference tables** — config options, API methods, comparison matrices
- **Semantics / edge-case sections** — subtle behaviour the docs underspecify
- **Pitfalls** — concrete mistakes and why they happen
- **Performance notes** — where relevant (not on every chapter)
- **Exercises** — 2–3 "try this" prompts at the end of complex chapters
- **Summary** — 5–8 bullet recap (useful for long chapters)
- **References** — links to official docs pages covered

---

## Topic-specific guidance by level

**Beginner chapters (B1–B7):** Prioritise mental models over completeness. Heavy use of diagrams and simple worked examples. Assume zero Databricks experience but some general programming experience. Avoid performance and internals — save for later chapters.

**Intermediate chapters (I1–I8):** API-focused. Full working code for each major pattern. Comparison tables (e.g., COPY INTO vs Auto Loader vs Lakeflow Connect). Note what's changed from the book resource if it's pre-2025.

**Advanced chapters (A1–A7):** Depth and nuance. Explain why, not just how. Spark UI screenshots/descriptions. Trade-off tables. Production patterns from BBDE and DA-ADE.

**Expert chapters (E1–E6):** Architecture and design judgment. Less "here's how the API works", more "here's how to decide and what breaks if you decide wrong." Include real system-design decisions with trade-offs.

---

## Code standards

```python
# Standard imports for Databricks notebooks
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import pyspark.sql.types as T
from delta.tables import DeltaTable

# SparkSession is pre-created in Databricks notebooks as `spark`
# In standalone scripts: spark = SparkSession.builder.getOrCreate()
```

- Use `F.col()`, `F.lit()`, `F.when()` — always qualify with `F.`
- Use `T.StructType()`, `T.StringType()` — always qualify with `T.`
- Lakeflow pipeline syntax: `CREATE OR REFRESH STREAMING TABLE` / `CREATE OR REFRESH MATERIALIZED VIEW`
- APPLY CHANGES: `APPLY CHANGES INTO target FROM source KEYS (...) SEQUENCE BY ...`
- Liquid Clustering: `CREATE TABLE t (...) CLUSTER BY (col1, col2)`; never `ZORDER BY` in new code

---

## Key patterns every Databricks DE practitioner needs

1. **Medallion pipeline with Lakeflow** — Bronze streaming table → Silver materialized view (with expectations) → Gold materialized view
2. **Auto Loader with schema evolution** — `cloudFiles` source + `mergeSchema` + checkpoint
3. **MERGE INTO for SCD logic** — MATCHED/NOT MATCHED branches; know when to use APPLY CHANGES instead
4. **DABs deployment** — `databricks.yml` + `resources/` YAML + `bundle deploy --target prod`
5. **Unity Catalog governance** — `GRANT SELECT ON TABLE catalog.schema.table TO `group``
6. **Liquid Clustering** — `CLUSTER BY` on query filter columns + periodic `OPTIMIZE`
7. **CDF-based delete propagation** — enable `delta.enableChangeDataFeed`, read `table_changes`, propagate deletes downstream

---

## Anti-patterns (never write these)

- `spark.read.csv(...).write.mode("overwrite").saveAsTable(...)` on every run — use incremental patterns
- `Z-ORDER BY` on new tables — use `CLUSTER BY` (Liquid Clustering) instead
- Mounting external storage with `dbutils.fs.mount` — use Unity Catalog external locations instead
- All-purpose clusters for production jobs — always use job clusters
- Ignoring watermarks on streaming aggregations — state store grows unbounded
- `VACUUM` with retention < 7 days — breaks time travel and concurrent readers
- Python UDFs for operations available in `pyspark.sql.functions` — massive performance penalty
