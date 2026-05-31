---
name: zensical-notes
description: Build and extend a Zensical "reading notes" site from PDF books, papers, or technical manuals — including multi-book setups studying one topic across several sources. Trigger whenever the user wants to take notes on a PDF, study chapter-by-chapter, summarize a book into durable docs, extend an existing notes site, add a second book to an existing site, or compare what multiple books say about a topic. Catches phrases like "take notes on this PDF", "let's do chapter X", "summarize this chapter", "I'm studying [topic]", "add this book to my notes", "compare these books on X", and any time a user uploads a PDF and asks for note-taking help — even without naming Zensical. Produces detailed-outline Markdown, scaffolds multi-book projects by default (per-book chapters plus cross-book topic pages), keeps nav/reading-log/glossary/topic-pages in sync, and refreshes version-specific content to the latest release at note-taking time.
---

# Zensical Notes

A workflow for turning PDFs into a personal study site built with [Zensical](https://zensical.org/) — the static-site generator from the Material for MkDocs team. The output is a folder of plain Markdown files plus a `zensical.toml` config; the user runs the site locally with `zensical serve` (or via Docker) and gets a clean, searchable, navigable docs site of their notes.

## When to use this skill

Use it whenever the user wants to *capture* knowledge from a PDF in a way they'll come back to. Strong cues:

- They've uploaded a PDF (a book, paper, manual, RFC, course handout) and want to study it.
- They mention chapter-by-chapter work: "let's do chapter 2", "next chapter", "give me a detailed outline".
- They mention an existing notes folder, or a Zensical / MkDocs project.
- They're studying a technology and want notes that stay useful as the technology evolves.
- They want to study the same topic across multiple books and have one place to think across them.

This skill is not for: short Q&A on a PDF, extracting a single quote, translating, OCR, or filling forms — defer to the **pdf** skill for those. If the user wants a Word doc or PowerPoint instead, defer to **docx** / **pptx**.

## Project layout

The **multi-book hybrid layout is the default**. Use it for every fresh project and every existing single-book project. Detect which state you're in before doing significant work — `ls` of the notes root answers it.

### Multi-book hybrid layout (default)

This is the standard layout even when starting with a single book. Per-book chapter notes live under `docs/books/<slug>/`; cross-book topic pages live under `docs/topics/`. Topic pages are written as backlog entries when only one book exists and promoted to full pages once a second book overlaps.

```
<notes-root>/
├── zensical.toml
├── docs/
│   ├── index.md              # hub linking Topics + Books + Reference
│   ├── topics/
│   │   ├── index.md          # topic list + "topics to write" backlog
│   │   ├── mvcc.md           # ← Ferrari Ch 11 + Rogov Ch 4 (once ≥2 books)
│   │   └── …
│   ├── books/
│   │   ├── ferrari/
│   │   │   ├── index.md      # per-book reading log
│   │   │   ├── page-map.md   # PDF page ranges (one-time extraction, reused every session)
│   │   │   ├── pdf-cache/    # raw extracted chapter text (reused across sessions)
│   │   │   │   ├── 01-<slug>.txt
│   │   │   │   └── …
│   │   │   └── chapters/
│   │   │       ├── 01-<slug>.md
│   │   │       └── …
│   │   └── <next-book>/
│   │       ├── index.md
│   │       └── chapters/…
│   └── reference/
│       ├── glossary.md       # merged across books, with source attribution
│       └── resources.md
├── Dockerfile
├── docker-compose.yml
└── README.md
```

**Detection:**
- `docs/books/` with at least one sub-folder → multi-book mode. Read `references/multi-book.md` and follow its workflow.
- `docs/chapters/` present, no `docs/books/` → **legacy single-book project**. Migrate to multi-book before adding any new chapter or book (see "Migration" below).
- Nothing present → scaffold multi-book from scratch using `references/scaffold.md`.

**Why default to multi-book even for one book?** The structure is ready for a second book the moment you start it, without a disruptive migration. Topic pages sit in the backlog — not wasted space, a useful reminder of what's waiting for a second source. Navigation is consistent regardless of how many books you eventually add.

**Read `references/multi-book.md`** at the start of every session involving a multi-book project. It has the full workflow, topic-page template, cross-linking convention, glossary format, and migration steps.
See `references/scaffold.md` for the drop-in templates to use when bootstrapping a fresh project.

### Single-book layout (legacy / explicitly requested)

Use this *only* when the user explicitly asks for the simpler layout or is working with an existing single-book project that they don't want to migrate.

```
<notes-root>/
├── zensical.toml
├── docs/
│   ├── index.md          # landing page + reading log table
│   ├── chapters/
│   │   ├── 01-<slug>.md
│   │   └── …
│   └── reference/
│       ├── glossary.md
│       └── resources.md
└── …
```

**Migration to multi-book:** whenever a single-book project needs a second book, or when the user asks for topic pages, migrate first. Steps:

1. Move `docs/chapters/` → `docs/books/<existing-slug>/chapters/`.
2. Create `docs/books/<existing-slug>/index.md` (reading log moves here from `docs/index.md`).
3. Create `docs/topics/index.md` with the topic-backlog structure.
4. Rewrite `docs/index.md` as the multi-book hub.
5. Restructure `nav` in `zensical.toml` to Topics / Books / Reference.
6. Add a `Source` column to every glossary table.
7. Run `zensical serve` and verify no broken links before adding the new book.

## The flavors of work

Almost every invocation of this skill is one of these:

1. **First time with a book, fresh site** — no notes folder yet. Scaffold a *multi-book* project (templates in `references/scaffold.md`). Read the PDF TOC, lay out placeholder chapter files under `docs/books/<slug>/chapters/`, write detailed notes for the requested chapter, add topics to the `docs/topics/index.md` backlog, update the per-book reading log, update glossary and resources.

2. **Adding a chapter to an existing multi-book site** — `docs/books/<slug>/` already exists. Fill in one more chapter file, flip the reading-log row to ✅, add new terms to the glossary (with source attribution), add links to resources. Then do the topic-page pass: identify which topics this chapter touches, decide whether to extend an existing topic page, create one (≥2 books overlap), or add to the backlog. Cross-link bidirectionally.

3. **Adding a new book to an existing multi-book site** — create `docs/books/<new-slug>/` with its own `index.md` and placeholder chapter files. Wire the new book into `zensical.toml` nav and `docs/index.md`. Then proceed as flavor 2 for each chapter studied.

4. **Legacy: adding a chapter to an existing single-book site** — if `docs/chapters/` is present and the user hasn't asked to migrate, continue in single-book mode: fill in the chapter file, update `docs/index.md` reading log, update glossary and resources. Flag the migration opportunity if a second book comes up.

5. **Chat Q&A → notes addition** — the user asks a conceptual question in the chat ("how does X work?", "what's the difference between X and Y?"), gets an answer in conversation, then says "add that to the notes" or "add a section for X". Workflow:
   1. Grep the chapter files to find where the related content lives — don't guess, confirm the exact line.
   2. Identify the right insertion point (after which section/subsection the new content belongs).
   3. Write the section using the detail from the conversation answer, styled to match the surrounding notes (callouts, code blocks, comparison tables as appropriate).
   4. If the user adds a follow-up ("what about X in Y context?") and then says "yes" (add it), append it as a callout or sub-section at the logical end of the section just written — don't restructure the whole section.
   5. No reading-log or glossary update needed unless the addition introduces new terms.

6. **Enriching from companion notebooks** — the user asks you to incorporate content from bonus/companion Jupyter notebooks (e.g., `ch03/` bonus notebooks alongside a textbook). Two mandatory rules apply — see "Working with companion notebooks" section below.

Always confirm which flavor applies before doing significant work. A quick `ls` of the notes root answers it.

## The detailed-outline note style

This is the only style this skill produces by default. It's a hierarchical outline that captures the *structure* of the chapter — sections, subsections, the few things in each subsection that actually matter — written in prose-y bullets and short paragraphs rather than a flat summary or quote dump.

Why this style and not "just summarize"? A reader returns to study notes mostly to *find a thing* — a definition, a command, the subtle distinction between two concepts. A faithful structural outline mirrors the chapter's own table of contents, so locating that thing later takes seconds. Pure prose summaries collapse the structure and force re-reading.

Why this style and not "extract every example"? Because cluttering the page with verbatim long passages defeats the point of *notes* — and risks copyright trouble on commercial books. Code blocks should be kept short; longer passages get *paraphrased* in your own words, with a page reference if helpful.

Read `references/note-style.md` for the full style guide, including:

- The exact section ordering for a chapter file (preface block → numbered sections → summary → references).
- How to render code, callouts, sidebars, and version notes.
- How to mark "open questions" and "things to revisit".
- A complete annotated example chapter you can model from.

Read it the first time you write a chapter in a session, then keep going.

## Working with companion notebooks

When the user asks you to enrich notes from companion Jupyter notebooks (bonus notebooks, exercise notebooks, supplementary code), two rules are **mandatory** — no exceptions:

### Rule 1 — Always download images locally

**Never** link images directly from external URLs (CDN, author's website, GitHub raw). Links rot, the site breaks offline, and the notes become incomplete without network access.

**Workflow:**

1. Grep each notebook for image references:
   ```bash
   grep -n "img src\|Image(\|imread\|https://.*\.png\|https://.*\.jpg" notebook.ipynb
   ```
2. For each image URL found, download it to `docs/books/<slug>/assets/<chNN>/<topic-slug>/`:
   ```powershell
   New-Item -ItemType Directory -Force "docs/books/<slug>/assets/ch02/my-topic"
   Invoke-WebRequest -Uri $url -OutFile "docs/books/<slug>/assets/ch02/my-topic/1.png"
   ```
3. Reference images in notes using relative paths and wrap each in a link to itself so the reader can click to enlarge:
   ```markdown
   [![Caption text](../assets/ch02/my-topic/1.png)](../assets/ch02/my-topic/1.png)
   ```
4. Write a descriptive alt/caption for each image — don't use generic names like "figure 1".

### Rule 2 — Always include the full runnable code example

Companion notebooks exist to make concepts concrete. Don't just describe what the notebook shows — include the actual runnable code. Every concept a notebook demonstrates must appear in the notes as a fenced code block with:

- All imports needed to run it standalone.
- Inline comments showing expected output where useful (e.g., `# tensor([[-0.34, -0.18, -0.30]])`).
- The key assertion or print that proves the claim (e.g., `print(torch.allclose(a, b))  # True`).

**What counts as "full":** the minimal self-contained snippet that proves the point, not a copy of the entire notebook. Strip scaffolding (progress bars, timing loops, plotting boilerplate) but keep every line that touches the concept being explained.

**Placement:** inside the relevant callout or as a fenced code block immediately after the prose that introduces the concept. Not at the bottom of the chapter.

## Working with the PDF

PDF extraction is what the **pdf** skill is for — read its SKILL.md if you need detail. The minimum you need here:

- For a chapter's contents, `pdftotext -layout` produces clean enough text for note-taking. You don't need OCR unless the PDF is scanned.
- Don't paste the raw text back to the user. Read it, internalize it, and produce the outline.

If the user uploaded the file, it lives under the conversation's uploads folder. If they're pointing at a file in the connected workspace, use that path directly.

### Chapter page map — extract once, reuse every session

When starting a new book project, build a chapter boundary table in one pass and save it to `docs/books/<slug>/page-map.md`. Every subsequent session reads that file instead of re-running `pdftotext` to find page ranges.

**Step 1 — find the PDF-to-print-page offset.** Printed page numbers almost always differ from PDF page numbers (front matter shifts everything). Scan the first ~30 pages to find a known landmark:

```bash
pdftotext -f 1 -l 30 -layout "<book>.pdf" -
```

If PDF page 34 shows "1" as the printed page number, the offset is +33 (PDF page = printed page + 33).

**Step 2 — enumerate chapter start pages.** Grep the full text for chapter headings:

```bash
pdftotext -layout "<book>.pdf" - | grep -n "^Chapter " | head -30
```

Confirm each hit with a targeted `pdftotext -f <page> -l <page>` to verify it's actually a chapter heading and not a running header or TOC entry.

**Step 3 — save to `page-map.md`.**

```markdown
# Page map — <Book Title>

PDF-to-print offset: +33  (PDF page 34 = printed page 1)

| Chapter | Title | PDF start | PDF end | Printed pages |
| --- | --- | --- | --- | --- |
| 1 | Introduction | 34 | 53 | 1–20 |
| 2 | Getting Started | 54 | 86 | 21–53 |
| … | … | … | … | … |
```

In subsequent sessions: read `page-map.md`, look up the chapter's PDF start/end, extract with `pdftotext -f <start> -l <end> -layout "<book>.pdf" -`.

### Chapter text cache — extract once, read many times

Once a chapter's text is extracted, save it so it never needs re-extracting in a future session.

**Before extracting,** check whether `docs/books/<slug>/pdf-cache/<NN>-<slug>.txt` already exists. If it does, read it directly — skip `pdftotext` entirely.

**If the cache file is missing,** extract and save in one step:

```bash
pdftotext -f <start> -l <end> -layout "<book>.pdf" \
  "docs/books/<slug>/pdf-cache/<NN>-<slug>.txt"
```

Then read from the saved file.

**Naming:** use the same `<NN>-<slug>` stem as the chapter `.md` file — `01-introduction.txt`, `05-advanced-statements.txt`. The pairing is then obvious at a glance.

> 💡 The cache contains raw book text. Consider adding `docs/books/*/pdf-cache/` to `.gitignore` if you don't want to commit extracted text to version control.

### Research cache — search once, reuse across sessions

The same principle applies to web searches: after verifying facts (version numbers, API behaviour, style guide guidance), save the results so future sessions skip the search entirely.

**Before web-searching**, check whether `docs/research-cache/<topic>.md` already has a recent answer. If the "Last verified" date looks current for the technology's release cadence, use it directly.

**After web-searching**, save findings to `docs/research-cache/<topic>.md`:

```markdown
# <Topic> — verified facts

Last verified: **YYYY-MM-DD** against <Technology> vX.Y.

| Claim | Verified value | Notes |
|---|---|---|
| `F.mode` added in | 3.4 | `deterministic` param added in 4.0 |
| ANSI mode on by default | Spark 4.0+ | |
```

**Naming:** short kebab-case topic name — `spark-api-versions.md`, `postgres-release-history.md`. One file per technology or tightly-related group of facts.

**Staleness:** the "Last verified" date tells future-you whether to trust the cache. A fact that hasn't changed across multiple major releases (e.g. "function X added in version Y") is durable; a fact about "the current stable release" expires whenever a new release ships — re-verify and update the date.

> 💡 `docs/research-cache/` is not wired into `zensical.toml` nav — it's a working file, not a published page. Consider adding it to `.gitignore` or committing it for convenience; either is fine.

## Version-aware notes (the key trick)

Books — especially technical books — go stale. The user is studying *now*; the book might cover PostgreSQL 16, Python 3.11, Kubernetes 1.28, while the current release is one or two majors newer. The point of these notes is to be useful *now and going forward*, so any version-specific content needs to be aligned with reality at note-taking time.

The behavior:

1. **Detect version-bound content.** As you read a chapter, watch for: explicit version numbers ("PostgreSQL 16"), release-date phrases ("released October 2023"), "what's new in vN" sections, install commands that pin a version (`postgresql-16`, `python3.11`), EOL/lifecycle claims, and version-comparison sidebars.

2. **Confirm what's current with a web search.** Use the `WebSearch` (or `web_fetch`) tool to look up the *current stable release* of the relevant technology. One search per technology is usually enough — search official sources first (`docs.python.org`, `postgresql.org`, project's own site) before secondary blogs.

3. **Adapt — don't rewrite the chapter.** Keep the chapter's structure and concepts (those rarely change). Update only the version-bound parts:
   - Replace the version number where the book uses "the current version".
   - Replace the "what's new in vN" section with a "what's new in v<latest>" section, sourced from the project's release notes.
   - Update install commands to the current major's package names / repo paths.
   - Update EOL math (release year + project's support window).
   - Update minor URLs that include version paths.

4. **Tell the reader what you did.** Add a note callout near the top of the chapter, e.g.:

   > 📌 **Notes adapted to <Tech> v<latest>.** The book covers v<book-version> (released <date>); v<latest> is the current production release as of <today>. Conceptual content is unchanged because the authors note that core concepts apply across versions.

   This is honest about the gap between the book and the notes, and gives a future-you reader a fighting chance of reconciling examples that don't quite match the book.

5. **Don't invent features.** If a search doesn't surface a clear answer for a specific feature, leave the book's content as-is and add a `> ❓ Revisit:` note. Hallucinating "what's new" content is worse than being honest about uncertainty.

The full decision rules and a worked example (PostgreSQL 16 → 18 adaptation) live in `references/version-handling.md`.

## Keeping the site in sync

A chapter note isn't done until the other site files are updated:

- **`zensical.toml`** — confirm the chapter is wired into `nav`. The file is TOML, not YAML — see `references/scaffold.md` for nested-nav syntax and `references/multi-book.md` for the multi-book nav structure.
- **Per-book reading log** (`docs/books/<slug>/index.md`) — flip the row from `⬜ todo` → `✅ done`, and fill in the "Topic page(s)" column with any topic pages this chapter informs.
- **`docs/reference/glossary.md`** — append any *new* terms the chapter introduced with source attribution. Don't rewrite existing entries unless they're now wrong. When two books define a term differently, keep both and attribute each.
- **`docs/reference/resources.md`** — append links the chapter cites that look useful long-term (project docs, repos, RFCs). Skip purely internal cross-references.
- **Topic pages and topic index** — for each topic the chapter informs, either extend an existing topic page, create a new one (≥2 books overlap), or add to the backlog in `docs/topics/index.md`. Add the bidirectional cross-link between chapter note and topic page. See `references/multi-book.md`.

These updates are small, but skipping them is the #1 way the site rots.

## Naming and slugs

- **Book slugs:** short, kebab-case, ideally one word — `ferrari`, `momjian`, `rogov`. Author surname unless ambiguous (e.g., two books by same author → `ferrari-2023`, `ferrari-2025`).
- **Chapter files:** `<NN>-<short-kebab-slug>.md` where `NN` is two-digit (`01`…`99`). Namespaced by book at the path level, so collisions across books are impossible.
- **Topic files:** short noun phrase, no number — `mvcc.md`, `replication.md`, `query-tuning.md`. Topic order is editorial.
- **Display titles in `nav`** get the full chapter or topic title, not the slug. The slug is for the filesystem; the title is for humans.

## Theme caveat (Zensical 0.0.x)

Zensical is pre-1.0 (0.0.x as of writing). Two practical consequences:

- **Don't set `[project.theme]` with `name = "modern"` or `"classic"`** unless the user has confirmed those themes are installed in their environment — the bundled-by-default themes referenced in newer docs aren't always present at install time. Leaving the `[project.theme]` block out makes Zensical use whatever it has built in, which is the safest default. See `references/scaffold.md` for the recommended config.
- **CLI flags can drift.** If a user reports "`zensical serve` doesn't accept `--dev-addr`," it's almost certainly a flag rename — guide them to `zensical serve --help` first.

Once Zensical hits 0.1+ this section can be revisited.

## Math support

Zensical ships with the `pymdownx.arithmatex` extension enabled by default. It processes `$...$` (inline) and `$$...$$` (display) delimiters in Markdown and outputs `<span class="arithmatex">\(...\)</span>` / `\[...\]` HTML. That's only half the pipeline — the browser still needs MathJax to render it.

To enable math rendering, two things must be in place:

1. **`docs/javascripts/mathjax.js`** — configures MathJax before the CDN script loads. The template is in `references/scaffold.md`.
2. **`extra_javascript` in `zensical.toml`** — loads both the local config file and the MathJax CDN script. The template is in `references/scaffold.md`.

If the chapter has no equations, omit both. If you add them but the Docker container is already running, restart it (`docker compose restart`) so the new JS file is picked up.

**Syntax to use in notes:**

- Inline: `$\omega_{ij} = x^{(i)} \cdot x^{(j)}$`
- Display: `$$\alpha_{ij} = \frac{\exp(\omega_{ij})}{\sum_k \exp(\omega_{ik})}$$`

`arithmatex` converts these to MathJax-compatible delimiters (`\(...\)` / `\[...\]`), so the `$` form is the right form to write in Markdown — don't write `\(...\)` by hand.

## A complete worked example

The user uploads a 745-page PDF of a Linux kernel internals book and says *"help me take notes on this, let's start with chapter 1."*

A good run looks like:

1. Confirm the notes destination folder and the book slug (one quick question if not obvious — don't ask four).
2. Inspect the folder. If empty, scaffold a **multi-book project** (`zensical.toml`, `docs/index.md` as hub, `docs/books/<slug>/`, `docs/topics/index.md`, `docs/reference/`). Templates in `references/scaffold.md`.
3. **Build the chapter page map** — extract chapter boundaries in one pass and save to `docs/books/<slug>/page-map.md` (see "Chapter page map" above). One-time cost; every future session reads this file directly.
4. Create placeholder files for chapters 2..N under `docs/books/<slug>/chapters/` so the navigation works from day one.
5. **Check the chapter text cache** — look for `docs/books/<slug>/pdf-cache/01-<slug>.txt`. If absent, extract and save: `pdftotext -f <start> -l <end> -layout "<book>.pdf" docs/books/<slug>/pdf-cache/01-<slug>.txt`. Then read from the file.
6. Detect version-bound content. **Check `docs/research-cache/` first** — if a relevant cache file exists and is current, use it. Otherwise web-search and save the results to a new cache file before continuing.
7. Write the chapter outline to `docs/books/<slug>/chapters/01-<slug>.md` using the style in `references/note-style.md`. Insert the version-adaptation callout if any updates were made.
8. Do the topic-page pass: identify which topics chapter 1 touches and add them to the `docs/topics/index.md` backlog (don't write topic pages yet — wait for a second book to overlap).
9. Update `zensical.toml` nav (if needed), `docs/books/<slug>/index.md` reading log (flip ✅), `docs/reference/glossary.md` (new terms with source), `docs/reference/resources.md` (links).
10. Tell the user how to run the site (`docker compose up` or `zensical serve` — README explains both) and ask whether to continue with chapter 2 next.

## Answering questions accurately

When the user asks a factual question — about Spark internals, API behaviour, version history, design rationale, or anything else — follow this sequence before answering:

1. **Web search first.** Always run at least one `WebSearch` before answering any factual question. Training data is a snapshot; it drifts, hallucinates, and misses post-cutoff releases. A search takes seconds and prevents confidently wrong answers.

2. **Verify URLs before citing them.** Never include a URL in a response or in the notes unless you have confirmed it resolves. Use `WebFetch` on any URL you intend to cite, or confirm it appeared live in a search result. A broken source is worse than no source — it erodes trust and wastes the reader's time.

3. **Trace claims to sources.** Every claim that goes into the notes should be traceable to a specific source (official docs, release notes, a verified article). If you can't find a source, say so explicitly and mark the content with `> ❓ Unverified:` rather than asserting it as fact.

4. **Distinguish confidence levels explicitly:**
   - Verified from a source retrieved this session → state the source.
   - Recalled from training but not verified this session → say so: *"From training data, not verified this session — treat with caution."*
   - Uncertain → add `> ❓ Revisit:` in the notes and do not present it as settled.

5. **Include sources in answers.** When answering a question in chat, list the URLs you consulted at the end of your response so the user can check them.

**Common hallucination traps in this domain:**
- Version numbers for when a feature was added/changed.
- Whether a URL or documentation page exists.
- Specific method signatures, config key names, or default values.
- Claims about what a third-party tool (Velox, Photon, Gluten) does or which product ships it.

## Anti-patterns to avoid

- **Don't scaffold a single-book layout for a new project.** Always start with multi-book — the extra folders cost nothing and avoid a painful migration later.
- **Don't re-run pdftotext if the cache exists.** Check `docs/books/<slug>/pdf-cache/<NN>-<slug>.txt` before extracting. A cache hit skips the extraction entirely and keeps the context window smaller.
- **Don't re-run web searches if results are cached.** Check `docs/research-cache/` before searching. If a cache file exists and its "Last verified" date is current, use it directly and skip the search.
- **Don't dump raw extracted text.** It's not notes; it's a copy. Re-state ideas in your own words.
- **Don't write a flat summary** of long chapters — keep the structure visible.
- **Don't rewrite chapters from scratch** when the book is just slightly out of date. Adapt the version-bound bits, leave concepts alone.
- **Don't quietly skip the reading-log update.** Future-you will lose track of what's done.
- **Don't pin versions unless asked.** A user studying technology generally wants notes against *current*, not whatever happened to be latest the day they ran the skill — but that's a soft preference. If they ask for "as of when the book was written," respect it.
- **Don't pretend to know latest versions from training.** Always web-search when version-currency matters.
- **Don't write topic pages with only one source.** Keep them in the backlog until a second book provides the comparison point — otherwise the topic page is just a chapter summary in disguise.
- **Don't forget the cross-links.** Topic pages without back-links to source chapters are orphaned; chapter notes without forward-links to topic pages are siloed. Bidirectional links are what make the hybrid useful.

## Reference files

Read these on demand. Each one stands alone.

- `references/note-style.md` — full style guide for chapter outlines, with an annotated example. Read once per session at minimum.
- `references/scaffold.md` — drop-in templates for the multi-book project (`zensical.toml`, `docs/index.md` hub, per-book reading log, topics index, glossary, resources, README, Dockerfile/compose). Also includes the lightweight single-book templates for reference. Read when bootstrapping a fresh project.
- `references/version-handling.md` — decision rules for adapting a book's version-specific content to current reality, with a worked PostgreSQL 16 → 18 example. Read when the chapter mentions any version, release, or install command.
- `references/multi-book.md` — the hybrid per-book + topic-page layout: full workflow, topic-page template, cross-linking convention, glossary handling across books, and migration steps from single-book. Read at the start of every multi-book session.
