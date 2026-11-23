---
name: agentic-ai-book
description: >
  Use when writing, drafting, reviewing, or extending a chapter in the personal Agentic AI book at
  C:\opt\learn\agentic-ai\notes\docs\book\ (built around Stanford CS329Z Engineering AI Agents,
  CS224V Agentic AI, and CS329A Self-Improving AI Agents). Triggers on: "write the chapter for X",
  "I finished topic B5", "I finished CS329Z lecture 6", "I finished CS329A part 3", "I finished the
  CS224V WikiChat lecture", "I finished HW1", "I just learned about ReAct / MCP / context engineering /
  GEPA / DSPy / verifiers / GRPO / test-time compute / STORM / SUQL / Genie worksheets", "add a
  chapter on multi-agent systems", "write the agentic ai book chapter for evals", any reference to a
  learning-path topic code (B1–B7, I1–I14, A1–A11, E1–E6), or any request to add/draft/review/extend
  a chapter in the agentic AI personal book. Also fires on agent-concept learning meant for the book
  ("explain LLM-as-judge for the book", "add a chapter on coding agents").
---

# Agentic AI Book: Chapter Writing

Synthesised chapters, one per learning-path topic, at `C:\opt\learn\agentic-ai\notes\docs\book\`.
A chapter blends **every source the user has worked through** on that topic — Stanford slides and
videos (CS329Z, CS224V, CS329A), Berkeley MOOC lectures, papers, book chapters, the user's own
homework or lab code, and current docs — into one explained treatment aligned to the learning-path
milestone.

This skill is invoked by **Phase 3** of the `learning-path` skill. Read
`learning-path/references/phase3-book.md` for the full workflow (gather notes → web-search current
practices → synthesis plan → write → sync index/glossary). This file supplies the **chapter arc**,
**invariants**, **toolkit**, and **agent-specific standards**.

**The book has three layers that must stay welded together.** Every chapter owes the reader:

- the **mechanism** — what ReAct, compaction, GEPA or a process reward model *is*, from first principles;
- the **built version** — plain-Python code the reader can run, framework-free first, the framework second;
- the **measured evidence** — what it does on an eval: success rate *with* cost, tokens, variance and
  failure taxonomy.

A chapter that is all concepts is a blog post. All code is a tutorial. All numbers is a leaderboard.
None of those is this book. For the research topics (CS329A, CS224V systems) the "built version"
becomes *the paper's method, and what you ran yourself*.

---

## Chapter arc

One chapter per learning-path topic, numbered sequentially across all four levels. File name:
`ch<NN>-<slug>.md`.

**The chapter list is not duplicated here.** It lives in `docs/book/index.md`, generated from
`docs/learning-path.md` by `scripts/sync_book_index.py`. Read that file for the number and title.

```bash
python scripts/sync_book_index.py     # regenerate; --check fails without writing
```

As of 2026-11-10 the path has **38 topics**: B1–B7 → 1–7, I1–I14 → 8–21, A1–A11 → 22–32,
E1–E6 → 33–38. Level map, for orientation only (the index is authoritative):

| Level | Codes | Spine |
|---|---|---|
| Beginner — foundations | B1–B7 | CS329Z L1–L4, L6 · BAAS Ch 1–5 · agent = loop + tools + retrieval + MCP |
| Intermediate — building & measuring | I1–I14 | CS329Z L5–L8, L13+ · CS224V WikiChat/SUQL/Genie · patterns, context, memory, frameworks, multi-agent, evals, safety |
| Advanced — improving & hard agent classes | A1–A11 | CS329Z L9–L12 · CS224V STORM/SatIR · CS329A Parts 2–5 · data, optimisation, deep research, coding, harnesses, TTC, verifiers, planning, multimodal, proactive |
| Expert — training & research | E1–E6 | CS329A Parts 4, 6–9 · RLHF book · BRM · feedback, RL, distillation, self-improvement, frontier evals, serving memory |

Rules the numbering follows:

- **A written chapter's number never changes.** `sync_book_index.py` refuses to renumber one.
- Every chapter header **must** declare its topic on its own line:

  ```markdown
  > **Learning-path topic:** [The agent loop: ReAct from scratch](../learning-path.md#b5-the-agent-loop-react-from-scratch)
  ```

  The link text is the topic **title**; the sync script reads the topic code from the anchor
  (`#b5-…`). A chapter file without this line is an error.
- **Never show a topic code (B5, I3, E2, …) anywhere in a chapter**: prose, tables, admonitions,
  See-also, What's next. Readers of a book navigate by chapter number; codes are learning-path
  bookkeeping. Refer to every chapter as **"Chapter N"** (number from `docs/book/index.md`), with its
  title where it helps:
  - **Written chapter** → link the file, with a section anchor when pointing at a section. Take the
    anchor from the built site (`id="…"`), never guess the slug.
  - **Unwritten chapter** → same "Chapter N" text, linked to its learning-path topic:
    `[Chapter 22](../learning-path.md#a1-data-for-agentic-systems)`. Switch to the file once written.
  - Course labels ("CS329Z Lecture 6", "CS329A Part 3", "CS224V Oct 19") and Mermaid node ids are
    not topic codes and are fine.

---

## Chapter invariants (every chapter, no exceptions)

These are contracts, not a shape. A chapter that satisfies all six and looks unlike every other
chapter is correct.

1. **Nothing is used before it is explained.** A reader never meets a term, message field, API,
   metric or algorithm the chapter leans on before this chapter or an earlier one has named it.
   **This is a book, not a notebook.** Every chapter states its exit contract up front as
   `## What you should be able to do by the end`: 4–6 concrete, checkable abilities derived from the
   topic's **Milestone** ("report pass@1 and pass^3 with confidence intervals on a 30-task eval"),
   not things the reader knows about. **That list is the only fixed opening; everything after it is
   chosen by topic.**
2. **All three layers:** mechanism, built version, measured evidence (see above).
3. **Teach toward the milestone.** The reader who finishes can do exactly what the milestone says.
4. **Current, runnable code.** Python 3.12+, dependencies pinned in the chapter's lab
   `pyproject.toml`, run with `uv`. Code runs as written against the versions in "Current versions"
   below. Never paste homework solution code from a course repo (CS329Z HW1/HW2 are graded
   assignments): explain the idea in your own code, or reference the reader's own implementation.
5. **Every body callout is a Material admonition**, never a `>` blockquote.
6. **End pointing forward** to the next chapter by number and title (never by topic code), naming
   what it builds on this one.

---

## Chapter shapes (choose one; do not default)

| Shape | Fits a topic where… | Arc |
| --- | --- | --- |
| **Problem-first** | the reader arrives burned: an agent that loops forever, a judge that disagrees with them, an injection that worked (I3, I13, I14) | the failure, reproduced → why → the mechanism → the fix, measured |
| **Orientation-first** | the reader arrives with nothing built and no grievance (B1, B2, A11) | the thing end to end → each part in depth → failure modes |
| **Mechanism-first** | the idea is the value (ReAct loop, MCP, memory tiers, GRPO, PRMs) | the model from first principles → what it buys → where SDKs/frameworks implement it |
| **Surface-first** | a body of API to become fluent in (LangGraph, DSPy, an agent SDK) | the construct's shape → semantics and edge cases → where it goes wrong |
| **Decision-first** | a trade-off (workflow vs agent, single vs multi-agent, prompt vs weight optimisation, which harness) | the decision → the axes → each option against them → how to pick, with your own numbers |
| **Paper-first** | a research topic from CS329A or CS224V (A3, A4, A7–A9, E1–E5) | the problem → the main papers' methods compared on one table → what you reproduced → critique and open questions |

A "The problem this solves" section is one option, never an obligation. Retrofitting a grievance onto
an orientation topic invents a motivation the reader does not have.

---

## Toolkit (draw on what the topic needs)

- A motivating failure (only where the reader really arrives with it) — show the actual trajectory
- First-principles mechanism prose; equations in MathJax (`$...$`, `$$...$$`) for RL, scaling laws and metrics
- **Raw message transcripts**: the literal request/response JSON for one loop iteration, tool call
  and tool result, so the abstraction is visible before an SDK hides it
- Worked examples: plain-Python version, then the framework/SDK version, side by side
- Mermaid diagrams: agent loops, state graphs, multi-agent topologies, data flywheels, RL loops
- **Trajectory walkthroughs**: an annotated real run, step by step, with where it went wrong
- Eval tables: success rate, mean ± CI over runs, tokens, $ cost, wall time, per configuration
- Failure taxonomies (e.g. MAST for multi-agent; your own categories from error analysis)
- Paper comparison tables (method, setting, benchmark, headline result, main critique)
- Pitfalls: what goes wrong and what it looks like in a trace
- Exercises mapping to the milestone; a `## Lab` that combines and breaks what was taught inline
- Summary and references

---

## Standards

### Code

- **Plain Python first.** Mechanism code uses the provider SDK directly (`anthropic` or `openai`) with
  no framework, so the loop is visible. The framework version (LangGraph, DSPy, Agents SDK, ADK)
  comes second, labelled as such.
- **One model constant per lab.** `MODEL = "claude-sonnet-5-5"` (cheap loops: `"claude-haiku-5-5"`;
  hardest reasoning: `"claude-opus-5-5"`). Never scatter model IDs, and never write retired IDs.
  Where a lab must be provider-agnostic, use LiteLLM or OpenRouter (CS329Z's labs use OpenRouter)
  and say so.
- API keys come from `.env` (gitignored) via `python-dotenv` — never inline.
- Every agent loop has a **hard step limit and a token/cost budget**, and handles tool exceptions.
  An example without them teaches a bug.
- Tool outputs are truncated or paginated in examples. Unbounded tool output is an anti-pattern.
- Seed what can be seeded; for LLM sampling, state temperature and run each eval ≥ 3 times.
- Runnable lab code lives in `labs/ch<NN>-<slug>/` with its own `pyproject.toml`; the chapter embeds
  the key excerpts and links the folder.

### Measured claims

Any number the chapter asserts — a success rate, a cost, a speedup, a judge agreement — comes from a
run the author did, with the setup on one line:
`claude-sonnet-5-5 · 2026-11-20 · 30 tasks × 3 runs · temp 1.0 · $0.84 total · harness: own ReAct`.
Report variance (pass^k or mean ± CI), never a single-run number. A number carried from a paper,
leaderboard or vendor post ("GEPA beats GRPO by 10%", "SWE-bench Verified 80%") is **attributed** as
theirs, not restated as measured. Always pair accuracy with cost (Kapoor et al., "AI Agents That
Matter").

### Research chapters (Paper-first)

- Cite each paper with arXiv/DOI link and venue/year, and say which course lecture assigns it.
- Separate **what the paper claims**, **what its evaluation actually shows**, and **known critiques**
  (contamination, harness confounds, reward hacking, judge bias). Never present a claim as settled fact.
- Include at least one thing the reader ran themselves (from the topic's "Hands-on" or "Reference" line).

### Version-gated facts

Record verified facts in `docs/research-cache/version-facts.md`. Known traps (as of 2026-11-10):

| Fact | Trap |
|---|---|
| MCP spec **2026-07-28** is current (stateless core) | CS329Z L4 assigns 2025-06-18; BAAS code pins `mcp>=1.0` (SDK v1); ADP predates it. No `initialize` handshake or `Mcp-Session-Id` any more; Roots/Sampling/Logging deprecated; tasks are an extension. Write code for SDK 2.x. |
| Anthropic engineering posts moved | `anthropic.com/engineering/...` redirects to `anthropic.com/research/...` — write the new path |
| Claude Agent SDK docs moved | `platform.claude.com/docs/en/agent-sdk/...` → `code.claude.com/docs/en/agent-sdk/...` |
| OpenAI docs host moved | `platform.openai.com/docs/guides/...` → `developers.openai.com/api/docs/guides/...`; the deep-research guide 404s |
| DSPy 3.4 docs reorganised | `/learn/programming/...` and `/learn/optimization/...` redirect into `/current/getting-started/...` and `/current/api/...` |
| TRL 1.17 has no PRM trainer page | `docs/trl/prm_trainer` exists only on `main`; don't depend on `PRMTrainer` |
| LangChain doc moves | RAG tutorial → `oss/python/deepagents/rag`; LangGraph durable execution → `oss/python/langgraph/persistence` |
| ADK docs moved | `google.github.io/adk-docs/...` → `adk.dev/...` |
| CS329A ADAS reading | the schedule labels arXiv 2505.22954 "Automated design of agentic systems", but that ID is the Darwin Gödel Machine; ADAS is arXiv 2408.08435 |
| *Learning LangChain* (LLC) | written for LangChain/LangGraph 0.x; current is 1.x — concepts only |
| CS329Z / CS224V Fall 2026 still running | slides after CS329Z L13 / CS224V Nov 9 were unpublished on 2026-11-10; check before citing |

---

## Current versions (verified 2026-11-10 on PyPI)

| Component | Version | Note |
|---|---|---|
| langgraph / langchain | 1.2.20 / 1.4.9 | 1.x API; persistence + interrupts for HITL |
| dspy | 3.4.1 | docs under `dspy.ai/current/` |
| mcp (Python SDK) | 2.3.0 | targets spec 2026-07-28 |
| a2a-sdk | 1.3.0 | spec at a2a-protocol.org/latest |
| openai-agents | 0.24.0 | pre-1.0: check API names |
| claude-agent-sdk | 0.2.180 | pre-1.0: check API names |
| google-adk | 2.14.0 | |
| anthropic / openai | 2.7.0 / 3.49.0 | provider SDKs used for plain-Python mechanism code |
| smolagents / pydantic-ai / crewai | 1.26.0 / 2.66.0 / 1.15.39 | |
| trl | 1.17.1 | GRPO, SFT, GKD, reward trainers |
| inspect-ai | 0.3.288 | eval framework used in I12/I13/E5 |

Re-verify before writing any chapter that states a version-dependent fact
(`curl -s https://pypi.org/pypi/<pkg>/json`).

---

## Key patterns every chapter should reinforce where relevant

1. **Climb the autonomy ladder only when forced.** LLM call → workflow → agent; justify each rung (CS329Z L1, ANT-BEA).
2. **The loop is simple; the interface is everything.** Tool and agent-computer-interface design decides success more than prompt wording (SWE-agent's ACI lesson).
3. **Context is a budget, not a bucket.** Every token in the window should earn its place (compaction, masking, isolation).
4. **Measure before you optimise, and measure cost with accuracy.** pass^k, CIs, $ per task; error analysis on real trajectories.
5. **Ground and verify; generation is cheap, verification is the bottleneck.** Claim-level checking (CS224V), verifiers for selection (CS329A).
6. **All tool output is untrusted input.** Design every tool and permission as if a page the agent reads is hostile.
7. **Data and feedback compound.** Traces → datasets → optimisation or training → better traces (the flywheel).

---

## Anti-patterns to never write

- A success rate from one run, or with no cost, model ID, date and task count
- Restating a paper's, vendor's or leaderboard's number as if measured here
- An agent loop with no step limit, no budget, or no tool-error handling
- Tools that return unbounded output (whole files, whole web pages) into context
- An unvalidated LLM judge presented as ground truth
- Framework-only examples that hide the message exchange the chapter is teaching
- Describing the MCP initialize handshake or session IDs as current
- Hardcoded API keys or retired model IDs
- Pasting CS329Z/CS224V homework solutions
- Reproducing more than a short attributed quote from any source
- Leaving a `>` blockquote in the chapter body

---

## Callout formatting (mandatory)

Every note, definition, aside, tip, warning, and version-gate in a chapter **body** is a Material
admonition:

```markdown
!!! note "Title"
    Body indented four spaces.
```

Types by what the reader must do: `warning` (will bite them: a changed API, a book now wrong),
`danger` (silent wrong results, security holes), `info` (naming or behaviour clarification), `tip`
(technique), `note` (additive context). `>` blockquotes are reserved for the chapter-header
front-matter only (source + summary + see-also + the Learning-path topic line); a `>` in the body is a
defect to convert on sight. Never indent an admonition into a list item.

---

## After writing a chapter

1. `python scripts/sync_book_index.py` — regenerates `docs/book/index.md`. Do not hand-edit it.
2. Flip the topic heading in `docs/learning-path.md` from `⬜` to `✅`.
3. Add the chapter to `zensical.toml` nav under `Book`.
4. Append new terms to `docs/reference/glossary.md` with the chapter link.
5. Record newly verified facts in `docs/research-cache/version-facts.md`.
6. Run the Phase 3 coverage audit (`learning-path/references/phase3-book.md` Step 5c).
7. Run Phase 5 of the `learning-path` skill to reconcile the path against the chapter.
8. Build: `.venv\Scripts\python -m zensical build`, then `python scripts/check_links.py site`.
