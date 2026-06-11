#!/usr/bin/env python3
"""
Add AiVRIC Academy links to all website HTML pages:
  1. Top bar — beside Platform Guide (icon version)
  2. Resources nav dropdown — new item after Blog
  3. Footer Company column — after Platform Guide
"""

from pathlib import Path

SITE = Path(r"C:\Projects\AiVRIC-Website")

# 1. Top bar: the icon-bearing Platform Guide link → add Academy after it
TOP_BAR_OLD = (
    '<li><a href="https://aivric.com/AiVRIC-UserGuide/index.html">'
    '<span class="top-bar-icon accent-cyan"><i class="fas fa-book-open"></i></span>'
    'Platform Guide</a></li>'
)
TOP_BAR_NEW = (
    TOP_BAR_OLD + "\n"
    '                    <li><a href="https://academy.aivric.com/">'
    '<span class="top-bar-icon accent-cyan"><i class="fas fa-graduation-cap"></i></span>'
    'Academy</a></li>'
)

# 2. Resources dropdown: Blog is last item, followed by blank line + </ul>
RESOURCES_OLD = 'href="blog-portal.html">Blog</a></li>\n\n                </ul>\n            </li>'
RESOURCES_NEW = (
    'href="blog-portal.html">Blog</a></li>\n'
    '                    <li><a href="https://academy.aivric.com/">Academy</a></li>'
    '\n\n                </ul>\n            </li>'
)

# 3. Footer: plain (no icon) Platform Guide link → add Academy after it
FOOTER_OLD = (
    '<li><a href="https://aivric.com/AiVRIC-UserGuide/index.html">Platform Guide</a></li>'
)
FOOTER_NEW = (
    FOOTER_OLD + "\n"
    '                    <li><a href="https://academy.aivric.com/">Academy</a></li>'
)

updated = 0
skipped_already = 0
skipped_no_match = 0
errors = 0

for f in sorted(SITE.rglob("*.html")):
    try:
        text = f.read_text(encoding="utf-8")

        # Don't double-insert
        if "academy.aivric.com" in text:
            skipped_already += 1
            continue

        new_text = text
        new_text = new_text.replace(TOP_BAR_OLD, TOP_BAR_NEW)
        new_text = new_text.replace(RESOURCES_OLD, RESOURCES_NEW)
        new_text = new_text.replace(FOOTER_OLD, FOOTER_NEW)

        if new_text != text:
            f.write_text(new_text, encoding="utf-8")
            updated += 1
        else:
            skipped_no_match += 1

    except Exception as e:
        print(f"ERROR {f.name}: {e}")
        errors += 1

print(f"Updated  : {updated} files")
print(f"Skipped (already had Academy): {skipped_already}")
print(f"Skipped (no matching pattern): {skipped_no_match}")
print(f"Errors   : {errors}")
