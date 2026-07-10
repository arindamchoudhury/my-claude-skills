"""
fetch_nav.py — discover a documentation site's own navigation tree.

Usage:
    python fetch_nav.py <url> [--all] [--json] [--timeout <ms>] [--match <substr>]

Why this exists:
    Notes nav should mirror the source site's own information architecture.
    But every docs platform exposes that architecture differently, and some
    sources expose none at all. This script probes the site and reports what
    it actually found, rather than assuming one platform's convention.

Evidence ladder (see SKILL.md). The script covers rungs 1, 3 and 5:

    1. machine-readable nav payload   (authoritative)
       - window.__NEXT_DATA__            Next.js / Vercel-hosted docs
       - window.__DOCUSAURUS_GLOBAL_DATA__
       - window.__NUXT__ and any other window.* global holding nav-shaped data
       - <script type="application/json"> blocks embedded in the page
    2. nav config in the docs' repo    (authoritative, MANUAL — mkdocs.yml,
       sidebars.js, toctree, SUMMARY.md)
    3. rendered nav DOM                (high confidence if fully expanded; may be a
                                        top navbar, not a sidebar)
    4. section index page              (medium, MANUAL)
    5. breadcrumb                      (LOW — truncates levels, hides the fact
                                        that a page can sit in two places)
    6. URL path segments               (very low, not attempted here)

    Rungs 2 and 4 are manual: if this script only reaches rung 3 or below,
    check whether the docs are open-source, or have a section index page,
    before settling for a weak signal.

    Always read the "# nav source:" line in the output. If it names rung 5,
    treat the result as low confidence and verify against the live page.

Known site quirks:
    - developer.hashicorp.com: breadcrumbs disagree with the sidebar. Clicking
      every button[aria-expanded='false'] leaves zero collapsed buttons yet
      still renders group <li>s with no children, so the DOM path is useless
      there. The __NEXT_DATA__ payload is the only reliable source.

Requirements:
    pip install playwright
"""

import argparse
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

# Nav labels routinely contain non-cp1252 characters. Without this, printing a
# tree on a Windows console dies with UnicodeEncodeError partway through.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not Path(CHROME_PATH).exists():
    CHROME_PATH = None

# Keys whose values look like a navigation tree.
NAV_KEYS = (
    "sidebarNavDataLevels",
    "navData",
    "navNodes",
    "navLevels",
    "sidebar",
    "sidebars",
    "docsSidebars",
    "navigation",
    "toc",
    "tableOfContents",
)

# Keys under which a node's children may hang.
CHILD_KEYS = ("routes", "items", "children", "menuItems", "links", "pages")

# Keys that carry a node's visible label / target.
LABEL_KEYS = ("title", "heading", "label", "name", "text")
HREF_KEYS = ("path", "href", "url")  # NOT "id": group nodes carry synthetic ids


def _hunt(node, path, found, depth=0):
    """Recursively locate nav-shaped structures anywhere in a JSON blob."""
    if depth > 30:
        return
    if isinstance(node, dict):
        for k, v in node.items():
            if k in NAV_KEYS and isinstance(v, (list, dict)) and v:
                found.append((f"{path}.{k}", v))
            _hunt(v, f"{path}.{k}", found, depth + 1)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            _hunt(v, f"{path}[{i}]", found, depth + 1)


def _score(tree):
    """Rank candidate trees: prefer the one with the most labelled, linked nodes."""
    blob = json.dumps(tree)
    hits = sum(blob.count(f'"{k}"') for k in CHILD_KEYS + HREF_KEYS)
    return (hits, len(blob))


def _best(found):
    if not found:
        return None, None
    found = sorted(found, key=lambda kv: _score(kv[1]), reverse=True)
    return found[0][1], found[0][0]


def _node_label(item):
    for key in LABEL_KEYS:
        val = item.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()
    return ""


def _node_href(item):
    for key in HREF_KEYS:
        val = item.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()
    return ""


def _render(items, depth, out, match=None):
    if isinstance(items, dict):
        items = [items]
    if not isinstance(items, list):
        return
    for item in items:
        if not isinstance(item, dict):
            continue
        if item.get("divider"):
            out.append("  " * depth + "---")
            continue
        label = _node_label(item)
        href = _node_href(item)
        if label:
            line = "  " * depth + label + (f"   [{href}]" if href else "")
            if match and match in href:
                line += "   <<< MATCH"
            out.append(line)
        child_depth = depth + 1 if label else depth
        for key in CHILD_KEYS:
            if isinstance(item.get(key), list):
                _render(item[key], child_depth, out, match)


# --- rung 1: machine-readable payloads -------------------------------------

GLOBALS_JS = r"""() => {
  const out = {};
  const seed = ['__NEXT_DATA__', '__DOCUSAURUS_GLOBAL_DATA__', '__NUXT__',
                '__remixContext', '__sveltekit', '__DOCS__', '__INITIAL_STATE__'];
  const names = new Set(seed);
  // Also sweep window for any other big JSON-ish global.
  for (const k of Object.getOwnPropertyNames(window)) {
    if (/^__/.test(k) || /nav|sidebar|docs|toc/i.test(k)) names.add(k);
  }
  for (const k of names) {
    try {
      const v = window[k];
      if (v && typeof v === 'object') {
        const s = JSON.stringify(v);
        if (s && s.length > 200 && s.length < 8000000) out[k] = s;
      }
    } catch (e) { /* getter threw or value is circular */ }
  }
  return out;
}"""

EMBEDDED_JSON_JS = r"""() => {
  const out = {};
  const nodes = document.querySelectorAll('script[type="application/json"], script[type="application/ld+json"]');
  let i = 0;
  for (const n of nodes) {
    const t = (n.textContent || '').trim();
    if (t.length > 200) out[(n.id || ('script[' + i + ']'))] = t;
    i++;
  }
  return out;
}"""


def _payload_candidates(page):
    """Return [(origin_label, tree)] for every nav-shaped payload found."""
    cands = []
    for origin, blobs in (
        ("window", page.evaluate(GLOBALS_JS)),
        ("embedded-json", page.evaluate(EMBEDDED_JSON_JS)),
    ):
        for name, raw in (blobs or {}).items():
            try:
                parsed = json.loads(raw)
            except Exception:
                continue
            found = []
            _hunt(parsed, name, found)
            tree, where = _best(found)
            if tree is not None:
                cands.append((f"{origin}:{where}", tree))
    cands.sort(key=lambda kv: _score(kv[1]), reverse=True)
    return cands


# --- rung 3: sidebar DOM ----------------------------------------------------

DOM_JS = r"""() => {
  const NL = String.fromCharCode(10);

  const harvest = (root) => {
    const out = [];
    for (const li of root.querySelectorAll('li')) {
      let depth = 0, p = li.parentElement;
      while (p && p !== root) { if (p.tagName === 'UL' || p.tagName === 'OL') depth++; p = p.parentElement; }
      const kids = [...li.childNodes].filter(n => n.nodeType === 1 && n.tagName !== 'UL' && n.tagName !== 'OL');
      let label = '';
      for (const d of kids) {
        const t = (d.innerText || d.textContent || '').trim();
        if (t) { label = t.split(NL)[0]; break; }
      }
      const a = li.querySelector(':scope > a') || li.querySelector(':scope > div > a');
      const href = a ? a.getAttribute('href') : '';
      if (label) out.push({ depth: Math.max(0, depth - 1), label, href });
    }
    return out;
  };

  // Any of these MAY be the site nav -- or the in-page table of contents,
  // which looks identical structurally. Not every theme puts the nav in a
  // sidebar: some (mkdocs Bootstrap) put it in a top navbar and give the
  // sidebar to the page TOC. Cast wide, then score.
  const sels = ['.theme-doc-sidebar-menu', '#sidebar', 'nav[aria-label*="idebar"]',
                '[class*="sidebar"]', 'aside nav', 'aside', 'nav',
                '[role="navigation"]', '[class*="nav"]', '[class*="menu"]',
                '.md-nav--primary'];
  const seen = new Set();
  let best = null, bestScore = -1;

  for (const s of sels) {
    for (const root of document.querySelectorAll(s)) {
      if (seen.has(root)) continue;
      seen.add(root);
      const items = harvest(root);
      if (items.length < 2) continue;
      // An in-page TOC links only to #anchors on the current page. A site nav
      // links to other pages. Prefer the latter, heavily.
      const pageLinks = items.filter(i => i.href && !i.href.startsWith('#')).length;
      const anchors   = items.filter(i => i.href && i.href.startsWith('#')).length;
      if (pageLinks === 0) continue;              // pure TOC -- never the nav
      const score = pageLinks * 10 - anchors + items.length;
      if (score > bestScore) { bestScore = score; best = items; }
    }
  }
  return best;
}"""

# --- rung 5: breadcrumb -----------------------------------------------------

BREADCRUMB_JS = r"""() => {
  const sels = ["nav[aria-label='Breadcrumb']", "nav[aria-label='breadcrumbs']", "[class*='readcrumb']"];
  for (const s of sels) {
    const el = document.querySelector(s);
    if (el) {
      const parts = [...el.querySelectorAll('li')].map(e => e.textContent.trim()).filter(Boolean);
      if (parts.length) return parts;
    }
  }
  return null;
}"""


def _print_dom(dom, match):
    for item in dom:
        href = f"   [{item['href']}]" if item["href"] else ""
        flag = "   <<< MATCH" if match and match in (item["href"] or "") else ""
        print("  " * item["depth"] + item["label"] + href + flag)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--all", action="store_true", help="show every signal found, not just the best")
    ap.add_argument("--json", action="store_true", help="dump the winning tree as JSON")
    ap.add_argument("--timeout", type=int, default=60000)
    ap.add_argument("--match", help="flag entries whose href contains this substring")
    args = ap.parse_args()

    with sync_playwright() as p:
        launch = {"headless": True}
        if CHROME_PATH:
            launch["executable_path"] = CHROME_PATH
        browser = p.chromium.launch(**launch)
        page = browser.new_page(viewport={"width": 1400, "height": 1200})
        page.goto(args.url, wait_until="domcontentloaded", timeout=args.timeout)
        # Client-hydrated docs (Docusaurus, Next.js) render the sidebar after
        # DOMContentLoaded; scoring before it exists picks the top navbar. Wait
        # for a nav-shaped element rather than networkidle -- analytics-heavy
        # doc sites never go idle and would burn the full timeout here.
        # Timeout is short on purpose: a site whose nav is a top navbar (mkdocs
        # Bootstrap) matches none of these, and every second here is dead time.
        try:
            page.wait_for_selector(
                ".theme-doc-sidebar-menu, aside nav, [class*='sidebar'] a",
                timeout=8000,
            )
        except Exception:
            pass
        page.wait_for_timeout(1000)

        # Deliberately no "expand every collapsed category" pass. Docusaurus (and
        # most doc themes) render the current page's ancestor chain already
        # expanded, which is the only branch needed to place the page in nav.
        # Clicking the remaining collapsed categories is both useless and slow:
        # they are off-screen in the sidebar's own scroll container, so every
        # click fails actionability and burns its full timeout. Measured on
        # docs.databricks.com: 33 categories x 6 passes = ~50s, zero new links.

        payloads = _payload_candidates(page)
        dom = page.evaluate(DOM_JS)
        crumbs = page.evaluate(BREADCRUMB_JS)
        # close() can stall for minutes on analytics-heavy doc sites whose
        # beacons keep the context alive. Everything is already extracted.
        try:
            browser.close()
        except Exception:
            pass

    if args.all:
        print(f"# signals found: payloads={len(payloads)} sidebar-dom={'yes' if dom else 'no'} "
              f"breadcrumb={'yes' if crumbs else 'no'}")
        for origin, tree in payloads:
            print(f"\n## rung 1 payload: {origin}")
            lines = []
            _render(tree, 0, lines, args.match)
            print("\n".join(lines[:400]))
        if dom:
            print("\n## rung 3 sidebar DOM")
            _print_dom(dom, args.match)
        if crumbs:
            print("\n## rung 5 breadcrumb (LOW CONFIDENCE)")
            print(" > ".join(crumbs))
        return

    if payloads:
        origin, tree = payloads[0]
        if args.json:
            print(json.dumps(tree, indent=1))
            return
        print(f"# nav source: rung 1, machine-readable payload ({origin})")
        lines = []
        _render(tree, 0, lines, args.match)
        print("\n".join(lines))
        return

    if dom:
        print("# nav source: rung 3, rendered nav DOM (collapsed groups may hide children - verify)")
        _print_dom(dom, args.match)
        return

    if crumbs:
        print("# nav source: rung 5, breadcrumb (LOW CONFIDENCE - truncates levels, hides dual placements)")
        print(" > ".join(crumbs))
        print("# check rungs 2 and 4 by hand: docs repo nav config, or a section index page", file=sys.stderr)
        return

    print("# nav source: NONE - no payload, nav DOM, or breadcrumb found.", file=sys.stderr)
    print("# This source may have no navigation to mirror; use the numbered-Notes convention.", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
