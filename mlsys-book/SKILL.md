---
name: mlsys-book
description: >
  Use when writing, drafting, reviewing, or extending a chapter in the personal ML Systems book at
  C:\opt\learn\machinelearning\notes\docs\book\ (TinyTorch + MLSysBook Vol I/II + Harvard CS249r
  Architecture 2.0). Triggers on: "write the chapter for X", "I finished topic B7", "I finished
  TinyTorch module 06", "I finished milestone 04", "I finished CS249r week 8", "I just learned about
  autograd / quantization / KV-cache / roofline / FSDP / accelerator dataflows / chip placement",
  "add a chapter on attention", "write the mlsys book chapter for pruning", any reference to a
  learning-path topic code (B1–B9, I1–I6, A1–A10, E1–E17), or any request to add/draft/review/extend
  a chapter in the ML systems personal book. Also fires on ML-systems concept learning ("explain
  PagedAttention for the book", "add a chapter on KernelBench").
---

# ML Systems Book: Chapter Writing

Synthesised chapters, one per learning-path topic, at `C:\opt\learn\machinelearning\notes\docs\book\`.
A chapter blends **every source the user has worked through** on that topic: TinyTorch module notes
and their own implementation, MLSysBook chapters, CS249r papers and blog posts, course lectures, and
current docs: into one explained treatment aligned to the learning-path milestone.

This skill is invoked by **Phase 3** of the `learning-path` skill. Read
`learning-path/references/phase3-book.md` for the full workflow (gather notes → web-search current
practices → synthesis plan → write → sync index/glossary). This file supplies the **chapter arc**,
**invariants**, **toolkit**, and **ML-systems-specific standards**.

**The book has three layers that must stay welded together.** Every chapter owes the reader the
*mechanism* (what autograd or a systolic array *is*, from first principles), the *built version*
(what the reader's own TinyTorch code does, or would do), and the *systems cost* (bytes, FLOPs,
latency, energy, which of Data/Algorithm/Machine bounds it). A chapter that is all maths is a DL
textbook; all code is a tutorial; all numbers is a benchmark report. None of those is this book. For
the Expert CS249r topics the "built version" becomes *the paper's method, and what you ran yourself*.

---

## Chapter arc

One chapter per learning-path topic, numbered sequentially across all four levels. File name:
`ch<NN>-<slug>.md`.

**The chapter list is not duplicated here.** It lives in `docs/book/index.md`, generated from
`docs/learning-path.md` by `scripts/sync_book_index.py`. Read that file for the number and title.

```bash
python scripts/sync_book_index.py     # regenerate; --check fails without writing
```

As of 2026-09-11 the path has **42 topics**: B1–B9 → 1–9, I1–I6 → 10–15, A1–A10 → 16–25,
E1–E17 → 26–42. Level map, for orientation only (the index is authoritative):

| Level | Codes | Spine |
|---|---|---|
| Beginner, Foundation | B1–B9 | D·A·M / Iron Law, then TinyTorch 01–08 (tensor → training) |
| Intermediate, Architecture | I1–I6 | TinyTorch 09–13 (conv, tokenization, embeddings, attention, transformer) + framework internals |
| Advanced, Optimization | A1–A10 | TinyTorch 14–20 (profiling → capstone) + V1 data selection, serving, MLOps |
| Expert, Scale | E1–E4 | Vol II: distributed training, fleet, inference at scale, production concerns |
| Expert, Architecture 2.0 | E5–E17 | CS249r Weeks 1–13 in order, then the survey capstone |

Rules the numbering follows:

- **A written chapter's number never changes.** `sync_book_index.py` refuses to renumber one.
- Every chapter header **must** declare its topic on its own line:

  ```markdown
  > **Learning-path topic:** [Autograd: computational graphs and reverse-mode differentiation](../learning-path.md#b7-autograd-computational-graphs-and-reverse-mode-differentiation)
  ```

  The link text is the topic **title**; the sync script reads the topic code from the anchor
  (`#b7-…`). A chapter file without this line is an error.
- **Never show a topic code (B7, I3, E12, …) anywhere in a chapter**: prose, tables, admonitions,
  See-also, What's next. Readers of a book navigate by chapter number; codes are learning-path
  bookkeeping. Refer to every chapter as **"Chapter N"** (number from `docs/book/index.md`), with
  its title where it helps:
  - **Written chapter** → link the file, with a section anchor when pointing at a section:
    `[Chapter 7, section 3 "The backward pass"](ch07-autograd.md#3-the-backward-pass)`. Take the
    anchor from the built site (`id="…"`), never guess the slug.
  - **Unwritten chapter** → same "Chapter N" text, linked to its learning-path topic (no file yet):
    `[Chapter 14](../learning-path.md#i5-…)`. Switch the link to the file once that chapter exists.
  - Chapter numbers are safe to print: written ones never change, and `sync_book_index.py` refuses
    to renumber them. If a path insert shifts *unwritten* numbers, grep the chapters for
    `learning-path.md#` links and update their "Chapter N" text.
  - Mermaid node ids like `A1[…]` are not topic codes and are fine. Course labels
    ("CS249r Week 8", "TinyTorch Module 06") are not topic codes either.

---

## Chapter invariants (every chapter, no exceptions)

These are contracts, not a shape. A chapter that satisfies all six and looks unlike every other
chapter is correct.

1. **Nothing is used before it is explained.** A reader never meets a term, tensor, symbol, API or
   mechanism the chapter leans on before this chapter or an earlier one has named it. **This is a
   book, not a notebook.** Every chapter states its exit contract up front as
   `## What you should be able to do by the end`: 4–6 concrete, checkable abilities derived from the
   topic's **Milestone** ("compute the KV-cache bytes for a 7 B model at 8 k context"), not things the
   reader knows about. That list is the one fixed opening; everything after it is chosen by topic.
2. **All three layers:** mechanism, built version, systems cost (see above).
3. **Teach toward the milestone.** The reader who finishes can do exactly what the milestone says.
4. **Runnable code.** NumPy/TinyTorch code runs as written on Python 3.10+ with the reader's own
   TinyTorch package (`from tinytorch.core.tensor import Tensor`); PyTorch comparisons run on the
   current stable PyTorch. Never paste TinyTorch *solution* code from the repo: write the idea in
   your own words/code or reference the reader's own implementation.
5. **Every body callout is a Material admonition**, never a `>` blockquote.
6. **End pointing forward** to the next chapter by number and title: never by topic code: naming
   what it builds on this one.

---

## Chapter shapes (choose one; do not default)

| Shape | Fits a topic where… | Arc |
| --- | --- | --- |
| **Problem-first** | the reader arrives burned, a `nan` loss, an OOM, a slow generator | the failure, reproduced → why → the mechanism → the fix |
| **Orientation-first** | the reader arrives with nothing built and no grievance (B1, E5) | the thing end to end → each part in depth → failure modes |
| **Mechanism-first** | the idea is the value (autograd, attention, roofline, systolic dataflow) | the model from first principles → what it buys → where frameworks/hardware implement it |
| **Surface-first** | a body of API the reader must become fluent in (`torch.distributed`, `tito`) | the construct's shape → semantics and edge cases → where it goes wrong |
| **Decision-first** | a trade-off between options (quantize vs prune, DP vs TP vs PP, RL vs BO for DSE) | the decision → the axes → each option against them → how to pick |
| **Paper-first** | a CS249r week (E6–E16) | the systems problem → the main papers' methods compared on one table → what you reproduced → critique and open questions |

A "The problem" section is one option, never an obligation. Retrofitting a grievance onto an
orientation topic invents a motivation the reader does not have.

---

## Toolkit (draw on what the topic needs)

- A motivating failure (only where the reader really arrives with it)
- First-principles mechanism prose, with equations in MathJax (`$...$`, `$$...$$`)
- Worked examples with real output from the reader's TinyTorch and from PyTorch side by side
- Mermaid diagrams: computation graphs, dataflows, parallelism layouts, EDA flows, agent loops
- Back-of-envelope cost tables: params, FLOPs, activation/optimizer/KV memory, bytes moved
- Roofline plots or arithmetic-intensity tables
- Paper comparison tables (method, search space, evaluation, headline result, main critique)
- Pitfalls: what goes wrong and what it looks like (`nan`, OOM, a graph break, a vacuous assertion)
- Exercises mapping to the milestone; a `## Lab` that combines and breaks what was taught inline
- Summary and references

---

## Standards

### Code

- NumPy first for mechanism code; TinyTorch API for "your framework"; PyTorch for "the production
  version". Label each block with which of the three it is.
- Show shapes in comments (`# (B, T, C)`), dtypes where precision matters.
- Seed randomness (`np.random.default_rng(0)`) so outputs reproduce.
- Use `torch.utils.benchmark` or TinyTorch's Module 19 tooling for timing: never a bare `time.time()`
  around one call.

### Measured claims

Any number the chapter asserts: a speedup, an accuracy, a memory size: comes from a run the author
did, with hardware, versions and settings stated on one line
(`TinyTorch v0.1.13, NumPy 2.x, Python 3.13, i7/32 GB, batch 64`). A number carried from a paper or
from TinyTorch's own pages ("8–16× smaller", "12–40× faster") is **attributed** as theirs, not
restated as measured. Derived numbers (FLOP counts, memory arithmetic) show the derivation.

### Paper chapters (E5–E17)

- Cite each paper with arXiv/DOI link and venue/year. Say what CS249r week it belongs to.
- Separate **what the paper claims**, **what the evaluation actually shows**, and **known
  critiques** (e.g. the Circuit Training evaluation debate). Never present a claim as settled fact.
- Include at least one thing the reader ran themselves (a tool from the topic's "Reference" line).

### Version-gated facts

Record verified facts in `docs/research-cache/version-facts.md`. Known traps:

| Fact | Trap |
|---|---|
| MLSysBook split into Vol I/II (2026) | CS249r Fall 2025 cites old single-volume chapter numbers; map them via the table in the learning path |
| TinyTorch is a **preview** (v0.1.x) | Module APIs and `tito` commands can change between releases; check `tito --version` and the module page before quoting a command |
| Torch Olympics "Coming Soon" | Do not describe a leaderboard or rules as live |
| PyTorch quantization moving to torchao | Older `torch.ao.quantization` tutorials may be deprecated |
| PyTorch docs moved to `docs.pytorch.org` | Old `pytorch.org/docs/...` links redirect; write the new host |
| TorchServe in limited maintenance | Prefer vLLM or similar when citing a serving runtime |

---

## Current versions (verified 2026-09-11: see docs/research-cache/version-facts.md)

| Component | Version | Note |
|---|---|---|
| MLSysBook Vol I | v0.7.2 (2026-08-31) | Release edition, MIT Press 2026 |
| MLSysBook Vol II | v0.2.1 (2026-07-03) | Preview; chapters stable, polish ongoing |
| TinyTorch | v0.1.13 (2026-06-24) | Preview; Python 3.10+; Windows via Git Bash |
| Python (local) | 3.13.15 | |

Re-verify before writing any chapter that states a version-dependent fact.

---

## Key patterns every chapter should reinforce where relevant

1. **Name the bottleneck: Data, Algorithm or Machine.** V1's D·A·M frame, applied every time.
2. **Count before you run.** Params, FLOPs, bytes and memory are derivable from shapes; derive them
   first, then measure and explain the gap.
3. **Memory traffic, not FLOPs, is usually the cost.** Use arithmetic intensity and the roofline.
4. **Profile, then optimise; benchmark, then claim.** Measure → optimise → validate.
5. **Build it to debug it.** Explain production behaviour through the reader's own implementation.
6. **Every optimisation is a trade.** Name what is paid: accuracy, memory, latency, generality.
7. **For AI-for-systems: correctness is the floor, optimality is the question, evaluation is the
   battleground.**

---

## Anti-patterns to never write

- A speedup or compression ratio with no baseline, hardware or settings
- Restating TinyTorch's or a paper's headline numbers as if measured here
- Pasting TinyTorch reference solutions (write your own; the reader is meant to build it)
- `softmax` then `log` as two separate steps in an example about losses
- Treating unstructured sparsity as an automatic speedup
- Presenting an AI-for-chip-design result without its evaluation caveats
- Citing a CS249r "Ch N" reading without mapping it to the 2026 volume
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
`danger` (silent wrong results), `info` (naming or behaviour clarification), `tip` (technique),
`note` (additive context). `>` blockquotes are reserved for the chapter-header front-matter only
(source + summary + see-also + the Learning-path topic line). Never indent an admonition into a list
item.

---

## After writing a chapter

1. `python scripts/sync_book_index.py`: regenerates `docs/book/index.md`. Do not hand-edit it.
2. Flip the topic heading in `docs/learning-path.md` from `⬜` to `✅`.
3. Add the chapter to `zensical.toml` nav under `Book`.
4. Append new terms to `docs/reference/glossary.md` with the chapter link.
5. Record newly verified facts in `docs/research-cache/version-facts.md`.
6. Run the Phase 3 coverage audit (`learning-path/references/phase3-book.md` Step 5c).
7. Run Phase 5 of the `learning-path` skill to reconcile the path against the chapter.
8. Build: `python -m zensical build` (a venv with `zensical` installed), then
   `python scripts/check_links.py site`.
