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
1. Research topic taxonomy — derive all topics from certification exams, university syllabi, job descriptions, and course curricula; classify each topic as Beginner / Intermediate / Advanced / Expert
2. Research top books (fetch full TOCs); note which topics each book covers
3. Research courses — official academies, university MOOCs (Coursera/edX), Udemy, YouTube, interactive platforms (DataCamp, Kaggle); note topics covered, hours, hands-on vs lecture
4. Research certifications — fetch official exam guides; record topics, weights, fees, and which level they validate
5. Validate current stable version against official docs
6. Scaffold `C:\opt\learn\<topic-slug>\notes\` (Zensical site, Docker)
7. Auto-generate `~/.claude/skills/<topic>-book/SKILL.md` with full chapter arc from taxonomy

Phase 1 flows directly into Phase 2.

---

## Phase 2 — Learning Path

Read `references/phase2-path.md` for full instructions.

**Summary:**
1. Organise topics into four levels: Beginner / Intermediate / Advanced / Expert
2. For each topic write: what it is (1 sentence), why you need it (1 sentence), **multi-modal "How to learn it"** (video first → interactive exercise → depth reading → reference docs), and a concrete milestone
3. Place certifications as level checkpoints (not as topics)
4. Do NOT organise by resource/book/course — topics are the primary unit; resources serve the topics
5. Every "How to learn it" section must include at least two different resource types (video, interactive, book, official course, docs, project)

---

## Phase 3 — Book Chapter Writing

Read `references/phase3-book.md` for full instructions.

**Notes** (written by `book-pdf-notes`) are source-faithful — one per book/article/course. **Book chapters** (written here) are topic-driven syntheses — one per learning-path topic, blending all sources the user has read on that topic.

**Summary:**
1. Trigger: user says "I finished topic X" or "write the chapter for X"
2. Identify the topic code and chapter number from the topic-book skill's arc table
3. Gather all notes already written for this topic (grep notes directory)
4. Web-search for current best practices and pitfalls not yet in the notes
5. Produce a synthesis plan — how to blend sources; note conflicts and different framings
6. Write one book chapter that blends all sources; chapter follows the learning-path topic's scope exactly
7. Fit the chapter's structure to the topic — free format guided by a few invariants, not a fixed 8-section template
8. Sync: book index, `zensical.toml`, glossary

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
