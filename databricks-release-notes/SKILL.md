---
name: databricks-release-notes
description: Fetch the latest Databricks release notes (platform, runtime, Lakeflow, SQL, DABs, serverless) and update the notes site at C:\opt\learn\databricks\notes. Triggers on "update databricks release notes", "check databricks releases", "refresh databricks release notes", or when run on the monthly schedule. Also flags any learning path updates (breaking changes, renames, new features relevant to a learning path topic).
---

# Databricks Release Notes Updater

Fetches all Databricks release note categories and updates the notes site at `C:\opt\learn\databricks\notes\docs\release-notes\`.

## Notes site location

```
C:\opt\learn\databricks\notes\docs\release-notes\
  index.md                         ← overview + LP flags
  platform/
    YYYY-<month>.md                ← one per calendar month
  runtime/
    dbr-<version>.md               ← one per major runtime version
  lakeflow/
    <year>.md                      ← annual Lakeflow pipeline notes
  sql/
    <year>.md                      ← annual SQL notes
  dabs/
    changelog.md                   ← rolling DABs changelog
  serverless/
    changelog.md                   ← rolling serverless changelog
```

---

## Step 1 — Determine what's new

### Find last captured month

Read `docs/release-notes/index.md` to find the most recent platform month already captured (look at the Platform table — the first row is the most recent).

### Determine months to fetch

Compare the most recent captured month against today's date (`currentDate` in context). Generate the list of missing months in the format `YYYY-<monthname>` (e.g., `2026-july`).

**URL pattern:**
```
https://docs.databricks.com/aws/en/release-notes/product/YYYY/<monthname>
```

### Feature-specific pages to always refresh

These pages update continuously — always re-fetch them regardless of last capture date:

| Page | URL |
|---|---|
| Lakeflow current year | `https://docs.databricks.com/aws/en/release-notes/dlt/<YYYY>` |
| SQL current year | `https://docs.databricks.com/aws/en/sql/release-notes/<YYYY>` |
| DABs bundles | `https://docs.databricks.com/aws/en/release-notes/dev-tools/bundles` |
| Serverless | `https://docs.databricks.com/aws/en/release-notes/serverless/` |
| Runtime index | `https://docs.databricks.com/aws/en/release-notes/runtime/` |

---

## Step 2 — Fetch missing platform months

For each missing month:

1. `WebFetch` the URL with prompt:
   > "Extract all notable feature announcements, changes, and deprecations. Group by category. Focus on data engineering relevance: Delta Lake, Lakeflow, pipelines, jobs, Unity Catalog, SQL, compute, DABs, streaming. Include dates. Keep full details for each item."

2. Write to `docs/release-notes/platform/YYYY-<month>.md` using the template:

```markdown
# Platform Release Notes — <Month> <YEAR>

> **Source:** [docs.databricks.com/.../YYYY/<month>](https://docs.databricks.com/aws/en/release-notes/product/YYYY/<month>)
> **Added:** YYYY-MM-DD

---

## Data Engineering highlights

### <Category>

**Feature name (status)** — date
Description.

[...]
```

3. Add a row to the Platform table in `docs/release-notes/index.md` at the top.

4. Add the new file to `zensical.toml` nav under `Release Notes > Platform` (insert at top of the list, before previous entries).

---

## Step 3 — Refresh feature-specific pages

For each feature page in Step 1:

### Lakeflow Pipelines

1. Fetch `https://docs.databricks.com/aws/en/release-notes/dlt/<YYYY>`.
2. If the year is new (file doesn't exist), create `docs/release-notes/lakeflow/<YYYY>.md`.
3. If the file exists, read it and **append only new entries** at the top (don't overwrite existing entries).
4. Add to nav if new year file was created.

### Databricks SQL

Same pattern as Lakeflow. File: `docs/release-notes/sql/<YYYY>.md`.

### DABs

1. Fetch the DABs bundles page.
2. Read existing `docs/release-notes/dabs/changelog.md`.
3. Find entries newer than the latest date in the existing file.
4. Prepend new entries to the top of the `## 2026` (or current year) section.

### Serverless

Same pattern as DABs. File: `docs/release-notes/serverless/changelog.md`.

### Runtime

1. Fetch the runtime index to discover new versions.
2. For any version not yet documented, fetch its page and create `docs/release-notes/runtime/dbr-<version>.md`.
3. Add new runtime rows to the Runtime table in `index.md` and to `zensical.toml` nav.

---

## Step 4 — Scan for learning path updates

After fetching all new content, review it for anything that affects `docs/learning-path.md`:

Look for:
- **Breaking changes** in any runtime or SQL version — flag the affected learning path topic
- **Product renames** (e.g., DLT → Lakeflow, Delta Sharing → OpenSharing)
- **API removals or deprecations** that appear in learning path code examples
- **New GA features** that should upgrade a topic's "How to learn it" advice
- **New certifications or exam guide updates** that affect learning path order

For each finding, add a row to the "Learning path cross-references" table in `docs/release-notes/index.md`:

```markdown
| <Topic code> (<Topic name>) | <Issue type> | <Detail> |
```

Then update `docs/learning-path.md` directly if the change is clear-cut (e.g., an API was removed and there's an exact replacement). If uncertain, just add the flag to the index and note `⚠️ Review needed`.

---

## Step 5 — Sync all files

After all writes:

- [ ] `docs/release-notes/index.md` — Platform table updated, LP flags table updated
- [ ] `zensical.toml` — all new files added to nav
- [ ] Each new monthly file created
- [ ] Feature-specific files updated (new entries only, no overwrites)

---

## Output to user

End with a summary:

```
## Databricks Release Notes — update complete

**Date:** YYYY-MM-DD
**New platform months added:** [list]
**Feature pages refreshed:** Lakeflow, SQL, DABs, Serverless, Runtime
**New runtime versions documented:** [list or "none"]

### Learning path flags
[table of new flags, or "No new flags"]

### Most notable DE changes this period
- [bullet 1]
- [bullet 2]
- [bullet 3]
```

---

## Edge cases

**Month not yet published:** If the current month's URL returns a 404 or thin content ("no releases yet"), skip it silently.

**Year rollover:** In January, create new annual files for Lakeflow (`lakeflow/<new-year>.md`) and SQL (`sql/<new-year>.md`). Add them to nav under the new year. Keep the previous year's files in nav.

**New runtime version:** Fetch `https://docs.databricks.com/aws/en/release-notes/runtime/<version>`. Use the standard runtime note template from the existing files.
