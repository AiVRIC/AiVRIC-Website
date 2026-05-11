#!/usr/bin/env python3
"""
AiVRIC Website – Global Nav Unification & Active Indicator
1. Fix cloudsignals-pricing.html nav (insert CS menu, remove Blogs, add blog links)
2. Fix pricing.html nav (remove Blogs, add blog links)
3. Inject full nav into: form-post-signup-thank-you.html, trust-old.html, aup.html
4. Append active-indicator CSS to custom.css
5. Append active-indicator JS to script.js
"""

import re
from pathlib import Path

SITE = Path(r"C:\Projects\AiVRIC-Website")
TEMPLATE = SITE / "cspm-cloudsignals.html"

# ── Extract pieces from template ──────────────────────────────────────────────
_tmpl = TEMPLATE.read_text(encoding="utf-8")

# Full <header>…</header> HTML (new nav with CS mega-menu)
_hdr_start = _tmpl.find('<header class="main-header">')
_hdr_end   = _tmpl.find('</header>', _hdr_start) + len('</header>')
NEW_HEADER_HTML = _tmpl[_hdr_start:_hdr_end]

# CS product menu LI (from index.html which was already updated)
_idx_content = (SITE / "index.html").read_text(encoding="utf-8")
_cs_start = _idx_content.find('            <li class="dropdown cs-product-menu">')
_portfolio_start = _idx_content.find('            <li class="dropdown"><a href="#">Portfolio</a>', _cs_start)
CS_MENU_HTML = _idx_content[_cs_start:_portfolio_start]

BLOG_LINKS = '''                    <li><a href="blog-portal.html">Blog</a></li>
                    <li><a href="why-aivric-exists.html">Why AiVRIC Exists</a></li>
                    <li><a href="blog-future-of-cloud-security.html">Future of Cloud Security</a></li>
                    <li><a href="blog-why-continuous-compliance-matters.html">Continuous Compliance</a></li>'''

# The standard CSS / JS includes that the nav needs (injected if missing)
NAV_CSS_INCLUDES = """\
<link href="assets/css/font-awesome-all.css" rel="stylesheet">
<link href="assets/css/flaticon.css" rel="stylesheet">
<link href="assets/css/owl.css" rel="stylesheet">
<link href="assets/css/bootstrap.css" rel="stylesheet">
<link href="assets/css/animate.css" rel="stylesheet">
<link href="assets/css/nice-select.css" rel="stylesheet">
<link href="assets/css/color.css" rel="stylesheet">
<link href="assets/css/elpath.css" rel="stylesheet">
<link href="assets/css/style.css?v=20250115" rel="stylesheet">
<link href="assets/css/responsive.css" rel="stylesheet">
<link href="assets/css/custom.css?v=20250115" rel="stylesheet">"""

NAV_JS_INCLUDES = """\
<script src="assets/js/jquery.js"></script>
<script src="assets/js/popper.min.js"></script>
<script src="assets/js/bootstrap.min.js"></script>
<script src="assets/js/owl.js"></script>
<script src="assets/js/wow.js"></script>
<script src="assets/js/appear.js"></script>
<script src="assets/js/scrollbar.js"></script>
<script src="assets/js/jquery.nice-select.min.js"></script>
<script src="assets/js/parallax-scroll.js"></script>
<script src="assets/js/script.js"></script>
<script src="assets/js/mega-hover.js"></script>
<script src="assets/js/mega-tabs.js"></script>
<script src="assets/js/blog-mega.js"></script>"""

def _remove_blogs_menu_li(raw):
    """Remove the entire <li class="dropdown blogs-menu">...</li> using
    nesting-aware counting so nested </li> tags don't confuse the match."""
    MARKER = '<li class="dropdown blogs-menu">'
    start = raw.find(MARKER)
    if start == -1:
        return raw  # nothing to remove
    # Walk forward counting <li and </li> to find the matching close
    depth = 0
    pos = start
    while pos < len(raw):
        open_pos  = raw.find('<li', pos)
        close_pos = raw.find('</li>', pos)
        if close_pos == -1:
            break  # malformed - bail
        if open_pos != -1 and open_pos < close_pos:
            depth += 1
            pos = open_pos + 3
        else:
            depth -= 1
            end = close_pos + len('</li>')
            if depth == 0:
                # Include the leading whitespace before MARKER
                lead_start = start
                while lead_start > 0 and raw[lead_start - 1] in (' ', '\t'):
                    lead_start -= 1
                # Also eat the newline before if present
                if lead_start > 0 and raw[lead_start - 1] == '\n':
                    lead_start -= 1
                return raw[:lead_start] + raw[end:]
            pos = end
    return raw  # fallback


# ─────────────────────────────────────────────────────────────────────────────
# 1.  Fix cloudsignals-pricing.html
# ─────────────────────────────────────────────────────────────────────────────
def fix_cloudsignals_pricing():
    path = SITE / "cloudsignals-pricing.html"
    raw = path.read_text(encoding="utf-8")

    # a. Insert CS menu between Platform </li> and Portfolio <li>
    if 'cs-product-menu' not in raw:
        m = re.search(
            r'(\s+</div>\s+</li>\s+)(<li class="dropdown"><a href="#">Portfolio</a>)',
            raw, re.DOTALL
        )
        if m:
            raw = raw[:m.start()] + m.group(1) + CS_MENU_HTML + m.group(2) + raw[m.end():]
            print("  [OK] CS menu inserted")
        else:
            print("  [!!] Could not find Platform/Portfolio anchor - CS menu NOT inserted")

    # b. Remove Blogs menu LI (nesting-aware)
    raw = _remove_blogs_menu_li(raw)

    # c. Add blog links to Resources (after Why AiVRIC)
    why_link = '<li><a href="why-aivric.html">Why AiVRIC</a></li>'
    if why_link in raw and 'blog-portal.html' not in raw:
        raw = raw.replace(why_link, why_link + '\n' + BLOG_LINKS, 1)

    path.write_text(raw, encoding="utf-8")
    print("[OK] cloudsignals-pricing.html updated")


# ─────────────────────────────────────────────────────────────────────────────
# 2.  Fix pricing.html  (has CS menu, still has top-level Blogs)
# ─────────────────────────────────────────────────────────────────────────────
def fix_pricing():
    path = SITE / "pricing.html"
    raw = path.read_text(encoding="utf-8")

    # Remove Blogs LI (nesting-aware)
    raw = _remove_blogs_menu_li(raw)

    # Add blog links to Resources if missing
    why_link = '<li><a href="why-aivric.html">Why AiVRIC</a></li>'
    if why_link in raw and 'blog-portal.html' not in raw:
        raw = raw.replace(why_link, why_link + '\n' + BLOG_LINKS, 1)

    path.write_text(raw, encoding="utf-8")
    print("[OK] pricing.html updated")


# ─────────────────────────────────────────────────────────────────────────────
# 3a. form-post-signup-thank-you.html — replace old header
# ─────────────────────────────────────────────────────────────────────────────
def fix_form_post():
    path = SITE / "form-post-signup-thank-you.html"
    raw = path.read_text(encoding="utf-8")

    # Find old header-style-two header and replace it
    old_hdr_start = raw.find('<header class="main-header header-style-two">')
    if old_hdr_start < 0:
        old_hdr_start = raw.find('<header class="main-header')
    if old_hdr_start < 0:
        print("  [!!] form-post: no header found")
        return

    old_hdr_end = raw.find('</header>', old_hdr_start) + len('</header>')
    raw = raw[:old_hdr_start] + NEW_HEADER_HTML + raw[old_hdr_end:]

    # Add missing CSS/JS if not present
    if 'cs-product-menu' not in raw:
        # Add custom.css if missing
        if 'custom.css' not in raw:
            raw = raw.replace('</head>', '  <link href="assets/css/custom.css?v=20250115" rel="stylesheet">\n</head>')
        if 'color.css' not in raw:
            raw = raw.replace('</head>', '  <link href="assets/css/color.css" rel="stylesheet">\n</head>')

    path.write_text(raw, encoding="utf-8")
    print("[OK] form-post-signup-thank-you.html updated")


# ─────────────────────────────────────────────────────────────────────────────
# 3b. trust-old.html — inject nav
# ─────────────────────────────────────────────────────────────────────────────
def fix_trust_old():
    path = SITE / "trust-old.html"
    raw = path.read_text(encoding="utf-8")

    # This page has its own header structure. Replace or prepend new nav.
    # Check for an existing <header>
    hdr_start = raw.find('<header')
    if hdr_start >= 0:
        hdr_end = raw.find('</header>', hdr_start) + len('</header>')
        raw = raw[:hdr_start] + NEW_HEADER_HTML + raw[hdr_end:]
    else:
        # Inject after <body> tag
        body_idx = raw.find('<body')
        body_end = raw.find('>', body_idx) + 1
        raw = raw[:body_end] + '\n' + NEW_HEADER_HTML + '\n' + raw[body_end:]

    # Ensure required CSS is present
    if 'color.css' not in raw:
        raw = raw.replace('</head>', '  <link href="assets/css/color.css" rel="stylesheet">\n</head>', 1)
    if 'elpath.css' not in raw:
        raw = raw.replace('</head>', '  <link href="assets/css/elpath.css" rel="stylesheet">\n</head>', 1)
    if 'font-awesome-all.css' not in raw:
        raw = raw.replace('</head>', '  <link href="assets/css/font-awesome-all.css" rel="stylesheet">\n</head>', 1)
    if 'bootstrap.css' not in raw:
        raw = raw.replace('</head>', '  <link href="assets/css/bootstrap.css" rel="stylesheet">\n</head>', 1)

    # Ensure JS is present for nav dropdowns
    if 'script.js' not in raw:
        raw = raw.replace('</body>', NAV_JS_INCLUDES + '\n</body>', 1)

    # Add top padding to first content container so it clears the sticky nav
    if 'nav-push' not in raw and 'pt-' not in raw:
        raw = raw.replace('<main', '<main style="padding-top:100px;"', 1)
        if '<section' in raw and 'padding-top:100px' not in raw:
            # Find first section after header
            first_section = raw.find('<section', raw.find(NEW_HEADER_HTML[:40]))
            if first_section > 0:
                pass  # already handled above

    path.write_text(raw, encoding="utf-8")
    print("[OK] trust-old.html updated")


# ─────────────────────────────────────────────────────────────────────────────
# 3c. aup.html — inject nav
# ─────────────────────────────────────────────────────────────────────────────
def fix_aup():
    path = SITE / "aup.html"
    raw = path.read_text(encoding="utf-8")

    # Find <body> tag
    body_idx = raw.find('<body')
    body_end = raw.find('>', body_idx) + 1

    # Inject nav after body open
    raw = raw[:body_end] + '\n' + NEW_HEADER_HTML + '\n' + raw[body_end:]

    # Fix body layout: remove flex centering, add top padding
    raw = raw.replace(
        'body{\n  margin:0;\n  font-family: Inter',
        'body{\n  margin:0;\n  padding-top:100px;\n  font-family: Inter'
    )
    raw = raw.replace(
        'display:flex;\n  align-items:center;\n  justify-content:center;',
        'display:block;'
    )
    # Also handle multiline with different whitespace
    raw = re.sub(
        r'body\s*\{([^}]*?)display\s*:\s*flex\s*;([^}]*?)align-items\s*:\s*center\s*;([^}]*?)justify-content\s*:\s*center\s*;',
        lambda m: 'body {' + m.group(1) + 'display:block;' + m.group(2) + m.group(3),
        raw, flags=re.DOTALL
    )

    # Ensure all required CSS is present (aup already has style.css, bootstrap, font-awesome)
    if 'color.css' not in raw:
        raw = raw.replace('</head>', '  <link href="assets/css/color.css" rel="stylesheet">\n</head>', 1)
    if 'elpath.css' not in raw:
        raw = raw.replace('</head>', '  <link href="assets/css/elpath.css" rel="stylesheet">\n</head>', 1)
    if 'custom.css' not in raw:
        raw = raw.replace('</head>', '  <link href="assets/css/custom.css?v=20250115" rel="stylesheet">\n</head>', 1)

    # Ensure JS is present
    if 'script.js' not in raw:
        raw = raw.replace('</body>', NAV_JS_INCLUDES + '\n</body>', 1)

    path.write_text(raw, encoding="utf-8")
    print("[OK] aup.html updated")


# ─────────────────────────────────────────────────────────────────────────────
# 4.  Active-indicator CSS → custom.css
# ─────────────────────────────────────────────────────────────────────────────
ACTIVE_NAV_CSS = """

/* ═══════════════════════════════════════════════════════════════════════════
   Global nav active / current-page indicator  (2026-05)
   Adds cyan underline to the top-level nav item matching the current page.
   Set via JS in script.js (setActiveNav).
══════════════════════════════════════════════════════════════════════════════ */
.main-menu .navigation > li.current > a,
.main-menu .navigation > li.current > a:hover {
  color: #00d1ff !important;
  text-decoration: underline !important;
  text-decoration-color: rgba(0, 209, 255, 0.85) !important;
  text-underline-offset: 5px !important;
  text-decoration-thickness: 2px !important;
}

/* Subtle glow dot below the active item (desktop only) */
@media (min-width: 992px) {
  .main-menu .navigation > li.current {
    position: relative;
  }
  .main-menu .navigation > li.current::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 50%;
    transform: translateX(-50%);
    width: 18px;
    height: 2px;
    background: #00d1ff;
    border-radius: 2px;
    box-shadow: 0 0 8px rgba(0, 209, 255, 0.6);
    pointer-events: none;
  }
}

/* Pricing page variant (uses header.main-header) */
header.main-header .main-menu .navigation > li.current > a {
  color: #00d1ff !important;
  text-decoration: underline !important;
  text-decoration-color: rgba(0, 209, 255, 0.85) !important;
  text-underline-offset: 5px !important;
  text-decoration-thickness: 2px !important;
}
"""


def add_active_css():
    css_path = SITE / "assets" / "css" / "custom.css"
    raw = css_path.read_bytes()
    if b"Global nav active / current-page indicator" in raw:
        print("[--] custom.css: active indicator CSS already present")
        return
    with open(css_path, "ab") as f:
        f.write(ACTIVE_NAV_CSS.encode("utf-8"))
    print("[OK] custom.css: active indicator CSS appended")


# ─────────────────────────────────────────────────────────────────────────────
# 5.  Active-indicator JS → script.js
# ─────────────────────────────────────────────────────────────────────────────
ACTIVE_NAV_JS = r"""

/* ── Active nav detection (2026-05) ──────────────────────────────────────── */
$(document).ready(function(){
  var page = (window.location.pathname.split('/').pop() || 'index.html')
               .replace(/[?#].*$/, '') || 'index.html';

  var $topItems = $('.main-menu .navigation > li');

  $topItems.each(function(){
    var $li = $(this);

    // 1. Check top-level anchor href
    var topHref = ($li.children('a').attr('href') || '').split('/').pop().replace(/[?#].*$/, '');
    if(topHref && topHref !== '#' && topHref === page){
      $li.addClass('current');
      return; // next li
    }

    // 2. Check all descendant links (mega-menu cards, dropdown items, etc.)
    var found = false;
    $li.find('a[href]').each(function(){
      var href = ($(this).attr('href') || '').split('/').pop().replace(/[?#].*$/, '');
      if(href && href === page){
        found = true;
        return false; // break .each
      }
    });
    if(found){ $li.addClass('current'); }
  });
});
"""


def add_active_js():
    js_path = SITE / "assets" / "js" / "script.js"
    js = js_path.read_text(encoding="utf-8", errors="replace")
    if "Active nav detection" in js:
        print("[--] script.js: active nav JS already present")
        return
    # Inject just before the closing })(window.jQuery);
    close_marker = "})(window.jQuery);"
    idx = js.rfind(close_marker)
    if idx >= 0:
        js = js[:idx] + ACTIVE_NAV_JS + "\n" + js[idx:]
    else:
        js += "\n" + ACTIVE_NAV_JS
    js_path.write_text(js, encoding="utf-8")
    print("[OK] script.js: active nav JS injected")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    print("=== Fixing pricing page navs ===")
    fix_cloudsignals_pricing()
    fix_pricing()

    print("\n=== Injecting nav into pages that lacked it ===")
    fix_form_post()
    fix_trust_old()
    fix_aup()

    print("\n=== Adding active indicator CSS + JS ===")
    add_active_css()
    add_active_js()

    # ── Final verification ──────────────────────────────────────────────────
    print("\n=== Verification ===")
    all_pages = sorted([f for f in SITE.glob("*.html") if f.is_file()])
    missing_nav = []
    missing_active = []
    for f in all_pages:
        if f.name in ("icon-cheatsheet.html", "demo-access.html", "new-home.html"):
            continue  # intentionally standalone
        content = f.read_text(encoding="utf-8", errors="replace")
        if "cs-product-menu" not in content:
            missing_nav.append(f.name)

    if missing_nav:
        print(f"Pages still without new nav ({len(missing_nav)}): {missing_nav}")
    else:
        print("[OK] All tracked pages have the new nav")

    print("\n[OK] Done.")


if __name__ == "__main__":
    main()
