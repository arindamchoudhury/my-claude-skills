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

## Note style for a source file

Each `docs/sources/<slug>.md` has this structure:

```markdown
# <Title>

> **Source:** [<display URL or filename>](<URL>)
> **Added:** YYYY-MM-DD
> **Source updated:** YYYY-MM-DD
> **Tags:** tag1, tag2, tag3
> **Type:** article | documentation | paper | blog | other

## Summary
One paragraph — the core argument or main takeaway of the source.

## Key points
- Bullet list of the most important ideas, claims, or findings.
- Keep each bullet concise; expand in sub-bullets only when needed.

## Notes
Structured prose or subsections mirroring the source's own sections.
Use headers (`###`) for major sections worth separating.

## Quotes worth keeping
> "Exact quote from the source." (section or page reference)

## Open questions
- Things this source raised but didn't answer.
- Contradictions with other sources.

## Related sources
- [[other-slug]] — one-line note on the relationship
```

**Style rules:**
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
- **Use the Related sources section for cross-links**, not just as a list — annotate *how* the sources relate (confirms, contradicts, extends, provides detail for, zooms out from).

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

**Documentation-site sources — group nav by the page's own breadcrumb.** When a course's sources are pages from a documentation site (Databricks, AWS, Google Cloud, etc.), each page carries a breadcrumb at the top (e.g. `Tables › Table types › External tables`). Mirror that breadcrumb in the `zensical.toml` nav instead of a flat numbered list — the docs team's own information architecture is almost always better than an ad-hoc one, and it makes notes easy to locate against the live docs.

Rules:

- **The nav group = the breadcrumb root**, not the URL path segment. They often differ — read the real breadcrumb, don't infer from the URL. (Examples seen on Databricks: every `…/optimizations/*` page breadcrumbs under **Tables › Optimization and performance**; the Spark-UI troubleshooting pages under `…/optimizations/spark-ui-guide/*` breadcrumb under **Compute › Classic compute › Troubleshoot**.)
- **Capture the breadcrumb when you fetch.** `fetch_page.py` saves it as the first line of `cache/web/<slug>.txt` (segments concatenated, e.g. `TablesTable typesExternal tables`). To regroup an existing course, read the first line of every cache file at once: `for f in cache/web/*.txt; do echo -n "${f}:: "; head -1 "$f"; done`.
- **Nest sub-groups to match breadcrumb depth** — but only add an intermediate level when its parent is *itself a captured page* (give that page an `"Overview"` entry, then nest its children under it) **or** the level has **≥2 children**. A breadcrumb level that is pure taxonomy with a single child and no captured overview page stays flat — don't bury one note under an empty header.
- **Label leaf entries by the breadcrumb leaf** (the page's own title), not a re-invented name.
- **Validate after editing:** `python -c "import tomllib; tomllib.load(open('zensical.toml','rb')); print('TOML OK')"`, then confirm every note file still appears exactly once in nav.

This breadcrumb-grouping rule replaces the flat sequence-numbered list **for documentation-site courses only**. Article/blog/paper courses keep the numbered-Notes convention above.

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
