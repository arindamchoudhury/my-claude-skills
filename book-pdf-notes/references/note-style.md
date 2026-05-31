# Detailed-outline note style

This is the canonical style for chapter notes in a Zensical study site.

## Why this style

The user comes back to study notes for two reasons: to **find** something specific (a definition, a command, a distinction) or to **review** the shape of an idea before re-reading the original. A faithful structural outline serves both: it mirrors the source's own table of contents (so finding things is fast) and it surfaces the *why* and the *relationships* (so reviewing is efficient).

This isn't a verbatim transcript and it isn't a paragraph summary either. Think of it as how a strong student would re-explain the chapter to themselves a week later — keeping the structure, dropping the filler, restating in their own words.

## Section ordering

Use this exact order at the top level of every chapter file. The header levels matter — Zensical uses them to build per-page navigation.

```markdown
# Chapter <N> — <Chapter Title>

> *Source: <Author(s)> (<Year>), Chapter <N>, pages <X>–<Y>.*
>
> 1–2 sentence framing of what the chapter is about and why it's in the book.
>
> 📌 (optional) **Notes adapted to <Tech> v<latest>.** … see version-handling.md

---

## 1. <First section title from the chapter>
…

## 2. <Second section title>
…

…

## N. Summary (chapter takeaways)
- 3–6 bullet recap of the chapter's load-bearing points.

---

## N+1. References
- Bullet list of links the chapter cites that are worth keeping.
```

Top-level numbering (`## 1.` etc.) is intentional — the chapter often has its own numbering, but mirroring it explicitly in the notes makes referencing back to the source easy. If the chapter doesn't number its sections, you can still number yours; the goal is *navigability*, not literal mirroring.

## Section content

Inside each section, the rhythm is:

- **Concept** — a short declarative bullet or sub-heading (`### …`).
- **Explanation** — 1–3 short sentences in your own words, in prose-y bullets or a paragraph.
- **Specifics** — commands, syntax, exact terms; render in code blocks if textual, in a small table if comparative.
- **Pointer** — a `> ❓ Revisit:` note when something is unclear or worth experimenting with later.

Avoid marathon bullets. If a thought is more than ~2 sentences, break it into sub-bullets or a short paragraph. Avoid bullet-of-bullets-of-bullets nesting deeper than three levels — at that point you're hiding structure rather than revealing it.

**CommonMark list formatting rule:** A bullet list that immediately follows a paragraph with no blank line between them will be rendered as continuation text (one long line) by CommonMark-based renderers including Zensical/MkDocs. Always put a blank line before a bullet list:

```markdown
`pos` is useful when:
- order matters     ← WRONG — collapses to inline text

`pos` is useful when:

- order matters     ← correct
```

This applies everywhere: after plain paragraphs, after bold lead-ins (`**X is useful when:**`), after code blocks. When in doubt, add the blank line.

**Diagnosing this problem from user reports:** When a user pastes text that looks like a collapsed run-on — bullets smashed onto one line with no line breaks — it is almost always this missing-blank-line issue rendered by the browser. The pasted text looks like:

```
pos is useful when: - Order matters — e.g. the first skill is the primary one,
the rest are secondary - Re-joining back — you need to re-assemble or compare
elements by their original position - Debugging — confirming array contents
line up with expectations
```

**Fix:** grep the file for the lead-in phrase (`pos is useful when`), read a few lines around it, confirm there is no blank line between the lead-in and the first `-` bullet, then add the blank line. No other change needed.

**CommonMark nested list indentation rule:** Sub-bullets must be indented by **4 spaces** (not 2) to render as a nested list in Zensical/MkDocs. With 2-space indent, CommonMark treats the sub-items as top-level bullets:

```markdown
- Parent item:
  - WRONG — renders as a separate top-level bullet

- Parent item:
    - correct — renders as nested sub-bullet
```

This applies any time a bullet has child bullets. When in doubt, use 4 spaces.

## Code, callouts, sidebars

**Commands and SQL** — render as fenced code blocks with the language tag. Keep them short and self-contained. If the book shows a 30-line example, capture only the lines that demonstrate the concept being taught and add a brief note pointing at the book's full example by page number.

````markdown
```bash
$ initdb -D /postgres/18/data
```
````

**Inline syntax** — backticks: `pg_ctl start`, `SELECT … RETURNING`.

**Tables** — for vocabulary, comparisons, defaults, version-by-version differences. Tables are excellent at the chapter's structural inflection points (e.g., "what's the difference between a backend process and a postmaster?").

**Sidebars / callouts** — render as Markdown blockquotes with a leading emoji-tag for skimming:

- `> 💡 **Tip** — ...`
- `> ⚠️ **Pitfall** — ...`
- `> 📌 **Version note** — ...`
- `> ❓ Revisit: ...` for open questions you want to chase later.

These are deliberately lightweight — Zensical doesn't require a special syntax for admonitions and most readers prefer the plain blockquote.

## Tone

Write in your voice, in your language. The notes are for *you*, six months from now. That means:

- Prefer "the postmaster forks a backend per connection" over "PostgreSQL utilizes a multi-process architecture wherein the postmaster process spawns dedicated backend processes for each incoming client connection."
- It's fine to add your own observations and aha-moments; mark them clearly so they don't get confused with the source: `> 💭 (mine):` or just inline italics.
- Don't mimic the book's marketing language ("rock-solid", "world-class") unless that's a quote that you're keeping for color.

## Copyright & quoting

- Long verbatim passages from a copyrighted book are out — both for legal reasons and because they defeat the purpose of *notes*. Re-state in your own words.
- Short quotations (a sentence or two) for color or attribution are fine; mark them with quotation marks or as a blockquote.
- Code samples shown in a book that demonstrate standard public APIs (e.g., `SELECT * FROM users`) are not copyrightable per se, so feel free to capture short ones; for longer original samples, paraphrase or point at the book's GitHub repo.

## What to leave out

- Filler ("In this chapter we will discuss…") — gone.
- Long historical narratives — compress to a 4-line timeline if relevant, drop otherwise.
- The book's own forward-references ("we'll see in Chapter 7") — usually safe to drop.
- Marketing tangents about the publisher, the authors' bios, etc. — not part of the chapter.

## Annotated example

Here's a real example you can model from. The chapter is "Introduction to PostgreSQL" (Ferrari & Pirozzi, *Learn PostgreSQL 2nd Ed.*, Packt, 2023).

````markdown
# Chapter 1 — Introduction to PostgreSQL

> *Source: Ferrari & Pirozzi (2023), Chapter 1, pages 1–20.*
>
> A scene-setting chapter: what PostgreSQL is, the project's history and release cadence, the vocabulary used throughout the rest of the book, and several ways to install PostgreSQL.
>
> 📌 **Notes adapted to PostgreSQL 18.** The book targets PostgreSQL 16; PostgreSQL 18 was released 25 September 2025 and is the current production version. Conceptual content is unchanged because the authors note that core concepts apply across versions.

---

## 1. PostgreSQL at a glance

### What it is

- An **open-source relational database** developed by the *PostgreSQL Global Development Group (PGDG)* — there is no single owning company, so the project cannot "go out of business."
- BSD-style license — embeddable in open- or closed-source projects.
- Considered an **enterprise-grade DBMS**: stability, scalability, safety; **fully ACID-compliant**.

### Capacity ("scary numbers")

A single instance can hold:

- > 4 billion databases, each with unlimited size.
- > 1 billion tables per database, each up to 32 TB.
- 1,600 columns per table, each up to 1 GB.

The point: capacity is rarely the bottleneck — *organization and tuning* are.

### What ACID means

| Property | Meaning |
| --- | --- |
| Atomicity | A multi-step op runs as one. |
| Consistency | Data is never left half-written. |
| Isolation | Concurrent ops don't corrupt each other. |
| Durability | Committed data survives crashes. |

> ❓ Revisit: which extensions are most worth installing on a fresh dev cluster?

---

## 5. Summary

- Mature, ACID-compliant, BSD-licensed, run by the PGDG.
- Vocabulary that matters: cluster, postmaster, database, schema, role, PGDATA, WAL, catalog.
- A cluster lives entirely in one PGDATA directory; the postmaster forks a backend per connection.

---

## 6. References

- Release notes: <https://www.postgresql.org/docs/release/18.0/>
- Book code: <https://github.com/PacktPublishing/Learn-PostgreSQL-Second-Edition>
````

Notice:

- Source citation in italics at the very top so attribution is unmissable.
- The version-adaptation callout sits right after the framing sentence, where the reader will see it before any technical content.
- Sections numbered to mirror the chapter's own structure.
- Short prose-y bullets, not flat summaries.
- A small comparison table for ACID instead of a paragraph.
- A `> ❓ Revisit:` to capture a thought without breaking the flow.
- The summary is genuinely short — the user will skim it; bury detail in the body.
