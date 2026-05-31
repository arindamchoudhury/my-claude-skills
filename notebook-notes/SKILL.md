---
name: notebook-notes
description: >
  Use when the user wants to take notes from a Python notebook (.ipynb file) or a set of notebooks.
  Triggers on: "take notes from this notebook", "explain this notebook", "what does this notebook do",
  "take notes from <path>.ipynb", "explain what's going on in these notebooks", "the notebook is bare,
  explain it", "add notebook to my notes", "document this notebook". Also use when the user shares
  a .ipynb path and wants it explained, documented, or added to their knowledge base.
  Produces: a research note (source-faithful reference) AND a book chapter (fully explained, with
  best practices and pitfalls), both validated against current official docs via web search.
---

# Notebook Notes Skill

Turn a bare Python notebook into a fully-explained, web-validated knowledge note.

Notebooks are often code-only — no explanations, no context, no best practices.
This skill fills the gap: reads every cell, researches every function and concept,
verifies everything against the latest release, and writes structured notes.

---

## Output

Every notebook (or set of related notebooks) produces **two outputs**:

1. **Research note** (`docs\sources\<course-slug>\<slug>.md`) — source-faithful reference: what the notebook showed, all code examples, brief explanations, cross-linked for future use
2. **Book chapter** (`docs\book\ch<NN>-<slug>.md`) — fully explained: why each function exists, how it works, best practices, common pitfalls, exercises

Follow the structure from the `learning-path` skill. If a `learning-path` is set up for the topic, write to that site. Otherwise, ask the user where to save notes.

---

## Workflow

### Step 1: Read the notebook(s)

Notebooks are JSON files. Read with the Read tool — it renders them cell by cell.

For each cell, extract:
- **Cell type**: `code` or `markdown`
- **Source**: the code or text
- **Output**: what the cell produced when run (often has actual return values or printed output — these tell you what functions return)

Build an inventory:
```
Imports:        from langchain.chat_models import init_chat_model
                from langchain_deepseek import ChatDeepSeek
                from langchain_ollama import ChatOllama
                ...
Functions used: init_chat_model(), model.invoke(), agent.stream(), ...
Classes used:   AIMessage, HumanMessage, ChatDeepSeek, ChatOllama, ...
Concepts shown: provider switching, temperature, streaming, multi-turn conversation
```

If multiple notebooks cover the same topic (e.g. main + ollama variant), read all of them before researching — they often complement each other.

### Step 2: Research every function and class

For each import, function, and class in the inventory:

**2a. Check `cache\search\` first** — grep for the name. If a verified entry exists and is recent (<30 days), use it. Skip the web search.

**2b. Web search if no cache entry:**
```
"<function-or-class> langchain documentation <year>"
"<package> <function> how it works best practices"
```

**2c. Fetch the official reference page** — e.g.:
```
https://reference.langchain.com/python/langchain/chat_models/base/init_chat_model
https://reference.langchain.com/python/langchain/agents/factory/create_agent
```

**Extract for each function/class:**
- Full signature with parameter types
- What it returns (type + structure)
- What each parameter does
- Auto-inferred defaults (e.g. provider inferred from model name prefix)
- Security or performance notes from the docs
- Any deprecation warnings

**2d. Save to `cache\search\<slug>.md`:**
```markdown
# <FunctionName>

**Checked:** YYYY-MM-DD
**Source:** <official-docs-url>

## Findings

- Signature: `function(param1: type, param2: type = default) -> ReturnType`
- Returns: description of return value and its structure
- Key parameters: param1 — what it does; param2 — what it does
- Provider inference: (if applicable)
- Deprecation: none / "X is deprecated, use Y instead"
- Best practices: bullet list
```

### Step 3: Check current version / deprecation

For every package imported in the notebook:

```
"<package> latest version pypi <year>"
"<package> changelog deprecations <version>"
```

Check:
- Is the import path still valid? (e.g. `from langchain.chat_models` not moved to `langchain_core`?)
- Is the function/class still the recommended API or is there a newer one?
- Does the version in the notebook match current stable?

If anything is deprecated or changed, flag it clearly in the notes:
```markdown
> ⚠️ **Deprecation:** `OldClass` was deprecated in v1.2. Use `NewClass` instead.
> ✅ **Current API (as of May 2026):** `from langchain.chat_models import init_chat_model`
```

### Step 4: Write the research note

File: `docs\sources\<course-slug>\<slug>.md`

```markdown
---
name: <slug>
description: <one-line summary>
---

# <Lesson/Notebook Title>

> **Source:** [<Course/Repo> — <Notebook filename(s)>](<url or path>)
> **Notebooks:** `<filenames>`
> **Added:** YYYY-MM-DD
> **Tags:** <tag1>, <tag2>, ...
> **Type:** notebook

> 📌 **Full explained chapter:** [[<book-chapter-slug>]]

## Summary
What this notebook demonstrates and why it matters.

## Key points
- Bullet list of the most important concepts demonstrated.
- One bullet per concept — be specific.

## Notes

### <Major Topic 1>

Brief explanation of what this topic is, then code:

```python
# Complete, runnable code from the notebook
# <package> <version> (Month Year)
from package import Something
...
```

What this does: one sentence.
Key detail worth knowing: ...

### <Major Topic 2>
...

## Deprecations / version notes
List anything that changed between what the notebook shows and the current release.
If nothing changed: omit this section.

## Open questions
- Things the notebook raised but didn't explain.

## Related sources
- [[previous-lesson]] — what it covered
- [[book-chapter-slug]] — full pedagogical treatment
```

### Step 5: Write the book chapter

File: `docs\book\ch<NN>-<slug>.md`

```markdown
# Chapter N: <Title>

> **Source:** [<Course> — <Lesson>](<url>)
> **Notebooks:** `<filenames>`
> **Version:** <package versions, e.g. "langchain 1.3.2 · langgraph 1.2.2">
> **Added:** YYYY-MM-DD

## What you'll learn
3–5 bullet points of concrete outcomes the reader will achieve.

## The problem this solves
One paragraph — WHY this exists. What would break or be harder without it.
Ground it in a real scenario.

## Core concept
200–400 words. The mental model.
- Use analogies where helpful
- Explain design decisions (why was it built this way?)
- Comparison tables for alternatives (e.g. cloud vs local models)

## Code examples
Build from minimal → complete. One new idea per example.
Rules:
- Every example is complete and runnable (all imports, load_dotenv())
- Add version comment: `# <package> <version> (Month Year)`
- Show actual output where helpful (from notebook outputs)
- If the notebook used a deprecated pattern, show the current equivalent and note it

## Best practices
3–5 bullet points derived from docs research — not from the notebook itself.
These are what the notebook didn't tell you but should have.

## Common pitfalls
3–5 bullets: what goes wrong, why, how to fix it.
Draw from: deprecation notes, parameter gotchas, provider-specific quirks.

## Exercises
1. **Recall** — answerable from reading (tests understanding)
2. **Apply** — requires running code (tests skill)
3. **Extend** — open-ended, no single right answer (tests creativity)

## Summary
3–5 bullets recapping what was covered.
Last sentence: "The next chapter builds on this by..."
```

### Step 6: Sync nav and indexes

**Book:**
- `docs\book\index.md` — add row
- `zensical.toml` Book group — add entry

**Research notes:**
- `docs\sources\<course-slug>\index.md` — add lesson row
- `docs\sources\index.md` — add row under course section
- `zensical.toml` Research Notes group — add entry under course nested group

**Reference:**
- `docs\reference\glossary.md` — add every new term (function name, class name, concept)
- `docs\topics\index.md` — add new topics to backlog
- `docs\reference\resources.md` — add new official doc links found during research

**Home page:**
- `docs\index.md` — update book progress

### Step 7: Confirm

```
✓ Research note:  "<Lesson Title>"  → docs\sources\<course-slug>\<slug>.md
✓ Book chapter:   "Chapter N: <Title>" → docs\book\ch<NN>-<slug>.md
  Validated: N functions/classes researched
  Deprecated APIs found: [none / list them]
  Version note: [added / not needed]
  New glossary terms: N
  New topics in backlog: N
```

---

## Code standards

- All code blocks complete and runnable — never truncate with `# ...`
- All imports at top of first block in each section
- `load_dotenv()` always present when API keys are used
- Version comment on every first block: `# <package> <version> (Month Year)`
- If notebook shows deprecated code → show current equivalent, add deprecation callout
- Never assert version facts from training data — always verify with web search

---

## When there is no learning-path site

If `docs\learning-path.md` doesn't exist for the topic, ask:
> "Where should I save these notes? I can create a new notes site at `C:\opt\learn\<topic>\notes\` or save to an existing one."

Then run Phase 1 of the `learning-path` skill to scaffold if needed, or just save to a path the user specifies.
