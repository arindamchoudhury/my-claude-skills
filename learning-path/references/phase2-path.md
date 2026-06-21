# Phase 2 — Learning Path

Write `C:\opt\learn\<topic-slug>\notes\docs\learning-path.md`.

The learning path is **topic-based, not resource-based**. The primary unit is a *topic* — a discrete concept or skill the learner must acquire. Resources (books, courses, videos, docs) are subordinate: they appear as advice *within* each topic, not as the organizing structure.

A resource-based path says: "Read Chapter 7 of Book X, then take Course Y."
A topic-based path says: "Learn window functions. Here is the best multi-modal path to do that."

---

## The structure

```
learning-path.md
├── Resources at a glance (abbreviation table)
├── Certifications (all certs, exam topics, level mapping, when to attempt)
├── Beginner
│   ├── Level goal + estimated hours
│   ├── Topic B1
│   ├── Topic B2
│   ├── ...
│   └── Checkpoint (what you can build; cert target if applicable)
├── Intermediate
│   └── (same pattern)
├── Advanced
│   └── (same pattern)
├── Expert
│   └── (same pattern)
└── Suggested study sequence (ASCII flow diagram)
```

---

## Rules for topic ordering

1. **Dependency first** — if topic B requires topic A, A comes before B, regardless of which resource covers it more prominently
2. **Within a level, order by concept breadth** — foundational mental models before specific APIs; APIs before performance tuning; tuning before production operations
3. **Certifications are checkpoints, not topics** — place them at the end of the level whose topics they validate
4. **Each level must have a clear exit condition** — a concrete mini-project or capability statement that tells the learner they are ready to advance

---

## Topic status tracking

Every topic heading carries a status emoji that is updated when the topic is completed:

- `⬜` — not yet started
- `✅` — done (book chapter written)

**Initial state:** all topics are `⬜`.

**When Phase 3 completes a chapter**, update the corresponding topic heading from `⬜` to `✅` in `learning-path.md`.

**When a new topic is discovered** (see Phase 3), insert it at the correct level with `⬜` status and add it to the book index.

---

## How to write each topic entry

Every topic entry has exactly these five parts. Keep each part tight.

```markdown
### ⬜ <Code> — <Title>

**What it is:** One sentence. The API, concept, or pattern being learned.

**Why you need it:** One sentence. What breaks or becomes impossible without it.

**How to learn it:**

1. **[Resource type] — [Resource name]** (~X min/hrs) — what specifically to do with it
2. **[Resource type] — [Resource name]** (~X min/hrs) — what specifically to do with it
3. ...

**Milestone:** One sentence. A concrete, self-testable outcome. Starts with "You can..."
```

---

## Rules for "How to learn it"

This is the most important part. Follow these rules:

### Use multiple resource types per topic

Every topic should have **at least two different resource types** from this list:

| Type | Examples | When to use |
|---|---|---|
| **Video / lecture** | Udemy section, YouTube video, MOOC lesson | First exposure — build the mental picture |
| **Interactive exercise** | DataCamp, Kaggle notebook, edX lab | Solidify understanding through doing |
| **Official docs** | Apache Spark docs, Delta Lake docs | Canonical reference; verify current behaviour |
| **Book chapter** | O'Reilly, Manning chapters | Depth and nuance after the mental picture exists |
| **University MOOC** | Coursera, edX, MIT OpenCourseWare | Structured academic treatment |
| **Official course** | Databricks Academy, LangChain Academy | Vendor-validated; often matches cert exams |
| **Hands-on project** | Build X against local stack | Only way to confirm real understanding |

### Sequence within a topic matters

The recommended sequence for most topics:

1. **Watch first** — a short video (5–30 min) to build the mental picture before reading
2. **Do an exercise** — interactive or notebook; confirms the picture is correct
3. **Read for depth** — a book chapter or official guide for nuance and edge cases
4. **Reference** — the official API docs; bookmark for when actually coding

Not every topic needs all four. Simple topics may need only two resources. Complex topics may need five.

### Be specific, not vague

❌ Wrong: "Read LS2e Chapter 7 for tuning."
✅ Right: "**Book chapter — LS2e Ch 7** (~2 hrs) — focus on the joins section (pp. 180–195) and the Spark UI walkthrough; skip the Datasets section (Python-irrelevant)."

❌ Wrong: "Take the Databricks course."
✅ Right: "**Official course — Databricks Advanced DE, Module 3** (~4 hrs) — the Spark UI analysis and skew optimisation sections specifically; the CI/CD module is for E7, skip it here."

### Do not default to books

Books are one resource type among many. For most beginner and intermediate topics, a **video + interactive exercise** combination produces faster and more durable learning than reading alone. Books are best for advanced topics where depth matters and for reference.

### Flag outdated resources

If a resource targets a version more than one major release behind current stable, add:
> 📌 Covers v\<X>; current is v\<Y>. Core concepts apply; verify API names against current docs.

---

## Certifications section

Write a table at the top of the file listing all certifications found in research:

```markdown
## Certifications

| Cert | Provider | Level | Topics tested (weights) | Fee | When to attempt |
|---|---|---|---|---|---|
| Name | Provider | Intermediate | Topic A 30%, Topic B 20%, ... | $X | After Intermediate |
```

- **Topics tested** — use actual percentages from the exam guide; don't invent them
- **When to attempt** — the level whose checkpoint this cert validates
- Place a reminder line at the bottom of the relevant level checkpoint: `**Certification target:** <cert name> — validates topics X through Y.`

---

## Resources at a glance

Write an abbreviation table at the top so the topic entries can use short codes:

```markdown
## Resources at a glance

| Abbrev | Name | Type | URL |
|---|---|---|---|
| **Abbrev** | Full resource name | Book / MOOC / Video course / Official course / Docs | URL |
```

Only include resources that are actually cited in topic entries.

---

## Checkpoint format

End each level with a checkpoint:

```markdown
### ✅ <Level> Checkpoint

You are ready to advance when you can:
- [Concrete capability 1 — something you can build or demonstrate]
- [Concrete capability 2]
- [Concrete capability 3]

**Certification target:** <cert name> — validates topics <X>–<Y>. Attempt after this checkpoint.
```

The capabilities must be **build-something or explain-something** statements, not "you have read X."

---

## Suggested study sequence

End the file with a text diagram:

```markdown
## Suggested study sequence

​```
Beginner (B1–BN)      → ~XX hrs  →  [Cert if applicable]
    ↓
Intermediate (I1–IN)  → ~XX hrs  →  [Cert if applicable]
    ↓
Advanced (A1–AN)      → ~XX hrs  →  [Cert if applicable]
    ↓
Expert (E1–EN)        → ~XX hrs  →  [Cert if applicable]
​```

**You are currently here:** <level, and which topics are done if known>
```

---

## Full file template

```markdown
# Learning Path: <Topic>

> **Last updated:** YYYY-MM-DD
> **Current stable version:** <version> (released <date>)
> **Local stack (if applicable):** <what the user is running>
>
> **How to read this page.** Topics are the primary unit. Each topic has a "How to learn it"
> section that recommends a multi-modal path — video first, then exercises, then depth reading.
> Resources (books, courses, docs) serve the topics; they are not the organizing structure.

---

## Resources at a glance

[abbreviation table]

---

## Certifications

[certifications table]

---

## Beginner

**Goal:** [one sentence — what a beginner can do when done]
**Estimated time:** ~XX hrs

---

### B1 — <Title>

**What it is:** ...
**Why you need it:** ...

**How to learn it:**

1. **Video — [name]** (~X min) — [specific instruction]
2. **Interactive — [name]** (~X hrs) — [specific instruction]
3. **Book chapter — [name]** (~X hrs) — [specific instruction]
4. **Reference — [name]** — [specific instruction]

**Milestone:** You can ...

---

[B2 through BN ...]

---

### ✅ Beginner Checkpoint

You are ready to advance when you can:
- ...

---

## Intermediate

[same pattern]

---

## Advanced

[same pattern]

---

## Expert

[same pattern]

---

## Suggested study sequence

[ASCII diagram + current position note]

---

## Sources consulted

[list of URLs fetched during research]
```

---

## After writing

Update `zensical.toml` — `learning-path.md` must be in the nav.

**Verify the site builds before claiming the scaffold is done.** This is the first point where every
nav entry has a real file behind it, so it's the moment to catch a broken nav, a missing stub, or a
bad TOML edit. Run the project's build and confirm it exits clean:

```
python -m venv .venv && .venv\Scripts\python -m pip install zensical   # first time only
.venv\Scripts\python -m zensical build
```

(Or `docker compose up` if the project uses the Docker flow.) A non-zero exit or an error about a
missing/duplicate nav target means a stub from Phase 1 Step 6 is missing or `zensical.toml` is
malformed — fix it before reporting success. Don't announce a working site you haven't built.

Tell the user:
- Learning path written at `docs/learning-path.md`
- How many topics across how many levels
- Which topic to start with (B1)
- That the site builds clean
- How to trigger Phase 3: "When you finish a topic, tell me what you completed and I'll write the book chapter"
