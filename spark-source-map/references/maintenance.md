# Maintenance — `regroup` and `new spark release`

> Reference for the `spark-source-map` skill. Load it when recarving groups.yaml or moving the map to a new Spark release.
> Read `SKILL.md` first — it holds the design intent and the autonomy contract that govern
> everything here.

### `regroup <subsystem>` — recarve groups.yaml (hand-authored, checker-verified)

Triggers: "regroup core", "add a group for X", "groups.yaml is missing Y", "check the carving",
"what isn't covered by any group".

`groups.yaml` is hand-authored — no generator writes it, so nothing notices when its scopes
drift from the source or when a new package has no owner. A package no group claims can never
be swept, so the gap conceals itself.

1. **Survey.** `check_drift.py --coverage` for unclaimed packages and identical-path collisions;
   `check_drift.py --sweeps` for packages a group claims but its sweep never opened — a scope
   naming code nobody swept is as much a carving problem as a package nobody claims;
   `gen_coverage.py --list-groups <subsystem>` for the current carving and what is already swept.
2. **Propose, then ask.** What deserves a group is editorial — it changes the sweep plan and the
   learning path. Bring a concrete proposal (new groups, extended scopes, with file counts and
   the topics each would back) and let the user choose. Note which unclaimed packages are
   plumbing you deliberately excluded (`util/`, `errors/`, `test/`, `dsl/`).
3. **Edit, avoiding the two YAML traps.** Numbers ascend within a subsystem; inserting after a
   `scope:` line orphans the following `description:` onto the new group, which `yaml.safe_load`
   accepts silently. Insert after `description:`, then verify with a duplicate-key-aware parse
   (the snippet is in the repo README, "Editing groups.yaml").
4. **Name real classes** — `WholeStageCodegenExec`, not "Whole-Stage CodeGen". A name is what
   makes a scope checkable. Then run `check_drift.py` and expect to be wrong: when a class
   legitimately lives in another module, add it to that group's `modules:` list rather than
   vaguening the scope. Loop until it exits 0.
5. **Re-run `--coverage`** to confirm the gap closed and no identical-path collision appeared.
   Declare deliberate sharing with `shared_scope: true`. Re-run `--sweeps` too: widening a scope
   can leave an already-`complete` sweep page no longer covering everything its group claims.
6. **Bump `_meta`** (`spark_version`, `verified_at`) and record *why* in `_meta.note` — nothing
   else captures the reasoning.
7. **Regenerate and sync.** Run **both** generators — each consumes `groups.yaml`:
   `gen_configs.py` (it renders every group's scope into `configs/index.md`, so a groups.yaml
   edit without it leaves that page describing the old carving) and `gen_coverage.py` (adds the
   group's row). The skill files carry no group table any more — they point at
   `gen_coverage.py --list-groups`, which cannot go stale — so the only hand-copied one left is
   the "Sweepable subsystems" table in the repo README. Update it, or the next reader plans a
   sweep against a carving that no longer exists.
8. **Commit** `groups.yaml` with the regenerated `index.md` and the doc updates, one commit.

---

---

### `new spark release <version>` — full release runbook

Triggers: "Spark 4.3 is out", "update to the new Spark", "bump the source map to <version>".

Run the seven-step runbook in the repo README ("When a new Spark version ships"), in order:
move the checkout to the tag; `gen_configs.py` plus the parser tests, checking the >1000 floor;
`check_drift.py` and fix every scope it names, then `--coverage` and `--sweeps` (a release that
adds a package under an already-swept scope turns a `status: complete` page into an overclaim, and
`--sweeps` is the only thing that notices); `gen_coverage.py`; **`refresh_anchors.py`, dry run then
`--apply`** (never find-and-replace the tag in a URL — line numbers drift heavily and a stale anchor
still renders fine on GitHub; the tool re-resolves by content and reports what it cannot place);
then decide which pages need a real re-trace on top of that; reconcile `learning-path-v2.md`'s header,
`spark-book/index.md` statuses and chapter version lines; commit together.

`refresh_anchors.py` settles line numbers, not meaning. A resolved anchor points at the same line
of source and says nothing about whether the page's prose is still true — re-trace wherever the
code moved a long way, wherever the tool resolved "via declaration", and wherever the release notes
say behaviour changed.

Re-tracing pages is a `trace` run each, one topic per run — propose the list and let the user
pick, rather than doing all of them unasked.

---
