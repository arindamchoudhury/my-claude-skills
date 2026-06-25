---
name: book-gap-filler
description: >
  Use when reviewing any chapter in the personal study-notes books at
  C:\opt\learn\spark\notes for information gaps. Triggers on: "review chapter N
  for information gap", "fill gaps in chapter N", "what's missing from chapter N",
  "what should we add to chapter N", or any request to identify and fill missing
  concepts in a book chapter. Encodes the full workflow: gap analysis → classify
  → verify against current version → add content → forward references → update/create
  later chapter stubs → wire nav → commit. Use this skill proactively whenever a
  chapter review for gaps is requested, even if the user does not say "skill".
---

# Book — Information Gap Workflow

A "gap" is a concept that belongs in a chapter's declared scope but is absent or
only surface-mentioned. This skill runs the full process: find gaps, classify them,
fill what belongs here, and defer the rest with forward references.

The book lives at `c:\opt\learn\spark\notes\docs\spark-book\`. Navigation is
controlled by `zensical.toml` — every new file must be wired there or it won't
appear in the site.

---

## Step 1 — Gap Analysis

Launch an Explore agent to read the chapter in full and the book index
(`docs/spark-book/index.md`). Give the agent:

- The chapter's declared scope (title, learning-path topic code)
- A list of topics **already covered** in the chapter (enumerate them explicitly
  so the agent doesn't re-flag them)
- The task: identify missing concepts with (a) what is missing, (b) why it belongs
  here vs a later specialist chapter, (c) which later chapter would own the deep dive

---

## Step 2 — Classify Gaps

Divide findings into two groups and present to the user before proceeding:

**Group A — Belongs in this chapter**
Concepts a reader needs to understand the chapter's core topic that no later
specialist chapter owns. These get full content added now.

**Group B — Belongs in a later chapter**
Deep implementation internals, API-usage details, performance tuning — anything
a specialist chapter already owns or will own. These get a forward reference in
the current chapter and a note in the later chapter's stub.

---

## Step 3 — Verify Group A Against Current Version

For every Group A gap, **verify all technical claims before writing**.

For the Spark book, fetch from:
- `https://spark.apache.org/docs/4.1.2/configuration.html`
- `https://spark.apache.org/docs/4.1.2/rdd-programming-guide.html`
- `https://spark.apache.org/docs/4.1.2/tuning.html`
- `https://spark.apache.org/docs/4.1.2/sql-programming-guide.html`
- GitHub source: `https://github.com/apache/spark/blob/v4.1.2/...`

Confirm: config property names, default values, component names, API names,
version numbers. Do not write content until verified.

For other books, fetch from the equivalent official documentation.

---

## Step 4 — Add Group A Content to the Chapter

For each verified gap:

1. Find the natural insertion point — the section where the concept logically belongs.
   Extend an existing section rather than creating a new one where possible.
2. Add full content. No summaries — explain the concept completely with config
   values, diagrams where the concept has multiple components or flows, and
   code examples where relevant.
3. After adding, add a one-sentence forward reference pointing to the later chapter
   that covers the deep dive:
   > "The [topic details] are covered in **Chapter NN (code — Title)**."

### Content conventions
- Short sentences over overloaded ones — one fact per sentence; split a clause-heavy
  sentence into several
- American English throughout (never: optimise, serialise, behaviour, materialise,
  synchronise, recognise, colour, favour)
- Mermaid diagrams for architecture, flows, pipelines — never ASCII art
- Blank line before every bullet list (Zensical requirement)
- `!!! note` admonitions for callouts — content indented with exactly 4 spaces
- Config values always cited with defaults: `` `spark.property.name` (default: `value`) ``

---

## Step 5 — Handle Group B Gaps

For each Group B gap, do both of the following:

### 5a — Forward reference in current chapter

Find where the concept is touched on (or where it logically belongs) and add
one sentence:

> "The [topic] — [brief description of what's deferred] — is covered in
> **Chapter NN (code — Title)**."

### 5b — Note in later chapter stub

Open `docs/spark-book/ch##-slug.md`.

**If the file exists:** Add the topic to the existing `📌 Topics deferred here
from Chapter N` callout.

**If the file does not exist:** Create it using the stub template below, then
wire it in `zensical.toml`.

**Stub template:**
```markdown
# Chapter NN — Title

> *Learning-path topic: XX (Level)*
> *Status: ⬜ Not yet written*

!!! note "📌 Topics deferred here from Chapter N"
    - **Topic name** — what it covers and why it belongs here

*This chapter is not yet written. The above topics will form its core.*
```

**Wiring in zensical.toml:** Add inside the `"Spark Book"` nav group:
```toml
{ "Ch NN. Title" = "spark-book/ch##-slug.md" }
```

Chapter numbers are always two-digit zero-padded (`ch01`, `ch14`, `ch30`).

---

## Step 6 — Final Checks

Run after all edits before committing:

```bash
grep -n "serialise\|optimise\|behaviour\|materialise\|synchronise\|recognise" <chapter-file>
```

Zero results expected.

Check every new `!!! note` admonition has content indented with 4 spaces.

Check every new bullet list has a blank line before it.

---

## Step 7 — Commit

Stage all changed files — the chapter, any updated stubs, new stub files,
and `zensical.toml` — and commit with a message that lists:

- Group A: one bullet per gap filled, with a brief description
- Group B: one bullet per forward reference added, naming the target chapter
- New stubs created (if any)

---

## Chapter-to-stub lookup (Spark book)

Use the spark-book skill's Chapter Arc table for chapter numbers and slugs.
The full arc is: B1–B9 → Ch01–09, I1–I10 → Ch10–19, A1–A10 → Ch20–29,
E1–E9 → Ch30–38.

Existing stub files (as of June 2026):
- `ch15-caching-persistence.md` (I6)
- `ch22-join-strategies.md` (A3)
- `ch30-spark-internals.md` (E1)
- `ch31-cluster-management.md` (E2)
