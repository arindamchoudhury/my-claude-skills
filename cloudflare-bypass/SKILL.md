---
name: cloudflare-bypass
description: >
  Use when fetching pages that are blocked by Cloudflare bot protection, bot verification screens,
  "Performing security verification" messages, or login walls that WebFetch cannot get past.
  Triggers on: WebFetch returning a sign-in or security page instead of content, "just a moment"
  Cloudflare challenge pages, any page that requires a logged-in browser session, or when the user
  says "automate login", "bypass bot check", "fetch authenticated page", or "page requires login".
  Also use when setting up a recurring web fetch workflow for a site with bot protection.
---

# Cloudflare Bot Bypass — Fetch Workflow

Modern Cloudflare (2025+) detects and blocks:
- `WebFetch` (server-side, no JS execution)
- Standard Playwright/Selenium (leaves webdriver fingerprints)
- `playwright-stealth` v2 (deprecated against current Cloudflare)

**The solution that works: `nodriver`** — communicates with Chrome via the Chrome DevTools Protocol (CDP) directly, without injecting any webdriver flag. Chrome behaves as a real browser. Cloudflare cannot distinguish it from a human session.

## Prerequisites

Install into the Python environment you'll use for fetching:

```bash
pip install nodriver python-dotenv
```

No browser download needed — `nodriver` uses the **system Chrome** already installed.

> On Windows with a corporate SSL proxy: browser downloads (`playwright install`, `camoufox fetch`) fail with SSL cert errors. `nodriver` avoids this entirely by using the system Chrome executable.

## Project structure

```
<notes-root>/
├── .env                        # credentials (gitignored)
├── scripts/
│   └── fetch_page.py           # fetch script (see below)
└── cache/
    ├── auth_state.json         # saved cookies (gitignored)
    └── web/
        └── <slug>.txt          # cached page text
```

## The `.env` file

```dotenv
SITE_EMAIL=your@email.com
SITE_PASSWORD=yourpassword
```

Adapt variable names to the site. Never commit this file.

## The fetch script (`scripts/fetch_page.py`)

This is the complete, working template. Copy it into your project and adapt the selectors and login URL.

```python
"""Fetch a Cloudflare-protected page using nodriver (Chrome CDP)."""
import argparse, asyncio, pathlib, sys, time, json
from dotenv import load_dotenv

load_dotenv(pathlib.Path(__file__).parent.parent / ".env")

import os
SITE_EMAIL    = os.environ.get("SITE_EMAIL", "")
SITE_PASSWORD = os.environ.get("SITE_PASSWORD", "")

NOTES_ROOT = pathlib.Path(__file__).parent.parent
CACHE_DIR  = NOTES_ROOT / "cache" / "web"
AUTH_FILE  = NOTES_ROOT / "cache" / "auth_state.json"
CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def _chrome():
    p = pathlib.Path(CHROME_EXE)
    return str(p) if p.exists() else None  # None = let nodriver find it


# ── Auth save ──────────────────────────────────────────────────────────────

async def _save_auth_async(
    login_url,
    email_selector="input[type='email'], input[name='user[email]'], input[id='user_email']",
    password_selector="input[type='password']",
    submit_selector="input[type='submit'], button[type='submit']",
    logged_in_check=lambda url, title: True,  # override to tighten detection
    email=None,
    password=None,
):
    import nodriver as uc
    AUTH_FILE.parent.mkdir(parents=True, exist_ok=True)

    browser = await uc.start(headless=False, browser_executable_path=_chrome())
    page = await browser.get(login_url)
    await asyncio.sleep(3)  # let Cloudflare challenge clear

    # Auto-fill credentials
    if email and password:
        print("Filling credentials...")
        try:
            email_field = await page.find(email_selector, timeout=10)
            await email_field.click()
            await email_field.send_keys(email)
            await asyncio.sleep(0.5)
            pass_field = await page.find(password_selector, timeout=5)
            await pass_field.click()
            await pass_field.send_keys(password)
            await asyncio.sleep(0.5)
            submit = await page.find(submit_selector, timeout=5)
            await submit.click()
            print("Submitted, waiting for redirect...")
        except Exception as e:
            print(f"Auto-fill failed ({e}) — log in manually in the browser.")

    print("Waiting for authenticated page...")

    # Poll until we see a post-login URL
    deadline = time.time() + 180
    while time.time() < deadline:
        await asyncio.sleep(2)
        try:
            url   = await page.evaluate("window.location.href")
            title = await page.evaluate("document.title")
            print(f"  url={url[:80]}  title={title[:50]}")
        except Exception as e:
            print(f"  poll error: {e}")
            continue
        if "sign_in" not in url and "login" not in url and "just a moment" not in title.lower():
            if logged_in_check(url, title):
                print(f"Logged-in page detected: {url}")
                break
    else:
        print("WARNING: timed out waiting for login", file=sys.stderr)

    # Save cookies
    try:
        raw = await page.send(uc.cdp.network.get_cookies())
        cookies = [c.to_json() for c in raw]
    except Exception as e:
        print(f"Cookie fetch failed: {e}", file=sys.stderr)
        cookies = []

    AUTH_FILE.write_text(json.dumps(cookies, indent=2), encoding="utf-8")
    print(f"Saved {len(cookies)} cookies -> {AUTH_FILE}")
    browser.stop()


# ── Page fetch ─────────────────────────────────────────────────────────────

async def _fetch_async(url, slug, timeout=60):
    import nodriver as uc
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE_DIR / f"{slug}.txt"

    browser = await uc.start(headless=False, browser_executable_path=_chrome())
    page = await browser.get("about:blank")

    # Restore cookies
    if AUTH_FILE.exists():
        cookies = json.loads(AUTH_FILE.read_text(encoding="utf-8"))
        for c in cookies:
            try:
                await page.send(uc.cdp.network.set_cookie(
                    name=c["name"], value=c["value"],
                    domain=c.get("domain", ""),
                    path=c.get("path", "/"),
                    secure=c.get("secure", False),
                ))
            except Exception:
                pass

    page = await browser.get(url)

    # Wait for Cloudflare to clear and content to appear
    deadline = time.time() + timeout
    while time.time() < deadline:
        await asyncio.sleep(2)
        try:
            title   = await page.evaluate("document.title")
            cur_url = await page.evaluate("window.location.href")
        except Exception:
            continue
        if "just a moment" in title.lower():
            print(f"  [cf] challenge running...")
            continue
        if "sign_in" in cur_url or "login" in cur_url:
            print("Redirected to login — cookies may be stale. Re-run --save-auth.")
            break
        # Check for content (adapt selector to the site)
        try:
            el = await page.find("article, main, .content, .lecture-content", timeout=2)
            if el:
                print("Content found.")
                break
        except Exception:
            pass
        print(f"  waiting... ({title[:60]})")

    await asyncio.sleep(2)

    # Expand hidden content
    try:
        for btn in await page.query_selector_all("button[aria-expanded='false']"):
            try: await btn.click(); await asyncio.sleep(0.3)
            except Exception: pass
    except Exception: pass

    text = await page.evaluate("document.body.innerText")
    browser.stop()

    cache_file.write_text(text, encoding="utf-8")
    print(f"Saved {len(text)} chars -> {cache_file}")
    return text


# ── CLI ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("url", nargs="?", default="")
    ap.add_argument("--slug")
    ap.add_argument("--timeout", type=int, default=60)
    ap.add_argument("--save-auth", action="store_true",
                    help="Open browser, log in, save session cookies")
    ap.add_argument("--login-url", default="")
    ap.add_argument("--email")
    ap.add_argument("--password")
    args = ap.parse_args()

    if args.save_auth:
        asyncio.run(_save_auth_async(
            login_url=args.login_url,
            email=args.email or SITE_EMAIL,
            password=args.password or SITE_PASSWORD,
        ))
    else:
        if not args.url or not args.slug:
            ap.error("url and --slug are required")
        asyncio.run(_fetch_async(args.url, args.slug, args.timeout))
```

## Usage

### Step 1 — Save auth (first time, or when cookies expire)

Run this in a terminal (not from Claude Code, because it opens a browser window):

```powershell
$env:PYTHONIOENCODING = "utf-8"
& "C:\Users\arind\miniforge3\envs\notes-fetch\python.exe" scripts\fetch_page.py `
    --save-auth `
    --login-url "https://example.com/users/sign_in"
```

The script opens Chrome, auto-fills credentials from `.env`, then **polls `window.location.href` every 2 seconds** until the URL no longer contains `sign_in` or `login`. No manual Enter-press needed. Cookies are saved to `cache/auth_state.json`.

### Step 2 — Fetch a page

```powershell
$env:PYTHONIOENCODING = "utf-8"
& "C:\Users\arind\miniforge3\envs\notes-fetch\python.exe" scripts\fetch_page.py `
    "https://example.com/some/page" --slug "my-page-slug"
```

Output is saved to `cache/web/my-page-slug.txt`. Always check cache before re-fetching.

## Common issues and fixes

**"Opening in existing browser session"**
Chrome is running and you tried `launch_persistent_context` with the main profile. Use `launch()` (not `launch_persistent_context`) — this creates a temporary profile that doesn't conflict with a running Chrome.

**Script hangs at "Waiting for authenticated page..."**
`page.url` doesn't update dynamically in nodriver. Always use `await page.evaluate("window.location.href")` to read the current URL.

**`input()` raises `EOFError` in background**
Background processes have no stdin. Never use `input()` to wait for login confirmation — poll `window.location.href` instead (as in the template above).

**`playwright install` or `camoufox fetch` fails with SSL cert error**
Corporate proxy with SSL inspection. Don't fight it — use `nodriver` with the system Chrome instead. No browser download needed.

**`playwright-stealth` import error or still blocked**
`playwright-stealth` v2 changed its API (`stealth_sync` → `Stealth().apply_stealth_sync(ctx)`) and is no longer effective against modern Cloudflare. Switch to `nodriver`.

**Chrome v130+ cookie extraction blocked** (`RuntimeError: appbound encryption`)
Extracting Chrome cookies with `rookiepy` requires admin rights on Chrome v130+. Use the `--save-auth` flow instead (logs in fresh and saves cookies directly via CDP).

**Windows asyncio pipe errors at script exit**
`ValueError: I/O operation on closed pipe` — harmless Windows cleanup noise from `asyncio`'s ProactorEventLoop. Ignore.

## When cookies expire

Re-run `--save-auth`. Cookie lifetime varies by site (hours to weeks). If a fetch redirects to the login page, that's the signal to refresh.
