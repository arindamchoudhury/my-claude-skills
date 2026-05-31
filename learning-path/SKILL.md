---
name: learning-path
description: >
  Use when a user wants to learn any technical topic from scratch or continue learning one.
  Triggers on: "I want to learn X", "start a learning path for X", "I finished module X of course Y",
  "I finished chapter X of book Y", "create a learning path for X", "set up notes for learning X",
  "I'm studying X", "help me learn X", "I completed X", "write a chapter on what I just learned".
  This skill researches the topic's book and course landscape, creates a structured learning path,
  auto-generates a topic-specific book writing skill, and writes a technical book chapter by chapter
  as the user progresses — blending new knowledge with existing chapters and keeping content current
  with the latest release of the technology. Works for any topic: LangChain, Databricks, Python,
  MLOps, Kubernetes, system design, etc.
---

# Learning Path Skill

A three-phase workflow for learning any technical topic, building a knowledge book as you go.

## Phase Detection

Before doing anything, check the topic's state:

```
topic slug = derive from user's message (e.g. "ai agents" → "ai-agents", "databricks" → "databricks")
notes root = C:\opt\learn\<topic-slug>\notes
```

| State | Action |
|---|---|
| `notes\` missing OR `docs\learning-path.md` missing | Run Phase 1 then Phase 2 |
| `learning-path.md` exists + user says "I finished X" | Run Phase 3 |
| `learning-path.md` exists + no module completed | Show learning path + book progress summary |

---

## Phase 1 — Research & Scaffold

Read `references/phase1-research.md` for full instructions.

**Summary:**
1. Research top books on the topic (TOCs, chapter arcs) via web search
2. Research top courses (official academies, Udemy, Coursera, YouTube)
3. Validate current stable version against official docs
4. Scaffold `C:\opt\learn\<topic-slug>\notes\` (Zensical site, fetch script, Docker)
5. Auto-generate `~/.claude/skills/<topic>-book/SKILL.md`
6. Write initial docs (index, sources, glossary, resources)

Phase 1 flows directly into Phase 2.

---

## Phase 2 — Learning Path

Read `references/phase2-path.md` for full instructions.

**Summary:**
1. Order resources by concept dependency (not prestige)
2. Write `docs\learning-path.md` with stages, time estimates, focus notes
3. Mark each resource: Essential / Recommended / Optional
4. Flag resources targeting older versions

---

## Phase 3 — Chapter Writing

Read `references/phase3-book.md` for full instructions.

**Every lesson produces TWO outputs:**
1. **Book chapter** (`docs\book\ch<NN>-<slug>.md`) — pedagogical, explained, with pitfalls and exercises
2. **Research note** (`docs\sources\<course-slug>\<slug>.md`) — source-faithful reference, cross-linked to book chapter

**Summary:**
1. Read the notebook(s) / lesson content
2. Validate every function/class against official docs; save findings to `cache\search\`
3. Determine: new book chapter or blend into existing?
4. Write the book chapter (full explanation, examples, pitfalls, exercises)
5. Write the research note (source-faithful, code examples, links to book chapter)
6. Add version callout if course material is behind current release
7. Sync nav: book + research notes in `zensical.toml`, source indexes, glossary, topics backlog

---

## Topic Slug Derivation

Convert the user's topic to a lowercase kebab-case slug:

| User says | Slug | Notes root |
|---|---|---|
| "ai agents" | `ai-agents` | `C:\opt\learn\ai-agents\notes` |
| "databricks" | `databricks` | `C:\opt\learn\databricks\notes` |
| "LangChain" | `langchain` | `C:\opt\learn\langchain\notes` |
| "MLOps" | `mlops` | `C:\opt\learn\mlops\notes` |

---

## After Every Phase 3 Run

Always end with:
- Confirmation of what was written / blended
- Current chapter count and book progress
- What's next in the learning path
