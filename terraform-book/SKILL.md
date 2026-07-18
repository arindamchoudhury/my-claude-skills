---
name: terraform-book
description: >
  Use when writing, drafting, reviewing, or extending a chapter in the personal Terraform
  Data/Infrastructure book at C:\opt\learn\terraform\notes\docs\book\. Triggers on: "write the
  chapter for X", "I finished topic B3", "I just learned about Terraform state / modules /
  OpenTofu", "add a chapter on <Terraform concept>", "write the terraform book chapter for
  modules/state/testing/Stacks", any reference to a learning-path topic code (B1–B9, I1–I8,
  A1–A8, E1–E6), or any request to add/draft/review/extend a chapter in the Terraform personal
  book. Also fires on Terraform/OpenTofu/HCL/HCP Terraform concept learning ("I learned about
  for_each", "add dynamic credentials").
---

# Terraform Book — Chapter Writing

Synthesized chapters, one per learning-path topic, at `C:\opt\learn\terraform\notes\docs\book\`.
A chapter blends **every source the user has read** on that topic (reading notes in `docs/sources/`,
plus current web best-practices) into one explained treatment aligned to the learning-path milestone.

This skill is invoked by **Phase 3** of the `learning-path` skill. Read
`learning-path/references/phase3-book.md` for the full workflow (gather notes → web-search current
practices → synthesis plan → write → sync index/glossary). This file supplies the **chapter arc**,
**invariants**, **toolkit**, and **Terraform-specific standards**.

---

## Chapter arc

One chapter per topic, numbered sequentially across all four levels. File name: `ch<NN>-<slug>.md`.

### Beginner
| Ch | Code | Title |
|----|------|-------|
| 01 | B1 | Infrastructure as Code & where Terraform fits |
| 02 | B2 | Install, providers & your first project |
| 03 | B3 | The core workflow: init / plan / apply / destroy |
| 04 | B4 | HCL language basics |
| 05 | B5 | Providers & resources |
| 06 | B6 | Input variables, outputs & locals |
| 07 | B7 | Expressions, operators & built-in functions |
| 08 | B8 | Data sources |
| 09 | B9 | State fundamentals |

### Intermediate
| Ch | Code | Title |
|----|------|-------|
| 10 | I1 | Meta-arguments: count, for_each, depends_on |
| 11 | I2 | The lifecycle meta-argument |
| 12 | I3 | Dynamic blocks & complex types |
| 13 | I4 | Using modules |
| 14 | I5 | Authoring modules |
| 15 | I6 | Remote state & backends |
| 16 | I7 | State management operations |
| 17 | I8 | Provider configuration in depth |

### Advanced
| Ch | Code | Title |
|----|------|-------|
| 18 | A1 | Provisioners, terraform_data & escape hatches |
| 19 | A2 | Testing, validation & checks |
| 20 | A3 | Terraform in CI/CD automation |
| 21 | A4 | HCP Terraform / Terraform Cloud |
| 22 | A5 | Policy as Code (Sentinel, OPA) |
| 23 | A6 | Secrets & sensitive data |
| 24 | A7 | Multi-environment & multi-account patterns |
| 25 | A8 | Refactoring at scale |

### Expert
| Ch | Code | Title |
|----|------|-------|
| 26 | E1 | Writing custom providers (Plugin Framework) |
| 27 | E2 | Terraform Stacks |
| 28 | E3 | OpenTofu deep dive |
| 29 | E4 | Large-scale state & repo architecture |
| 30 | E5 | Debugging, performance & scaling |
| 31 | E6 | Platform engineering & self-service |

---

## Chapter invariants (every chapter, no exceptions)

1. **Motivate first** — open with the concrete problem this topic solves; the reader should feel the pain before the syntax.
2. **Teach toward the learning-path milestone** — the chapter must make the topic's `Milestone` achievable.
3. **Current, runnable HCL** — code targets Terraform **1.15** / OpenTofu **1.12**; every block should actually apply.
4. **End pointing forward** — close with what this unlocks and which chapter comes next.
5. **Callouts are admonitions, never blockquotes** — see [Callout formatting](#callout-formatting-mandatory). A `>` blockquote for any note/definition/tip/warning/aside is a defect to fix on sight.
6. **Ship a 🧪 Lab (every chapter B2 onward)** — a hands-on section the reader can actually run, for free, against a local AWS emulator. See [Hands-on lab](#hands-on-lab-every-chapter-from-b2). Ch1 holds the one-time setup; every later chapter has a `## 🧪 Lab`.

## Toolkit (draw on what the topic needs — NOT a fixed template)

Learning outcomes · motivating problem · core-concept prose · worked examples · Mermaid diagrams
(dependency graph, plan/apply flow, state lifecycle) · reference tables (functions, meta-args, CLI
flags) · semantics/edge-case sections (what state does on X) · pitfalls · performance notes ·
exercises · summary · references (link the `docs/sources/` notes and HCDocs pages used).

**Fit structure to topic type:**
- **Setup/workflow chapter** (B2, B3, A3) → step-by-step + command output + a diagram of the loop.
- **Language/API chapter** (B4, B6, B7, I1–I3) → concept → syntax → worked examples → pitfalls → function/meta-arg table.
- **Architecture chapter** (I6, A4, A7, E2, E4, E6) → problem → options with tradeoffs → recommended pattern → diagram.
- **Operations/tuning chapter** (I7, A8, E5) → symptom → diagnosis → safe procedure → recovery.
- **Extension chapter** (E1) → protocol mental model → scaffold → CRUD → tests.

A chapter is fit to its topic, not poured into fixed headings.

---

## Terraform code standards

- **Always pin providers.** Every example config has a `terraform { required_providers { ... } required_version = ">= 1.15" } }` block (or `>= 1.12` for OpenTofu-specific chapters).
- **`for_each` over `count`** for keyed/named resource sets; only use `count` for simple on/off (`count = var.enabled ? 1 : 0`) or truly index-identical N.
- **Config-driven state ops** — prefer `import` / `moved` / `removed` blocks over `terraform state mv/rm` CLI surgery in written examples; show the CLI only when explaining recovery.
- **No secrets in HCL or state examples** — use variables + `sensitive = true`, reference Vault / dynamic credentials; never hard-code a key even in a sample.
- **Explicit versions in prose** — when a feature is version-gated, say so ("`terraform test` requires ≥ 1.6"; "dynamic `prevent_destroy` is OpenTofu-only").
- **Show the plan.** When behavior is non-obvious, include the relevant `terraform plan` output excerpt (`+`/`~`/`-/+`) so the reader can predict it.
- **Name the tool.** When Terraform and OpenTofu differ, say which; otherwise write tool-neutral (`terraform`/`tofu` are interchangeable for shared features).

## Hands-on lab (every chapter from B2)

Every chapter from **B2 onward** ends with a `## 🧪 Lab` section (placed **before "Common pitfalls"**) that runs the chapter's concept for real against a **local AWS emulator** — free, no AWS account, no cloud credentials. This is the book's practice surface; keep it in every chapter where the topic can be exercised in HCL.

**The environment** (set up once in Ch1, `#lab-setup-a-free-local-aws-docker`):
- A Docker AWS emulator on gateway port **4566**. Committed compose file: `labs/docker-compose.yml`.
- **Default emulator: Floci** (`floci/floci`, MIT, no token, serves the LocalStack API). Alternatives: **MiniStack** (`ministackorg/ministack`), **LocalStack** (needs a free token since March 2026). All three are interchangeable on `:4566`.
- Facts caches (re-check before writing, per [[feedback_ground_book_chapters_in_notes]]): `docs/research-cache/floci-facts.md`, `ministack-facts.md`, `localstack-facts.md`. Convention memory: [[project_localstack_labs]].

**Lab section rules:**
- **Open with a start step** (reused verbatim every chapter):
  ```shell
  docker compose -f labs/docker-compose.yml up -d      # start the emulator on :4566
  curl -s http://localhost:4566/_localstack/health     # wait until services "available"
  ```
- **Run Terraform via `tflocal`** (`tflocal init/plan/apply/destroy`) — it targets `:4566`, drives any of the three emulators, and leaves `.tf` files portable to real AWS. Never hard-wire an `endpoints{}` block into the main example (show it only as an aside, alongside the `AWS_ENDPOINT_URL` alternative).
- **Emulator-neutral prose** — say "the emulator", not "LocalStack". Name Floci/MiniStack/LocalStack only when listing options.
- **Reliable free surface only: S3, DynamoDB, SQS, SNS, IAM, STS.** EC2 is *mocked* — do not apply EC2/AMI examples; swap for an S3 bucket and say why in a `!!! note`.
- **Always include the "emulation ≠ AWS" `!!! warning`** — a green apply proves HCL/workflow, not AWS-fidelity; validate load-bearing configs on real free-tier AWS.
- **Verify results** with `awslocal ...` and/or `terraform state list` / `terraform output`; then `tflocal destroy`.
- Add the facts-cache links to the chapter's **References** (`🧪 Lab: [Floci Facts](...) · [MiniStack Facts](...) · [LocalStack Facts](...)`).

## Callout formatting (mandatory)

**Every callout is a MkDocs admonition (`!!! type "Title"`) — never a `>` blockquote.** Blockquotes are reserved for the chapter-header front-matter block (source citation + summary + see-also) only. Any note, definition, aside, tip, warning, version-gate, or "(mine)" observation in the chapter body MUST be an admonition. Content indents 4 spaces under the `!!!` line; never indent a callout inside a list item.

Fixed vocabulary (do not invent new types):

| Use for | Admonition | Old blockquote marker |
|---|---|---|
| general note, aside, definition, deferred-to-later | `!!! note "..."` | `> 💭`, `> ❓`, `> **Definition**` |
| personal observation | `!!! note "(mine)"` | `> 💭 (mine):` |
| version/feature-history fact, neutral fact box | `!!! info "..."` | `> 📌` |
| **OpenTofu divergence** (see [[feedback_tid_opentofu_difference_notes]]) | `!!! info "OpenTofu — ..."` | — |
| best-practice / do-this advice | `!!! tip "..."` | `> 💡` |
| footgun, easy-to-get-wrong | `!!! warning "..."` | ⚠️ blockquote |
| data-loss / security / irreversible | `!!! danger "..."` | — |

A `>` blockquote anywhere in the chapter body is a defect — convert it before committing.

## Current versions (verified 2026-07-04 — see docs/research-cache/version-facts.md)

| Tool | Version | License |
|------|---------|---------|
| Terraform CLI | 1.15.7 | BSL 1.1 |
| OpenTofu | 1.12.3 | MPL 2.0 |

> Always re-check `docs/research-cache/version-facts.md` before writing — it's the single source of truth and is bumped as releases ship.

## Key patterns every chapter should reinforce where relevant

1. **Desired-state, not scripts** — declare the end state; let the graph order the work.
2. **Implicit dependencies via attribute references** beat `depends_on`.
3. **Remote state + locking** is the baseline for any collaboration.
4. **Modules are the unit of reuse** — validated inputs, documented outputs, versioned.
5. **Plan is a contract** — review it; in CI, save it (`-out`) and apply the exact artifact.
6. **Least-privilege, short-lived credentials** (OIDC) over static keys.
7. **Empty plan after a refactor** is the proof of a safe refactor (`moved`/`import`/`removed`).

## Anti-patterns to never write

- Hand-editing `terraform.tfstate`.
- `count` for a set of named resources (reindex-on-delete destroys the wrong ones).
- Provisioners (`local-exec`/`remote-exec`) where a data source or provider feature would do.
- Static long-lived cloud keys committed or stored in CI variables.
- CLI workspaces presented as environment isolation (they share backend config/blast radius).
- `-auto-approve` in examples meant for humans (only in explicitly-CI contexts).
- Unpinned providers / `latest` module sources.

---

## After writing a chapter

1. Add the row to `docs/book/index.md` (Ch | Topic | Status ✅).
2. Append any new terms to `docs/reference/glossary.md`.
3. Flip the topic `⬜ → ✅` in `docs/learning-path.md` and update "You are currently here".
4. Confirm the chapter carries a `## 🧪 Lab` (B2 onward) with the start step + `tflocal` + "emulation ≠ AWS" warning, and that its References cite the emulator facts caches.
5. Build the site (`python -m zensical build` from the notes root) — expect "No issues found" before committing.
6. Report: what was blended, current chapter count, and the next topic in the path.
