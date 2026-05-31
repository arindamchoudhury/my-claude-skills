# Version handling — keeping notes current

Books on fast-moving technology age. The user is studying *now* and will revisit the notes later, so version-bound content should reflect *current* reality, not the snapshot the book froze into print. This document explains how to do that without rewriting the chapter.

## When to engage this rule

Engage when the chapter mentions **any of these**:

- An explicit version number ("PostgreSQL 16", "Python 3.11", "React 18", "Kubernetes 1.28").
- A "What's new in version N" section.
- An install command that pins a version (`postgresql-16`, `apt install python3.11`, `npm install react@18`).
- A release date or "released [year]".
- An EOL/lifecycle claim ("v16 reaches EOL in 2028").
- A "current as of [date]" claim.
- A URL with a version segment in the path (e.g., `/docs/16/`).

Don't engage for:

- Foundational concepts that are version-agnostic (ACID, CAP, REST principles, big-O, the difference between TCP and UDP).
- Historical facts the book describes (the project's origin year, the original creator's name, the language it was first written in).
- Terminology that hasn't changed (a "primary key" is still a primary key in any version of any RDBMS).

## The three-step workflow

### 1. Detect

While reading the chapter, mentally tag every version-bound sentence. Don't fix anything yet — first you need to know what the book is anchored to (e.g., "the book targets vN").

### 2. Look up

Use `WebSearch` (or `web_fetch`) to find the **current stable release**.

- Search the **official source first**. For a language: `python.org`, `nodejs.org`. For a database: `postgresql.org`, `mongodb.com`. For a framework: the project's own docs site.
- Use a query like `<technology> latest stable release <current-year>` or `<technology> release notes <current-year>`. The current year is in the env block in your system context.
- Read the *release notes* for the major version, not just a press release — release notes have the level of detail a study note needs.
- One search per technology in the chapter is usually enough. Don't go down a rabbit hole.

If the search is inconclusive, **stop**. Don't guess. Mark the gap with `> ❓ Revisit:` and move on.

### 3. Adapt — surgically

The goal is to keep the chapter recognizable while making the version-bound bits accurate.

**Do replace:**

- The "current version" the chapter discusses → current stable.
- "What's new in vN" → "What's new in v<latest>", *re-sourced from official release notes*. Don't auto-translate the book's bullets to the new version — the new version's "what's new" is a different list.
- Install commands — package names, repo paths, distro suffixes (`postgresql18-server` vs `postgresql16-server`).
- EOL math — release year + project's official support window.
- URLs that include version paths.

**Don't replace:**

- The chapter's *concepts* and *terminology* — those usually carry forward unchanged.
- The chapter's *examples and exercises* — even if a syntax has been refined, the book's example is what the user will look up. Note the deprecation in a callout instead of silently swapping it.
- Historical narrative ("released October 2023") — that's a fact about the book's chosen version, not about today.

**Do add a callout** at the top of the chapter to flag the adaptation:

```markdown
> 📌 **Notes adapted to <Tech> v<latest>.** The book targets v<book-version> (released <date>); v<latest> is the current production release as of <today>. Conceptual content is unchanged because the authors note that core concepts apply across versions.
```

This is non-negotiable when you've made any version updates — it's the difference between *honest, current notes* and *invisible drift the user discovers months later when an example doesn't work*.

## Worked example

The book is *Learn PostgreSQL 2nd Ed.* by Ferrari & Pirozzi (Packt, 2023), which covers PostgreSQL 16. The user is studying in 2026, so PostgreSQL 18 (released 25 September 2025) is current.

### What changed in the notes

| Book (PG16) | Notes (PG18) |
| --- | --- |
| "PostgreSQL 16 is the latest production release" | "PostgreSQL 18 is the latest production release as of <today>" |
| "What's new in PostgreSQL 16: revised permissions, JSON functions, …" | New section: "What's new in PostgreSQL 18: async I/O subsystem, B-tree skip scan, virtual generated columns by default, `uuidv7()`, OAuth auth, temporal constraints, …" — sourced from PG18 release notes |
| `apt install postgresql-16` | `apt install postgresql-18` (using the modern PGDG `apt.postgresql.org.sh` setup script) |
| `/usr/pgsql-16/bin/postgresql-16-setup initdb` | `/usr/pgsql-18/bin/postgresql-18-setup initdb` |
| `wget https://ftp.postgresql.org/pub/source/v16.0/postgresql-16.0.tar.bz2` | `wget https://ftp.postgresql.org/pub/source/v18.0/postgresql-18.0.tar.bz2` |
| "EOL in 2028" (book wrote 2023 + 5 years) | "EOL in 2030" (release 2025 + 5-year window) |
| `[Service] Environment=PGDATA=/postgres/16/data` | `[Service] Environment=PGDATA=/postgres/18/data` |

### What stayed the same

- The "PostgreSQL at a glance" framing — still accurate, paragraphs unchanged.
- The capacity numbers (1,600 columns, 32 TB tables, etc.) — those haven't moved.
- The history section (Ingres → POSTGRES → Postgres95 → PostgreSQL) — historical facts.
- The terminology section (cluster, postmaster, schema, role, PGDATA, WAL) — vocabulary is stable.
- The `pgenv` workflow — still the same tool, same Bash script.

### What got an honest "I don't know"

A book example demonstrating syntax that *might* be subtly different in v18 but where the official release notes don't clearly confirm: leave the book's example in place, add `> ❓ Revisit: confirm this still works on v18 — book uses the v16 spelling.`

## Anti-patterns

- **Rewriting the chapter to be "v18-native."** The user is studying the book; aligning notes too aggressively with the new version makes the book hard to follow. Keep the chapter recognizable.
- **Hallucinating a "What's new" list.** If a search doesn't surface a clear "what's new in vN" doc, don't invent one. Cite official release notes or skip.
- **Updating versions silently.** If the user can't see what was adapted, they can't trust the notes when an example doesn't behave as the book describes. The 📌 callout is mandatory whenever any update was made.
- **Updating non-version-bound content "while you're at it."** That's how scope creep ruins a chapter. Stay focused on version-bound spans only.

## When the user asks "do this against the book's version, not latest"

Some users are studying for a specific exam or working on a system that's pinned to a particular version. Respect the request — skip the version search entirely and write the notes faithfully to the book. You can still flag where v<latest> behaves differently in a `> 📌` callout if you happen to know it, but don't *adapt* the content.

The default, absent a request, is "current at note-taking time."
