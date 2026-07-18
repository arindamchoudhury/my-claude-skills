# Phase 4 — Review & Refresh

A learning path is a living document. The topic taxonomy is stable, but the facts wrapped around it
are not: certifications get re-versioned (question counts, domain weights, fees change), runtimes and
packages ship new stable releases, training courses get renamed or retired, and new platform features
land that belong as callouts on existing topics. Phase 4 re-verifies the path against current reality
and syncs it — without re-running the whole Phase 1 research from scratch.

The goal is an honest path: every volatile claim either re-verified against an official source today,
or corrected. Report both — what changed *and* what you checked and found still correct. "Verified, no
change" is a real and valuable outcome; don't manufacture edits to look busy.

---

## Step 0 — Decide what's actually volatile

Most of the path does not need re-checking. Concept definitions, "why you need it", milestones, and
the dependency ordering are stable. Spend your effort on the facts that drift:

| Volatile fact | Where it lives | Source of truth |
|---|---|---|
| Cert question count, time, fee, domain weights | Certifications table | Official cert/exam-guide page |
| Current stable + LTS + beta versions | Header block | Official release-notes / changelog |
| Breaking changes, renames, deprecations | Topic callout admonitions (`!!! warning`/`info`/`note`) | Release notes, migration guides |
| Course names, hours, links, retirements | Resources table + topic entries | Official training catalog |
| New features mapping to existing topics | Topic callouts | Product announcements, docs |
| Topic `⬜`/`✅` status | Topic headings | Which book chapters actually exist |

Check the path header's `Last updated` line first. If it was refreshed very recently, say so and focus
only on what could have changed since — don't redo a pass that was just done.

---

## Step 1 — Re-fetch the volatile sources

Use `fetch_page.py` (see SKILL.md "Fetching vendor pages") — not WebFetch — for every vendor page.
The whole point of this phase is exact facts, and WebFetch loses them.

Fetch, in parallel where possible:
- Each certification's official page (question count, time, fee, and the domain-weight list)
- The runtime / package release-notes index (current stable, LTS, any beta; release dates; end-of-support)
- The training catalog entries for every course cited in the Resources table (confirm still live, same name)

The `Sources consulted` list at the bottom of the path is your fetch checklist — it records exactly
which URLs were used last time.

---

## Step 2 — Diff each fact and correct

For every fetched page, compare the live fact to what the path claims. Make a small ledger:

```
DCDEP weights — path: 10 domains → page: all 10 match (22/13/10/10/10/10/7/7/6/5)   ✅ unchanged
DBR stable    — path: 18 / Spark 4.1.0 / Jun 10 → page: same, EOS Jun 10 2029        ✅ unchanged
DA-MGUC course— path: live → page: 404 / retired                                      ❌ replace
```

Apply only the mismatches. When a course is retired, find its official replacement and swap it
everywhere it's cited (Resources table *and* the topic entry that uses it). When a version advances,
update the header and re-check that the breaking-change callouts still describe the *current* release.

If a source has genuinely been superseded by a newer one (a course replaced, a protocol renamed),
follow the same honesty rules as Phase 3 blending: name the change, keep the point-in-time term only
where a dated release note requires it, and use the current name everywhere else.

---

## Step 3 — Sync topic status with reality

`⬜`/`✅` per topic should match what the user has actually completed. The ground truth is the book:
a topic is `✅` when its chapter exists (not a stub). List the chapters in the topic-book directory and
reconcile against the headings. Flip any that are out of sync. If a chapter file exists but is only a
parked stub, the topic is still `⬜` — note the distinction rather than over-claiming progress.

Also update the `**You are currently here:**` line in the study-sequence diagram, and the per-level
counts if the path uses them.

---

## Step 4 — Fold in new features as callouts

New platform capabilities usually don't need a new topic — they refine an existing one. A new
autonomous-optimization feature belongs as a callout on the storage-optimization topic, not as its
own entry. Callouts are **admonitions, never `>` blockquotes** — use the type that matches the fact:

- `!!! warning "..."` — breaking change the learner must test for before upgrading
- `!!! info "..."` — naming / behaviour note (old vs new term, exam-vs-current divergence)
- `!!! note "New — ..."` — new feature that sits on top of what the topic teaches

Keep callouts tied to the milestone: explain how the feature changes what the learner does, and make
clear whether they still need the manual/older skill (usually yes — for exams, for the non-managed
case, and for understanding what the platform now does for them).

Only when a genuinely new *concept* appears with no home does it become a new topic — and then follow
the new-topic procedure in `phase3-book.md` (place by dependency level, renumber or use a decimal code,
add to the book index and the topic-book skill's arc table).

---

## Step 5 — Update header and sources

Refresh the header block:

```markdown
> **Last updated:** YYYY-MM-DD (research pass: <one line — what was verified and what changed>)
> **Current stable version:** <...>
> **LTS version:** <...>
> **In Beta:** <... — not yet GA; learn against current stable>
```

The changelog clause is the record of this pass — terse, factual, naming the sources checked
("verified certs/runtime/courses against official pages") and the substantive edits. Update
`Sources consulted` with any new URLs fetched and drop any that are now dead.

---

## Step 6 — Report, then offer to commit

Lead with a compact verification table — claim vs. official vs. status — so the user can see at a
glance what was checked, not just what changed. Then:

- If nothing was wrong: say so plainly. "Path is current; verified certs + runtime + courses against
  official sources today; no content edits needed" is a complete, honest result.
- If you edited: summarize the corrections.

Commit only if the user asks (or has standing authorization for this repo). Stage only the path file
(and any sibling files the status sync touched — book index, zensical nav) — never the `cache/web`
fetch scratch. Match the repo's existing commit style.
