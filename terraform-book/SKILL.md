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

1. **Nothing is used before it is explained.** A reader must never meet a term, an object, a command or a mechanism the chapter leans on before the chapter — or an earlier chapter — has named it. **This is a book, not a notebook.** Whatever a section takes for granted, something before it must have supplied. The failure this prevents: an opening poses a problem that silently assumes four things the chapter has not introduced, so the reader carries four unnamed objects until a later section rescues them.
   Every chapter states its exit contract up front as `## Learning outcomes` — 3–5 concrete, checkable abilities from the topic's milestone, written as things the reader *does*, not things they know about. That list is the one fixed opening; **the arc after it is chosen by topic — see [Chapter shapes](#chapter-shapes--choose-one-do-not-default).**
2. **Teach toward the learning-path milestone** — the chapter must make the topic's `Milestone` achievable.
3. **Current, runnable HCL** — code targets Terraform **1.15** / OpenTofu **1.12**; every block should actually apply.
4. **End pointing forward** — close with what this unlocks and which chapter comes next, as `**Next: Chapter N — Title.**`.
5. **Callouts are admonitions, never blockquotes** — see [Callout formatting](#callout-formatting-mandatory). A `>` blockquote for any note/definition/tip/warning/aside is a defect to fix on sight.
6. **Ship a 🧪 Lab (every chapter B2 onward)** — a hands-on section the reader can actually run, for free, against a local AWS emulator. See [Hands-on lab](#hands-on-lab-every-chapter-from-b2). Ch1 holds the one-time setup; every later chapter has a `## 🧪 Lab`.
7. **Never show a topic code (B4, I6, A3, …) in a chapter** — prose, tables, admonitions, Next lines, references. Codes are learning-path bookkeeping; a book reader navigates by chapter number. Write **"Chapter N"** using the arc table above (a "Covered in" cell listing two becomes `Chapters 13, 14`; a range becomes `Chapters 1–17`). The book's style is plain, unlinked "Chapter N" — link only when pointing at a section anchor (`[Chapter 1's lab setup](ch01-iac-fundamentals.md#lab-setup-a-free-local-aws-docker)`). Watch the article: "an A6 topic" becomes "a Chapter 23 topic". Not codes, and fine: Mermaid node ids (`A1["…"]`), hex bytes (`E9`), and other books' chapters ("TID's Chapter 5"). `docs/book/index.md` keeps its code column.

## Chapter shapes — choose one, do not default

**The arc is fit to the topic, and the topic decides.** Before writing, ask what actually brings a reader to this material and what they already hold. Then pick — or build — the shape that serves that. These are the common answers, not a menu you must pick from.

| Shape | Fits a topic where… | Arc |
| --- | --- | --- |
| **Problem-first** | the reader arrives already burned — something broke, was slow, or gave a wrong answer | the failure, felt and reproduced → why it happens → the mechanism → the fix |
| **Orientation-first** | the reader arrives with nothing built and no grievance | what the thing is, end to end at the terminal → each part in depth → the failure modes |
| **Mechanism-first** | the value is the idea itself, and applications follow from it | the model from first principles → what it buys → where Terraform implements it |
| **Surface-first** | the topic is a body of syntax or an API the reader must become fluent in | the shape of the construct → semantics and edge cases → where it goes wrong |
| **Decision-first** | the topic is a choice between options with real trade-offs | the decision and what rides on it → the axes → each option against them → how to pick |

Two corollaries:

- **A "The problem this solves" section is one option, never an obligation.** Write it when a reader genuinely arrives with that problem. Retrofitting a grievance onto an orientation topic invents a motivation the reader does not have, and costs a section.
- **Navigation is separate from motivation.** A long chapter (8+ sections) owes the reader a map of which section answers what. That map needs no problem to hang on — it can be a short lead-in, a table, or the tail of the opening section.

Section titles, ordering and depth are the chapter's own call. What every chapter owes is the invariant above: nothing used before it is explained.

## Toolkit (draw on what the topic needs — NOT a fixed template)

Learning outcomes (mandatory) · motivating problem (optional — see Chapter shapes) · core-concept prose · worked examples · Mermaid diagrams
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
- **Version-gate every source-derived claim.** The checkouts at `C:\opt\learn\terraform\repos\` track **`main`**, which is ahead of the release the book targets. Reading a behavior in `internal/` proves what `main` does, not what the current stable release does. Before that behavior goes into a chapter — and *especially* before "correcting" a reading note against it — find the release it shipped in:

    ```bash
    git log -S'<exact changed string>' --oneline -- <path>   # the commit
    git tag --contains <sha> | head -5                        # the first release
    ```

    If the first tag is a pre-release above the target version, the target-version behavior stays the chapter's main text and the newer behavior goes in an `!!! info "… in <version>"` box. A reading note only earns a 🔄 marker once the contradicting change is confirmed shipped at or below the target version. Ch3's cycle-error output was "corrected" the wrong way exactly this way: `dag.go` on `main` renders cycles vertically, but that commit lands only in `v1.16.0-alpha*`, so 1.15.7's comma-joined line was right all along.
- **Show the plan.** When behavior is non-obvious, include the relevant `terraform plan` output excerpt (`+`/`~`/`-/+`) so the reader can predict it.
- **Name the tool.** When Terraform and OpenTofu differ, say which; otherwise write tool-neutral (`terraform`/`tofu` are interchangeable for shared features).

## Measured claims (numbers the chapter asserts)

A number in a chapter is a claim, and a claim needs evidence a reader can re-run.

- **Commit the lab directory.** Every chapter's lab lives at `labs/chapter<NN>/` (`.tf` files, plus any
  runner script); state files are gitignored. If the directory is missing, the chapter's numbers cannot
  be checked and a later audit has to re-derive them from nothing. Ch9's serial numbers survived only
  because they were re-measured; the lab that produced them had never been committed.
- **Repeat before generalizing.** Never turn one observation into a rule. Run the configuration from
  scratch at least three times — destroy, delete state, re-apply — and write down every result.
  Ch9 shipped "a first apply lands at *resources + 1*" from a single run; four identical runs of one
  four-resource config later gave 1, 1, 1, 4, and the rule was simply false.
- **Publish the series, not the summary.** `5, 4, 4, 1, 5, 5` teaches what "unpredictable" means;
  an average hides it. If runs disagree, *that disagreement is the finding* — lead with it.
- **Give the reader the runner.** When the point is variability, ship a script that loops the
  measurement (see `labs/chapter9/lab2/measure-serial.ps1` / `.sh`) in both PowerShell and bash.
- **Measure OpenTofu, don't infer it.** Both CLIs are installed. Re-run the same lab under `tofu`
  before writing any "OpenTofu also/differs" sentence; for emulator labs use
  `TF_CMD=tofu tflocal <cmd>`, which tflocal honours. Divergences found this way (state write cadence,
  crash-window behaviour) are exactly the `!!! info "OpenTofu — ..."` boxes required by
  [[feedback_tid_opentofu_difference_notes]].
- **Probe in `labs/sandbox/`, not in a lab directory.** Exploratory runs leave state, a generated
  override, or an edited resource behind, and a committed lab is the archive a chapter's transcripts
  point at. `labs/sandbox.sh` (and `.ps1`) gives throwaway workspaces that are gitignored, run against
  the same emulator through `tf-docker`, and destroy before they delete:
  ```shell
  labs/sandbox.sh new lifecycle-probe        # workspace + a main.tf stub with the labs' provider pin
  labs/sandbox.sh run lifecycle-probe apply -auto-approve
  labs/sandbox.sh rm lifecycle-probe         # destroy, then delete
  ```
  `SANDBOX_RUNNER=tflocal` runs on the host instead of in the container. Details in
  `labs/sandbox/README.md`.
- **Capture the final transcript from the committed directory, never from a scratch copy.** Error and
  plan output carries file names and positions — `on main.tf line 17`, `still declared at main.tf:9,1`.
  A transcript captured in a throwaway `both.tf`, or in a file without the comment header the committed
  one carries, prints coordinates the reader will never see, and the mismatch survives review because
  every other character matches. Ch16 §4 shipped two of these and both had to be recaptured after the
  lab README was written. Probe in the sandbox; re-run once in the directory that ships, and quote
  that run.
- **A measured table is a walkthrough, not just a result.** When a table or transcript comes from a lab,
  the section itself carries the configuration, the commands in order, and the cleanup, so a reader can
  reproduce it without opening the repository. The lab directory is the archive; the section is the
  instructions. Naming the directory is not enough on its own. The shape, as real fenced blocks and not
  a description of them:

  ~~~markdown
  This one is worth running rather than reading, and the configuration is committed at
  `labs/chapter16/section3/bare-address/`. Two instances of one resource, which is all it takes:

  ```hcl
  resource "aws_s3_bucket" "shard" {
    for_each = toset(["a", "b"])
    bucket   = "ch16-parsers-${each.key}"
  }
  ```

  ```shell
  tflocal apply -auto-approve            # two buckets, two instance keys in state
  ```

  Now hand the same bare `aws_s3_bucket.shard` to each operation in turn:

  ```shell
  terraform state list aws_s3_bucket.shard            # both instances
  terraform state show aws_s3_bucket.shard            # error
  tflocal plan -destroy -target aws_s3_bucket.shard   # a plan, not an apply
  terraform state rm aws_s3_bucket.shard              # both, no prompt
  ```

  Measured on **v1.15.8**:

  | … the table the commands produce … |
  ~~~

  Three things that block carries and prose alone would not: an `hcl` fence with the exact
  configuration, a `shell` fence per stage with an inline comment saying what each command answers,
  and flags in the **space form** (`-target ADDR`), because PowerShell splits an unquoted
  `-flag=value`. Ch16 §3 and Ch1's setup are the worked models. If the last step leaves objects
  nothing tracks, the cleanup follows in a `!!! warning`, since `destroy` will not do it.
- **When a measured claim is falsified, sweep every copy.** A number that reached a chapter has usually
  also reached `docs/reference/glossary.md`, the source reading note under `docs/sources/` or
  `docs/books/`, and the chapter's entry in `docs/learning-path.md`. Grep the distinctive phrase before
  calling the correction done.

## Sourced claims (things the chapter asserts about other people's projects)

Measured claims get evidence you re-run. Claims about an upstream tool get evidence you *read*, and
they fail differently.

- **Never assert a cause.** "Tool X can't do Y because it depends on Z" is the shape that gets through,
  because the observable half checks out and the causal half rides along unexamined. A search snippet
  said terraform-docs is stuck on OpenTofu because it parses with HashiCorp's `terraform-config-inspect`;
  its `go.mod` requires the project's **own fork**. Write only what is observable — issue open, PR
  closed unmerged, dependency pinned here — and stop. No maintainer statement means no cause to write,
  and a replacement guess is not an improvement.
- **Verify the claim, not its neighbour.** "`test.go` exists at tag v1.6.0" does not establish
  "`tofu test` shipped in 1.6.0" — the file was inherited from Terraform's history. The command
  registration (`cmd/tofu/commands.go`) plus the CHANGELOG entry does establish it. Ask what would make
  the claim false, then look for that.
- **Prefer the repo over the docs over a blog, and read the manifest.** `go.mod`, `CHANGELOG.md`, and
  `git tag --contains <sha>` settle most tooling questions outright; see
  [[feedback_version_gate_source_claims]] and [[feedback_prefer_official_docs]].
- **A version printed in a book is a snapshot, not a fact.** Check every pinned version in a chapter
  against the project's own releases API before repeating it, and record the result in
  `docs/research-cache/` so the next chapter does not re-fetch it.
- **Confirm a cited URL resolves.** Books ship dead links (TID Ch7 cites `www.cookiecutter.io`, which
  does not resolve). Fetch before repeating, and log the dead one as a book defect.

## Citing issues and PRs

- **Markdown:** always a real link — `[#1738](https://github.com/opentofu/opentofu/pull/1738)`. A bare
  `#1738` is not autolinked inside a repository file and renders as plain text on the site, so it is a
  number the reader cannot follow.
- **Commit messages:** use `owner/repo#1738`. GitHub *does* autolink here, against the repo being
  viewed, so a bare `#845` links into this repo's own empty tracker.
- **Confirm the owning repo first** — a squashed merge commit carries its PR number as a `(#NNNN)`
  suffix, so `git log -1 --format=%s <sha>` in the local checkout settles it. Guessing swaps an
  unfollowable number for a link to the wrong project.
- `python scripts/check_markdown.py --commits origin/master..HEAD` enforces both, plus the
  admonition-title escape rule from [[feedback_no_escaped_quotes_in_admonition_titles]].

## Self-containment (a chapter must stand alone)

- **Name the page you are quoting.** "the docs say" is a defect. Write the page title, link it, and give
  the section when the page is long: *HashiCorp's [Purpose of Terraform State](...) page, under*
  Mapping to the Real World. Quote the whole sentence that carries the claim, not a four-word fragment.
- **Define a term the first time the chapter leans on it**, even when a later chapter owns the topic —
  `backend`, `snapshot`, `edge`. One or two sentences plus a forward reference, not a deferral.
- **A callout must state its own claim.** If the title asserts a rule ("The rule is an invariant"), the
  body says what the rule *is*, rather than referring to "this rule".

## Hands-on lab (every chapter from B2)

Every chapter from **B2 onward** ends with a `## 🧪 Lab` section (placed **before "Common pitfalls"**) that runs the chapter's concept for real against a **local AWS emulator** — free, no AWS account, no cloud credentials.

!!! warning "The Lab reinforces; it does not introduce"
    **Teach every concept at the keyboard where it is introduced.** Inline hands-on comes first: the moment the chapter explains a mechanism, show the command that makes it visible and the output it produces, right there in the body. Keep those inline pieces small — one command, its real output, one sentence on what to notice — and say which line matters rather than leaving the reader to guess.

    The `🧪 Lab` then has a different job: the reader has already run each command once, so the lab makes them **combine, vary, break and diagnose**. Include at least one step where something fails and they work out why. **A lab that is the reader's first contact with the chapter's commands is a defect** — move that material inline and rebuild the lab on top of it.

This is the book's practice surface; keep it in every chapter where the topic can be exercised in HCL.

**The environment** (set up once in Ch1, `#lab-setup-a-free-local-aws-docker`):
- A Docker AWS emulator on gateway port **4566**. Committed compose file: `labs/docker-compose.yml`.
- **Default emulator: Floci** (`floci/floci`, MIT, no token, serves the LocalStack API). Alternatives: **MiniStack** (`ministackorg/ministack`), **LocalStack** (needs a free token since March 2026). All three are interchangeable on `:4566`.
- Facts caches (re-check before writing, per [[feedback_ground_book_chapters_in_notes]]): `docs/research-cache/floci-facts.md`, `ministack-facts.md`, `localstack-facts.md`. Convention memory: [[project_localstack_labs]].
- A throwaway workspace for probing behaviour before it becomes a lab: `labs/sandbox.sh` / `.ps1`, documented in `labs/sandbox/README.md` and memory [[project_terraform_lab_sandbox]]. Gitignored, so nothing probed there can reach a commit.

**Lab section rules:**
- **Open with a start step** (reused verbatim every chapter):
  ```shell
  docker compose -f labs/docker-compose.yml up -d      # start the emulator on :4566
  curl -s http://localhost:4566/_floci/health          # wait until the services read "running"
  ```
  Floci's **native** path is `/_floci/health` and every chapter uses it. It also serves
  `/_localstack/health` as a byte-identical alias, mentioned once in Ch1 because it is what makes
  the MiniStack/LocalStack images drop-in swaps. Service status reads `running`, never "available".
- **Run Terraform via `tflocal`** (`tflocal init/plan/apply/destroy`) — it targets `:4566`, drives any of the three emulators, and leaves `.tf` files portable to real AWS. Never hard-wire an `endpoints{}` block into the main example (show it only as an aside, alongside the `AWS_ENDPOINT_URL` alternative).
- **Emulator-neutral prose** — say "the emulator", not "LocalStack". Name Floci/MiniStack/LocalStack only when listing options.
- **Reliable free surface only: S3, DynamoDB, SQS, SNS, IAM, STS.** EC2 is *mocked* — do not apply EC2/AMI examples; swap for an S3 bucket and say why in a `!!! note`.
- **Always include the "emulation ≠ AWS" `!!! warning`** — a green apply proves HCL/workflow, not AWS-fidelity; validate load-bearing configs on real free-tier AWS.
- **Verify results** with `awslocal ...` and/or `terraform state list` / `terraform output`; then `tflocal destroy`.
- **Failing configurations are legitimate lab content.** A directory whose whole purpose is
  `Error: Moved object still exists` earns its place next to the ones that apply. Say in its README
  which directories never reach an apply, so nobody waits for an emulator they do not need.
- **A lab that is the end of an edit must ship its starting file.** When the committed `.tf` is the
  *after* state — a renamed label, a block added, a `count` swapped for `for_each` — the README gives
  the exact **before** file, not a prose description of it. Otherwise the reader has to reverse-engineer
  the starting point from a comment, which is what `labs/chapter16/section4` looked like before it got
  a README.
- **Cleanup instructions must match what the lab actually did.** A lab ending in `state rm` or a
  `removed` block leaves live objects nothing tracks, so `tflocal destroy` is a no-op and the objects
  survive. Give the `awslocal` deletion, or the re-import path, and say which step is the point of no
  return. Every lab group with more than one directory gets its own README doing this per directory.
- Add the facts-cache links to the chapter's **References** (`🧪 Lab: [Floci Facts](...) · [MiniStack Facts](...) · [LocalStack Facts](...)`).

## Callout formatting (mandatory)

**Every callout is a MkDocs admonition (`!!! type "Title"`) — never a `>` blockquote.** Blockquotes are reserved for the chapter-header front-matter block (source citation + summary + see-also) only. Any note, definition, aside, tip, warning, version-gate, or "(mine)" observation in the chapter body MUST be an admonition. Content indents 4 spaces under the `!!!` line; never indent a callout inside a list item.

**Never escape a quote as `\"` inside the title string** — Zensical renders it as a literal backslash (`\"nines\"` shows on the page). Use curly quotes for a quoted phrase in a title: `!!! note "Measured in “nines”"`. Sweep after editing — `grep -rnE '^\s*(!!!|\?\?\?|===)\s+.*\\"' docs --include='*.md'` must be empty. See [[feedback_no_escaped_quotes_in_admonition_titles]].

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

## Current versions (verified 2026-07-20 — see docs/research-cache/version-facts.md)

| Tool | Version | License |
|------|---------|---------|
| Terraform CLI | 1.15.8 | BSL 1.1 |
| OpenTofu | 1.12.4 | MPL 2.0 |

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
5. **Commit `labs/chapter<NN>/`** — the configuration that produced every command output and number in the chapter, so the claims stay checkable. Then re-read the chapter's measured tables and transcripts against it: each one names its directory, carries the commands that reproduce it, and any multi-directory group has a README giving each directory's starting file, its expected output, and a cleanup that matches what it did. Delete the state files first (`terraform.tfstate*` are gitignored, `tfplan` and `*.log` too); `destroy` before you leave so the emulator is clean for the next chapter. Clear the probes too — `labs/sandbox.sh list` should come back empty, and `labs/sandbox.sh rm --all` gets it there.
6. Build the site (`python -m zensical build` from the notes root) — expect "No issues found" before committing.
7. Report: what was blended, current chapter count, and the next topic in the path.
