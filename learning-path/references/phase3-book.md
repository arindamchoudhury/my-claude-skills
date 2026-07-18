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

1. **Grep the reading-notes directory** for the topic name and related terms:
   ```
   grep -rl "window function" docs/sources/ --include="*.md"
   ```
   `docs/sources/` is the canonical reading-notes location (see SKILL.md "Canonical project layout");
   in an older project this is `docs/books/` — grep whatever exists.
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

The chapter must cover everything in the "What it is" definition and enable the milestone. If a source covers more than the topic's scope, do not include the extra material — it belongs in a different chapter. If the sources together don't cover something in the scope, fill the gap from web research or official docs — **never from training memory alone**. A milestone can name a comparison or fact no note covers (e.g. "explain how Terraform differs from Ansible" when no read source mentions Ansible at all). That is the trigger to web-search and save the verified result to `docs/research-cache/<topic>.md`, then write the passage grounded in that cache file — the same way version numbers and current-state facts get verified, not recalled. Treat comparison tables, "common misconceptions" sections, and any named third-party tool/product claim with the same suspicion as a version number: if it isn't in a note, it needs a citation before it goes in the chapter.

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

Read the topic-book skill's chapter guidance (e.g., `~/.claude/skills/spark-book/SKILL.md`) for code standards and the element toolkit. There is no fixed chapter template — see "Chapter form" below.

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

### Chapter form — fit the topic, don't fill a template

**There is no fixed section list.** The right structure depends on what kind of topic this is. A setup/installation chapter, an API-walkthrough chapter, an architecture/internals chapter, and a tuning chapter each want a different shape. Forcing all of them through the same headings produces padded, unnatural chapters where half the sections are filler.

Instead, every chapter must satisfy a few **invariants**, and otherwise draws freely from a **toolkit of elements** in whatever order reads best for the topic.

**Invariants — every chapter, no exceptions:**

- Opens by establishing why the topic matters — the problem it solves or the capability it unlocks. The reader should know within the first screen why they're here.
- Teaches toward the learning-path milestone for this topic. When the reader finishes, they can do the thing the milestone names.
- All code is current (Spark 4.x / Python 3.10+), complete, and runnable — no deprecated APIs, no `# ...` truncation.
- Prose is built from short sentences — one idea per sentence, not long clause-stacked ones. Easier to read and to revise.
- No em-dash-bracketed comma lists as an aside (`"...practices — versioning, review, CI/CD — that..."`). That construction reads as one long clause wearing a short-sentence disguise — it fails the "short sentences" invariant above even when the individual words are short. Write the list as its own sentence, or introduce it with a colon: `"...practices that manual provisioning never had: versioning, review, and CI/CD."` Split into separate sentences if the aside is doing real work, don't just swap the dashes for a colon and call it fixed.
- **Every body callout is a Material admonition** (`!!! note "Title"` / `tip` / `warning` / `info` / `danger`), never an emoji-blockquote. This is mandatory, not size-conditional: a one-line aside, a definition, a `(mine)` observation, and a version-gate box are all admonitions. `>` blockquotes are reserved for the chapter-header front-matter (source citation + summary + see-also) only; a `>` blockquote anywhere in the chapter body is a defect to convert on sight. A blockquote also can't box a table and silently corrupts an adjacent list. Never indent an admonition or blockquote *into* a list item — it swallows the following bullets. Place it after the list, or unindented between two bullets of an *unordered* list (splits it cleanly; don't do this inside a numbered list). Rebuild and confirm the following bullets still render. Full formatting rules: `book-pdf-notes/references/note-style.md` → "Code, callouts, sidebars".
- Ends pointing forward — the closing lines connect to the next topic or to what this chapter unlocks.

**Toolkit — use the elements the topic needs, in the order that serves it:**

- Learning outcomes up front (valuable for dense topics; skip for short ones)
- A motivating problem or failed-the-hard-way scenario
- Core-concept / mental-model prose (the WHY)
- Worked examples, minimal → complete, one new idea each
- Diagrams (Mermaid) where a picture beats prose — architecture, data flow, partitioning
- A reference table where the topic is API-shaped (a family of functions, config keys, frame types)
- A semantics / edge-case section where correctness is subtle (streaming watermarks, null handling, frame defaults)
- Common pitfalls drawn from all sources + web research
- Performance notes where the topic has cost implications
- Exercises (recall / apply / extend)
- Summary
- References (all sources that informed the chapter)

**Match the shape to the topic — examples:**

- *Setup / environment* → mostly procedure + verification; heavy on "what can go wrong"; few or no exercises.
- *API family* (e.g. DataFrame transformations) → organised around a reference table plus one tight example per important operation.
- *Architecture / internals* → prose and diagrams lead; code is illustrative, not the point.
- *Concept* (e.g. window functions) → problem → mental model → examples → semantics → pitfalls.
- *Tuning / operations* → symptom → diagnosis → fix, with Spark UI walkthroughs and before/after metrics.

Let the topic pick the structure. A chapter that needs only four of these elements should have only four — don't manufacture a "Pitfalls" or "Exercises" section just to fill a slot.

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

4. **Add it to the book index** (`docs/book/index.md`, or `docs/<topic>-book/index.md` in older projects) — insert a new `⬜` row at the correct chapter position. Update the chapter numbers of subsequent rows.

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

## Step 5c — Audit coverage against every source

**A chapter with zero false claims can still be incomplete.** Being grounded (nothing invented) is a different property from being complete (nothing dropped) — checking one does not check the other. Do this pass even when the draft reads fine and nothing seems obviously missing; the gaps this step catches are exactly the kind that don't surface on a re-read looking for errors, only on a line-by-line diff against the source.

1. Re-open every note and topic page cited in the synthesis plan (Step 4), one at a time.
2. Walk each one section by section. For every substantive point — not just headline claims, but named tools, named pillars/categories, worked examples, and specific figures — confirm it landed somewhere in the chapter.
3. For anything that didn't land, it must fall into exactly one of two buckets:
   - **In scope, just missing** → add it to the chapter now, at the logical insertion point (not appended at the bottom).
   - **Out of scope for this topic** → say so explicitly, naming which later topic owns it (e.g. "full CLI walkthrough → B3", "state internals → B9", "CI/CD depth → A3"). A deliberate, named deferral is fine. A silent omission is not.
4. Do not treat "the source's own summary/bullet list" as sufficient proxy for its full content — sources often bury a real point (a named comparison, a specific pillar, a fourth example in a list of nine) inside prose the synthesis pass can skim past. Check the actual section headers of the note, not just its final summary.

If this step turns up several missing items, fix them all in the same pass rather than one at a time — re-running the whole audit after each small fix wastes turns.

---

## Step 6 — Sync site files

After writing the chapter:

1. **`docs/learning-path.md`** — flip the topic heading from `⬜` to `✅`
2. **Book index** (`docs/book/index.md`, or `docs/<topic>-book/index.md` in older projects) — flip ⬜ to ✅, add date
3. **`zensical.toml`** — add chapter entry under the book nav group
4. **`docs/reference/glossary.md`** — append new terms (source: "Book Ch NN")
5. **`docs/topics/index.md`** — *only if the project has a topic backlog* (older projects do; new scaffolds don't) — move this topic to active or mark complete

---

## Step 7 — Confirm to user

```
✓ Chapter NN: "<Title>" written → docs/book/ch<NN>-<slug>.md
  Learning path: <code> marked ✅
  Sources blended: [list source names]
  Coverage audit: [done — N gaps found and fixed, or "clean, nothing missing"]
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
