---
name: spark-source-map
description: >
  Use when mining the Apache Spark source to drive the personal Spark book at
  C:\opt\learn\spark\notes. Triggers on: "generate the config catalog", "refresh
  the spark configs", "trace B7", "trace the joins topic", "sweep core", "sweep
  sql/catalyst", "map the joins code paths", "what configs relate to <topic>",
  "update the source coverage matrix", "regroup core", "add a group for X",
  "what isn't covered by any group", "check the carving", "groups.yaml is
  stale", "Spark 4.3 is out", "bump the source map to the new Spark", or any
  request to build/refresh the source-derived config catalog, per-topic traces,
  source sweeps, the group carving in groups.yaml, or the topic-coverage matrix
  under docs/reference/spark-source-map/. Also fires when a Spark release lands
  and the map must be re-verified against it, or on "refresh the anchors". Three
  engines: a deterministic Python config parser (whole repo), a topic-first LLM
  tracer (one learning-path topic at a time), and a source-first LLM sweeper that
  discovers topics and features to learn from the code itself — independently of
  the book and of the learning path, which it then extends. Plus checker-driven
  maintenance of the hand-authored groups.yaml and mechanical re-resolution of
  file:line anchors. Spark source is at C:\opt\learn\spark\repos\spark.
---

# Spark Source Map — Skill

Hybrid pipeline for mining Apache Spark source to drive the spark-book.

> **The learning path is `docs/learning-path-v2.md`** — 185 topics, `####` headings, one
> 🎯 checkpoint closing each level. `docs/learning-path.md` is v1: deprecated, frozen, and
> never read or written by this skill or by `gen_coverage.py`. v1 codes mean different
> topics than v2 codes; the crosswalk is at the end of v2. Most v2 topics have **no trace
> page** — the traces were written against v1 codes, so the coverage matrix showing them
> untraced is accurate, not a bug.

- **Topic traces** (`trace <topic-code>`) — start from a learning-path topic, find the backing source, configs, and code paths. Topic pages live at `docs/reference/spark-source-map/topics/<code>.md`.
- **Source sweeps** (`sweep <subsystem>`) — scan a subsystem for concepts, **whether or not any topic covers them**. Sweep pages live at `docs/reference/spark-source-map/sweeps/<slug>.md`. Concepts no topic covers become `propose:` blocks, auto-appended to `learning-path-v2.md`.
- **Config catalog** (`gen configs`) — deterministic whole-repo config parser. Used as a lookup by both engines.

## What this skill is for — read before judging its output

**The sweeper discovers topics and features to learn independently of the book and of the
learning path.** That is the whole point of the source-first engine, and it has three
consequences that look like problems if you assume the opposite:

- **The learning path is an *output* of sweeping, not a constraint on it.** A sweep does not ask
  "what does the book need next" — it asks "what is in this code". Concepts that map to no topic
  are the product, not an anomaly. A run that finds none has probably swept too shallowly.
- **Sweeps legitimately grow the path, and do so without asking.** Filling in a `propose:` block
  and appending the topic *is the job*. It is not curriculum drift, and it is not the
  ask-condition about taxonomy (see the autonomy contract) — that condition governs *retitling,
  renumbering and reordering* the topics a human chose, not adding what the source turned up.
  Expect a healthy fraction of the path to be source-derived over time.
- **Sweep order is not driven by what chapter comes next.** Order by discovery yield — dense,
  unexplored subsystems first. A subsystem whose concepts back no written chapter is a perfectly
  good sweep; the chapter may not exist *because* nobody has mapped that code yet.

What the skill does **not** own: writing or updating the spark-book. A trace's "Not in spark-book"
list and a sweep's new topics are handed off to the `spark-book` and `book-gap-filler` skills.
Discovering and documenting is where this skill's job ends.

---

- Design spec: `C:\opt\learn\spark\notes\docs\superpowers\specs\2026-06-06-spark-source-map-design.md`
- Spark source: `C:\opt\learn\spark\repos\spark` (verify Spark facts here, not the web)
- Artifacts: `C:\opt\learn\spark\notes\docs\reference\spark-source-map\`
  - `groups.yaml` — **directly under that directory**, not under `configs/`. It is the only
    hand-authored file there; `configs/catalog.yaml`, `configs/index.md` and `index.md` are all
    generated.
- Tools: `C:\opt\learn\spark\notes\tools\spark_source_map\`
- Requires: `python`, `pyyaml` (`pip install pyyaml`); tests need `pytest`.
- **Windows console:** every tool here prints em dashes and arrows, which cp1252 cannot encode,
  and so does any ad-hoc `python -c` that dumps `groups.yaml`. Prefix with `PYTHONIOENCODING=utf-8`
  or the run dies on a `UnicodeEncodeError` that has nothing to do with the data.
- **Windows file writes — the same hazard, but silent.** A page written through a cp1252 round trip
  stores mojibake instead of dying: every `→` becomes `â†’`, every `—` becomes `â€”`. Nothing
  fails, no checker looks at encoding, and the damage reaches concept names and headings, so it
  propagates into the generated `index.md` too. Two sweep pages carried 362 such sequences
  undetected for three days. Always write with an explicit `encoding='utf-8'`, and after writing a
  page, grep it for `â€` and `â†` before committing:

  ```bash
  grep -c 'â€\|â†' docs/reference/spark-source-map/sweeps/*.md
  ```

  Repair is a literal replacement — `â†’`→`→`, `â€”`→`—`, `â€¦`→`…`, `â€“`→`–`, `â‰¥`→`≥`,
  `â‡’`→`⇒`, `Ã—`→`×` — then re-run `gen_coverage.py` to clean the index.

> **Version caveat (check every run):** the checkout is on `v4.2.0` and the catalog was
> parsed from it (`meta.spark_version: 4.2.0`, 1558 configs, 2026-07-19). The checkout may
> drift to `master` (`spark_version: 5.0.0-SNAPSHOT`); to pin a release,
> `git -C C:\opt\learn\spark\repos\spark checkout v4.2.0` before `gen configs`.
> The catalog `meta.spark_version` always records what was actually parsed — trust it over
> this line, and over the config counts anywhere else.

## Autonomy contract

A verb is a whole job, not a step. Run it to completion: every command, every checker fixed to
green, every document the change invalidated updated, committed. The user asked for the outcome,
not a plan.

**Ask only when one of these is true.** Each is observable — check it, don't estimate your
confidence:

1. **The change *rearranges* the learning path's taxonomy** — retitling, renumbering, reordering,
   merging or deleting topics the user already has. That structure is the user's curriculum.

   **Adding a topic the source turned up is not this condition.** Source-first discovery exists to
   grow the path, so a sweep's `propose:` block goes in without asking: fill in `what` / `why`, the
   resources and a real milestone, and append it. If you find yourself about to ask "should this
   become a topic?", the answer the skill has already given is yes — write it well instead. The
   only thing to bring back is a proposal that would *displace* something (a new topic that
   supersedes an existing one, or that only makes sense if two current topics merge).
2. **Two options are defensible and the source cannot decide between them** — which group owns
   a package, whether a package is plumbing or worth a group, which of several topics a concept
   backs. Bring the options with file counts and a recommendation.
3. **A fix requires inventing a fact** — a checker names a class that exists nowhere in the
   checkout, a config has no discoverable default, a trace cannot follow a path. Say what you
   could not verify rather than writing a plausible guess.
4. **The action reaches outside the repo or is hard to undo** — push, force-push, deleting a page
   with content in it, rewriting history, touching anything outside `C:\opt\learn\spark`.

**Proceed without asking in every other case.** Specifically, these are not doubt:

- The next command in the verb is determined → run it.
- A checker named a specific fix (`add the module to `modules:``, `fix the name`) → apply it.
- A doc, table or nav entry now disagrees with the change → sync it.
- The commit is repo-local and inside the verb's scope → commit it.
- You are unsure whether the user wants the *whole* verb → they asked for the verb; do all of it.

**Report, don't ask, when something surprised you.** A wrong scope, a false positive in your own
check, a regression you caused — fix it, then say plainly what it was in the summary. Discovering
you were wrong is not a reason to stop and ask; it is a reason to correct and disclose.

Two failure modes to avoid, both of which read as helpful:

- **Handing back a checklist.** "Here are the commands to run" is a half-done verb. Run them.
- **Asking to confirm the obvious.** "Shall I regenerate index.md?" — the verb says to. Do it.

## The verbs

Each verb is a whole job, not a step — see the autonomy contract above. The two cheap,
deterministic ones are documented here; the three that need judgement live in reference files,
**which you must read before running that verb.**

| Verb | What it does | Where it is documented |
|---|---|---|
| `gen configs` | Deterministic whole-repo config parser + drift checks | below |
| `coverage` | Regenerate the landing page and matrix | below |
| `refresh anchors` | Re-resolve `file:line` anchors against a newer Spark | below |
| `trace <topic-code>` | Topic-first: one learning-path topic, its source, configs, code paths | `references/trace.md` |
| `sweep <subsystem> [<group>]` | Source-first: one group, discovering concepts and new topics | `references/sweep.md` |
| `regroup <subsystem>` | Recarve `groups.yaml`, checker-verified | `references/maintenance.md` |
| `new spark release <ver>` | Move the whole map to a new Spark | `references/maintenance.md` |

Read the reference file in full before starting — the page contracts and the subagent briefs live
there with the verb, and a page written without its contract will not feed the generators.

### `gen configs` — refresh the whole-repo config catalog (deterministic, cheap)

1. Run from the notes repo root:
   ```
   python tools/spark_source_map/gen_configs.py \
     --source C:/opt/learn/spark/repos/spark \
     --out-dir docs/reference/spark-source-map/configs
   ```
2. Read the printed summary: `spark <version>: <N> configs, <U> unparsed`.
   - **Floor check:** N should be > 1000. A sharp drop means a parser regression — run
     `python -m pytest tools/spark_source_map/test_gen_configs.py` and fix before committing.
   - If `U > ~5`, open `catalog.yaml` `unparsed:` and check they are genuinely hard
     (nested string interpolation, indirect constant refs). Never hand-edit `catalog.yaml`.
3. **Check for drift** — a new Spark release is the moment hand-authored scopes go stale:
   ```
   python tools/spark_source_map/check_drift.py
   ```
   Exits 1 and names the offenders. It verifies `groups.yaml`'s `_meta.spark_version` against
   the catalog, that every subsystem is a real module, and that every class and package named
   in a group `scope` still exists **inside that group's modules**. When a class has moved
   modules (Spark 4.x did this repeatedly — `StorageLevel` → `common/utils`, `DataType` →
   `sql/api`), either add the owning module to that group's `modules:` list or fix the name;
   then bump `_meta.spark_version` / `_meta.verified_at`. Warnings about sweep/topic pages
   recorded against an older Spark are advisory — they flag anchor drift, not a blocker.

   Then run the inverse check — what exists that no scope names:
   ```
   python tools/spark_source_map/check_drift.py --coverage
   ```
   **Reconcile whatever it lists; do not just report the count.** A package no group claims can
   never be swept, so its concepts can never surface as proposals — the gap conceals itself, and
   leaving it listed defers the same decision to every future run. It prints only packages *not
   yet judged*, so the list is normally empty and any entry is new code since the last refresh.

   For each listed package, open it and decide:
   - **Belongs to an existing group** → extend that group's `scope`. This is the common case and
     it is mechanical: do it, don't ask. Name a class rather than a path when the path would be
     too coarse — a scope token becomes a path *segment*, so `unsafe/map/` also claims every
     `.../util/collection/unsafe/`, silently suppressing an unrelated package.
   - **Plumbing** (helpers, shims, test scaffolding, generated error definitions) → add
     `<subsystem>:<package>` to `_meta.plumbing` with a one-line reason, so it is never raised
     again. Judge it by looking, not by the name.
   - **A real concept with no home** → that is ask-condition 2. Bring it with a file count and a
     recommendation; a new group may imply a new learning-path topic, which is the user's call.

   The same report flags **two groups claiming the identical package path** — both sweeps
   would walk the same code. Parent/child is fine and is not flagged (`execution/` vs
   `execution/joins/`). When the sharing is deliberate, set `shared_scope: true` on each
   group involved; `resource-managers/kubernetes` splits `k8s/` by theme this way.
   Finally, check the sweep pages against the scopes you just verified:
   ```
   python tools/spark_source_map/check_drift.py --sweeps
   ```
   Fails when a page claiming `status: complete` cites no file from a package its group's scope
   claims. On a scope edit this catches both directions: a scope that grew past what its sweep
   covered, and a package claimed by the wrong group (`deploy/security/` was claimed by
   `submit-standalone` but swept by `config-security`). It also lists topic traces overlapping
   each sweep's topic codes, flagging any recorded against an older Spark.
4. Run `coverage` (below) so the sweep-status table picks up new config counts.
5. Wire `configs/index.md` into `zensical.toml` nav if not already present; commit.

This regenerates `configs/catalog.yaml` (source of truth) and `configs/index.md` (rendered,
grouped by subsystem → prefix, GitHub-linked). Re-runnable per Spark version in seconds.

---

### `coverage` — regenerate the landing page + matrix (deterministic, cheap)

```
python tools/spark_source_map/gen_coverage.py
```

Rebuilds `docs/reference/spark-source-map/index.md` from:
- `learning-path-v2.md` (the 40 topics)
- `spark-book/index.md` (topic → chapter mapping)
- `configs/catalog.yaml` (subsystem config counts)
- `topics/*.md` (topic-first traces — drives coverage matrix)
- `sweeps/*.md` (source-first sweeps — drives gap discovery and sweep-status table)

Also auto-appends `propose:` blocks from sweep gaps to `learning-path-v2.md` (pass
`--no-write-proposals` to skip). Run after any trace, sweep, or `gen configs`, or whenever
the learning path changes. Never hand-edit `index.md`.

---

### `refresh anchors` — re-resolve file:line anchors after a release (mechanical)

Every anchor on a topic or sweep page is a GitHub blob URL pinned to a tag *and a line number*.
Line numbers drift heavily between releases and a stale anchor still renders perfectly on GitHub
while pointing at the wrong code, so bumping the tag by hand is worse than doing nothing. Against
the current corpus (1314 anchors, 32 pages) a two-release move relocates about **40%** of them —
far too many to re-resolve by hand, which is how a release runbook stalls.

```
python tools/spark_source_map/refresh_anchors.py                    # dry run, every page
python tools/spark_source_map/refresh_anchors.py --to v4.3.0
python tools/spark_source_map/refresh_anchors.py --page topics/b7.md --apply
```

It reads each anchor's line *as it was at the version the page records*, finds that same line in
the target version (exact content match, falling back to the nearest enclosing declaration plus an
offset), and rewrites the URL, the `#L`, and every `:N` in the visible label. Unresolvable anchors
are reported and left untouched, and a page with any unresolved anchor keeps its old
`spark_version` so it stays flagged. Pages with `version_pinned` are skipped.

**This does the mechanical half only.** A resolved anchor points at the same *line of source*; it
says nothing about whether the prose around it is still true. Read the diff, and re-verify content
wherever the target moved a long way or resolved "via declaration". The re-tracing rule in
`references/maintenance.md` still applies — this just removes the line-number bookkeeping from it.

## Conventions (project memory)

- Blank line before every bullet list (Zensical won't render otherwise).
- Mermaid for diagrams, never ASCII art.
- **Callouts are admonitions.** Use `!!! note` / `!!! warning` / `!!! info` (with a quoted title and
  a 4-space-indented body) for every note, caveat, or aside — in topic pages, sweep pages, chapters,
  and the learning path alike. Pick the type by what the reader must do: `warning` for something
  that will bite them, `info` for a naming or behaviour clarification, `note` for additive context.
  - Admonitions render correctly **anywhere**, including directly after a bullet or numbered list.
    An earlier version of this file claimed otherwise; that was a misdiagnosis of a missing
    `admonition` markdown extension in `zensical.toml`, fixed 2026-07-18. If an `!!!` block ever
    renders as literal text again, check the extension is still enabled before rewriting content.
  - Chapter *metadata* headers (`> *Learning-path topic: …*`) stay blockquotes; they are a header
    block, not a callout.
- Every new **page** must be added to `zensical.toml` nav. Data files (`catalog.yaml`) and
  `.gitkeep` are not pages — leave them out of nav.
- Verify all Spark facts against the **local source**, not the web.
- Never hand-edit generated files (`catalog.yaml`, `configs/index.md`, `index.md`) — re-run
  the generator. Topic and sweep pages are authored; their front matter feeds `gen_coverage.py`.
- **`groups.yaml` is hand-authored**, despite sitting beside two generated files. No tool writes
  it — `gen_configs.py` and `gen_coverage.py` only read it. Editing it directly is the *only* way
  to change it, and no generator run will notice when its scopes drift from the source. Its
  `_meta.spark_version` / `verified_at` record when the scopes were last walked against a
  checkout; re-verify and bump them whenever you re-point the catalog at a new Spark release,
  since nothing else will catch a stale scope. Group `scope` fields are package *hints* for a
  human or a sweeper subagent — not resolvable paths, so a literal path check will throw false
  positives.

## Tests and checks

```
python -m pytest tools/spark_source_map/
```

`test_gen_configs.py` covers the config parser (type/default/version/doc extraction, constant-key
resolution, dynamic-key flagging) plus a real-source floor assertion (`entry_count > 1000`, known
configs present). `test_gen_coverage.py` covers the learning-path proposal writer: ascending code
order regardless of the order concepts are declared in, placement under the right level heading,
never reusing an existing topic's code, and idempotence on a repeated run.
`test_refresh_anchors.py` covers anchor re-resolution: exact-content matching across insertions,
the enclosing-declaration fallback, ambiguity handling, label rewriting, and the link regex.
`test_check_drift.py` covers two halves of `--sweeps`: the config-coverage half (family threshold,
partly-cited case, subsystem-scoped `_meta.config_plumbing`) and the named-class half, which drives
`report_sweeps()` against a miniature checkout built in `tmp_path` — a named class cited, a named
class uncited, a capitalised prose word that resolves to no source, a class reached through the
group's `modules:` list, and a `status: partial` page going unchecked. Run them after any change to
the corresponding tool.

The read-only checks, and what each one can actually catch:

| Command | Catches | Fails the run? |
|---|---|---|
| `check_drift.py` | a scope naming a class or package that no longer exists in its modules; a stale `_meta.spark_version`; pages recorded against an older Spark (warning) | yes, on scope errors |
| `check_drift.py --coverage` | packages no group claims — code that can never be swept | no, editorial |
| `check_drift.py --sweeps` | a `status: complete` page that cites nothing from a package its own scope claims; a `status: complete` page that never cites a **class its own scope names**; a whole config family cited by no page of a fully-swept subsystem; topic traces overlapping a sweep at a different Spark version | yes, on any uncited claim |

None of them checks whether a sweep page's *prose* is true — that is what verifying every anchor
against the local checkout is for.

**The cheapest re-sweep trigger is the per-package ratio `--sweeps` already prints.** For each
`status: complete` page it lists `<package>  N files  M cited  (P%)`. The check itself only *fails*
on a package cited zero times, so those percentages pass silently — but they are the one number in
the whole toolchain that reliably separates a swept group from a re-declared one. Read them on
every run:

```
python tools/spark_source_map/check_drift.py --sweeps
```

Treat **anything under ~50% on a `status: complete` page as a re-sweep candidate**, and confirm by
hand before acting: the printed totals include sub-package files and `package-info.java`, so they
are a screening signal, not the number to quote. `core — execution-engine` sat at `executor/` 21%,
`internal/io/` 33%, `scheduler/` 28% while passing every check, and the re-sweep it triggered
(2026-08-09) added eleven concepts and two topics.

**A class named in a group's `scope` is not evidence the sweep opened it** — but `--sweeps` now
checks it. Check 3 only verifies that a named class still *exists* in the module; `SparkHadoopWriter`
was named in `core — execution-engine`'s scope for two weeks, appeared on no page of a
`status: complete` sweep, and every check passed until a file-by-file diff found it (2026-08-09).
`--sweeps` now prints `scope names N class(es)  M cited` per page and **fails** any uncited one,
because a scope names a class exactly when the package is too coarse — and the package check is
satisfied by any one file from the same directory, so it structurally cannot see this miss.

Three things it deliberately does not do, so a green line is not over-read:

- **Only classes that resolve to real source are demanded.** Scope prose carries capitalised words
  that are not classes; an unresolvable name is check 3's error, not this one, and is reported as
  `(N unresolved — see check 3)` rather than failed twice.
- **The whole page counts, breadth-check tables included.** A page that lists the class as knowingly
  uncovered passes — it has at least seen it. Whether the prose does it justice is not mechanical.
- **Prefixes do not count.** `BlockManagerMasterEndpoint` does not satisfy a demand for
  `BlockManagerMaster`; they are different classes in different files. That distinction is what
  flagged `core — storage-serializer` on the first real run.

**Counting cited files: read the concept body only.** A naive grep for `*.scala` over the whole
page counts the filenames listed in breadth check 2's own *uncited* table, and every filename in
the sweep log, as citations — which inflates the number precisely on the pages that were honest
about their gaps. Split on the first `## Breadth check 1` and count against what precedes it.

**What `--coverage` structurally cannot catch: a nested package inside a claimed one.** It walks
only the *top-level* packages under each source root (`root.iterdir()`), so once a scope token
claims `internal/`, everything beneath it — `internal/config/`, `internal/io/`, `internal/plugin/` —
is invisible to the check whether or not any of it was ever swept. `--sweeps` does not catch it
either: that check is satisfied as soon as the page cites *something* from `internal/`. The two are
therefore both green on a group that swept one sub-package out of three, which is exactly how
`internal/io/` (the whole Hadoop commit protocol, 6 files) sat unswept and unreported until
2026-07-25. Two consequences:

- **Walk sub-packages by hand** when sweeping a group whose scope names a package that has any.
  `ls -R` the scope's directories and compare against what the page cites; do not trust a green
  `--coverage`.
- A scope token is a path *segment*, so narrowing `internal/` to `internal/config/` documents the
  intent but changes nothing mechanically — the package key is still `internal`. Fixing the blind
  spot properly means teaching `--coverage` to recurse, which would surface new packages across
  every subsystem at once and is its own job.
