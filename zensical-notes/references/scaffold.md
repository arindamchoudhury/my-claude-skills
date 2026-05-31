# Scaffolding a fresh Zensical notes site

The **multi-book hybrid layout is the default**. Use these templates to bootstrap any new project. They produce a working site that runs immediately with `zensical serve` (or `docker compose up`) and follows the conventions the rest of this skill assumes.

Replace anything in `<angle-brackets>` with the real value before writing the file.

---

## Multi-book layout (default)

### `zensical.toml`

```toml
[project]
site_name = "<Topic> — Reading Notes"
site_description = "Personal study notes on <topic>, drawing on multiple books."
site_author = "<User name or handle>"
copyright = "Copyright © <Year> <User>. Notes are personal study summaries."

nav = [
    { "Home" = "index.md" },
    { "Topics" = [
        { "Topic index" = "topics/index.md" },
        # Active topic pages get added here as they're written, e.g.:
        # { "Architecture" = "topics/architecture.md" },
        # { "MVCC" = "topics/mvcc.md" },
    ]},
    { "Books" = [
        { "<Author> (<Year>)" = [
            { "Reading log" = "books/<slug>/index.md" },
            { "1. <Chapter 1 title>" = "books/<slug>/chapters/01-<slug>.md" },
            { "2. <Chapter 2 title>" = "books/<slug>/chapters/02-<slug>.md" },
            # … one per chapter
        ]},
        # Second book added here when the time comes:
        # { "<Author2> (<Year>)" = [
        #     { "Reading log" = "books/<slug2>/index.md" },
        #     …
        # ]},
    ]},
    { "Reference" = [
        { "Glossary"  = "reference/glossary.md" },
        { "Resources" = "reference/resources.md" },
    ]},
]

# Math rendering — include MathJax if the notes contain equations.
# arithmatex (which processes $...$ and $$...$$) is built into Zensical's
# defaults; you just need the JavaScript to actually render it in the browser.
extra_javascript = [
    "javascripts/mathjax.js",
    {path = "https://unpkg.com/mathjax@3/es5/tex-mml-chtml.js", defer = true},
]

# NOTE: [project.theme] is intentionally omitted. Zensical 0.0.x ships only its
# default theme by name; setting name = "modern" or "classic" causes a
# "Theme '<x>' is not installed" error in current releases. Once Zensical 0.1+
# ships, you can add e.g.:
#
#   [project.theme]
#   name = "modern"
#   language = "en"
```

If the book has no math, omit `extra_javascript` entirely (no cost to leaving it in though).

For books with many chapters, group them into parts using nested arrays — but only if the book itself is structured that way:

```toml
{ "<Author> (<Year>)" = [
    { "Reading log" = "books/<slug>/index.md" },
    { "Part I — Getting Started" = [
        { "1. <…>" = "books/<slug>/chapters/01-<slug>.md" },
        { "2. <…>" = "books/<slug>/chapters/02-<slug>.md" },
    ]},
    { "Part II — Advanced" = [
        { "3. <…>" = "books/<slug>/chapters/03-<slug>.md" },
    ]},
]},
```

### `docs/index.md` (hub page)

```markdown
# <Topic> — Reading Notes

A growing personal study site for **<topic>**, drawing on multiple books.

## Topics

Cross-book synthesis — each page distills how multiple books treat the same topic.

- [Topic index](topics/index.md)

_(Topic pages appear here once ≥2 books cover the same ground.)_

## Books

- [<Author(s)> — *<Book title>* (<Year>)](books/<slug>/index.md)

## Reference

- [Glossary](reference/glossary.md)
- [Resources](reference/resources.md)
```

### `docs/topics/index.md`

```markdown
# Topics

Cross-book synthesis — each page distills how multiple books treat the same topic.

## Active topic pages

_(None yet — topic pages are written once ≥2 books cover the same ground.)_

## Single-source backlog (waiting for a second book)

- **<Topic>** — <Author> Ch <N> only. *(Add a second source to write this page.)*
```

The "single-source backlog" is updated after every chapter. When a second book covers a backlogged topic, promote it to an active topic page.

### `docs/books/<slug>/index.md` (per-book reading log)

```markdown
# <Book Title> — Reading Log

> <Authors> (<Year>). *<Full title with subtitle>* (<edition>). <Publisher>. ISBN <…>.

| Status | Chapter | Topic page(s) |
| ------ | ------- | ------------- |
| ⬜ todo | 1. <Chapter 1 title> | — |
| ⬜ todo | 2. <Chapter 2 title> | — |
| ⬜ todo | 3. <Chapter 3 title> | — |
| … | … | … |

## Conventions

- **Concepts** are introduced as short, declarative bullets.
- **Commands / syntax** appear in fenced code blocks.
- **Open questions** are marked with `> ❓`.
- **Version-adapted content** is flagged with a 📌 callout at the top of each chapter.
```

Flip `⬜ todo` to `✅ done` and fill in the "Topic page(s)" column as chapters are completed.

### `docs/books/<slug>/chapters/<NN>-<slug>.md` (placeholder)

For every chapter not yet studied, create a placeholder so navigation works from day one:

```markdown
# Chapter <N> — <Chapter Title>

> *Source: <Authors> (<Year>), Chapter <N>.*
>
> Notes pending — this chapter hasn't been studied yet.

## Outline placeholder

- [ ] Read the chapter
- [ ] Capture key concepts
- [ ] Note new commands / syntax
- [ ] Record open questions

## References

_(to be added)_
```

### `docs/reference/glossary.md`

In multi-book mode, every term carries a source attribution. Once the glossary grows past ~30 entries, group by initial letter (`## A`, `## B`, …).

```markdown
# Glossary

A running glossary of terms across all books. Each entry is attributed to its source.

## From <Author> (<Year>)

| Term | Meaning | Source |
| --- | --- | --- |
| <Term> | <Short, standalone definition.> | <Author> Ch <N> |
```

When two books define a term differently, keep both rows and attribute each — different definitions usually reflect different lenses on the same idea.

### `docs/reference/resources.md`

```markdown
# Resources

Links collected from all books — a single place to find them later.

## Official <Topic> docs

- <Title> — <https://…>

## Tooling

- <Tool name> — <https://…>

## Books

- <Author> (<Year>): source code — <https://…>
```

---

## `README.md` (project root)

```markdown
# <Topic> — Reading Notes

A [Zensical](https://zensical.org/) static site built from personal study notes on <topic>.

## Run with Docker (recommended)

```bash
docker compose up
# open http://localhost:8000
```

`zensical.toml` and `docs/` are bind-mounted, so edits live-reload.

## Run locally with Python

```bash
python -m venv .venv
. .venv/Scripts/Activate.ps1   # macOS/Linux: source .venv/bin/activate
pip install zensical
zensical serve
```

## Adding a new chapter's notes

1. Edit `docs/books/<slug>/chapters/<NN>-<slug>.md`.
2. Nav is already wired in `zensical.toml`.
3. Flip the row to ✅ in `docs/books/<slug>/index.md`.
4. Update `docs/topics/index.md` backlog with any topics the chapter touches.
```

---

## `serve.py`

`zensical serve` uses watchdog/inotify for file watching, which does not receive events from Docker volume mounts on Windows (Docker Desktop + WSL2). Use `livereload` instead — it polls the filesystem and works on all platforms.

```python
import subprocess
from livereload import Server


def build():
    subprocess.run(["zensical", "build"], check=True)


build()  # initial build on startup

server = Server()
server.watch("docs/", build)
server.watch("zensical.toml", build)
server.serve(root="site", port=8000, host="0.0.0.0")
```

## `Dockerfile`

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Zensical is pre-1.0 (0.0.x); pin under 0.1 to avoid surprises if a 0.1
# breaking release lands.
RUN pip install --no-cache-dir "zensical>=0.0.30,<0.1" livereload

COPY serve.py /app/serve.py

EXPOSE 8000
CMD ["python", "serve.py"]
```

## `docker-compose.yml`

```yaml
services:
  docs:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: <project-slug>-docs
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

## `.dockerignore`

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
node_modules/
```

## `.gitignore`

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
```

---

## After scaffolding

Tell the user the site is ready and how to run it. Then proceed straight into whichever chapter they asked for using `note-style.md` as the guide. Remind them that topic pages live in the backlog until a second book covers the same ground.

---

## Single-book layout (legacy / explicitly requested only)

Use this *only* when the user explicitly asks for the simpler layout or is maintaining an existing single-book project they don't want to migrate.

### `zensical.toml` (single-book)

```toml
[project]
site_name = "<Book Title> — Reading Notes"
site_description = "Detailed reading notes on <Book Title> by <Authors> (<Publisher>, <Year>)."
site_author = "<User name or handle>"
copyright = "Copyright © <Year> <User>. Notes summarize concepts from <Book Title> by <Authors> (<Publisher>, <Year>)."

nav = [
    { "Home" = "index.md" },
    { "Chapters" = [
        { "1. <Chapter 1 title>" = "chapters/01-<slug>.md" },
        { "2. <Chapter 2 title>" = "chapters/02-<slug>.md" },
    ]},
    { "Reference" = [
        { "Glossary"  = "reference/glossary.md" },
        { "Resources" = "reference/resources.md" },
    ]},
]
```

### `docs/index.md` (single-book)

```markdown
# <Book Title> — Reading Notes

Detailed reading notes for **<Book Title>** by <Authors> (<Publisher>, <Year>).

## Reading log

| Status | Chapter |
| ------ | ------- |
| ⬜ todo | 1. <Chapter 1 title> |
| ⬜ todo | 2. <Chapter 2 title> |

## About the source book

> <Authors> (<Year>). *<Full title with subtitle>* (<edition>). <Publisher>. ISBN <…>.
```
