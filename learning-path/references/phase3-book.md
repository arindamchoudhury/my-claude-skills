# Phase 3 — Chapter Writing

Triggered when: user wants notes from a notebook/lesson they just studied

Every lesson produces **two outputs**:
1. **Research note** (`docs\sources\<course-slug>\<slug>.md`) — source-faithful reference, code examples, cross-linked
2. **Book chapter** (`docs\book\ch<NN>-<slug>.md`) — fully explained, pedagogical, with pitfalls and exercises

---

## Step 1: Identify what was covered

From the user's message or the notebook file(s), determine:
- Which course and which module/lesson
- What concepts were demonstrated (read the notebook cells)
- What the user's notes or impressions are (if they share any)

Read the notebook(s) directly from the course repo. Check `cache\web\` first if the lesson is a web page.

---

## Step 2: Validate against official docs + cache

Before writing a single word:

1. **Check `cache\search\`** — grep for the main concept. If a recent verified entry exists, use it.
2. **Web-search and fetch official docs** for each function/class used in the notebooks. Verify:
   - Current API / import path
   - All parameters and their types
   - Return type and structure
   - Current stable version
   - Any deprecation warnings
3. **Save new findings** to `cache\search\<slug>.md`:

```markdown
# <concept>

**Checked:** YYYY-MM-DD
**Source:** <url>

## Findings
[Key facts, parameter list, return type, examples]
```

4. **Compare versions** — if the course was teaching on version X but current stable is Y, note the differences.

---

## Step 3: Determine book action — new chapter or blend

Read `docs\book\index.md` to see existing chapters.

| Situation | Action |
|---|---|
| Topic not covered yet | Create new `docs\book\ch<NN>-<slug>.md` |
| Topic partially covered | Blend new content into existing chapter |
| Topic contradicts existing content | Add both framings + explicit comparison |
| Minor addition | Add a new section to existing chapter |

**Chapter number:** count existing chapters in `docs\book\index.md` + 1.
**Slug:** kebab-case of main topic — `foundational-models`, `prompt-templates`, `rag-pipeline`.

---

## Step 4: Write the book chapter

Use the topic book skill's chapter template (`~/.claude/skills/<topic>-book/SKILL.md`).

```markdown
# Chapter N: <Title>

> **Source:** [<Course> — <Module/Lesson>](<url>)
> **Notebooks:** `<notebook-filenames>`
> **Version:** <package versions>
> **Added:** YYYY-MM-DD

## What you'll learn
3–5 bullet points of concrete outcomes.

## The problem this solves
One paragraph — WHY this exists, what breaks without it.

## Core concept
200–400 words explaining the WHY, not just the WHAT.
Use analogies or a comparison table where helpful.

## Code examples
Build from minimal → complete. One new idea per example.
Every example must be complete and runnable — all imports, load_dotenv().

## Common pitfalls
3–5 bullets: what goes wrong, why, how to fix it.

## Exercises
1. Recall — can answer from reading
2. Apply — requires running the code
3. Extend — open-ended, no single right answer

## Summary
3–5 bullets. Last sentence: what the next chapter builds on.
```

### Blending into an existing chapter

1. Read the full existing chapter before touching it
2. Never silently replace existing content — add alongside
3. New sections go at the logical insertion point, not always the bottom
4. When two sources frame the same concept differently, present both framings explicitly
5. Contradictions: name them: *"Unlike [[earlier-source]] which says X, this source argues Y because..."*
6. Update the version note if the new source covers a more recent version

---

## Step 5: Write the research note

After the book chapter is done, write a lighter source note at `docs\sources\<course-slug>\<lesson-slug>.md`.

The research note is **source-faithful** — it captures what the lesson/notebook actually showed. The book chapter is the explanation. The research note is the reference.

```markdown
---
name: <lesson-slug>
description: <one-line summary of what this lesson covers>
---

# <Lesson Title>

> **Source:** [<Course> — <Module/Lesson>](<url>)
> **Notebooks:** `<filenames>`
> **Added:** YYYY-MM-DD
> **Tags:** tag1, tag2, tag3
> **Type:** notebook / course lesson

> 📌 **Full explained chapter:** [[<book-chapter-slug>]] — includes deeper explanations, best practices, exercises.

## Summary
One paragraph — what this lesson covers and why it matters.

## Key points
- Bullet list of the most important concepts demonstrated.

## Notes
Code-first walkthrough of what the notebook showed.
Use `###` subsections for each major topic in the lesson.
Include all code examples from the notebook (complete, runnable).
Add brief explanation above each block — what it does and why.

## Open questions
- Things the notebook raised but didn't explain.
- Anything to investigate further.

## Related sources
- [[previous-lesson-slug]] — relationship note
- [[book-chapter-slug]] — full pedagogical treatment
```

---

## Step 6: Version callouts

If the course was teaching on an older version than current stable, add to the book chapter (after frontmatter, before "What you'll learn"):

```markdown
> 📌 **Version note:** Taught on <package> v<X>. Current stable is v<Y> as of <date>.
> Key differences: <what changed>. See [migration guide](<url>).
```

Add to research note similarly. No callout needed for patch-only differences (1.2.0 vs 1.2.2).

---

## Step 7: Sync everything

After writing both files, update all of these:

**Book nav:**
- `docs\book\index.md` — add row: `| N | [Chapter title](ch<NN>-<slug>.md) | Source | date |`
- `zensical.toml` Book group: `{ "N. Chapter Title" = "book/ch<NN>-<slug>.md" }`

**Research notes nav:**
- `docs\sources\<course-slug>\index.md` — add lesson row to the Lessons table
- `docs\sources\index.md` — add row under the correct course section
- `zensical.toml` Research Notes group: add `{ "X.Y Lesson Title" = "sources/<course-slug>/<lesson-slug>.md" }` under the course nested group

**Reference:**
- `docs\reference\glossary.md` — add every new term introduced in the lesson
- `docs\topics\index.md` — add new topics to backlog (or promote to active topic page if ≥2 sources now cover it)
- `docs\reference\resources.md` — add any new official doc links used during research

**Home page:**
- `docs\index.md` — update book progress count and latest chapter

---

## Step 8: Confirm to user

```
✓ Book chapter:    "Chapter N: <Title>" → docs\book\ch<NN>-<slug>.md
✓ Research note:   "<Lesson Title>"     → docs\sources\<course-slug>\<lesson-slug>.md
  Version note: [added / updated / none needed]
  Glossary: N new terms added
  Topics backlog: N new topics added

Book progress: N chapters
Next in learning path: <what to study next>
```

---

## Code standards

- Every code block must be complete and runnable — no truncation, no ellipsis
- Always include imports at the top of the first code block in a chapter/note
- Always include `load_dotenv()` when API keys are used
- Add inline version comment: `# <package> <version> (Month Year)`
- Use current APIs — if the notebook used a deprecated pattern, show the current equivalent and note the change
