---
name: research-notes
description: Use when the user wants to take notes from web links (URLs) or PDF files — articles, blog posts, documentation pages, research papers, or any non-book source. Triggers on phrases like "take notes on this link", "summarize this article into my notes", "add this page to my notes", "I want to save notes from this URL", "take notes from this PDF" (when not a book/chapter workflow), "add this paper to my notes", "I'm building a research collection", or any time a user shares a URL or PDF and asks to capture or organize the content. Produces structured Markdown notes in a Zensical site, organized by source with cross-topic synthesis pages.
---

# Research Notes

A workflow for turning web links and PDFs into a searchable personal notes site built with [Zensical](https://zensical.org/). Sources can be articles, blog posts, documentation pages, research papers, or any web/PDF content. The output is a folder of Markdown files plus a `zensical.toml` config; run the site locally with `zensical serve` (or Docker) for a clean, navigable notes site.

## When to use this skill

- User shares a URL and wants to capture notes from it.
- User shares a PDF that is NOT a book being studied chapter-by-chapter (for books, use **book-pdf-notes** instead).
- User wants to build a research collection across multiple sources on a topic.
- User says "add this to my notes", "take notes on this article/paper/page".
- User wants a searchable personal knowledge base from web and PDF sources.

**Use book-pdf-notes instead for:** books being studied chapter-by-chapter, technical manuals with chapter structure, study notes on a single long-form text.

## Project layout

```
<notes-root>/
├── zensical.toml
├── docs/
│   ├── index.md              # hub: courses overview, topics overview
│   ├── topics/
│   │   ├── index.md          # topic list + backlog
│   │   └── <topic>.md        # notes synthesized across sources
│   ├── sources/
│   │   ├── index.md          # log of all sources, organised by course
│   │   └── <course-slug>/    # one folder per course (human-readable name)
│   │       ├── index.md      # course overview: title, ID, lesson list
│   │       └── <slug>.md     # notes from one lesson/source
│   └── reference/
│       ├── glossary.md
│       └── resources.md
├── cache/
│   ├── web/
│   │   └── <slug>.txt        # fetched page text (saved after first fetch)
│   └── pdf/
│       └── <slug>.txt        # extracted PDF text (saved after first extraction)
└── README.md
```

**Course folder naming:** use a short human-readable slug, not the course ID — `ai-agents-google-cloud`, `gemini-enterprise`, `developer-agent-fundamentals`. The course ID goes in the `index.md` frontmatter only.

**Course numbering:** courses are numbered in the order they are added. The number appears in the nav group header (`"1. AI Agents on Google Cloud"`), in `docs/index.md` course list, and in `docs/sources/index.md` section headers. Don't renumber existing courses when adding new ones — assign the next available number.

**`[[slug]]` wikilinks work across subdirs** because `serve.py` uses a custom `build_url` that scans `docs/` recursively for `<slug>.md`. Source notes never need to include the course path in cross-references.

**Detection — confirm which state you're in before doing significant work:**
- `docs/sources/` present → existing research-notes project. Read the source log and continue.
- Nothing present → scaffold fresh project using the templates in "Scaffold templates" below.

## The flavors of work

### 1. Fresh project, first source
Scaffold the project structure, then proceed as flavor 2.

### 2. Adding a new source (URL or PDF)
1. **Check cache first.** For URLs: check `cache/web/<slug>.txt`. For PDFs: check `cache/pdf/<slug>.txt`. If present, read directly — skip fetching/extraction.
2. **Fetch or extract if cache is missing.**
   - URL: use `WebFetch` with an **exhaustive verbatim prompt** (see below), then save to `cache/web/<slug>.txt`.
   - PDF: extract using pymupdf (available in the `notes-fetch` conda env) — see PDF intake workflow below.

   **WebFetch prompt discipline — always use this exact pattern:**

   > Extract the complete verbatim content of every section on this page. Do not summarize or paraphrase anything. Include every bullet point, every caveat, every condition, every fallback behavior ("if X then Y"), every note, callout, and warning, and every code example — all quoted exactly as written on the page. I need the full text of every section.

   Then do a **second targeted fetch** for any section that describes conditional or fallback behavior, quoting it word-for-word:

   > Quote the complete verbatim text of [section name], including every caveat, fallback, and parenthetical. Do not summarize.

   **Why:** a summarizing WebFetch prompt omits critical caveats (e.g. "falls back to full refresh if results cannot be computed incrementally"). The notes must capture these conditions exactly — they are often the most important part.
3. **Determine the course folder.** Check `docs/sources/` for an existing folder that matches this source's course. If none exists, create `docs/sources/<course-slug>/` and write a `docs/sources/<course-slug>/index.md` course overview page.
4. **Write the source note** to `docs/sources/<course-slug>/<slug>.md` using the note style below.
5. **Update the source log** (`docs/sources/index.md`) — add a row under the correct course section.
6. **Do the topic pass** — identify which topics this source informs. Either extend an existing topic page, create a new one (≥2 sources overlap), or add to the backlog in `docs/topics/index.md`. Cross-link bidirectionally.
7. **Update** `zensical.toml` nav (add entry under the course's nested group), `docs/reference/glossary.md` (new terms), `docs/reference/resources.md` (useful links).

### 3. Adding a topic page
Create `docs/topics/<topic>.md` only when ≥2 sources overlap on that topic. Pull key points from each source note, add synthesis commentary, and cross-link back to each source note. Add it to the topic index.

**When extending an existing topic page with new sources — blend, never overwrite.**
- Read the full existing topic page before touching it.
- Add new content alongside old content, not in place of it.
- When two sources frame the same concept differently, present both framings as complementary lenses (e.g., "Lens 1 — three core capabilities · Lens 2 — five characteristics") and explain how they relate.
- Never silently drop a section, quote, or framing that came from an earlier source — the value of a topic page is the accumulation across sources.
- New sections go at the logical insertion point, not always at the bottom.

### 4. Chat answer → notes addition
User asks a question, gets an answer, then says "add that to my notes":
1. Grep source notes to find where related content lives.
2. Insert a new section at the logical location — styled to match surrounding notes.
3. If a topic page is relevant, add a reference there too.

### 5. Coverage-gap check → note → learning-path fold-in

**TRIGGER:** user shares a documentation URL and asks some form of *"do we have this in the learning path?"* / *"is this covered?"* — in a project that has BOTH `docs/sources/` (research notes) and `docs/learning-path.md` (a learning-path project, e.g. the Databricks notes). This is the full loop the two skills run together; don't stop at answering the coverage question.

Run these steps in order. Don't skip the fold-in just because the answer to step 1 is "kind of":

1. **Coverage check.** Grep `docs/learning-path.md` for the concept. Classify the result honestly:
   - **Absent** — not mentioned → gap.
   - **Name-dropped** — appears only inside a feature list / callout, never explained → still a gap (this is the most common and most missable case).
   - **Covered** — a topic already scopes it with its own reference/milestone → no note needed; say so and stop.
2. **Fetch** the page with `fetch_page.py` (NOT `WebFetch` for JS-rendered doc sites — see "Fetching web pages"). Read `cache/web/<slug>.txt`. Do **not** assume its first line is a breadcrumb — on many sites it is the version selector or the page title.
3. **Write the source note** (flavor 2 note style). Set `**Source updated:**` from the page's "Last updated" line. Cross-link related notes with `[[slug]]`.
4. **Wire in by sidebar** — nav group = the docs site's own sidebar section, extracted with `scripts/fetch_nav.py` (see the sidebar-grouping rule under Nav convention; **do not group by breadcrumb**). Then course index, source log.
5. **Fold into the learning path (Phase 5).** This is the step the coverage question exists to set up — do not omit it. Add the note as a **reference** under the topic(s) it informs; add a dated callout if it introduces a new distinction/version/rename; bump the `learning-path.md` header `Last updated` line with a one-line changelog. A note landing ≠ topic completion — leave the topic's ⬜/✅ status unless a chapter was actually written. This mirrors **learning-path skill, Phase 5** — load it if available; the steps here are the same diff-one-note reconcile.
6. **Validate + commit.** `python -c "import tomllib; tomllib.load(open('zensical.toml','rb')); print('TOML OK')"`, confirm every note file appears once in nav, then commit the note + path edits together.

**Why this is one flavor, not two separate asks:** "do we have X?" is almost always a request to *close the gap*, not just report it. Reporting "no, we don't" and stopping is the failure mode — the user then has to ask again. If coverage is genuinely complete, say so and stop; otherwise run the loop through the commit.

## Note style for a source file

**Note structure is dynamic — mirror the source page, don't impose a skeleton.** A note's body follows the *source's own* headings, sections, tables, images, and order — not a fixed `Summary / Key points / Notes / Quotes / Related sources` template. Keep only the metadata header (Source / Added / Source updated / Tags / Type) and a light trailing line of `[[wikilink]]` cross-references; everything between is shaped by the page. A short page gets a short note; a page with four sections gets four sections.

The **only** fixed part is the metadata header and the trailing cross-links:

```markdown
# <Title>

> **Source:** [<display URL or filename>](<URL>)
> **Added:** YYYY-MM-DD
> **Source updated:** YYYY-MM-DD
> **Tags:** tag1, tag2, tag3
> **Type:** article | documentation | paper | blog | other

<body — mirrors the source's own headings/sections/tables/images/order>

---
Related: [[other-slug]] — one-line note on the relationship.
```

**Do not** start from a `Summary / Key points / Notes / Quotes worth keeping / Open questions / Related sources` skeleton. Those headings are only valid when the source itself is organized that way. Let the page's structure drive the note's structure.

**Style rules:**
- **Short sentences over overloaded ones.** Prefer several short declarative sentences to one long clause-stacked one. One fact per sentence — easier to skim and revise later.
- Paraphrase ideas in your own words. Short quotes only where the exact wording matters.
- No wall-of-text dumps from the source. The notes should be 20–40% the length of the source.
- Mark uncertain claims with `> ❓ Unverified:` rather than stating them as fact.
- For technical content: **always copy code examples and workflow steps in full — never truncate or paraphrase them.** The exact code is the point; summaries lose precision. Strip surrounding boilerplate (imports already shown, repeated scaffolding) but keep every meaningful line.

**Markdown formatting rules — lists must always be preceded by a blank line:**

A label ending in `:` followed immediately by a list (no blank line) collapses into a single paragraph in most renderers. The same applies to italic labels (`*label:*`) before code blocks or lists.

```markdown
❌ Wrong — list collapses:
Tips for effective instructions:
- Be specific
- Use markdown

❌ Wrong — italic before list collapses:
*venv (from PDF):*
- step one
- step two

✅ Correct — bold heading + blank line before list:
**Tips for effective instructions**

- Be specific
- Use markdown

✅ Correct — bold heading + blank line before code block:
**venv (from PDF)**

```shell
...
```
```

Rule: **never use a plain sentence or italic text as a label directly before a list or code block.** Always use a `**bold heading**` and leave a blank line before the list/block.

**Blending with existing notes — always.**
Before writing a source note, read the existing source notes that cover related ground. Then:
- **Don't re-capture what's already there.** If an existing note already explains concept X, say "confirms [[other-slug]]'s point on X" or "see [[other-slug]]" rather than writing it out again.
- **Do capture what's genuinely new or different.** A new angle, a better example, a contradiction, a more precise definition — these deserve their own prose.
- **Call out contradictions and differences explicitly.** If this source frames something differently from an existing note, name the difference: "Unlike [[other-slug]] which says X, this source argues Y."
- **Annotate the trailing `[[wikilink]]` cross-links** — don't just list slugs; say *how* the sources relate (confirms, contradicts, extends, provides detail for, zooms out from).

This same blending rule applies when extending existing source notes (e.g. after re-fetching with new content): merge new material into the existing structure, don't append independent sections.

## Tracking source freshness

The `**Source updated:**` field records the date the source page was last updated (as shown on the page — not when you captured it). Always capture this date when taking notes from documentation pages.

**How to find the date:**
- Documentation pages (Databricks, AWS, etc.): look for "Last updated" near the page title or footer. Fetch with `WebFetch` and check the returned text.
- Articles/blog posts: use the publication or last-revised date. If absent, omit the field.
- PDFs: use the publication date from the cover or copyright page.

**Staleness check script** (Databricks notes project): `scripts/check-docs-freshness.py`

```bash
python scripts/check-docs-freshness.py                          # check all source notes
python scripts/check-docs-freshness.py --course databricks-docs # one course folder
python scripts/check-docs-freshness.py --skip-fetch             # metadata only, no HTTP
```

The script parses `**Source:**` URLs and `**Source updated:**` dates from all notes, fetches each live page, and reports STALE / OK / NEEDS-CLAUDE. Databricks docs are JavaScript-rendered — static HTTP fetch cannot read their "Last updated" date; those pages are flagged with a ready-to-paste Claude prompt.

**When Claude verifies freshness:** ask Claude to `WebFetch` each flagged URL and compare the live "Last updated" date against the note's `**Source updated:**` field. Update the field and note any content changes.

## Source log format (`docs/sources/index.md`)

```markdown
# Sources

| Title | Type | Added | Tags | File |
|---|---|---|---|---|
| [Article title](sources/slug.md) | article | 2026-05-26 | tag1, tag2 | [url](https://...) |
```

## Fetching web pages

Two paths depending on whether the page requires JavaScript:

**Simple pages (static HTML):** Use `WebFetch`. Save raw text to `cache/web/<slug>.txt`.

**SPAs / JS-rendered pages:** Use the Playwright script at `notes/scripts/fetch_page.py`. It handles:
- Content-ready wait (polls until "Your content is loading" disappears)
- Accordions: clicks `button[aria-expanded='false']` and `button[class*='accordion__header']` — **header buttons only**, never body/container divs (see pitfall below)
- Tabs: clicks all `.blocks-tabs__header-item` and `[role='tab']` elements
- Reveal buttons: "Show more", "Learn more", etc.
- Final re-open pass: clicks any `button[aria-expanded='false']` still remaining after tabs/toggles, as a safety net
- **Carousel card decks** (see below)

```
python notes/scripts/fetch_page.py <url> --slug <slug> --timeout 45000
```

The script saves to `cache/web/<slug>.txt` and prints the path on stdout.

### Accordion pitfall — don't use `[class*='accordion']`

**Never** use a broad selector like `[class*='accordion']:not([aria-expanded='true'])` to click accordions. It matches not just header buttons but also body/container divs (e.g. `blocks-accordion__body`) that have "accordion" in their class but no `aria-expanded` attribute. Clicking those after the header was already opened toggles the accordion back closed, silently losing the content.

**Always** target the trigger element specifically: `button[class*='accordion__header']`, `[class*='accordion__header']:not([aria-expanded='true'])`, or `button[aria-expanded='false']`. Then add a final re-open pass at the end.

### Exclusive tab panels

Some pages use exclusive tab widgets (only one panel visible at a time). Clicking all tabs and then extracting with `inner_text()` captures only the last-clicked panel. The fix is `extract_tab_panels()` in `fetch_page.py`: it temporarily sets each panel's `style.display = 'block'` via JavaScript, reads its `innerText`, then restores the original display value. The captured panels are appended as a `=== Tab Panels ===` section — one panel per `---` separator.

This runs automatically during every fetch. No manual intervention needed.

### Carousel card decks

Some SPAs (e.g. Google Cloud training) show sequential flip-card quizzes where only one card is visible at a time — cards 2–N are in the DOM but hidden by CSS, invisible to `inner_text()`. The fix is in `extract_carousel_cards()`: detects a carousel by the presence of `[aria-label="Go to next slide"]`, then navigates through each card, flips it (`.flashcard-side-flip__btn`), and collects text at each step. The captured cards are appended to the main content as an `=== Knowledge Check Cards ===` section.

**If a ⚠️ Partial capture warning appears in a source note:** don't leave it — delete the cache file, fix the fetch script if needed, and re-fetch. Partial captures rot into permanent gaps.

### Embedded YouTube videos

Some training pages embed a YouTube video alongside a text transcript. The transcript is captured by the fetch script, but the video URL is not. To find it:

```python
# Run in a Playwright session after page load
results = page.evaluate('''() => {
    return [...document.querySelectorAll('iframe')]
        .filter(el => el.src.includes('youtube.com/embed'))
        .map(el => el.src);
}''')
```

Extract the video ID from the `embed/` URL and embed it inline at the point in the Notes section where it's discussed:

```html
<iframe width="720" height="405" src="https://www.youtube.com/embed/<id>" frameborder="0" allowfullscreen></iframe>
```

Place the iframe at the **top of the Notes section**, before the first subsection, so it sits alongside the written walkthrough it accompanies. Do not put the video URL in the frontmatter.

**When to do this:** whenever a YouTube video is embedded in the source page — even if the transcript is captured, the video is useful for UI walkthroughs where seeing the interface matters.

### Content images

The fetch script also extracts content image URLs via `extract_images()`. Images ≥ 200×100 px are collected; data URIs and tiny icons are skipped. They are appended to the cache file as an `=== Images ===` section, one Markdown image tag per line with dimensions noted.

**Always download images locally — never link external URLs directly.** Links rot, the site breaks offline, and notes become incomplete without network access.

**Workflow:**

1. For each meaningful image URL (architecture diagrams, workflow charts, UI screenshots — skip decorative/redundant visuals), download it to `docs/sources/<course-slug>/assets/<slug>/`:

    ```powershell
    New-Item -ItemType Directory -Force "docs/sources/<course-slug>/assets/<slug>"
    Invoke-WebRequest -Uri $url -OutFile "docs/sources/<course-slug>/assets/<slug>/01-breakpoints.gif"
    ```

2. Reference images using **relative paths** and wrap each in a link to itself so the reader can click to enlarge:

    ```markdown
    [![Breakpoints in the cell gutter](assets/notebook-debugger/01-breakpoints.gif)](assets/notebook-debugger/01-breakpoints.gif)
    *Caption describing what the image shows.*
    ```

3. Name files descriptively (`01-breakpoints.gif`, `02-variable-explorer.png`) — not generic names like `image1.png`.

4. Place each image at the logical point in the Notes section where it illustrates the concept — not at the end.

**Before downloading, verify the URL resolves.** Use `WebFetch` on the URL first; if it errors or redirects, tell the user before writing any notes.

## Search result cache

Verified search findings are saved to `cache/search/<slug>.md` so the same web search is never repeated. **Before any web search or WebFetch on a factual question, grep `cache/search/` first.**

```
cache/search/
  adk-python-versions.md         # Python version support, current PyPI version
  adk-v2-breaking-changes.md     # ADK 2.0 breaking changes, current version
  adk-api-server-endpoints.md    # /run and /run_sse endpoint specs + cURL
  adk-non-gcp-deployment.md      # AWS, Databricks, container deployment
  vertex-ai-rename.md            # Vertex AI → Gemini Enterprise Agent Platform
```

**When to save a new cache entry:** after any web search or fetch that yields a verified, reusable finding — version numbers, API specs, renamed services, breaking changes, deployment options. One file per topic, slug describes the topic not the date.

**Cache file format:**

```markdown
# Topic title

**Checked:** YYYY-MM-DD
**Source:** <URL>

## Findings

[Key facts, bullet points or short prose]
```

**When to re-check:** if the checked date is >30 days old and the topic is version-specific (release notes, API specs). Evergreen facts (architecture concepts, protocol specs) rarely expire.

## Answering questions accurately

Before answering any factual question about source content:

1. **Check `cache/search/`** — grep for the topic before making any web request.
2. **Re-read the cache file** — don't rely on memory of what you fetched earlier in the session.
3. **Web search to verify** only if no cache entry exists or the entry is stale (>30 days, version-specific).
4. **Save new findings** to `cache/search/<slug>.md` after any search that yields reusable facts.
5. **Cite sources** — include the URL at the end of any answer that references specific claims.
6. **Mark uncertainty** — use `> ❓ Unverified:` in notes; use "not verified this session" in chat answers.

## Version-aware notes

For sources that reference a specific software version (docs, tutorials, release notes):
1. Note the version covered at the top of the source note.
2. If the current version is known to differ, add a callout:
   > 📌 **Version note:** This source covers v<X>. Current stable is v<Y> as of <date>. Check release notes for changes.
3. Don't rewrite the source's content — just flag what's stale.

## Keeping the site in sync

A source note isn't done until:
- [ ] `docs/sources/<course>/index.md` — lesson row added to the course overview.
- [ ] `docs/sources/index.md` — new row added under the correct course section.
- [ ] `zensical.toml` nav — source file added under the course's nested group (create the group if this is a new course).
- [ ] `docs/index.md` — course listed under Courses (add entry if this is a new course).
- [ ] `docs/topics/index.md` — relevant topics updated (new entries to backlog, or existing topic pages extended).
- [ ] `docs/reference/glossary.md` — new terms added.
- [ ] `docs/reference/resources.md` — any important links added.

## Slugs and naming

- **Source slugs:** short, kebab-case, ideally derived from the source title or domain — `react-server-components`, `postgres-vacuum-internals`, `attention-is-all-you-need`. No dates in slug unless two sources would collide.
- **Topic slugs:** short noun phrase — `concurrency`, `vector-search`, `transformer-architecture`.
- **Cache files:** same slug as the source note — `cache/web/react-server-components.txt`.

## Scaffold templates

### `zensical.toml`
```toml
[project]
site_name = "Research Notes"
site_description = "Personal notes from articles, documentation, papers, and web sources."
site_author = "your@email.com"

nav = [
    { "Home" = "index.md" },
    { "Topics" = [
        { "All Topics" = "topics/index.md" },
    ]},
    { "Notes" = [
        { "All Notes" = "sources/index.md" },
        # Add numbered entries as sources are added:
        # { "1. First Note Title" = "sources/first-slug.md" },
        # { "2. Second Note Title" = "sources/second-slug.md" },
    ]},
    { "Reference" = [
        { "Glossary" = "reference/glossary.md" },
        { "Resources" = "reference/resources.md" },
    ]},
]
```

**Nav convention:** The section is called **Notes** (not Sources). Each note entry is prefixed with its sequence number (`1.`, `2.`, `3.`…) so the reader can navigate in order. Assign numbers in the order notes are added; don't renumber existing entries when adding new ones.

**Documentation-site sources — mirror the source's own navigation.** When a course's sources are pages from a documentation site, reproduce that site's **own navigation tree** in the `zensical.toml` nav instead of a flat numbered list. The docs team's information architecture is almost always better than an ad-hoc one, and it makes notes easy to locate against the live docs.

The principle is fixed. **How you discover that navigation is site-specific** — every docs platform exposes it differently, and some sources expose nothing at all. Do not assume the last site's method works on this one.

### Evidence ladder — find the strongest signal this site offers

Work down this list and stop at the first one that yields a full tree. Record which rung you landed on.

| Rung | Signal | Confidence | Typical of |
|---|---|---|---|
| 1 | **Machine-readable nav payload** — framework JSON embedded in the page or served as a file | Authoritative | `__NEXT_DATA__` (Next.js/Vercel), `__DOCUSAURUS_GLOBAL_DATA__`, `__NUXT__`, Mintlify `docs.json`, GitBook JSON, a `toc.json`/`nav.json` fetched by the page |
| 2 | **Nav config in the docs' own repo** | Authoritative | `mkdocs.yml` `nav:`, Sphinx `toctree`, Docusaurus `sidebars.js`, Antora `nav.adoc`, `SUMMARY.md` (mdBook/GitBook) |
| 3 | **Rendered nav DOM** — not always a *sidebar*; some themes put site nav in a top navbar and give the sidebar to the page's own table of contents | High, if fully expanded | Most static-site generators |
| 4 | **A section index / "In this section" page** listing its children | Medium | AWS, Microsoft Learn, many hand-built docs |
| 5 | **Breadcrumb** | **Low — see the warning below** | Nearly everything |
| 6 | **URL path segments** | Very low | fallback only |
| 7 | Your own invented taxonomy | Never | — |

!!! danger "A breadcrumb is not an information architecture"
    A breadcrumb is a *rendered convenience*. It routinely **truncates levels**, and when a page sits in **two places** in the nav it reports only one — often the reference dump rather than the task-oriented section a reader would actually look under.

    Verified failure (HashiCorp Terraform docs, 2026-07-10): `language/block/provider` breadcrumbs as `Configuration Language › provider`, but the sidebar files it under **Configure providers**. `language/files/dependency-lock` breadcrumbs under `Files and configuration structure` while *also* living under **Configure providers**. Two of nine pages were misfiled before the mismatch was caught.

    Use rung 5 or 6 only when nothing above them exists, say so in the commit, and eyeball the result against the live page.

### Probe the site with `scripts/fetch_nav.py`

The script (in this skill's directory) walks the ladder for you and reports **every** signal it finds, so you can compare rather than trust one blindly:

```
python <skill-dir>/scripts/fetch_nav.py <url-of-any-page-in-the-section>
python <skill-dir>/scripts/fetch_nav.py <url> --all     # show every signal found, not just the best
python <skill-dir>/scripts/fetch_nav.py <url> --json    # raw tree, for scripting
python <skill-dir>/scripts/fetch_nav.py <url> --match <substr>   # flag entries whose href contains substr
```

It always prints a `# nav source:` line naming the rung it used. **Read that line.** It covers rungs 1, 3, and 5 automatically, and scans arbitrary `window.*` globals and embedded `<script type="application/json">` blocks for nav-shaped data, so it is not limited to the frameworks named above. Rungs 2 and 4 are manual — if the script reports a weak rung, check whether the docs are open-source (rung 2) or have a section index page (rung 4) before settling.

When the script finds nothing, that is a real answer: **the source has no navigation to mirror.** Fall back to the numbered-Notes convention and say so.

### Site-specific findings (append as you learn them)

- **developer.hashicorp.com** — rung 1, `__NEXT_DATA__ → props.pageProps.layoutProps.sidebarNavDataLevels`. Breadcrumbs mislead (above). `fetch_page.py` does **not** cache a breadcrumb; the first line of `cache/web/<slug>.txt` is the version selector (`v1.15.x (latest)`). Expanding the sidebar DOM by clicking every `button[aria-expanded='false']` leaves zero collapsed buttons yet still renders group `<li>`s with no children — don't retry it.
- **opentofu.org** — Docusaurus, but no usable global payload; resolves at rung 3, which nests correctly.
- **mkdocs.org** (Bootstrap theme) — the element matching `[class*="sidebar"]` is the **page's table of contents**, all `#anchor` links; the real site nav is a top navbar. A naive "grab the sidebar" probe returns the TOC and looks plausible. The script now rejects any candidate whose links are all anchors, but check the output when a site resolves at rung 3.
- **docs.databricks.com** — Docusaurus. **The breadcrumb is authoritative here — the `danger` box above does not apply.** Docusaurus generates `theme-doc-breadcrumbs` from the same `sidebars.js` that renders the sidebar, so the two cannot disagree. `fetch_page.py` now writes it as a `=== Breadcrumb ===` header line in `cache/web/<slug>.txt`; **use that line directly as the nav path.** (Before that fix the crumbs ran together into an unreadable `Data engineeringLakeflow Spark Declarative PipelinesStandalone pipelinesSchedule refreshes` — easy to skim past, and I did.) `fetch_nav.py` also resolves it at rung 3 (`ul.theme-doc-sidebar-menu`) in ~5s, but only because it now waits for hydration: the sidebar is client-rendered, and the first `<nav>` in the DOM is the top navbar (Support / Knowledge Base / Community), which a pre-hydration probe silently returns instead. **Never run an "expand every collapsed category" pass on this site** — the current page's ancestor chain is already expanded, and the other ~33 categories sit off-screen in the sidebar's own scroll container, so every click fails actionability and burns its full timeout (measured: 6 passes = ~50s, zero new links).

### Rules once you have the tree

- **The nav group = the section in the source's navigation**, not the URL path segment. They often differ — read the real tree, don't infer from the URL.
- **The source's navigation beats conceptual re-grouping — always.** Even if a page feels like it belongs elsewhere, place it exactly where the source puts it, not under a section you invented. Failure mode: filing under "Concepts" or "Reference" when the source already scopes it precisely.
- **When a page appears twice, file it under the task-oriented section**, not the reference dump. HashiCorp lists `provider block reference` under both *Configure providers* and *REFERENCE › Configuration blocks*; the first is where a reader looks. Note the duplication in the commit message.
- **Nest sub-groups to match the source's depth** — but only add an intermediate level when its parent is *itself a captured page* (give that page an `"Overview"` entry, then nest its children under it) **or** the level has **≥2 children**. A level that is pure taxonomy with a single child and no captured overview page stays flat — don't bury one note under an empty header.
- **Label leaf entries with the source's own label**, not a re-invented name.
- **Record the rung** you used in the course's `docs/sources/<course-slug>/index.md`, so a later session regroups from the same signal instead of re-deriving (or silently picking a weaker one).
- **Validate after editing:** `python -c "import tomllib; tomllib.load(open('zensical.toml','rb')); print('TOML OK')"`, confirm every note file appears exactly **once** in nav, then **actually build the site** (`python -c "from zensical import build; build('zensical.toml', clean=False)"`) — a valid TOML nav can still fail to render.

This mirroring rule replaces the flat sequence-numbered list **for documentation-site courses only**. Article, blog, and paper courses have no upstream navigation to mirror, so they keep the numbered-Notes convention above.

### `docs/index.md`
```markdown
# Research Notes

Personal notes from articles, documentation, papers, and web sources.

## Recent additions
<!-- Updated as sources are added -->

## Topics
See [Topics](topics/index.md) for cross-source synthesis.

## All sources
See [Sources](sources/index.md) for the full source log.
```

### `docs/topics/index.md`
```markdown
# Topics

Cross-source notes synthesizing multiple sources on the same topic.

## Active topic pages
<!-- Topic pages with ≥2 sources -->

## Backlog
Topics to write once a second source covers them:
- <topic> — currently from: [[source-slug]]
```

### `docs/sources/index.md`
```markdown
# Sources

| Title | Type | Added | Tags | URL/File |
|---|---|---|---|---|
```

### `docs/reference/glossary.md`
```markdown
# Glossary

| Term | Definition | Source |
|---|---|---|
```

### `docs/reference/resources.md`
```markdown
# Resources

| Title | URL | Notes |
|---|---|---|
```

## Docker Compose setup

Every new project gets Docker Compose so the site can run without a local Python install.
Create these four files at the project root alongside `zensical.toml`.

### `serve.py`

```python
import glob as _glob
import os
from livereload import Server

import zensical.config as _zc


def _make_wikilink_resolver(docs_dir):
    # Resolve [[slug]] by scanning docs/ recursively for <slug>.md.
    # Allows source files to live in course subdirectories without breaking
    # cross-references when files are reorganised.
    def build_url(label, base, end):
        slug = label.strip().replace(" ", "-").lower()
        matches = _glob.glob(
            os.path.join(docs_dir, "**", f"{slug}.md"), recursive=True
        )
        if matches:
            rel = os.path.relpath(matches[0], docs_dir).replace("\\", "/")
            return "/" + rel[:-3] + "/"
        return f"/sources/{slug}/"
    return build_url


_docs_dir = os.path.join(os.path.dirname(os.path.abspath("zensical.toml")), "docs")

# Patch the module-level build_url in the wikilinks extension directly.
# Passing build_url via the config dict is unreliable — Zensical may not
# forward callables through its config pipeline. Patching the module function
# is the only way to guarantee it's picked up regardless of how the extension
# is initialised internally.
import markdown.extensions.wikilinks as _wikilinks_ext
_wikilinks_ext.build_url = _make_wikilink_resolver(_docs_dir)

# Monkey-patch DEFAULT_MARKDOWN_EXTENSIONS to add [[slug]] wiki-link support.
# Must happen before importing zensical.build so the patch is in effect when
# Rust calls back into parse_zensical_config().
_zc.DEFAULT_MARKDOWN_EXTENSIONS["wikilinks"] = {
    "base_url": "/sources/",
    "end_url": "/",
}

from zensical import build as _zensical_build

_CONFIG_FILE = os.path.abspath("zensical.toml")


def build():
    _zensical_build(_CONFIG_FILE, {"clean": False, "strict": False})


build()  # initial build on startup

server = Server()
server.watch("docs/", build)
server.watch("zensical.toml", build)
server.serve(root="site", port=8000, host="0.0.0.0")
```

**Why this works:** Zensical's build loop is in Rust but calls back into Python's `parse_zensical_config()` which reads `DEFAULT_MARKDOWN_EXTENSIONS` as the default when `markdown_extensions` is not set in `zensical.toml`. Patching the dict before calling `build()` makes wikilinks active without losing the ~20 default pymdownx extensions.

**Why patch the module, not the config dict:** Passing `build_url` as a callable via the `DEFAULT_MARKDOWN_EXTENSIONS` config dict is unreliable — Zensical may not forward callables through its config pipeline. Patching `markdown.extensions.wikilinks.build_url` at the module level guarantees the resolver is used regardless of how the extension is initialised internally.

**Effect:** `[[slug]]` in any `.md` file resolves to the correct URL regardless of which course subdirectory the file lives in. All cross-references remain stable when files are reorganised.

`zensical serve` uses inotify/watchdog which doesn't receive events from Docker volume mounts on Windows (Docker Desktop + WSL2). `livereload` polls the filesystem instead and works on all platforms.

### `Dockerfile`

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir "zensical>=0.0.30,<0.1" livereload

COPY serve.py /app/serve.py

EXPOSE 8000
CMD ["python", "serve.py"]
```

### `docker-compose.yml`

```yaml
services:
  docs:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: research-notes-docs
    ports:
      - "8000:8000"
    volumes:
      - ./zensical.toml:/app/zensical.toml
      - ./docs:/app/docs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request,sys;sys.exit(0 if urllib.request.urlopen('http://localhost:8000', timeout=3).status==200 else 1)"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 20s
```

### `.dockerignore`

```
.venv/
__pycache__/
*.pyc
site/
.zensical/
.git/
.vscode/
.idea/
.DS_Store
Thumbs.db
cache/
scripts/
```

### `.gitignore`

```
site/
.zensical/
.venv/
__pycache__/
*.pyc
.vscode/
.idea/
.DS_Store
Thumbs.db
cache/
```

**To run:** `docker compose up` then open http://localhost:8000. Edits to `docs/` live-reload.

---

## PDF intake workflow

The user drops PDFs into `C:\opt\learn\agent\take-note` and says "take note". Process all PDFs found there, then move each one to `C:\opt\learn\agent\pdf` when done.

**Steps for each PDF found in `take-note\`:**

1. Derive a slug from the filename (lowercase, spaces → hyphens, drop extension).
2. Check `cache/pdf/<slug>.txt` — if present, read directly and skip extraction.
3. If cache is missing, extract using pymupdf (in the `notes-fetch` conda env):
   ```python
   & "C:\Users\arind\miniforge3\envs\notes-fetch\python.exe" -c "
   import pymupdf, pathlib
   doc = pymupdf.open(r'<path-to-pdf>')
   text = '\n'.join(page.get_text('text') for page in doc)
   pathlib.Path(r'C:\opt\learn\agent\notes\cache\pdf\<slug>.txt').write_text(text, encoding='utf-8')
   print(f'Extracted {len(text)} chars, {len(doc)} pages')
   "
   ```
4. Write the source note to `docs/sources/<course-slug>/<slug>.md`.
5. Update course index, source log, nav, glossary, topics backlog — same as any other source.
6. Move the PDF: `Move-Item "<take-note\file.pdf>" "C:\opt\learn\agent\pdf\"`.

**Paths:**
- Intake folder: `C:\opt\learn\agent\take-note\`
- Archive folder: `C:\opt\learn\agent\pdf\`
- Notes project: `C:\opt\learn\agent\notes\`
- PDF cache: `C:\opt\learn\agent\notes\cache\pdf\`

---

## Anti-patterns to avoid

- **Don't use a summarizing WebFetch prompt.** Always ask for verbatim content. A prompt like "what does this page cover?" silently drops caveats, fallback conditions, and qualifications that are often the most important detail. Use the exhaustive verbatim prompt in step 2 above.
- **Don't dump raw fetched text** into the notes. Summarize and paraphrase — but only *after* you have captured all verbatim detail from the fetch. Compress for readability; never compress away conditions or fallbacks.
- **Don't re-fetch a URL if the cache exists.** Check `cache/web/<slug>.txt` first.
- **Don't re-extract a PDF if the cache exists.** Check `cache/pdf/<slug>.txt` first.
- **Don't create topic pages with only one source.** Put them in the backlog.
- **Don't skip the source log update.** It's how you track what's been captured.
- **Don't write topic pages without cross-links.** Source notes and topic pages must link to each other bidirectionally.
- **Don't assert version-specific facts from training data.** Web-search to verify.
- **Don't include unverified URLs in notes.** Check every link with `WebFetch` before writing it.
- **Don't link images from external URLs.** Always download to `docs/sources/<course-slug>/assets/<slug>/` and reference with a relative path. External image links rot and break the site offline.
- **Don't leave ⚠️ Partial capture warnings in notes permanently.** Delete the cache file, fix the fetch script if needed, re-fetch, and update the note. A partial capture that stays in the notes becomes a permanent gap.
