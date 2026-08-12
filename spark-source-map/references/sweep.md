# Source sweeps — the `sweep` verb

> Reference for the `spark-source-map` skill. Load it when running a `sweep <subsystem> [<group>]`.
> Read `SKILL.md` first — it holds the design intent and the autonomy contract that govern
> everything here.

### `sweep <subsystem> [<group>]` — source-first discovery sweep (LLM, on-demand)

Scan a subsystem for major concepts and identify which have no learning-path topic. **One group
per run** — this expands the learning path with things you didn't know to include.

Both invocations are valid:

- `sweep core execution-engine` — sweep that group directly.
- `sweep core` — no group named; run the scope check in step 2 and ask the user to pick one.

To see what groups a subsystem has, and which are already done:

```
python tools/spark_source_map/gen_coverage.py --list-groups <subsystem>
```

Prints each group's topics, scope, swept status, Spark version, and page filename; omit the
subsystem for all of them. Read-only. Use it in pre-flight rather than reading `groups.yaml`
by hand — it is the only view that also shows what has already been swept.

**The subsystem and group list is not copied here.** `groups.yaml` is hand-authored and gains
groups whenever someone regroups a subsystem, so any table in this file starts rotting the day it
is written — which is what happened to the sweep-status line that used to sit below. Get the live
list, with each group's scope and whether it has already been swept:

```
python tools/spark_source_map/gen_coverage.py --list-groups <subsystem>
python tools/spark_source_map/gen_coverage.py --list-groups          # all of them
```

**Config counts live only in `index.md`.** Its sweep-status table is generated from `catalog.yaml`
on every `coverage` run, so it is always right. Read counts there.

`sql/core` and `sql/pipelines` register no configs of their own — nearly every SQL config is
declared in catalyst's `SQLConf.scala` — but they hold the physical execution behind most of what
Spark actually does, so they are dense in undiscovered concepts.

!!! warning "Structured Streaming is not in the `streaming` subsystem"

    The `streaming` module is DStream only. Structured Streaming executes in `sql/core`
    (`execution/streaming/runtime/`) and is covered by the `sql/core — streaming-exec` group.

**Order by discovery yield, not by what the book needs next.** Take the densest unexplored
subsystems first — `sql/catalyst` and `sql/core` lead on config density and on concept count per
file. A group whose concepts back no written chapter is still a good sweep: the chapter may be
missing precisely because nobody has mapped that code. One group per run.

**What has already been swept is not recorded here** — the same reason the config counts aren't.
A copy in this file is a second number to maintain and rots at the next sweep, which is exactly
what happened to the line that used to sit here. Run `gen_coverage.py --list-groups <subsystem>`
for the live answer, or read the sweep-status table in `index.md`.

### Re-sweeping a group that already says `status: complete`

`sweep <subsystem> <group>` on a group already marked complete **at the same Spark version** is a
legitimate and productive run, not a no-op. `status: complete` means the last pass believed it had
covered the scope; it is not evidence that it had. Do not decline the verb because the listing says
complete — run the two breadth checks above and let them decide whether there is work.

**Screen for candidates with the per-package ratios `check_drift.py --sweeps` prints** (see the
checks section in `SKILL.md`). Under ~50% cited on a `status: complete` page means the page is
almost certainly a re-declaration; that is the whole pre-flight.

Evidence from re-sweeping all nine `core` groups at an unchanged 4.2.0 (2026-07-25): **every one of
the eight attempted found new concepts**, 30 in total, and three of them justified new
learning-path topics (E17 output commit coordination, A20 map output sizes, I19 sampling). Two
groups had a whole layer missing — `BlockTransferService` and the Hadoop commit protocol — on pages
that both checkers passed.

Evidence from the second re-sweep of `core — execution-engine` (2026-08-09), the group that batch
had *already* re-swept: still only **24 of 88 in-scope files cited**. Eleven concepts and two topics
(E49, E50) came out of it, including the entire per-task metrics layer, the `Task`/`TaskDescription`
pair, and `SparkHadoopWriter` — a class the group's own scope names. **One re-sweep does not settle
a group**; the July pass fixed the package the *config* check pointed at (`internal/io/`) and never
walked the other three.

Two things to do differently on a re-sweep:

- **Say in the sweep-log row that it was a re-sweep at an unchanged version, and which breadth
  check found the work.** That is what tells the next reader whether the group is now genuinely
  covered or merely re-declared complete.
- **A re-sweep that maps every concept onto existing topics is a normal outcome**, not a failure.
  The "a run that finds none has probably swept too shallowly" warning is about *concepts*, not
  about `propose:` blocks. Four of the eight re-sweeps proposed no topic and were still worth
  running; say so plainly rather than manufacturing a proposal.
- **Reconcile topics the *original* pass mapped but never linked.** Checking only the topics whose
  mappings are new to this run misses them — `B1` and `A14` had carried a storage mapping since
  July with no resource entry, found only by listing every topic in the front matter and diffing
  against the ones that link the page.
- **A page missing its trailing sections is itself the finding.** Before reading any source, check
  the page has all four `##` sections. One with a sweep log and no breadth checks was never
  breadth-checked — nothing recorded what it skipped, so `status: complete` on it means only that
  someone stopped. `core — execution-engine` was in exactly that state and is not one of the nine
  `sql/core` pages the "do not invent a fifth shape" warning names, so **audit the shape per page**;
  the known-bad list is not the whole set.

1. **Pre-flight:** confirm `configs/catalog.yaml` exists and note its `meta.spark_version`. Run
   `gen_coverage.py --list-groups <subsystem>` to see the groups and which are already swept.
2. **Scope check.** If the user named a group, confirm it exists in that listing and go. If not,
   show the groups with their scopes and ask which to sweep — never pick silently, and never
   attempt the whole subsystem. A run covering one group of several sets `status: partial`
   *for the subsystem*; the page's own `status:` describes whether that group's scope was
   fully covered.
3. **Config slice — narrow it to the group, not the subsystem.** "Every config whose `subsystem`
   matches" is 750 keys for `sql/catalyst`, six groups' worth, which makes the breadth check in
   step 5 unrunnable. Take the subsystem's configs, then filter to the **namespaces this group
   owns** plus the specific keys its rules read:

   ```bash
   PYTHONIOENCODING=utf-8 python -c "
   import yaml, re
   d = yaml.safe_load(open('docs/reference/spark-source-map/configs/catalog.yaml', encoding='utf-8'))
   cs = [c for c in d['configs'] if c['subsystem'] == '<subsystem>']
   pat = re.compile(r'<group namespaces, e.g. \.optimizer\.|\.cbo\.|\.statistics\.>')
   sel = sorted({c['key'] for c in cs if pat.search(c['key'])})
   print(len(sel)); [print(k) for k in sel]
   "
   ```

   Build the pattern by reading the group's `scope`, not by guessing: a rule named there tells you
   which prefix to include. Expect 50–150 keys. Err wide — a key that turns out to belong to
   another group becomes an *out-of-scope* row in the breadth table, which is a useful finding;
   a key you never pulled is invisible. Record the pattern in the page so the next refresh
   reproduces the same slice.
4. **Run the sweeper brief** ("Sweeper subagent brief", at the end of this file). It is a checklist, not a delegation
   requirement: run it inline yourself, or dispatch a read-only subagent **if the harness allows
   agent calls and the user asked for one**. Some harnesses forbid unprompted subagent spawning —
   in those, work the brief inline and say so in the summary rather than silently skipping it.
   Either way the inputs are the same: the subsystem path, the config slice, `docs/learning-path-v2.md`
   (for existing topic codes), and `groups.yaml` (for group scope definitions).
5. **Write** `docs/reference/spark-source-map/sweeps/<slug>.md` using the sweep page contract
   below. `<slug>` is the subsystem with `/` → `-`, then `-<group>` when the run covered one
   group (e.g. `core` + group `rdd-layer` → `core-rdd-layer.md`; `sql/catalyst` + `optimizer`
   → `sql-catalyst-optimizer.md`). **One page per group — never merge groups into one file.**
   `gen_coverage.py` keys the sweep-status table on `(subsystem, group)` and `group:` is a
   scalar, so a file holding two groups reports only one and the other stays `⬜ pending`.
   Filenames are otherwise meaningless to the generator — it globs `sweeps/*.md` and reads
   front matter — but they must be unique, hence the group suffix.

   **Sweep the subsystem, not the concepts you already recognise.** The stopping condition is
   *the group's scope is covered* — never *the page has enough concepts*. A sweep exists to find
   unknown unknowns, so the concept you cannot name yet is the one that justifies the run. Two
   completeness dimensions, and a sweep needs both:

   - **Breadth — did you visit everything in scope?** There are **two independent breadth checks
     and you need both**, because either can be green while the other is badly red:

     1. *Config breadth.* Every config in the slice must tie to a concept; one that doesn't means
        an unvisited area. Mechanical — run it before writing.
     2. *Package breadth.* Walk the packages named in the group's `scope` field, list the classes,
        and compare against what the page cites. A package you never opened is a concept you
        cannot have found. **Walk nested sub-packages by hand** — `--coverage` cannot see them
        (see the checks table in `SKILL.md`).

     Which one bites varies by group and is not predictable. Observed on the nine `core` groups:
     `rdd-layer` was 22/24 configs cited while `rdd/` was 8 of 43 files; `monitoring` had all 118
     configs attributed while `status/` was 8 of 45; `submit-standalone` was red on both.
     Running only the config check and declaring the group done is the standard way to miss a
     whole layer — that is how `BlockTransferService`, the entire block data plane, had no concept
     on a page marked `status: complete`.
   - **Depth — for each concept, the same layers a trace demands.** Do not stop at the entry point
     and the happy path. For each concept ask: registration/lookup, discovery/planning,
     splitting/distribution, per-record execution, **error and edge paths** (especially anything
     that fails *silently*), termination/commit and its guarantees, and alternative APIs (V1 vs V2,
     classic vs Connect). A concept recorded as an entry point and one class is a placeholder, not
     a mapped concept.

   Record what you *chose not to* cover. A sweep that silently omits half its scope is worse than
   one marked `status: partial` with the remainder named — the first looks finished.

   **Then write the four trailing sections** — both breadth checks, the overlapping topic traces,
   and the sweep log. They are part of the contract, not an optional appendix, and both checkers
   pass without them, so nothing but this instruction will catch their absence.

   **Check the topic traces that already cover your codes.** A sweep maps concepts to topic codes;
   any code that already has a `topics/<code>.md` page is prior coverage of the same rules from the
   other direction, and the two can disagree — most often because the trace was recorded against an
   older Spark. `check_drift.py --sweeps` lists the overlaps and flags version mismatches. Read the
   overlapping traces before writing: agree with them, or say plainly where the source now differs
   and re-verify the trace's anchors. Two pages contradicting each other at different versions is
   worse than either page alone.
6. **Reconcile every learning-path topic the sweep touched — always.** A sweep maps concepts to
   topic codes, so it tells you exactly which topics to revisit; the generator only handles the
   *new* ones. Two jobs:

   - **Existing topics** (any concept whose `topics:` list is non-empty). For each, add to its
     **"Learn it with"** a sweep entry — `**Source sweep — [<subsystem> sweep](reference/spark-source-map/sweeps/<slug>.md)**` — plus any official docs page the sweep proved the topic
     needs, and correct the scope line if the sweep showed it has drifted. Same book-and-docs rule
     as a trace. A concept that maps to a topic but reveals something the topic never mentions is a
     path gap, not just a source finding.
   - **New topics** (`propose:` blocks, auto-appended by `gen_coverage.py`). **These are the run's
     deliverable — finish them to the same standard as a hand-written topic, and do not ask first.**
     The generator writes a stub with a placeholder resource list; leaving it as generated is the
     one failure mode that makes source-first discovery look like noise. A stub whose only entry is
     "Spark-docs — see official documentation" and whose milestone is `TBD` fails the book-and-docs
     rule. Fill in `what` / `why`, cite a real book chapter or an explicit "No book covers this"
     callout, cite the specific docs page the topic needs, and write a milestone someone could
     actually check. A new topic often has no book coverage at all — say so plainly and lean on the
     docs and the sweep page.

   Then flip any written chapter the sweep left behind to 🔄 — the three-place procedure is in
   `references/trace.md`, step 6.
7. **Regenerate the matrix:** `python tools/spark_source_map/gen_coverage.py`
   This auto-appends any `propose:` blocks to `learning-path-v2.md`. Pass `--no-write-proposals` to skip.

   Then **verify the `status:` you just claimed**:
   ```
   python tools/spark_source_map/check_drift.py --sweeps
   ```
   It resolves the group's `scope` to real directories and checks that every claimed package has at
   least one file cited on your page. A `status: complete` page that cites *nothing* from a package
   its own scope claims fails the check — either sweep it or downgrade to `status: partial` and name
   what was left out. The cited/total ratio it prints is informational; a sweep names the files that
   carry a concept, not every file in the package.

   Read the generated proposals before moving on. They are appended per level in code order —
   if they come out descending, or land under the wrong level heading, fix the ordering by hand and
   fix the generator.
8. **Wire** the new sweep page into `zensical.toml` nav under `Spark Source Map → Sweeps`;
   commit the sweep page, the learning-path edits from step 6, and any 🔄 status changes together.

---

## Sweep page contract

The sweeper writes Markdown with this front matter — `gen_coverage.py` reads it:

```markdown
---
subsystem: sql/core
spark_version: "4.1.2"    # copy from catalog meta
swept_at: 2026-06-06       # date this sweep was run (ISO 8601)
group: joins-and-agg       # optional; set when sweeping a large subsystem in parts
# All planned groups for this subsystem, copied from groups.yaml in that order.
# Repeat it identically on EVERY page for the subsystem — gen_coverage.py takes the
# list from whichever page sorts first alphabetically, so a page that omits it or
# carries a stale list silently drops rows from the sweep-status table.
all_groups: [joins-and-agg, streaming-integration, connector-v2]
status: complete            # or: partial
concepts:
  - name: joins
    topics: [B7, A3]        # learning-path codes this concept already backs
  - name: aqe
    topics: [A2]
  - name: vectorized-reader
    topics: []              # no topic covers this yet — the sweep's actual product.
                            # Add a propose: block; it becomes a new learning-path topic.
    propose:
      code: A12             # next unused code for this level (check learning-path-v2.md);
                            # if it is taken, gen_coverage.py reallocates rather than dropping
      level: Advanced       # Beginner | Intermediate | Advanced | Expert
      title: "Vectorized Reads and Columnar Execution"
      what: "One sentence: what this concept is."
      why: "One sentence: why a practitioner needs to understand it."
---

## Joins
**What it is:** one paragraph.
**Code path:** `Dataset.join` → Analyzer (ResolveJoin) → `JoinSelection` → `SortMergeJoinExec` / `BroadcastHashJoinExec`
**Anchor files:** [JoinSelection.scala](https://github.com/apache/spark/blob/v4.1.2/...)
**Configs:** `spark.sql.autoBroadcastJoinThreshold`, `spark.sql.join.preferSortMergeJoin`
**Maps to topics:** B7 (Joins), A3 (Join Strategies)
```

### Required trailing sections

**A page is not finished at its last concept.** Four `##` sections close every page, in this order.
No generator reads them — they are the record a human (or the next sweep) uses to judge whether the
group is genuinely covered, which is exactly what neither checker can tell you. Write all four even
when the answer is "nothing":

```markdown
## Breadth check 1 — the config slice
## Breadth check 2 — the packages
## Overlapping topic traces
## Sweep log
```

- **Breadth check 1 — the config slice.** State the slice (the pattern from step 3, reproducibly),
  the count, and tie every key to a concept. Keys the group does *not* read are a finding, not an
  omission — say which group owns them. Configs the group reads that are **not in the catalog**
  (dynamic prefixes, bare `getBoolean`/`getOption` string keys) belong here too; they are invisible
  to `--sweeps` and so can only ever be caught by eye.

    **Write every key literally in the `**Configs:**` lines — never a family or a suffix.**
    `the spark.dynamicAllocation.* family`, or `` `spark.speculation`, `.interval`, `.multiplier` ``,
    reads fine and defeats both the tooling and this check: `--sweeps` counts literal keys, so a
    dozen attributed keys score as one, and *you* cannot tell an abbreviated family from a partly
    swept one. `core — execution-engine` measured 38/111 on a literal count and 86/111 once the
    shorthand was expanded — a 43-point error in the check that is supposed to decide whether the
    group is done. Expand any shorthand you inherit before trusting the number.
- **Breadth check 2 — the packages.** Walk the scope's packages *and their sub-packages by hand*,
  and give the cited/total ratio per package. Name what you chose not to cover under a heading a
  reader cannot mistake for coverage. This is the check that catches a missing layer;
  `--coverage` structurally cannot see nested packages (see the checks table in `SKILL.md`).

    Also walk the **class names the group's `scope` field spells out** — a named class that appears
    nowhere on the page is the sharpest possible finding, and no checker looks for it.

    Count citations against the **concept body only** (split on the first `## Breadth check 1`).
    Counting the whole page folds this section's own uncited list, and the sweep log's filenames,
    back in as citations — so the more honest the page, the more it over-reports.

    For an uncited file, decide and say which: swept by another group (name it), plumbing with no
    concept, or a genuine gap. **A file no sweep page anywhere cites is a finding worth recording
    even when it belongs to another group** — that is how `SparkListener`, `SparkListenerBus`,
    `ReplayListenerBus` and `StatsReportListener` were found missing from `core — monitoring`, by a
    walk of `core — execution-engine`. Record it; do not fix the other group's page in this run.
- **Overlapping topic traces.** List the `topics/<code>.md` pages that already cover any code in
  your front matter — `check_drift.py --sweeps` prints them — and say for each whether you agree
  with it or where the source has moved since. **Write the section even when there are none**, with
  one line saying so; "no trace exists for these codes" and "I forgot to look" are indistinguishable
  from a missing section.
- **Sweep log.** A `| Date | Spark | What changed |` table, newest row last. One row per run: what
  the run covered, the concept and proposal counts, which breadth check found the work, and the
  findings worth carrying. On a re-sweep say plainly that it was a re-sweep and whether the version
  changed — that is what tells the next reader whether the group is now covered or merely
  re-declared complete. A page that is later re-resolved by `refresh anchors` gains a
  `## Refresh log` alongside it.

!!! warning "Do not invent a fifth shape"

    The corpus drifted once already: a run of `sql/core` sweeps merged the two breadth checks into a
    single `## Breadth checks`, dropped the overlap section partway through, and wrote **no sweep log
    at all** on any of its nine pages. That is the one batch not to copy. The `resource-managers` and
    `sql/pipelines` pages are the current standard.

---

## Sweeper subagent brief

**This is the sweep checklist**, subject to the same inline-or-dispatch rule as the tracer brief
above. The brief:

> Sweep the **`<subsystem>`** subsystem of Apache Spark at `C:\opt\learn\spark\repos\spark`.
>
> **Find what is in this code — not what the learning path already knows about.** The path is
> supplied only so you can *label* concepts that happen to match an existing topic; it is not a
> checklist to fill, and it must not narrow what you look at. Concepts it does not cover are the
> point of the run, and a sweep that finds none has probably swept too shallowly.
>
> For each major concept in scope (see supplied groups.yaml scope field): identify the
> entry point, the analysis/planning path, and the physical execution classes — with
> `file:line` anchors. Pull the relevant configs from the supplied catalog slice. Then map each
> concept onto learning-path topic codes (B/I/A/E) if any fit, and `[]` when none do.
>
> **Cover the subsystem, not the concepts you recognise.** The point of a sweep is unknown
> unknowns, so a concept you cannot name yet is exactly the one worth reporting. Include the
> error/fallback paths and the commit or termination logic, not just the success path — and
> treat any config in the slice you cannot tie to a concept as evidence of something you have
> not found yet.
>
> For every `[]` concept, add a `propose:` block with: the next unused topic code for the
> appropriate level (check the highest existing code in that level first), a `level`
> (Beginner/Intermediate/Advanced/Expert), a concise `title`, a one-sentence `what`, and a
> one-sentence `why`. These become new learning-path topics — that is the deliverable, so judge
> them on whether a practitioner would benefit from studying the concept, not on whether they fit
> the path's current shape.
>
> Return the sweep page in the exact front-matter contract above.
> **Be source-faithful:** if you cannot confidently trace a path, say so — never invent one.
