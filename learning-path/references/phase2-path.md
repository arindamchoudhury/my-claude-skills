# Phase 2 — Learning Path

Write `C:\opt\learn\<topic-slug>\notes\docs\learning-path.md`.

## Ordering principles

1. **Concept dependency first** — a topic that requires prior knowledge comes after what it depends on, regardless of how popular or well-reviewed the resource is
2. **Official resources early** — official docs, official academy, or official tutorials belong in Stage 1 or Stage 2
3. **Hands-on before deep theory** — get the user running code first, then explain internals
4. **Mark version currency** — if a resource targets a version more than one major release behind current stable, flag it with 📌

## Resource classification

- **Essential** — covers foundational concepts with no good substitute; must do
- **Recommended** — adds important depth or a different angle; do if time allows
- **Optional** — specialised, niche, or can be referenced rather than studied fully

## Time estimates

Be realistic. Include: watching/reading time + hands-on lab time + re-doing examples.
- Short video module: 0.5–1 hr
- Full Udemy/Coursera course: 8–20 hrs
- Technical book: 15–40 hrs
- Official docs walkthrough: 2–6 hrs

## File format

```markdown
# Learning Path: <Topic>

> **Last updated:** YYYY-MM-DD
> **Current stable version:** <version>

## Prerequisites

What you should already know before starting this path:
- ...

---

## The Path

### Stage 1: Foundations (~X hours total)

#### <Resource Name>
- **Type:** Official course / Book / Video course / Docs
- **URL:** <url>
- **Priority:** Essential
- **Time:** ~X hours
- **Focus:** What to pay close attention to
- **Skip:** Sections that are optional, dated, or covered better elsewhere
- **Version note:** *(only if targeting older version)* 📌 Covers v<X>; current is v<Y>

---

### Stage 2: Core Concepts (~X hours total)

#### <Resource Name>
...

---

### Stage N: Production & Advanced (~X hours total)

...

---

## Quick Reference

| Resource | Type | Priority | Hours | Version |
|---|---|---|---|---|
| [Name](url) | Book | Essential | ~20 hrs | v1.x |
| [Name](url) | Course | Recommended | ~12 hrs | v2.x |

---

## What to build as you learn

Mini-projects to attempt at each stage (use these as chapter capstone exercises):

- **After Stage 1:** ...
- **After Stage 2:** ...
- **After Stage N:** ...
```

## After writing

Update `zensical.toml` nav — `learning-path.md` should already be in the nav from Phase 1 scaffold.

Tell the user:
- Learning path written at `docs\learning-path.md`
- How many stages, total estimated hours
- Which resource to start with
- How to trigger Phase 3: "When you finish a module or chapter, tell me what you completed and I'll write the book chapter"
