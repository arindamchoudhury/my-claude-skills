# Phase 3 — Book Chapter Writing

## The model

**Notes** (written by the `book-pdf-notes` skill) are source-faithful records — one per book chapter, article, or course module, capturing what that source said. They are the raw material.

**Book chapters** (written here) are topic-driven syntheses — one per learning-path topic, blending everything the user has read about that topic into a single authoritative chapter written in their own voice. The book chapter is not a summary of any one source. It is the user's integrated understanding, informed by all sources.

```
Source 1 (Rioux Ch 10)     ──┐
Source 2 (LS2e Ch 5)        ──┤──► Book Chapter: "Window Functions"
Source 3 (Spark docs)       ──┤
Source 4 (blog post)        ──┘
```

---

## Trigger

Phase 3 is triggered when the user says they have learned enough about a topic to write the chapter. Common phrasings:

- "I finished topic I2"
- "I know window functions well enough, write the chapter"
- "Write the book chapter for B7 — I've read Rioux Ch 5 and LS2e Ch 4"
- "I've been reading about Delta Lake MERGE, write chapter A6"
- "I completed the medallion architecture topic"

**Do not trigger Phase 3 after a single source.** The book chapter should synthesise multiple perspectives. If the user triggers after only one source, note which sources are still recommended for this topic (from the learning path entry) and ask if they want to proceed now or wait.

---

## Step 1 — Identify the topic

From the user's message, determine:
- The learning-path topic code (B1–E9 for Spark, or equivalent for other topics)
- The chapter number and slug from the topic-book skill's arc table
- Whether the chapter file already exists (read it if so — this may be an enrichment, not a new chapter)

Read the topic's entry in `docs/learning-path.md` to see:
- What the topic covers
- Which resources were recommended
- The milestone (the "you can..." statement)

---

## Step 2 — Gather all sources for this topic

Find every source the user has already read that covers this topic:

1. **Grep the notes directory** for the topic name and related terms:
   ```
   grep -r "window function" docs/books/ docs/topics/ --include="*.md" -l
   ```
2. **Read those note files** — extract the key concepts, code examples, distinctions, and pitfalls each source contributed
3. **Check the research cache** (`docs/research-cache/`) for any verified API facts about this topic
4. **Note what each source emphasised differently** — one book may focus on the API, another on performance, a third on common mistakes. These differences are valuable: the blended chapter should include all three angles.

If the user mentioned additional sources in their trigger message (web pages, articles), note those too — ask for the URL or content if not already in the notes.

---

## Step 3 — Web-search before writing

**Always run at least two searches before writing**, even if the notes seem complete. The goal is to:
- Verify current API behaviour against the latest version
- Find any pitfalls or gotchas not covered by the sources already read
- Check if best practices have evolved since the sources were written

```
"<topic> PySpark Spark 4.x best practices 2025 2026"
"<topic> common mistakes pitfalls PySpark"
```

Save any new verified facts to `docs/research-cache/`.

---

## Step 3b — Scope the chapter against the learning path

**The learning-path topic entry defines the chapter's scope — not the sources.**

Before writing, re-read the topic's entry in `docs/learning-path.md`. That entry specifies:
- **What it is** — the exact concepts this chapter must cover
- **Milestone** — the concrete outcome the reader must be able to achieve

The chapter must cover everything in the "What it is" definition and enable the milestone. If a source covers more than the topic's scope, do not include the extra material — it belongs in a different chapter. If the sources together don't cover something in the scope, fill the gap from web research or official docs.

**Example:** Topic I2 is "Window Functions". Its scope includes WindowSpec, aggregate functions over windows, ranking functions, analytic functions, frame boundaries, and UDFs on windows. If Rioux Ch 10 also touched on performance implications of windows — that belongs in A3 (Join Strategies and Tuning) or A4 (Data Skew), not here. Keep this chapter focused.

This is the key difference from notes: notes capture everything a source said; the book chapter captures only what belongs to this topic.

---

## Step 4 — Synthesise, don't summarise

Before writing, produce a **synthesis plan** — a brief outline that shows how the sources will be blended:

```
Topic: Window Functions (I2)

Sources:
- Rioux Ch 10: best motivating example (self-join → window); full API walkthrough; GSOD dataset
- LS2e Ch 5:   SQL-flavoured framing; higher-order function connection
- SDG Ch 7:    deepest explanation of frame semantics (ordered vs unordered default)
- Spark docs:  current API; frame boundary constants

Synthesis plan:
1. Problem (self-join is the wrong tool) — from Rioux
2. Mental model (partition / apply / combine without collapsing) — from Rioux + LS2e
3. WindowSpec builder — API from Spark docs, verified
4. Aggregate functions over windows — Rioux example + SDG semantic explanation
5. Ranking functions — Rioux examples; table comparing all five
6. Analytic functions (lag/lead/cume_dist) — Rioux + SDG
7. Frame boundaries — SDG explanation (best); Rioux example (best); the ordering-changes-default-frame surprise
8. UDFs on windows — Rioux §10.4
9. Pitfalls — from all sources + web research

Conflicts / different framings:
- Rioux uses "partition/apply/combine"; SQL tradition uses different vocabulary — present both
- SDG frames window specs differently from Rioux — use SDG's framing for the frame boundary section (more precise)
```

Show the synthesis plan to the user before writing the full chapter if the topic is complex. For simple topics, proceed directly.

---

## Step 5 — Write the chapter

Use the topic-book skill's chapter template (e.g., `~/.claude/skills/spark-book/SKILL.md`).

### Blending rules

**Present the best explanation, not the first explanation.** If Source B explains a concept more clearly than Source A, use Source B's framing — even if the user read Source A first. The book chapter is not a reading log.

**When sources frame the same concept differently, present both explicitly:**
> *"Rioux calls this the split-apply-combine pattern; the SQL tradition calls the three stages partition, apply, and implicitly combine. Same mechanics, different vocabulary — you will encounter both."*

**When sources contradict, name the contradiction:**
> *"Rioux (2022) recommends X; the current Spark 4.x docs recommend Y instead because of Z. Use Y."*

**When a newer source supersedes an older one, say so:**
> *"The `@F.pandas_udf('double', PandasUDFType.GROUPED_AGG)` syntax shown in older books is deprecated. The current pattern (Spark 3.0+) uses type hints: `def fn(s: pd.Series) -> float:`"*

**Use the best code example across all sources.** Don't copy-paste from one source. Write a new example that is cleaner, more complete, and illustrates the point better than any single source managed. All code must be current (Spark 4.x, Python 3.10+) and runnable.

**Do not cite sources in the body prose.** The chapter is written in the user's voice, as their understanding. Source attribution lives in the References section at the end.

### Chapter structure

Follow the topic-book skill's template exactly:
1. What you'll learn (3–5 bullet outcomes)
2. The problem this solves (concrete scenario)
3. Core concept (200–400 words; the WHY)
4. Examples (minimal → complete; one new idea per example)
5. Common pitfalls (3–5; drawn from all sources + web research)
6. Exercises (recall / apply / extend)
7. Summary (3–5 bullets; last sentence points to next chapter)
8. References (bullet list of all sources that informed this chapter)

---

## Step 5b — Discover new topics and enrich completed ones

While gathering sources and writing the chapter, two things can happen:

1. **A concept with no topic entry is found** — add it to the learning path as a new `⬜` topic
2. **New information about an already-✅ topic is found** — blend it into that topic's existing chapter

Both are equally important. A ✅ mark means "a chapter exists", not "the chapter is frozen". The book grows richer as more sources are read.

---

### For each NEW topic found (no entry yet in the learning path):

1. **Determine its level** — does it require prior topics to understand? Place it at the correct level using the dependency rule: if it requires knowledge from level X, it belongs at level X or higher.

2. **Determine where it fits in sequence** — insert it near related topics, not at the end of the level.

3. **Add it to `docs/learning-path.md`** — use the standard topic entry format with `⬜` status:
   ```markdown
   ### ⬜ <Code> — <Title>

   **What it is:** ...
   **Why you need it:** ...

   **How to learn it:**
   1. ...

   **Milestone:** You can ...
   ```
   Re-number subsequent topic codes if inserting mid-sequence (e.g., inserting after B3 shifts B4→B5 etc.). If renumbering is disruptive, use a decimal code instead: `B3a`.

4. **Add it to the book index** (e.g. `docs/spark-book/index.md`) — insert a new `⬜` row at the correct chapter position. Update the chapter numbers of subsequent rows.

5. **Add it to the topic-book skill's arc table** (`~/.claude/skills/<topic>-book/SKILL.md`) — insert a row in the chapter arc at the correct position.

---

### For ENRICHING an already-✅ topic:

When a source being read for topic X contains significant new information about an already-completed topic Y:

1. **Read the existing chapter for topic Y** in full before touching it.

2. **Identify the insertion point** — where does the new information belong? It may be:
   - A new subsection within an existing section
   - An additional pitfall
   - A better or complementary code example
   - A different framing of an existing concept (present both explicitly)
   - A version-specific note (if the new source is more current)

3. **Blend it in** — do not append to the bottom of the chapter. Insert at the logical place. Follow the same blending rules as Step 4:
   - If the new framing is clearer than the existing one, replace or present both explicitly
   - If the new source contradicts the existing content, name the contradiction
   - If the new source is more current, update the version note

4. **Add any new glossary terms** from the new content.

5. **The chapter stays ✅** — enrichment does not reset the status. The chapter was done before; it is richer now.

---

Report at the end of Step 7 confirmation:
- New topics added: list them with their codes
- Existing chapters enriched: list the chapter numbers and what was added

---

## Step 6 — Sync site files

After writing the chapter:

1. **`docs/learning-path.md`** — flip the topic heading from `⬜` to `✅`
2. **Topic-book index** (e.g. `docs/spark-book/index.md`) — flip ⬜ to ✅, add date
3. **`zensical.toml`** — add chapter entry under the book nav group
4. **`docs/reference/glossary.md`** — append new terms (source: "Book Ch NN")
5. **`docs/topics/index.md`** — if this topic was in the backlog, move it to active or mark complete

---

## Step 7 — Confirm to user

```
✓ Chapter NN: "<Title>" written → docs/spark-book/ch<NN>-<slug>.md
  Learning path: <code> marked ✅
  Sources blended: [list source names]
  New glossary terms: N

  New topics added to learning path: [list with codes, or "none"]
  Existing chapters enriched: [e.g. "Ch 11 (I2 Window Functions) — added rangeBetween pitfall", or "none"]

Book progress: N / total chapters  (N ✅  |  N ⬜)
Next learning-path topic: <code> — <title>
```

---

## Code standards

All code in book chapters must follow the topic-book skill's code standards exactly.

For Spark chapters specifically:
- Always `import pyspark.sql.functions as F` and `import pyspark.sql.types as T`
- Every example is complete and runnable — all imports present, SparkSession created
- Version comment on first block: `# Apache Spark 4.1.x / Python 3.10+`
- Show actual output as inline comments where helpful
- Never truncate with `# ...` or `# etc`
- Use current APIs — if an older source showed a deprecated pattern, show only the current equivalent with a note that the old pattern existed
