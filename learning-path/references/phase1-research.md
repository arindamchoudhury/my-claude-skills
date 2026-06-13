# Phase 1 — Research, Scaffold & Topic Skill Generation

Phase 1 has two goals: (1) understand the full topic landscape deeply enough to produce a good taxonomy, and (2) set up the notes site. Do not skip steps — the quality of Phase 2 depends entirely on the depth of research here.

---

## Step 1: Research the topic taxonomy

The taxonomy is the backbone of Phase 2. Derive it from multiple sources so it reflects what the field actually requires — not just what one book covers.

**Search for curricula from certification exams:**
```
"<topic> certification exam topics syllabus 2025 2026"
"<topic> associate professional exam guide topics percentage"
```
Certification exam guides list exactly which topics are tested and at what weight. This is the most reliable signal for what matters.

**Search for university and MOOC syllabi:**
```
"<topic> university course syllabus topics weeks 2024 2025"
"<topic> Coursera edX course modules topics 2025"
"<topic> MIT Stanford Berkeley course topics"
```
Cross-check 2–3 syllabi. Topics that appear in all of them are must-covers.

**Search for job descriptions:**
```
"<topic> engineer job description required skills 2025"
"senior <topic> developer skills requirements"
```
Job descriptions reveal which topics employers test for — useful for separating foundational from advanced.

**From this research, produce a topic list** — every distinct concept, skill, or technique that a person must learn to be competent in the subject. Aim for 25–50 topics total. Examples from PySpark: "DataFrame API basics", "window functions", "Catalyst optimizer", "Structured Streaming watermarking", "Delta Lake MERGE INTO", "Dagster assets".

**Classify each topic by level:**

| Level | Signal |
|---|---|
| **Beginner** | Covered in every intro course; required to write a first working program |
| **Intermediate** | Covered in most full courses; required to build real production pipelines |
| **Advanced** | Covered in certification exams and senior job descriptions; requires prior topics |
| **Expert** | Covered in advanced courses and architecture discussions; requires all prior levels |

Topics must form a **dependency graph** — if topic B requires knowing topic A, A is a lower level than B. Follow the dependency order, not prestige of the resource.

---

## Step 2: Research books

```
"best books on <topic> 2024 2025 2026 table of contents"
"<topic> book site:oreilly.com OR site:manning.com OR site:packtpub.com"
```

For each of the top 3–5 books:
- Fetch the publisher page and extract the **full chapter list**
- Note which topics from your taxonomy each book covers well
- Note version — is it targeting a current or outdated release?

Books are **reference material for the "Learn it with" advice per topic** — not the organizing principle.

---

## Step 3: Research courses (all types)

### Official academies and docs
Every major technology has one. Search specifically:
```
"<technology> official training academy certification course 2025"
```
Examples: Databricks Academy, LangChain Academy, AWS Training, Google Cloud Skills Boost, Dagster University.

### University MOOCs
```
"<topic> edX Coursera university course 2025 full syllabus"
"MIT Stanford Berkeley Carnegie Mellon <topic> open course"
```
Fetch the syllabus/module list for any promising hit. Note: hours per module.

### Video courses (Udemy, YouTube)
```
"best <topic> Udemy course 2025 syllabus curriculum"
"<topic> free YouTube course playlist hours"
```
For each top result, get the **section/module list** — not just the title. The curriculum reveals which topics it covers and at what depth.

### Interactive platforms
DataCamp, Codecademy, Kaggle, Mode Analytics, etc. — note which ones have tracks for this topic.

For each course found, record:
- What topics from your taxonomy it covers
- At what depth (intro / practical / deep)
- Approximate hours
- Whether it's current (within 1–2 major versions)
- Whether it's hands-on (exercises, labs) or lecture-only

---

## Step 4: Research certifications

```
"<topic> certification 2025 2026 exam guide topics"
"<topic> professional associate certification comparison"
```

For each certification found:
- Exact exam topics and percentage weights (fetch the official exam guide page)
- Prerequisites or recommended experience
- Fee and format (questions, time limit)
- Which level it maps to (Beginner exit / Intermediate exit / Advanced exit / Expert)
- Prep resources officially recommended

Certifications serve as **level checkpoints** in Phase 2 — placed at the end of the level whose topics they validate.

---

## Step 5: Validate current version

```
"<topic main package> latest version pypi 2026"
"<topic> changelog release notes 2025 2026"
```

Note:
- Current stable version
- Any major breaking changes in the past 12 months
- Whether any found books/courses target a version now more than one major behind

---

## Step 6: Scaffold notes folder

Create the full structure at `C:\opt\learn\<topic-slug>\notes\`:

### zensical.toml
```toml
[project]
site_name = "<Topic> Learning Notes"
site_description = "Personal notes and book from learning <topic>."
site_author = "arindam@live.com"
extra_css = ["stylesheets/extra.css"]
extra_javascript = ["javascripts/sidebar-toggle.js"]

nav = [
    { "Home" = "index.md" },
    { "Learning Path" = "learning-path.md" },
    { "Book" = [
        { "Contents" = "book/index.md" },
    ]},
    { "Reference" = [
        { "Glossary" = "reference/glossary.md" },
        { "Resources" = "reference/resources.md" },
    ]},
]
```

### docs/stylesheets/extra.css
```css
/* Sidebar collapse — sticky so panels float while main content scrolls */
.md-sidebar {
  position: sticky;
  top: 0;
  align-self: flex-start;
  transition: width 0.2s ease, min-width 0.2s ease;
}

.md-sidebar__scrollwrap {
  visibility: visible;
  opacity: 1;
  transition: visibility 0.2s, opacity 0.2s;
}

.md-sidebar.is-collapsed {
  width: 1.4rem !important;
  min-width: 1.4rem !important;
  overflow: hidden;
}

.md-sidebar.is-collapsed .md-sidebar__scrollwrap {
  visibility: hidden;
  opacity: 0;
}

/* Toggle button */
.sidebar-toggle {
  position: absolute;
  top: 0.6rem;
  z-index: 10;
  background: none;
  border: none;
  padding: 0.1rem 0.3rem;
  cursor: pointer;
  font-size: 0.85rem;
  color: var(--md-default-fg-color--light);
  line-height: 1;
}

.sidebar-toggle:hover {
  color: var(--md-accent-fg-color);
}

.md-sidebar--primary .sidebar-toggle { right: 0; }
.md-sidebar--secondary .sidebar-toggle { left: 0; }
```

### docs/javascripts/sidebar-toggle.js
```javascript
(function () {
  function setup(sidebar, storageKey, collapseChar, expandChar) {
    var btn = document.createElement('button');
    btn.className = 'sidebar-toggle';
    btn.title = 'Toggle sidebar';

    var collapsed = localStorage.getItem(storageKey) === '1';
    if (collapsed) sidebar.classList.add('is-collapsed');
    btn.textContent = collapsed ? expandChar : collapseChar;

    btn.addEventListener('click', function () {
      var nowCollapsed = sidebar.classList.toggle('is-collapsed');
      localStorage.setItem(storageKey, nowCollapsed ? '1' : '0');
      btn.textContent = nowCollapsed ? expandChar : collapseChar;
    });

    sidebar.prepend(btn);
  }

  document.addEventListener('DOMContentLoaded', function () {
    var nav = document.querySelector('.md-sidebar--primary');
    var toc = document.querySelector('.md-sidebar--secondary');
    if (nav) setup(nav, 'sidebar-nav-collapsed', '◀', '▶');
    if (toc) setup(toc, 'sidebar-toc-collapsed', '▶', '◀');
  });
})();
```

Copy `serve.py`, `Dockerfile`, `docker-compose.yml`, `.gitignore` verbatim from an existing project — these are topic-agnostic.

---

## Step 7: Auto-generate topic book skill

Create `C:\Users\arind\.claude\skills\<topic>-book\SKILL.md`.

The skill must include:
1. **YAML frontmatter** — name: `<topic>-book`, trigger description
2. **Full chapter arc** — all topics from the taxonomy, numbered as chapters, grouped by level
3. **Chapter writing guidance — NOT a fixed template.** Give the book skill a short set of *invariants* every chapter must satisfy (motivate why the topic matters; teach toward the learning-path milestone; current runnable code; end pointing forward) plus a *toolkit* of optional elements it can draw from (learning outcomes, motivating problem, core-concept prose, worked examples, Mermaid diagrams, reference tables, semantics/edge-case sections, pitfalls, performance notes, exercises, summary, references). State explicitly that chapter structure adapts to the topic type — a setup chapter, an API-family chapter, an architecture chapter, and a tuning chapter each take a different shape. A chapter is fit to its topic, not poured into fixed headings.
4. **Code standards** — current version imports and patterns
5. **Current package versions** — verified in Step 5
6. **Key patterns** — the 5–8 patterns every practitioner needs
7. **Anti-patterns** — common mistakes to never write

The chapter arc maps directly from the taxonomy: one chapter per topic, chapters numbered sequentially across all four levels.

---

## Step 8: Announce and move to Phase 2

Tell the user:
- Notes site scaffolded at `C:\opt\learn\<topic-slug>\notes\`
- Topic book skill created: `<topic>-book`
- N topics identified across 4 levels
- Moving to Phase 2: building the learning path
