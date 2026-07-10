"""
fetch_nav.py — extract a documentation site's real sidebar navigation tree.

Usage:
    python fetch_nav.py <url> [--json] [--timeout <ms>] [--match <substr>]

Why this exists:
    Breadcrumbs are NOT a docs site's information architecture. They truncate
    levels, and when a page appears twice in the sidebar they report only one
    placement. Grouping notes nav by breadcrumb silently produces a tree that
    disagrees with the source docs.

    This script reads the sidebar itself. It tries, in order:
      1. Next.js __NEXT_DATA__ payload   (HashiCorp, many Vercel-hosted docs)
      2. Docusaurus global data          (Meta-style docs)
      3. The rendered sidebar DOM        (generic fallback)
      4. The breadcrumb                  (last resort, low confidence)

    It always prints which source it used. If that line says "breadcrumb",
    treat the output as low-confidence and verify against the live page.

Notes:
    - Expanding the sidebar DOM by clicking aria-expanded=false buttons does
      NOT reliably reveal children (verified broken on developer.hashicorp.com:
      zero collapsed buttons remain, yet group <li>s render no children).
      That is why the JSON payloads are tried first.
    - Uses the system Chrome if present, else Playwright's bundled Chromium.

Requirements:
    pip install playwright
"""

import argparse
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not Path(CHROME_PATH).exists():
    CHROME_PATH = None

# Keys that hold a nav tree in the various framework payloads.
NAV_KEYS = (
    "sidebarNavDataLevels",
    "navData",
    "navNodes",
    "navLevels",
    "sidebar",
    "docsSidebars",
)

# Keys under which a node's children may hang.
CHILD_KEYS = ("routes", "items", "children", "menuItems", "links")


def _hunt(node, path, found):
    """Recursively locate nav-shaped structures in a JSON blob."""
    if isinstance(node, dict):
        for k, v in node.items():
            if k in NAV_KEYS and isinstance(v, (list, dict)) and v:
                found.append((f"{path}.{k}", v))
            _hunt(v, f"{path}.{k}", found)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            _hunt(v, f"{path}[{i}]", found)


def _node_label(item):
    for key in ("title", "heading", "label", "name", "text"):
        val = item.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()
    return ""


def _node_href(item):
    # Deliberately excludes "id": group nodes carry synthetic ids like
    # "sidebar-nav-item-1" which are not links and only add noise.
    for key in ("path", "href", "url"):
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


def _from_next_data(page):
    raw = page.evaluate("() => window.__NEXT_DATA__ ? JSON.stringify(window.__NEXT_DATA__) : null")
    if not raw:
        return None, None
    found = []
    _hunt(json.loads(raw), "root", found)
    if not found:
        return None, None
    # Prefer the deepest/richest tree.
    found.sort(key=lambda kv: len(json.dumps(kv[1])), reverse=True)
    return found[0][1], f"__NEXT_DATA__ ({found[0][0]})"


def _from_docusaurus(page):
    raw = page.evaluate(
        "() => window.__DOCUSAURUS_GLOBAL_DATA__ "
        "? JSON.stringify(window.__DOCUSAURUS_GLOBAL_DATA__) : null"
    )
    if not raw:
        return None, None
    found = []
    _hunt(json.loads(raw), "root", found)
    if not found:
        return None, None
    found.sort(key=lambda kv: len(json.dumps(kv[1])), reverse=True)
    return found[0][1], f"__DOCUSAURUS_GLOBAL_DATA__ ({found[0][0]})"


DOM_JS = r"""() => {
  const side = document.querySelector('#sidebar')
    || document.querySelector('nav[aria-label*="idebar"]')
    || document.querySelector('[class*="sidebar"]')
    || document.querySelector('aside nav');
  if (!side) return null;
  const NL = String.fromCharCode(10);
  const out = [];
  for (const li of side.querySelectorAll('li')) {
    let depth = 0, p = li.parentElement;
    while (p && p !== side) { if (p.tagName === 'UL' || p.tagName === 'OL') depth++; p = p.parentElement; }
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
  return out.length ? out : null;
}"""

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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--json", action="store_true", help="dump the raw tree as JSON")
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
        page.wait_for_timeout(2000)

        tree, source = _from_next_data(page)
        if tree is None:
            tree, source = _from_docusaurus(page)

        if tree is not None:
            if args.json:
                print(json.dumps(tree, indent=1))
                browser.close()
                return
            lines = []
            _render(tree, 0, lines, args.match)
            print(f"# nav source: {source}")
            print("\n".join(lines))
            browser.close()
            return

        dom = page.evaluate(DOM_JS)
        if dom:
            print("# nav source: sidebar DOM (collapsed groups may be missing children - verify)")
            for item in dom:
                href = f"   [{item['href']}]" if item["href"] else ""
                flag = "   <<< MATCH" if args.match and args.match in (item["href"] or "") else ""
                print("  " * item["depth"] + item["label"] + href + flag)
            browser.close()
            return

        crumbs = page.evaluate(BREADCRUMB_JS)
        browser.close()

    if crumbs:
        print("# nav source: breadcrumb (LOW CONFIDENCE - breadcrumbs truncate and hide dual placements)")
        print(" > ".join(crumbs))
        return

    print("# nav source: NONE - could not find a sidebar, payload, or breadcrumb", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
