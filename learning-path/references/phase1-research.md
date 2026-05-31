# Phase 1 — Research, Scaffold & Topic Skill Generation

## Step 1: Research books

Run these searches (substitute `<topic>`):

```
"best books on <topic> 2026 table of contents"
"<topic> book site:oreilly.com OR site:manning.com OR site:packtpub.com 2024 2025 2026"
"<topic> book amazon table of contents chapters"
```

For each of the top 3–5 books found:
- Fetch the publisher/Amazon page and extract the full chapter list
- Note: what comes first (foundations), what comes last (production/advanced)
- Note: what topics appear in EVERY book (must-covers) vs only some

From this, derive the **progression arc** — the natural learning order for this topic.

## Step 2: Research courses

```
"best <topic> courses 2026 Udemy Coursera"
"<topic> official course OR academy OR tutorial 2026"
```

Also check for official learning platforms:
- LangChain → academy.langchain.com
- Databricks → customer-academy.databricks.com
- AWS → aws.amazon.com/training
- Google Cloud → cloudskillsboost.google.com

For each top course, note: module names, number of modules, hands-on labs.

## Step 3: Validate current version

```
"<topic main package> latest version pypi 2026"
"<topic> release notes changelog 2026"
```

Fetch the official documentation home page. Note:
- Current stable version
- Any major breaking changes in the last 12 months
- Whether any of the found books/courses target a version that's now outdated

## Step 4: Scaffold notes folder

Create the full structure at `C:\opt\learn\<topic-slug>\notes\`:

### zensical.toml
```toml
[project]
site_name = "<Topic> Learning Notes"
site_description = "Personal notes and book from learning <topic>."
site_author = "arindam@live.com"

nav = [
    { "Home" = "index.md" },
    { "Learning Path" = "learning-path.md" },
    { "Book" = [
        { "Contents" = "book/index.md" },
    ]},
    { "Sources" = [
        { "All Sources" = "sources/index.md" },
    ]},
    { "Reference" = [
        { "Glossary" = "reference/glossary.md" },
        { "Resources" = "reference/resources.md" },
    ]},
]
```

### serve.py, Dockerfile, docker-compose.yml, .gitignore
Copy verbatim from `C:\opt\learn\langchain\notes\` — these are topic-agnostic.

### .env template
```dotenv
SITE_EMAIL=
SITE_PASSWORD=
```

### scripts\fetch_page.py
Copy verbatim from `C:\opt\learn\langchain\notes\scripts\fetch_page.py`.
Uses nodriver (Chrome CDP) to bypass Cloudflare. Reads credentials from `.env`.

### Initial docs

**docs\index.md**
```markdown
# <Topic> Learning Notes

Personal notes and book built while learning <topic>.

## Book
See [Book Contents](book/index.md) for chapters written as I learn.

## Learning Path
See [Learning Path](learning-path.md) for the recommended study order.

## Sources
See [Sources](sources/index.md) for notes from individual books and courses.
```

**docs\book\index.md**
```markdown
# Book: <Topic>

Chapters written as I complete each course module or book chapter.

| # | Chapter | Source | Added |
|---|---|---|---|
```

**docs\sources\index.md**
```markdown
# Sources

| Title | Type | Added | Tags | URL/File |
|---|---|---|---|---|
```

**docs\reference\glossary.md**
```markdown
# Glossary

| Term | Definition | Source |
|---|---|---|
```

**docs\reference\resources.md**
```markdown
# Resources

| Title | URL | Notes |
|---|---|---|
```
Populate with the official docs, top book links, and course links found in Step 1–2.

## Step 5: Auto-generate topic book skill

Create `C:\Users\arind\.claude\skills\<topic>-book\SKILL.md`.

The skill must include:

1. **YAML frontmatter** — name: `<topic>-book`, description triggering on book/chapter writing requests for this topic
2. **Proven chapter arc** — derived from the TOC research (what order to cover topics)
3. **Standard chapter template** (see below)
4. **Code standards** — current version imports and patterns for the technology
5. **Current package versions** — verified in Step 3
6. **Key patterns** — the 3–5 patterns every book on this topic covers
7. **Anti-patterns** — common mistakes seen across the books researched

### Standard chapter template (embed in the generated skill)
```markdown
# Chapter N: <Title>

> **Source:** [Course/Book — Module/Chapter]
> **Version:** <tech version>
> **Added:** YYYY-MM-DD

## What you'll learn
## The problem this solves
## Core concept
## Code examples
## Common pitfalls
## Exercises
## Summary
```

### Code standards rule to embed
- All imports complete and runnable
- Load env vars with `load_dotenv()` when using API keys
- Pin version in comment: `# <package> <version>`
- Never truncate code with `# ... rest of code`

## Step 6: Announce completion

Tell the user:
- Notes site scaffolded at `C:\opt\learn\<topic-slug>\notes\`
- Topic book skill created: `<topic>-book`
- Run `docker compose up` in the notes folder to browse at http://localhost:8000
- Moving to Phase 2: building the learning path
