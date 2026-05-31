# Multi-book mode — hybrid layout for studying a topic across multiple books

Use this layout when the user is studying **the same topic from multiple books** and wants both:

- **Per-book chapter notes** — the source of truth, faithful to each book's narrative.
- **Topic pages** — synthesized cross-book views that compare, reconcile, and distill.

This is the layout serious self-study tends to evolve toward. Per-book notes preserve each author's voice and let you re-find a fact in its original context; topic pages let you actually *think* across the books.

## When to switch into multi-book mode

Detect the mode from the project layout. The signal is the presence of `docs/books/` (with at least one sub-folder). If you see it, the project is already in hybrid mode — don't try to scaffold a single-book project on top of it.

The other trigger is when the user explicitly asks to add a second (or third, …) book to an existing single-book site. That's the moment to **migrate** the site from single-book to hybrid (see "Migration" below).

## The hybrid layout

```
docs/
├── index.md                       # landing — surfaces both topics and books
├── topics/
│   ├── index.md                   # topic index + "topics to write" backlog
│   ├── architecture.md            # ← Ferrari Ch 1 + Momjian Ch 1 + Rogov Ch 1
│   ├── mvcc.md                    # ← Ferrari Ch 11 + Rogov Ch 4
│   └── replication.md
├── books/
│   ├── ferrari/
│   │   ├── index.md               # per-book reading log
│   │   └── chapters/
│   │       ├── 01-introduction.md
│   │       └── 11-mvcc.md
│   ├── momjian/
│   │   ├── index.md
│   │   └── chapters/01-…md
│   └── rogov/
│       ├── index.md
│       └── chapters/04-mvcc.md
└── reference/
    ├── glossary.md                # merged across books, with attribution
    └── resources.md
```

Notes on the structure:

- **`docs/topics/` is listed first in the navigation**, even though `docs/books/` was populated first chronologically. Topics are the *thinking layer* — that's where the user goes to learn, so it deserves the prime nav slot.
- **Each book gets its own folder under `docs/books/`** named with a short slug — author surname or a clear nickname (`ferrari`, `momjian`, `rogov`). Avoid full titles in the path; keep slugs readable.
- **Each book has its own `index.md`** acting as that book's reading log — the single-book reading-log table moves *into* the per-book folder rather than living at the top level.
- **`docs/index.md` becomes a hub**, surfacing both navigations: a "Topics" section linking to the synthesized pages, and a "Books" section linking to each book's reading log.

## Naming and slugs

- Book slug: short, kebab-case, ideally one word — `ferrari`, `momjian`, `rogov`. Use the author's surname unless that's ambiguous (e.g., two books by Ferrari → `ferrari-2023`, `ferrari-2025`).
- Chapter file: same as single-book mode — `<NN>-<short-slug>.md` — but now namespaced by book at the path level, so collisions across books are impossible.
- Topic file: `<short-noun-phrase>.md` — `mvcc.md`, `replication.md`, `query-tuning.md`. Don't number topics; their order is editorial and may change as more books get added.

## Navigation

```toml
nav = [
    { "Home" = "index.md" },
    { "Topics" = [
        { "Architecture"        = "topics/architecture.md" },
        { "MVCC & concurrency"  = "topics/mvcc.md" },
        { "Replication"         = "topics/replication.md" },
        { "Topic index"         = "topics/index.md" },
    ]},
    { "Books" = [
        { "Ferrari & Pirozzi (2023)" = [
            { "Reading log"         = "books/ferrari/index.md" },
            { "1. Introduction"     = "books/ferrari/chapters/01-introduction-to-postgresql.md" },
            { "11. MVCC, WAL, …"    = "books/ferrari/chapters/11-mvcc.md" },
        ]},
        { "Momjian — PostgreSQL (Ed. 3)" = [
            { "Reading log"         = "books/momjian/index.md" },
            { "1. …"                = "books/momjian/chapters/01-…md" },
        ]},
        { "Rogov — PostgreSQL Internals" = [
            { "Reading log"         = "books/rogov/index.md" },
            { "4. MVCC"             = "books/rogov/chapters/04-mvcc.md" },
        ]},
    ]},
    { "Reference" = [
        { "Glossary"  = "reference/glossary.md" },
        { "Resources" = "reference/resources.md" },
    ]},
]
```

The "Books" section nests one level deeper than single-book mode — each book is its own collapsible group containing its reading log + chapters. This keeps the nav tree manageable as the number of books grows.

## The workflow

The chapter-note-first rhythm from single-book mode is unchanged. What's new is a *second pass* per chapter that decides whether the chapter informs a topic page.

For each chapter the user studies:

1. **Read and write the per-book chapter notes** under `books/<book>/chapters/<NN>-<slug>.md`. This is exactly the existing detailed-outline workflow — see `note-style.md`. The chapter is the source of truth; topic pages refer back to it.

2. **Identify which topics this chapter touches.** Most chapters touch one primary topic; some touch several. Be honest — if a chapter is genuinely a grab-bag, list each topic separately rather than forcing a single label.

3. **For each touched topic, decide what to do:**

    - **Topic page already exists** → add this book's perspective as a new section to the topic page. Don't rewrite existing sections; *augment*.
    - **Topic page doesn't exist, but only one book has covered it so far** → don't create the topic page yet. Instead, add it to the "Topics to write" backlog at the bottom of `topics/index.md`, with the source citation. *Why defer:* a topic page with one source isn't a topic page, it's a chapter summary.
    - **Topic page doesn't exist, and now ≥2 books overlap on this topic** → create the topic page now. The trigger is "I just wrote a chapter that meaningfully overlaps with one I wrote earlier from a different book."

4. **Cross-link.** Add a forward-link from the chapter note to the topic page(s) it informs; add a back-link from the topic page to each source chapter. See "Cross-linking" below for the exact convention.

5. **Update the per-book reading log** (`books/<book>/index.md`) and, if you created or extended a topic page, the topic index (`topics/index.md`).

6. **Update glossary and resources** as in single-book mode, with the per-book attribution shown below.

## Topic page template

Use this exact structure for new topic pages. The headers serve a purpose — readers skim topic pages in a different mode than chapter notes (they're hunting for a perspective, not a definition), so the structure should foreground perspective and contrast.

```markdown
# <Topic name>

> **Sources:** <Author1 ChN> · <Author2 ChM> · <Author3 ChK>

## In one paragraph
<Your own one-paragraph framing of the topic — what is it, why does it matter,
where does it sit in the larger system. Plain prose. No quotes. No bullets.>

## Key concepts (cross-book)
- **<Concept>** — <Author1> calls this <X> (Ch N §m); <Author2> calls it <Y>
  (Ch M §p). Same idea, different vocabulary. <One-sentence resolution.>
- **<Concept>** — only <Author> covers this. <Brief gloss.>

## Where the books differ
- <Author1> emphasizes <perspective A> — focused on <use case>.
- <Author2> emphasizes <perspective B> — focused on <other use case>.
- Disagreement worth flagging: <…> (if any).

## When to read which (book → use case)
- Working a real production cluster? → <Author>, ch <N>.
- Want the implementation deep dive? → <Author>, ch <M>.
- Need a clean conceptual model? → <Author>, ch <K>.

## Sources

- [<Author1> Ch <N> — <chapter title>](../books/<slug>/chapters/<NN>-…md)
- [<Author2> Ch <M> — <chapter title>](../books/<slug>/chapters/<NN>-…md)
- [<Author3> Ch <K> — <chapter title>](../books/<slug>/chapters/<NN>-…md)

## Open questions
> ❓ <Things you'd want to chase down later, especially across books.>
```

A topic page is **shorter** than the sum of its source chapters — it's the *distilled* view, not the union. If you find yourself copying chapter content into a topic page, you've blurred the layers. The chapter note is the truth; the topic page is the perspective.

## Cross-linking convention

Every chapter note that informs a topic page gets a forward-link, immediately after the framing block at the top:

```markdown
> 🔗 **See also:** [Topic — MVCC & concurrency](../../topics/mvcc.md), which
> synthesizes this chapter with Rogov Ch 4 and Momjian Ch 5.
```

Every topic page lists its source chapters in the `## Sources` section (template above). Use *relative* links so the site survives directory restructuring (`../books/<slug>/chapters/<NN>-…md`).

This bidirectional linking is what makes the hybrid layout actually useful — a reader on a topic page can dive into any source's full treatment in one click, and a reader inside a chapter can pop up to the cross-book synthesis.

## Glossary in multi-book mode

The glossary becomes a single page with terms attributed to source(s). When two books define the same term differently, **keep both definitions** and attribute each — different definitions usually reflect different lenses on the same idea, and capturing both is more useful than picking a winner.

```markdown
## M

| Term | Definition | Source |
| --- | --- | --- |
| **MVCC** | Multi-version concurrency control — a strategy for letting readers and writers operate without blocking by giving each transaction a consistent snapshot. | Ferrari Ch 11 |
| **MVCC** | An implementation technique using `xmin`/`xmax` row headers to track tuple visibility per transaction. | Rogov Ch 4 |
```

Group entries by initial letter (`## A`, `## B`, …) once the glossary grows past ~30 entries — easier to scan than one giant alphabetized table.

## Per-book reading log (`books/<book>/index.md`)

Each book has its own reading log, *not* a shared one. This way each book reads as a self-contained unit and the user can see at a glance how far through any book they are.

```markdown
# <Book Title> — reading log

> <Authors> (<Year>). *<Title with subtitle>* (<edition>). <Publisher>. ISBN <…>.

| Status | Chapter | Topic page(s) |
| ------ | ------- | ------------- |
| ✅ done | 1. Introduction | [Architecture](../../topics/architecture.md) |
| ✅ done | 11. MVCC, WAL, … | [MVCC](../../topics/mvcc.md) |
| ⬜ todo | 12. Extensions | — |
```

The "Topic page(s)" column is the per-book index of which topic pages each chapter ended up informing. It earns its keep when you're three books in and trying to reconstruct *"which chapter of which book did I cover X in?"*

## Site landing page (`docs/index.md`)

In multi-book mode, the home page acts as a hub:

```markdown
# <Site title> — Reading Notes

A growing personal study site for **<topic / domain>**, drawing on multiple books.

## Topics
- [Architecture](topics/architecture.md)
- [MVCC & concurrency](topics/mvcc.md)
- [Replication](topics/replication.md)
- [Full topic index](topics/index.md)

## Books
- [Ferrari & Pirozzi — *Learn PostgreSQL* (2023)](books/ferrari/index.md)
- [Momjian — *PostgreSQL: Up and Running*](books/momjian/index.md)
- [Rogov — *PostgreSQL Internals*](books/rogov/index.md)

## Reference
- [Glossary](reference/glossary.md)
- [Resources](reference/resources.md)
```

## Topic index (`docs/topics/index.md`)

```markdown
# Topics

Cross-book synthesis — each page distills how multiple books treat the same topic.

## Active topic pages

- [Architecture](architecture.md) — Ferrari Ch 1, Momjian Ch 1, Rogov Ch 1
- [MVCC & concurrency](mvcc.md) — Ferrari Ch 11, Rogov Ch 4
- [Replication](replication.md) — Ferrari Ch 17–18, Momjian Ch 7

## Topics to write (≥2 source chapters available)

_(empty — all eligible topics have pages)_

## Single-source backlog (waiting for a second book)

- **Foreign data wrappers** — Ferrari Ch 12 only.
- **WAL archiving** — Ferrari Ch 15 only.
- **Logical decoding internals** — Rogov Ch 6 only.
```

The "single-source backlog" is the most useful section — it's an explicit reminder that *these chapters need a second source before they earn a topic page*. When you study a new book that touches one of them, you have a built-in nudge to write the topic page.

## Migration: single-book → multi-book

If the user already has a single-book site (the layout in `scaffold.md`) and asks to add a second book, migrate before adding:

1. **Move existing chapters** from `docs/chapters/<NN>-…md` to `docs/books/<existing-book-slug>/chapters/<NN>-…md`.
2. **Create the per-book reading log** at `docs/books/<existing-book-slug>/index.md`. The reading-log table moves there from `docs/index.md`.
3. **Create empty `docs/topics/index.md`** with the structure shown above. Move "topics to write" any chapter slots that obviously deserve cross-book treatment.
4. **Convert `docs/index.md`** to the multi-book hub format above.
5. **Restructure `nav`** in `zensical.toml` to the multi-book shape (Topics / Books / Reference).
6. **Update glossary entries** to add a `Source` column attributing each entry to the existing book.
7. **Verify locally** — `zensical serve` should build cleanly. Fix any broken links.
8. **Then** scaffold the new book — create `docs/books/<new-book-slug>/` with its own `index.md` and a placeholder per chapter.

The migration is mechanical but worth doing carefully. Test the site after migration *before* starting on the new book; debugging two changes at once is harder than debugging one.

## Anti-patterns

- **Writing topic pages with a single source.** That's a chapter summary in disguise — keep it as a chapter note until a second book provides a comparison point.
- **Topic pages that copy chapter content.** Distill, don't duplicate. If a topic page is as long as the chapter it draws from, the layers have collapsed.
- **Forgetting the cross-links.** Topic pages without back-links to source chapters are orphaned; chapter notes without forward-links to topic pages are siloed. The bidirectional links are what makes the hybrid useful.
- **Letting the topic backlog go stale.** Every new chapter should pass through the "does this match a backlog topic?" check. Otherwise the backlog becomes wishful thinking.
- **Naming books after their full title.** Long folder paths break links visually and waste navigation real estate. Author surname is almost always the right slug.
