from pathlib import Path

SITE = Path(r"C:\Projects\AiVRIC-Website")

REMOVE = [
    '<li><a href="why-aivric-exists.html">Why AiVRIC Exists</a></li>',
    '<li><a href="blog-future-of-cloud-security.html">Future of Cloud Security</a></li>',
    '<li><a href="blog-future-of-cloud-security.html">Future of Cloud Security</a></li>',
    '<li><a href="blog-why-continuous-compliance-matters.html">Continuous Compliance</a></li>',
]

# Also handle the variant with extra whitespace/newlines around them
import re

PATTERNS = [
    r'\s*<li><a href="why-aivric-exists\.html">Why AiVRIC Exists</a></li>',
    r'\s*<li><a href="blog-future-of-cloud-security\.html">Future of Cloud Security</a></li>',
    r'\s*<li><a href="blog-why-continuous-compliance-matters\.html">Continuous Compliance</a></li>',
]

files_changed = 0

for f in sorted(SITE.glob("*.html")):
    raw = f.read_text(encoding="utf-8", errors="replace")
    updated = raw
    for pattern in PATTERNS:
        updated = re.sub(pattern, '', updated)
    if updated != raw:
        files_changed += 1
        f.write_text(updated, encoding="utf-8")

print(f"Files updated: {files_changed}")
