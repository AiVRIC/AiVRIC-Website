#!/usr/bin/env python3
"""
Replace old preloader with new AiVRIC ultra-modern preloader on all live HTML pages.

What it does per file:
  1. Adds <link href="…/aivric-preloader.css"> as the FIRST stylesheet
     (before font-awesome-all.css), if not already present.
  2. Replaces the old <!-- preloader --> … <!-- preloader end --> block
     with the new markup.
  3. Inserts <script src="…/aivric-preloader.js"></script>
     just before <script src="…/script.js"></script>, if not already present.

Asset path prefix:
  Root-level pages   → assets/
  assets/blog-…/     → ../assets/
"""
import re
from pathlib import Path

SITE = Path(r"C:\Projects\AiVRIC-Website")

SKIP_DIRS = {"_backup", "_archive", "aivric-enterprise"}

# ── New preloader HTML ───────────────────────────────────────────────────────
NEW_PRELOADER = '''        <!-- preloader -->
        <div id="apl-wrap">
          <div class="apl-scan"></div>
          <div class="apl-corner tl"></div>
          <div class="apl-corner tr"></div>
          <div class="apl-corner bl"></div>
          <div class="apl-corner br"></div>
          <div class="apl-center">
            <div class="apl-logo-wrap">
              <div class="apl-ring r1"></div>
              <div class="apl-ring r2"></div>
              <div class="apl-ring r3"></div>
              <img class="apl-logo" src="{prefix}images/logo/aivric.svg" alt="AiVRIC">
            </div>
            <div class="apl-brand">AiVRIC</div>
            <div class="apl-tagline">Security Intelligence Platform</div>
            <div class="apl-progress-wrap">
              <div class="apl-progress-fill" id="apl-fill"></div>
            </div>
            <div class="apl-status-row">
              <span class="apl-status" id="apl-status">Initializing Signal Engine</span>
              <span class="apl-pct" id="apl-pct">0%</span>
            </div>
          </div>
        </div>
        <!-- preloader end -->'''

# Matches the old preloader block (any whitespace/indentation variants)
OLD_PRELOADER_RE = re.compile(
    r'<!--\s*preloader\s*-->'
    r'.*?'
    r'<!--\s*preloader end\s*-->',
    re.DOTALL | re.IGNORECASE,
)


def asset_prefix(path: Path) -> str:
    """Return 'assets/' for root pages, '../assets/' for one level deep."""
    rel = path.relative_to(SITE)
    depth = len(rel.parts) - 1   # 0 = root, 1 = one subdir
    return "../" * depth + "assets/"


def process(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8", errors="replace")
    result = raw
    prefix = asset_prefix(path)

    changed = False

    # ── 1. Inject preloader CSS link ────────────────────────────────────────
    css_link = f'<link href="{prefix}css/aivric-preloader.css" rel="stylesheet">'
    if css_link not in result:
        # Insert before the first stylesheet link
        fa_link_re = re.compile(
            r'(<link[^>]*font-awesome-all\.css[^>]*>)',
            re.IGNORECASE,
        )
        m = fa_link_re.search(result)
        if m:
            result = result[:m.start()] + css_link + "\n" + result[m.start():]
            changed = True

    # ── 2. Replace old preloader HTML block ─────────────────────────────────
    if OLD_PRELOADER_RE.search(result):
        new_html = NEW_PRELOADER.replace("{prefix}", prefix)
        result = OLD_PRELOADER_RE.sub(new_html, result, count=1)
        changed = True

    # ── 3. Inject preloader JS before script.js ─────────────────────────────
    js_tag = f'<script src="{prefix}js/aivric-preloader.js"></script>'
    if js_tag not in result:
        script_js_re = re.compile(
            r'(<script[^>]*script\.js[^>]*></script>)',
            re.IGNORECASE,
        )
        m = script_js_re.search(result)
        if m:
            result = result[:m.start()] + js_tag + "\n    " + result[m.start():]
            changed = True

    if result == raw:
        return False

    path.write_text(result, encoding="utf-8")
    return True


changed = 0
skipped = 0

for html in sorted(SITE.rglob("*.html")):
    # Skip unwanted directories
    if any(d in html.parts for d in SKIP_DIRS):
        continue
    if process(html):
        changed += 1
        print(f"  updated: {html.relative_to(SITE)}")
    else:
        skipped += 1
        print(f"  skipped: {html.relative_to(SITE)}")

print(f"\nDone — {changed} files updated, {skipped} files unchanged.")
