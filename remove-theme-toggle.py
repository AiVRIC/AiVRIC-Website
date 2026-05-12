#!/usr/bin/env python3
"""
Remove dark/light mode toggle from all HTML pages.
Strips:
  1. <span class="top-bar-separator">|</span>  (only the one adjacent to the button)
  2. <button class="theme-toggle" ...>...</button>
  3. <script src="assets/js/theme-toggle.js"></script>
  4. <script src="../assets/js/theme-toggle.js"></script>
Skips: aivric-enterprise/ subdirectory.
"""
import re
from pathlib import Path

SITE = Path(r"C:\Projects\AiVRIC-Website")

# Patterns to remove (each compiled to a regex for robustness)
REMOVALS = [
    # separator + button together (with any indentation / whitespace between)
    re.compile(
        r'\s*<span[^>]*class="top-bar-separator"[^>]*>\|</span>\s*'
        r'<button[^>]*class="theme-toggle"[^>]*data-theme-toggle[^>]*>.*?</button>',
        re.DOTALL
    ),
    # button alone (in case separator is absent)
    re.compile(
        r'\s*<button[^>]*class="theme-toggle"[^>]*data-theme-toggle[^>]*>.*?</button>',
        re.DOTALL
    ),
    # script tag (relative path variants)
    re.compile(r'\s*<script[^>]*assets/js/theme-toggle\.js[^>]*></script>'),
]

def process(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8", errors="replace")
    result = raw
    for pattern in REMOVALS:
        result = pattern.sub("", result)
    if result == raw:
        return False
    path.write_text(result, encoding="utf-8")
    return True

changed = 0
skipped = 0

for html in sorted(SITE.rglob("*.html")):
    # Skip aivric-enterprise mirror
    if "aivric-enterprise" in html.parts:
        continue
    if process(html):
        changed += 1
        print(f"  cleaned: {html.relative_to(SITE)}")
    else:
        skipped += 1

print(f"\nDone — {changed} files cleaned, {skipped} files unchanged.")
