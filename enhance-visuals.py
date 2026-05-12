#!/usr/bin/env python3
"""
AiVRIC Website Visual Enhancement Script
=========================================
Injects cinematic video + brand-asset sections into every key page.

ASSET NAMING — drop files here before videos are ready:
  assets/images/brand/
    Threat-Signals-1.png     (world map threat arcs)
    CS-Montage-1.png         (4-panel dashboard reveal)
    CS-Montage-2.png         (6-panel risk intelligence)
    Main-Screen-Promo.png    (full promo hero layout)
    RiskOps-Dashboard.png    (RiskOps portal — from ChatGPT_Image_May_12)

  assets/videos/
    clip1-threat-signals.mp4
    clip2-platform-reveal.mp4
    clip3-risk-intelligence.mp4
    clip4-main-promo.mp4
    clip5-riskops-portal.mp4
    clip6-threat-arc.mp4
    clip7-shield-activation.mp4

Run:  python enhance-visuals.py  (idempotent — safe to re-run)
"""
from pathlib import Path

SITE = Path(r"C:\Projects\AiVRIC-Website")
CSS_REL   = "assets/css/visual-enhancements.css"
CSS_LINK  = f'<link href="{CSS_REL}" rel="stylesheet">'
CSS_LINK2 = '<link href="../../assets/css/visual-enhancements.css" rel="stylesheet">'

# ── helpers ──────────────────────────────────────────────────────────────────
def add_css(html, link=CSS_LINK):
    if "visual-enhancements.css" in html:
        return html
    return html.replace("</head>", f"{link}\n</head>", 1)

def guard(html, marker):
    return marker in html

def before(html, anchor, snippet):
    pos = html.find(anchor)
    return html if pos == -1 else html[:pos] + snippet + html[pos:]

def after(html, anchor, snippet):
    pos = html.find(anchor)
    return html if pos == -1 else html[:pos+len(anchor)] + snippet + html[pos+len(anchor):]

def save(path, html):
    path.write_text(html, encoding="utf-8")
    sz = path.stat().st_size // 1024
    print(f"  enhanced: {path.name}  ({sz} KB)")


# ════════════════════════════════════════════════════════════════════════════
# HTML SNIPPETS
# ════════════════════════════════════════════════════════════════════════════

# ── 1. Platform Film (index.html) ────────────────────────────────────────────
VE_PLATFORM_FILM = """
<!-- ═══════════ VE: Platform Film ═══════════ -->
<section class="ve-platform-film">
  <div class="ve-platform-film__atmo" style="position:absolute;inset:0;pointer-events:none;background:radial-gradient(900px 480px at 50% 0%,rgba(0,209,255,.055),transparent 65%),radial-gradient(600px 380px at 80% 90%,rgba(46,229,157,.03),transparent 65%);"></div>
  <div class="auto-container" style="position:relative;">
    <div class="ve-pf-header">
      <div class="ve-eyebrow" style="justify-content:center;margin-bottom:14px;">
        <span class="ve-eyebrow-dot"></span>&nbsp;Platform in Action
      </div>
      <h2 class="ve-h2" style="text-align:center;">See CloudSignals+RiskOps&trade; live on<br><span class="ve-grad-cyan">your infrastructure.</span></h2>
      <p class="ve-sub centred" style="margin-bottom:0;">From your first misconfiguration to board-ready compliance reports &mdash; the complete risk operations workflow, hosted entirely in your environment.</p>
    </div>
    <div class="ve-pf-wrap">
      <div class="ve-vid-frame ve-pf-frame">
        <div class="ve-vid-scanlines"></div>
        <video autoplay muted loop playsinline poster="assets/images/brand/Main-Screen-Promo.png">
          <source src="assets/videos/clip4-main-promo.mp4" type="video/mp4">
        </video>
        <div class="ve-vid-overlay"></div>
        <div class="ve-pf-ctrl ve-ctrl-bar">
          <span class="ve-ctrl-live"><span class="ve-live-dot"></span>&nbsp;LIVE DEMO</span>
          <span class="ve-ctrl-meta"><i class="fas fa-play-circle"></i>&nbsp;~18 sec</span>
          <span class="ve-ctrl-meta"><i class="fas fa-expand"></i>&nbsp;1080p</span>
        </div>
      </div>
      <div class="ve-chip ve-chip-1"><i class="fas fa-shield-alt"></i>&nbsp;350+ cloud checks running</div>
      <div class="ve-chip ve-chip-2 green"><i class="fas fa-robot"></i>&nbsp;AIRE autonomous fix queued</div>
      <div class="ve-chip ve-chip-3"><i class="fas fa-check-circle"></i>&nbsp;SOC 2 evidence captured</div>
    </div>
    <div class="ve-cta-row">
      <a href="https://gcp-defense.aivric.com/sign-up?plan=pkg-cloudsignals-free&amp;source=platform_film" class="ve-btn primary"><i class="fas fa-rocket"></i>&nbsp;Try it free</a>
      <a href="request-demo.html" class="ve-btn ghost">Schedule a live walkthrough</a>
    </div>
  </div>
</section>
<!-- ═══════════ END VE: Platform Film ═══════════ -->
"""

# ── 2. Threat map bg (index.html hp-stats-section) ───────────────────────────
VE_THREAT_BG = """
<div class="ve-threat-bg">
  <img src="assets/images/brand/Threat-Signals-1.png" alt="">
  <video autoplay muted loop playsinline>
    <source src="assets/videos/clip1-threat-signals.mp4" type="video/mp4">
  </video>
  <div class="ve-threat-bg-vignette"></div>
</div>
"""

# ── 3. How-section visual (index.html, before hp-deploy) ────────────────────
VE_HOW_VISUAL = """
<!-- ═══════════ VE: How-section Visual ═══════════ -->
<section class="ve-how-visual">
  <div class="auto-container">
    <div class="ve-hv-inner">
      <div class="ve-hv-copy">
        <div class="ve-eyebrow"><span class="ve-eyebrow-dot"></span>&nbsp;Risk Intelligence</div>
        <h3>Six panels. One unified<br><span class="ve-grad-cyan">security picture.</span></h3>
        <p>CloudSignals aggregates posture data, risk radar signals, attack path chains, and real-time threat monitoring into a single, unified view &mdash; so every team sees the same ground truth.</p>
        <a href="cspm-cloudsignals.html" class="ve-btn ghost">Explore the platform &rarr;</a>
      </div>
      <div class="ve-vid-frame ve-hv-frame">
        <div class="ve-vid-scanlines"></div>
        <img src="assets/images/brand/CS-Montage-2.png" alt="CloudSignals risk intelligence panels">
        <video autoplay muted loop playsinline poster="assets/images/brand/CS-Montage-2.png">
          <source src="assets/videos/clip3-risk-intelligence.mp4" type="video/mp4">
        </video>
        <div class="ve-vid-overlay"></div>
        <div class="ve-frame-label">Risk Intelligence</div>
      </div>
    </div>
  </div>
</section>
<!-- ═══════════ END VE: How-section Visual ═══════════ -->
"""

# ── 4. Dashboard Showcase (cloudsignals-findings.html) ───────────────────────
VE_DASHBOARD_SHOWCASE = """
<!-- ═══════════ VE: Dashboard Showcase ═══════════ -->
<section class="ve-dashboard-showcase">
  <div class="auto-container" style="position:relative;">
    <div class="ve-ds-header">
      <div class="ve-eyebrow" style="justify-content:center;margin-bottom:14px;">
        <span class="ve-eyebrow-dot"></span>&nbsp;Platform Reveal
      </div>
      <h2 class="ve-h2" style="text-align:center;">The dashboard your team<br><span class="ve-grad-cyan">actually wants to open.</span></h2>
      <p class="ve-sub centred">Every finding scored. Every risk prioritized. All your frameworks mapped automatically &mdash; in one unified, always-on workspace.</p>
    </div>
    <div class="ve-ds-grid">
      <div class="ve-vid-frame ve-ds-main">
        <div class="ve-vid-scanlines"></div>
        <img src="assets/images/brand/CS-Montage-1.png" alt="CloudSignals platform dashboard reveal">
        <video autoplay muted loop playsinline poster="assets/images/brand/CS-Montage-1.png">
          <source src="assets/videos/clip2-platform-reveal.mp4" type="video/mp4">
        </video>
        <div class="ve-vid-overlay"></div>
        <div class="ve-frame-label">Platform Overview</div>
      </div>
      <div class="ve-vid-frame ve-ds-side">
        <div class="ve-vid-scanlines"></div>
        <img src="assets/images/brand/CS-Montage-2.png" alt="Risk intelligence panels">
        <video autoplay muted loop playsinline poster="assets/images/brand/CS-Montage-2.png">
          <source src="assets/videos/clip3-risk-intelligence.mp4" type="video/mp4">
        </video>
        <div class="ve-vid-overlay"></div>
        <div class="ve-frame-label">Risk Intelligence</div>
      </div>
    </div>
    <div class="ve-cta-row">
      <a href="https://gcp-defense.aivric.com/sign-up?plan=pkg-cloudsignals-free&amp;source=cf_showcase" class="ve-btn primary"><i class="fas fa-rocket"></i>&nbsp;Launch free</a>
      <a href="request-demo.html" class="ve-btn ghost">Request a demo</a>
    </div>
  </div>
</section>
<!-- ═══════════ END VE: Dashboard Showcase ═══════════ -->
"""

# ── 5. Threat Intel Map (rogueagent.html) ────────────────────────────────────
VE_THREAT_INTEL = """
<!-- ═══════════ VE: Threat Intel Map ═══════════ -->
<section class="ve-threat-intel">
  <div class="auto-container" style="position:relative;">
    <div class="ve-ti-header">
      <div class="ve-eyebrow" style="justify-content:center;margin-bottom:14px;">
        <span class="ve-eyebrow-dot" style="background:var(--ve-red);box-shadow:0 0 6px var(--ve-red);"></span>&nbsp;Global Signal Coverage
      </div>
      <h2 class="ve-h2" style="text-align:center;">Attack surface telemetry.<br><span class="ve-grad-red">Everywhere your targets live.</span></h2>
      <p class="ve-sub centred">RogueAgent continuously maps your external attack surface and correlates it against live global threat intelligence &mdash; so you see what adversaries see before they act.</p>
    </div>
    <div class="ve-vid-frame ve-ti-frame">
      <div class="ve-vid-scanlines"></div>
      <img src="assets/images/brand/Threat-Signals-1.png" alt="Global threat intelligence map">
      <video autoplay muted loop playsinline poster="assets/images/brand/Threat-Signals-1.png">
        <source src="assets/videos/clip1-threat-signals.mp4" type="video/mp4">
      </video>
      <div class="ve-vid-overlay"></div>
      <div class="ve-ctrl-bar" style="bottom:16px;left:50%;transform:translateX(-50%);">
        <span class="ve-ctrl-live"><span class="ve-live-dot"></span>&nbsp;LIVE SIGNAL FEED</span>
        <span class="ve-ctrl-meta"><i class="fas fa-globe"></i>&nbsp;Global coverage</span>
      </div>
    </div>
    <div class="ve-ti-stats">
      <div class="ve-ti-stat"><span class="ve-ti-num">6</span><span class="ve-ti-lab">continents tracked</span></div>
      <div class="ve-ti-stat"><span class="ve-ti-num c">24/7</span><span class="ve-ti-lab">live signal feed</span></div>
      <div class="ve-ti-stat"><span class="ve-ti-num a">OSINT</span><span class="ve-ti-lab">+ commercial intel</span></div>
      <div class="ve-ti-stat"><span class="ve-ti-num p">ASM</span><span class="ve-ti-lab">external surface</span></div>
    </div>
  </div>
</section>
<!-- ═══════════ END VE: Threat Intel Map ═══════════ -->
"""

# ── 6. Vision AI Demo (aivric-vision-professional.html) ──────────────────────
VE_VISION_DEMO = """
<!-- ═══════════ VE: Vision AI Demo ═══════════ -->
<section class="ve-vision-demo">
  <div class="auto-container" style="position:relative;">
    <div class="ve-vd-header">
      <div class="ve-eyebrow purple" style="justify-content:center;margin-bottom:14px;">
        <span class="ve-eyebrow-dot"></span>&nbsp;AI Vision Intelligence
      </div>
      <h2 class="ve-h2" style="text-align:center;">Ask questions. Get answers.<br><span class="ve-grad-purple">Across your entire security posture.</span></h2>
      <p class="ve-sub centred">Vision AI ingests your complete cloud, compliance, and offensive intelligence dataset and makes it conversational. Query findings, generate reports, and surface insights in natural language.</p>
    </div>
    <div class="ve-vd-screens">
      <div class="ve-vid-frame ve-vd-frame">
        <div class="ve-vid-scanlines"></div>
        <img src="assets/images/app/VISION-Chat-Entry.jpg" alt="Vision AI chat interface">
        <div class="ve-vid-overlay" style="background:linear-gradient(135deg,rgba(167,139,250,.06) 0%,transparent 55%),linear-gradient(to bottom,transparent 65%,rgba(6,11,20,.7));"></div>
        <div class="ve-frame-label purple">Chat Entry</div>
      </div>
      <div class="ve-vid-frame ve-vd-frame">
        <div class="ve-vid-scanlines"></div>
        <img src="assets/images/app/VISION-Chat-QandA.jpg" alt="Vision AI Q&amp;A response">
        <div class="ve-vid-overlay" style="background:linear-gradient(135deg,rgba(167,139,250,.06) 0%,transparent 55%),linear-gradient(to bottom,transparent 65%,rgba(6,11,20,.7));"></div>
        <div class="ve-frame-label purple">AI Response</div>
      </div>
    </div>
    <div class="ve-cta-row">
      <a href="request-demo.html" class="ve-btn primary" style="background:var(--ve-purple);color:#fff;"><i class="fas fa-brain"></i>&nbsp;See Vision in action</a>
      <a href="pricing.html" class="ve-btn ghost" style="border-color:rgba(167,139,250,.35);color:var(--ve-purple);">View pricing</a>
    </div>
  </div>
</section>
<!-- ═══════════ END VE: Vision AI Demo ═══════════ -->
"""

# ── 7. RiskOps Portal (air-remediation.html) ─────────────────────────────────
VE_RISKOPS_PORTAL = """
<!-- ═══════════ VE: RiskOps Portal ═══════════ -->
<section class="ve-riskops-portal">
  <div class="auto-container" style="position:relative;">
    <div class="ve-rp-header">
      <div class="ve-eyebrow amber" style="justify-content:center;margin-bottom:14px;">
        <span class="ve-eyebrow-dot"></span>&nbsp;RiskOps Portal
      </div>
      <h2 class="ve-h2" style="text-align:center;">Your team's risk operations workspace.<br><span class="ve-grad-amber">Powered by AIRE.</span></h2>
      <p class="ve-sub centred">Submit remediation requests, track agentic fix progress, monitor playbook execution, and generate audit-ready evidence &mdash; all from one portal your security and compliance teams share.</p>
    </div>
    <div class="ve-vid-frame ve-rp-frame">
      <div class="ve-vid-scanlines"></div>
      <img src="assets/images/brand/RiskOps-Dashboard.png" alt="RiskOps Portal dashboard">
      <video autoplay muted loop playsinline poster="assets/images/brand/RiskOps-Dashboard.png">
        <source src="assets/videos/clip5-riskops-portal.mp4" type="video/mp4">
      </video>
      <div class="ve-vid-overlay" style="background:linear-gradient(135deg,rgba(255,214,58,.04) 0%,transparent 55%),linear-gradient(to bottom,transparent 60%,rgba(6,11,20,.7));"></div>
      <div class="ve-rp-ctrl">
        <span class="ve-ctrl-live" style="color:var(--ve-green);"><span class="ve-live-dot green"></span>&nbsp;PORTAL LIVE</span>
      </div>
    </div>
    <div class="ve-rp-feats">
      <div class="ve-rp-feat"><i class="fas fa-clipboard-list"></i><span>Request tracking</span></div>
      <div class="ve-rp-feat"><i class="fas fa-robot"></i><span>Agentic remediation</span></div>
      <div class="ve-rp-feat"><i class="fas fa-lock"></i><span>Confidential &amp; secure</span></div>
      <div class="ve-rp-feat"><i class="fas fa-award"></i><span>Audit-ready outcomes</span></div>
    </div>
    <div class="ve-cta-row">
      <a href="request-demo.html" class="ve-btn primary" style="background:var(--ve-amber);color:#030a12;"><i class="fas fa-flask"></i>&nbsp;Request alpha access</a>
      <a href="pricing.html" class="ve-btn ghost" style="border-color:rgba(255,214,58,.35);color:var(--ve-amber);">View pricing</a>
    </div>
  </div>
</section>
<!-- ═══════════ END VE: RiskOps Portal ═══════════ -->
"""

# ── 8. Trust Reel (pricing.html) ─────────────────────────────────────────────
VE_TRUST_REEL = """
<!-- ═══════════ VE: Trust Reel ═══════════ -->
<section class="ve-trust-reel">
  <div class="auto-container" style="position:relative;">
    <div class="ve-tr-inner">
      <div class="ve-tr-copy">
        <div class="ve-eyebrow"><span class="ve-eyebrow-dot"></span>&nbsp;Enterprise Grade</div>
        <h3>Security you can verify.<br><span class="ve-grad-cyan">Compliance you can prove.</span></h3>
        <p>Every AiVRIC deployment ships with immutable audit trails, zero-trust architecture, and evidence-grade reporting built in from day one &mdash; so you can show regulators and customers exactly what&rsquo;s protected.</p>
        <div style="margin-top:24px;display:flex;flex-wrap:wrap;gap:10px;">
          <span style="display:inline-flex;align-items:center;gap:6px;font-size:12px;color:#2ee59d;"><i class="fas fa-check-circle"></i> Customer-hosted, your data</span>
          <span style="display:inline-flex;align-items:center;gap:6px;font-size:12px;color:#2ee59d;"><i class="fas fa-check-circle"></i> SOC 2 / ISO 27001 mapping</span>
          <span style="display:inline-flex;align-items:center;gap:6px;font-size:12px;color:#2ee59d;"><i class="fas fa-check-circle"></i> Immutable audit trail</span>
          <span style="display:inline-flex;align-items:center;gap:6px;font-size:12px;color:#2ee59d;"><i class="fas fa-check-circle"></i> Zero-trust architecture</span>
        </div>
      </div>
      <div class="ve-vid-frame ve-tr-frame">
        <div class="ve-vid-scanlines"></div>
        <img src="assets/images/service/shield-glow.avif" alt="AiVRIC security shield">
        <video autoplay muted loop playsinline>
          <source src="assets/videos/clip7-shield-activation.mp4" type="video/mp4">
        </video>
        <div class="ve-vid-overlay"></div>
      </div>
    </div>
  </div>
</section>
<!-- ═══════════ END VE: Trust Reel ═══════════ -->
"""

# ── 9. Blog hero video background (template — asset_prefix is "" or "../../") ─
def ve_ba_vid_bg(clip_mp4, poster_png, asset_prefix=""):
    return f"""
<div class="ve-ba-vid-bg">
  <video autoplay muted loop playsinline poster="{asset_prefix}assets/images/brand/{poster_png}">
    <source src="{asset_prefix}assets/videos/{clip_mp4}" type="video/mp4">
  </video>
  <div class="ve-ba-vid-grad"></div>
</div>
"""


# ════════════════════════════════════════════════════════════════════════════
# PAGE ENHANCERS
# ════════════════════════════════════════════════════════════════════════════

def enhance_index():
    path = SITE / "index.html"
    html = path.read_text(encoding="utf-8")
    html = add_css(html)

    # 1. Platform Film — before CloudSignals spotlight
    if not guard(html, "ve-platform-film"):
        html = before(html, '<section class="hp-cs-spotlight">', VE_PLATFORM_FILM)

    # 2. Threat map background inside stats section
    if not guard(html, "ve-threat-bg"):
        html = after(html, '<section class="hp-stats-section">\n', VE_THREAT_BG)

    # 3. How-section visual — before Data Sovereignty section
    if not guard(html, "ve-how-visual"):
        html = before(html, '<section class="hp-deploy-section">', VE_HOW_VISUAL)

    save(path, html)


def enhance_cloudsignals_findings():
    path = SITE / "cloudsignals-findings.html"
    html = path.read_text(encoding="utf-8")
    html = add_css(html)

    # Dashboard showcase — after cf-hero closes, before capabilities
    if not guard(html, "ve-dashboard-showcase"):
        anchor = '</section>\n\n          <!-- ── CAPABILITIES'
        html = after(html, anchor, VE_DASHBOARD_SHOWCASE)

    save(path, html)


def _enhance_product_page(filename, ve_section, guard_str,
                           close_anchor='</section>\n\n          <div class="csp-divider'):
    path = SITE / filename
    html = path.read_text(encoding="utf-8")
    html = add_css(html)
    if not guard(html, guard_str):
        html = after(html, close_anchor, ve_section)
    save(path, html)


def enhance_rogueagent():
    _enhance_product_page("rogueagent.html", VE_THREAT_INTEL, "ve-threat-intel")


def enhance_vision():
    _enhance_product_page("aivric-vision-professional.html", VE_VISION_DEMO, "ve-vision-demo")


def enhance_remediation():
    _enhance_product_page("air-remediation.html", VE_RISKOPS_PORTAL, "ve-riskops-portal")


def enhance_pricing():
    path = SITE / "pricing.html"
    html = path.read_text(encoding="utf-8")
    html = add_css(html)
    if not guard(html, "ve-trust-reel"):
        html = before(html, '<section class="pricing-pillar">', VE_TRUST_REEL)
    save(path, html)


# Blog pages: article → (clip mp4, poster png)
BLOG_CLIPS = {
    "blog-why-continuous-compliance-matters.html": ("clip2-platform-reveal.mp4",    "CS-Montage-1.png"),
    "blog-integrating-into-DevOps.html":           ("clip3-risk-intelligence.mp4",   "CS-Montage-2.png"),
    "blog-future-of-cloud-security.html":           ("clip1-threat-signals.mp4",      "Threat-Signals-1.png"),
    "blog-details.html":                            ("clip3-risk-intelligence.mp4",   "CS-Montage-2.png"),
}
# Subdirectory blog
BLOG_SUB = {
    "assets/blog-managing-healthcare-risk/index.html": ("clip5-riskops-portal.mp4", "RiskOps-Dashboard.png", "../../"),
}

def enhance_blogs():
    # Root-level blog pages
    for fname, (clip, poster) in BLOG_CLIPS.items():
        path = SITE / fname
        if not path.exists():
            print(f"  SKIP (not found): {fname}")
            continue
        html = path.read_text(encoding="utf-8")
        html = add_css(html)
        if not guard(html, "ve-ba-vid-bg"):
            html = after(html, '<section class="ba-hero">\n', ve_ba_vid_bg(clip, poster))
        save(path, html)

    # Subdirectory pages
    for fpath, (clip, poster, prefix) in BLOG_SUB.items():
        path = SITE / fpath
        if not path.exists():
            print(f"  SKIP (not found): {fpath}")
            continue
        html = path.read_text(encoding="utf-8")
        html = add_css(html, CSS_LINK2)
        if not guard(html, "ve-ba-vid-bg"):
            html = after(html, '<section class="ba-hero">\n', ve_ba_vid_bg(clip, poster, prefix))
        save(path, html)


# ════════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("AiVRIC Visual Enhancement — applying to all target pages...\n")

    enhance_index()
    enhance_cloudsignals_findings()
    enhance_rogueagent()
    enhance_vision()
    enhance_remediation()
    enhance_pricing()
    enhance_blogs()

    print(f"\nDone — all visual enhancements applied.")
    print()
    print("NEXT STEPS — drop these files in place to activate visuals:")
    print("  assets/images/brand/  ← Threat-Signals-1.png, CS-Montage-1.png,")
    print("                           CS-Montage-2.png, Main-Screen-Promo.png,")
    print("                           RiskOps-Dashboard.png")
    print("  assets/videos/        ← clip1-threat-signals.mp4  ..  clip7-shield-activation.mp4")
    print()
    print("Video slots show the poster image (brand PNG) while videos are pending.")
    print("Brand PNG slots show a dark glass container while images are pending.")
