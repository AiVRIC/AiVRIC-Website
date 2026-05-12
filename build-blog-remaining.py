#!/usr/bin/env python3
"""
Rebuild two remaining blog pages:
  1. blog-details.html              → "The CISO's Guide to Cloud Security Posture Management"
  2. assets/blog-managing-healthcare-risk/index.html → "Managing AI Risk in Healthcare" (redesigned)

For the subdirectory page all relative paths are rewritten with ../../ prefix.
"""
import re
from pathlib import Path

SITE     = Path(r"C:\Projects\AiVRIC-Website")
TEMPLATE = SITE / "cloudsignals-findings.html"

raw_t = TEMPLATE.read_text(encoding="utf-8", errors="replace")

def between(src, start, end):
    s = src.find(start)
    e = src.find(end, s) + len(end)
    return src[s:e] if s != -1 else ""

NAV_ROOT   = between(raw_t, "<!-- main header -->", "<!-- End Mobile Menu -->")
FOOTER_ROOT = between(raw_t, "<!-- main-footer -->",  "<!-- main-footer end -->")

gf_s = raw_t.find('<style id="gf-styles">')
gf_e = raw_t.find("</style>", gf_s) + len("</style>")
GF_STYLES = raw_t[gf_s:gf_e] if gf_s != -1 else ""

# Rewrite relative paths in NAV/FOOTER for subdirectory (../../) usage
_REL_HREF = re.compile(r'(href|src)="(?!https?://|//|#|/|mailto:|tel:)([^"]+)"')

def prefix_paths(html, prefix):
    return _REL_HREF.sub(lambda m: f'{m.group(1)}="{prefix}{m.group(2)}"', html)

NAV_SUB    = prefix_paths(NAV_ROOT,    "../../")
FOOTER_SUB = prefix_paths(FOOTER_ROOT, "../../")

GTAG = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-EG2Q8GD30V"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-EG2Q8GD30V');
</script>"""

SCRIPTS_ROOT = """<script src="assets/js/jquery.js"></script>
<script src="assets/js/popper.min.js"></script>
<script src="assets/js/bootstrap.min.js"></script>
<script src="assets/js/owl.js"></script>
<script src="assets/js/wow.js"></script>
<script src="assets/js/validation.js"></script>
<script src="assets/js/jquery.fancybox.js"></script>
<script src="assets/js/appear.js"></script>
<script src="assets/js/scrollbar.js"></script>
<script src="assets/js/isotope.js"></script>
<script src="assets/js/jquery.nice-select.min.js"></script>
<script src="assets/js/parallax-scroll.js"></script>
<script src="assets/js/aivric-preloader.js"></script>
<script src="assets/js/script.js"></script>
<script src="assets/js/mega-hover.js"></script>
<script src="assets/js/mega-tabs.js"></script>"""

SCRIPTS_SUB = prefix_paths(SCRIPTS_ROOT, "../../")

PRELOADER_TPL = """        <!-- preloader -->
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
        <!-- preloader end -->"""

TOC_JS = """<script>
(function(){
  var tocLinks = document.querySelectorAll('.ba-toc a[href^="#"]');
  if(!tocLinks.length) return;
  var headings = [];
  tocLinks.forEach(function(a){
    var el = document.querySelector(a.getAttribute('href'));
    if(el) headings.push({el:el,a:a});
  });
  function onScroll(){
    var sy = window.scrollY + 120;
    var active = null;
    headings.forEach(function(h){ if(h.el.offsetTop <= sy) active = h; });
    tocLinks.forEach(function(a){ a.classList.remove('active'); });
    if(active) active.a.classList.add('active');
  }
  window.addEventListener('scroll', onScroll, {passive:true});
  onScroll();
})();
</script>"""

BA_CSS = """<style>
/* ============================================================
   AiVRIC Blog Article — ba- design system
   ============================================================ */
:root{
  --ba-bg:#060b14; --ba-surface:#0c1525; --ba-surface-2:#0f1b2e;
  --ba-border:rgba(148,163,184,.1); --ba-border-2:rgba(148,163,184,.18);
  --ba-text:#e2e8f0; --ba-text-2:#cbd5e1; --ba-muted:#64748b; --ba-muted-2:#94a3b8;
  --ba-cyan:#00d1ff; --ba-green:#2ee59d; --ba-amber:#ffd63a;
  --ba-purple:#a78bfa; --ba-orange:#fb923c;
  --ba-radius:14px;
}
body.ba-page{background:var(--ba-bg);color:var(--ba-text);font-family:'Inter',system-ui,sans-serif;-webkit-font-smoothing:antialiased;}
.ba-hero{padding:80px 0 0;position:relative;overflow:hidden;}
.ba-hero::before{content:'';position:absolute;inset:0;background:radial-gradient(900px 600px at 70% 0%,rgba(0,209,255,.07),transparent 60%),radial-gradient(700px 500px at 0% 60%,rgba(46,113,229,.06),transparent 60%);pointer-events:none;}
.ba-hero-inner{max-width:820px;margin:0 auto;padding:0 24px;}
.ba-meta-row{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-bottom:20px;}
.ba-cat{display:inline-flex;align-items:center;gap:6px;padding:4px 12px;border-radius:100px;font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;}
.ba-cat.compliance{background:rgba(0,209,255,.1);border:1px solid rgba(0,209,255,.25);color:var(--ba-cyan);}
.ba-cat.devsecops{background:rgba(46,229,157,.1);border:1px solid rgba(46,229,157,.25);color:var(--ba-green);}
.ba-cat.ai{background:rgba(167,139,250,.1);border:1px solid rgba(167,139,250,.25);color:var(--ba-purple);}
.ba-cat.healthcare{background:rgba(251,146,60,.1);border:1px solid rgba(251,146,60,.25);color:var(--ba-orange);}
.ba-read-time{font-size:12px;color:var(--ba-muted);display:flex;align-items:center;gap:5px;}
.ba-hero-title{font-family:'Jost','Inter',sans-serif;font-size:clamp(32px,5vw,52px);font-weight:800;line-height:1.08;letter-spacing:-.5px;color:#f8fafc;margin:0 0 20px;}
.ba-hero-lead{font-size:18px;line-height:1.75;color:var(--ba-text-2);margin:0 0 28px;max-width:72ch;}
.ba-author-row{display:flex;align-items:center;gap:12px;padding-bottom:28px;border-bottom:1px solid var(--ba-border);}
.ba-author-avatar{width:40px;height:40px;border-radius:50%;background:rgba(0,209,255,.1);border:1px solid rgba(0,209,255,.2);display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.ba-author-avatar img{width:26px;height:auto;}
.ba-author-name{font-size:13.5px;font-weight:600;color:#f1f5f9;}
.ba-author-role{font-size:12px;color:var(--ba-muted);}
.ba-hero-visual{position:relative;margin:0;height:380px;overflow:hidden;}
.ba-hero-visual img{width:100%;height:100%;object-fit:cover;display:block;mask-image:linear-gradient(to bottom,rgba(0,0,0,1) 55%,rgba(0,0,0,0) 100%);-webkit-mask-image:linear-gradient(to bottom,rgba(0,0,0,1) 55%,rgba(0,0,0,0) 100%);}
.ba-layout{max-width:1200px;margin:0 auto;padding:56px 24px 80px;display:grid;grid-template-columns:1fr 320px;gap:52px;align-items:start;}
@media(max-width:1024px){.ba-layout{grid-template-columns:1fr;}}
.ba-body h2{font-family:'Jost','Inter',sans-serif;font-size:28px;font-weight:800;color:#f1f5f9;margin:48px 0 14px;padding-left:16px;border-left:3px solid var(--ba-cyan);line-height:1.2;}
.ba-body h3{font-family:'Jost','Inter',sans-serif;font-size:22px;font-weight:700;color:#f1f5f9;margin:36px 0 12px;padding-left:14px;border-left:3px solid rgba(0,209,255,.4);line-height:1.25;}
.ba-body h4{font-size:16px;font-weight:700;color:#e2e8f0;margin:28px 0 8px;display:flex;align-items:center;gap:8px;}
.ba-body h4::before{content:'';width:6px;height:6px;border-radius:50%;background:var(--ba-cyan);flex-shrink:0;}
.ba-body p{font-size:16px;line-height:1.85;color:var(--ba-text-2);margin:0 0 20px;}
.ba-body strong{color:#f1f5f9;}
.ba-body a{color:var(--ba-cyan);text-decoration:none;}
.ba-body a:hover{text-decoration:underline;}
.ba-callout{background:var(--ba-surface);border:1px solid var(--ba-border-2);border-left:3px solid var(--ba-cyan);border-radius:var(--ba-radius);padding:22px 24px;margin:28px 0;}
.ba-callout.green{border-left-color:var(--ba-green);}
.ba-callout.amber{border-left-color:var(--ba-amber);}
.ba-callout.purple{border-left-color:var(--ba-purple);}
.ba-callout.orange{border-left-color:var(--ba-orange);}
.ba-callout-label{font-size:10px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--ba-cyan);margin-bottom:8px;}
.ba-callout.green .ba-callout-label{color:var(--ba-green);}
.ba-callout.amber .ba-callout-label{color:var(--ba-amber);}
.ba-callout.purple .ba-callout-label{color:var(--ba-purple);}
.ba-callout.orange .ba-callout-label{color:var(--ba-orange);}
.ba-callout p{margin:0;font-size:15px;line-height:1.7;color:var(--ba-text-2);}
.ba-quote{margin:36px 0;padding:24px 28px;background:var(--ba-surface);border-radius:var(--ba-radius);position:relative;}
.ba-quote::before{content:'\201C';position:absolute;top:-10px;left:24px;font-size:64px;line-height:1;color:var(--ba-cyan);opacity:.35;font-family:Georgia,serif;}
.ba-quote p{font-size:18px;line-height:1.7;font-style:italic;color:#e2e8f0;margin:0;padding-left:8px;}
.ba-checklist{list-style:none;padding:0;margin:0 0 28px;display:flex;flex-direction:column;gap:10px;}
.ba-checklist li{display:flex;gap:12px;align-items:flex-start;font-size:15px;color:var(--ba-text-2);line-height:1.65;}
.ba-checklist li::before{content:'\f058';font-family:'Font Awesome 5 Free';font-weight:900;color:var(--ba-cyan);font-size:13px;margin-top:2px;flex-shrink:0;}
.ba-checklist.green li::before{color:var(--ba-green);}
.ba-checklist.orange li::before{color:var(--ba-orange);}
.ba-checklist strong{color:#f1f5f9;}
.ba-steps{display:flex;flex-direction:column;gap:0;margin:0 0 28px;}
.ba-step{display:flex;gap:18px;align-items:flex-start;padding:18px 0;border-bottom:1px solid var(--ba-border);}
.ba-step:last-child{border-bottom:none;}
.ba-step-num{width:32px;height:32px;border-radius:50%;background:rgba(0,209,255,.12);border:1px solid rgba(0,209,255,.3);display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;color:var(--ba-cyan);flex-shrink:0;}
.ba-step-body h5{font-size:15px;font-weight:700;color:#f1f5f9;margin:0 0 4px;}
.ba-step-body p{font-size:14px;color:var(--ba-text-2);margin:0;line-height:1.65;}
.ba-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:28px 0;}
@media(max-width:600px){.ba-stats{grid-template-columns:1fr 1fr;}}
.ba-stat{background:var(--ba-surface);border:1px solid var(--ba-border-2);border-radius:var(--ba-radius);padding:20px;text-align:center;}
.ba-stat-val{font-family:'Jost',sans-serif;font-size:32px;font-weight:800;color:var(--ba-cyan);line-height:1;margin-bottom:6px;}
.ba-stat-val.green{color:var(--ba-green);}
.ba-stat-val.amber{color:var(--ba-amber);}
.ba-stat-val.orange{color:var(--ba-orange);}
.ba-stat-label{font-size:12px;color:var(--ba-muted);line-height:1.4;}
.ba-img-block{margin:32px 0;border-radius:var(--ba-radius);overflow:hidden;border:1px solid var(--ba-border);}
.ba-img-block img{width:100%;display:block;}
.ba-img-caption{padding:12px 16px;background:var(--ba-surface);font-size:12.5px;color:var(--ba-muted);line-height:1.5;}
.ba-tags{display:flex;flex-wrap:wrap;gap:8px;margin-top:40px;padding-top:28px;border-top:1px solid var(--ba-border);}
.ba-tag{padding:5px 14px;border-radius:100px;background:rgba(148,163,184,.07);border:1px solid var(--ba-border-2);font-size:12px;color:var(--ba-muted-2);text-decoration:none;transition:all .18s;}
.ba-tag:hover{background:rgba(0,209,255,.09);border-color:rgba(0,209,255,.3);color:var(--ba-cyan);}
.ba-author-card{display:flex;gap:18px;align-items:flex-start;background:var(--ba-surface);border:1px solid var(--ba-border-2);border-radius:var(--ba-radius);padding:24px;margin-top:40px;}
.ba-author-card-avatar{width:56px;height:56px;border-radius:50%;background:rgba(0,209,255,.1);border:1px solid rgba(0,209,255,.2);display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.ba-author-card-avatar img{width:36px;height:auto;}
.ba-author-card-name{font-size:16px;font-weight:700;color:#f1f5f9;margin-bottom:2px;}
.ba-author-card-role{font-size:12px;color:var(--ba-cyan);margin-bottom:8px;font-weight:600;}
.ba-author-card-bio{font-size:13.5px;color:var(--ba-text-2);line-height:1.65;margin:0;}
.ba-sidebar{position:sticky;top:88px;display:flex;flex-direction:column;gap:20px;}
.ba-sidebar-card{background:var(--ba-surface);border:1px solid var(--ba-border-2);border-radius:var(--ba-radius);padding:20px;}
.ba-sidebar-title{font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:var(--ba-muted-2);margin-bottom:14px;padding-bottom:10px;border-bottom:1px solid var(--ba-border);}
.ba-toc{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:6px;}
.ba-toc li a{font-size:13px;color:var(--ba-muted);text-decoration:none;display:block;padding:4px 0 4px 10px;border-left:2px solid transparent;transition:all .15s;line-height:1.4;}
.ba-toc li a:hover{color:#f1f5f9;border-left-color:var(--ba-cyan);}
.ba-toc li a.active{color:var(--ba-cyan);border-left-color:var(--ba-cyan);}
.ba-related{display:flex;flex-direction:column;gap:14px;}
.ba-related-item{display:flex;gap:12px;text-decoration:none;transition:opacity .15s;}
.ba-related-item:hover{opacity:.82;}
.ba-related-img{width:60px;height:48px;border-radius:8px;object-fit:cover;flex-shrink:0;background:var(--ba-surface-2);}
.ba-related-title{font-size:13px;font-weight:600;color:#e2e8f0;line-height:1.4;margin-bottom:3px;}
.ba-related-date{font-size:11px;color:var(--ba-muted);}
.ba-sidebar-cta{background:linear-gradient(135deg,rgba(0,209,255,.12),rgba(46,229,157,.08));border:1px solid rgba(0,209,255,.25);border-radius:var(--ba-radius);padding:22px;text-align:center;}
.ba-sidebar-cta-icon{font-size:28px;color:var(--ba-cyan);margin-bottom:10px;}
.ba-sidebar-cta h4{font-size:16px;font-weight:700;color:#f1f5f9;margin:0 0 6px;}
.ba-sidebar-cta p{font-size:13px;color:var(--ba-muted);margin:0 0 14px;line-height:1.55;}
.ba-sidebar-cta a{display:inline-flex;align-items:center;gap:7px;background:var(--ba-cyan);color:#030a12;padding:9px 18px;border-radius:100px;font-size:13px;font-weight:700;text-decoration:none;transition:all .2s;}
.ba-sidebar-cta a:hover{background:#33daff;transform:translateY(-1px);}
.ba-sidebar-tags{display:flex;flex-wrap:wrap;gap:7px;}
.ba-cta-banner{background:linear-gradient(135deg,#0c1525 0%,#0f1b2e 100%);border-top:1px solid var(--ba-border);border-bottom:1px solid var(--ba-border);padding:64px 24px;text-align:center;position:relative;overflow:hidden;}
.ba-cta-banner::before{content:'';position:absolute;inset:0;background:radial-gradient(600px 400px at 50% 50%,rgba(0,209,255,.06),transparent 70%);pointer-events:none;}
.ba-cta-banner-eyebrow{font-size:11px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--ba-cyan);margin-bottom:14px;}
.ba-cta-banner h2{font-family:'Jost',sans-serif;font-size:clamp(26px,4vw,40px);font-weight:800;color:#f8fafc;margin:0 0 14px;letter-spacing:-.3px;}
.ba-cta-banner p{font-size:16px;color:var(--ba-text-2);max-width:540px;margin:0 auto 28px;line-height:1.7;}
.ba-cta-banner-actions{display:flex;align-items:center;justify-content:center;gap:12px;flex-wrap:wrap;}
.ba-btn-primary{display:inline-flex;align-items:center;gap:8px;padding:12px 26px;border-radius:100px;background:var(--ba-cyan);color:#030a12;font-size:14px;font-weight:700;text-decoration:none;transition:all .2s;position:relative;z-index:1;}
.ba-btn-primary:hover{background:#33daff;transform:translateY(-1px);}
.ba-btn-ghost{display:inline-flex;align-items:center;gap:8px;padding:12px 26px;border-radius:100px;background:transparent;color:#f1f5f9;font-size:14px;font-weight:700;text-decoration:none;border:1px solid rgba(255,255,255,.2);transition:all .2s;position:relative;z-index:1;}
.ba-btn-ghost:hover{background:rgba(255,255,255,.07);transform:translateY(-1px);}
</style>"""

def head_block(title, meta_desc, asset_prefix="assets/"):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
<title>{title} | AiVRIC</title>
<meta name="description" content="{meta_desc}">
<meta property="og:title" content="{title} | AiVRIC">
<meta property="og:description" content="{meta_desc}">
<meta property="og:type" content="article">
<link rel="icon" href="{asset_prefix}images/Aivric-favicon-logo.ico" type="image/x-icon">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Jost:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap" rel="stylesheet">
<link href="{asset_prefix}css/aivric-preloader.css" rel="stylesheet">
<link href="{asset_prefix}css/font-awesome-all.css" rel="stylesheet">
<link href="{asset_prefix}css/flaticon.css" rel="stylesheet">
<link href="{asset_prefix}css/owl.css" rel="stylesheet">
<link href="{asset_prefix}css/bootstrap.css" rel="stylesheet">
<link href="{asset_prefix}css/animate.css" rel="stylesheet">
<link href="{asset_prefix}css/color.css" rel="stylesheet">
<link href="{asset_prefix}css/elpath.css" rel="stylesheet">
<link href="{asset_prefix}css/style.css?v=20250115" rel="stylesheet">
<link href="{asset_prefix}css/responsive.css" rel="stylesheet">
<link href="{asset_prefix}css/custom.css?v=20250115" rel="stylesheet">
{BA_CSS}
{GF_STYLES}
</head>"""

def page(title, meta_desc, body_content, asset_prefix="assets/", nav=None, footer=None, scripts=None):
    nav     = nav     or NAV_ROOT
    footer  = footer  or FOOTER_ROOT
    scripts = scripts or SCRIPTS_ROOT
    preloader = PRELOADER_TPL.replace("{prefix}", asset_prefix)
    return f"""{head_block(title, meta_desc, asset_prefix)}
{GTAG}
<body class="ba-page">
<div class="boxed_wrapper">

{preloader}

{nav}

{body_content}

{footer}
<!-- main-footer end -->

<div class="scroll-to-top">
  <div><div class="scroll-top-inner">
    <div class="scroll-bar"><div class="bar-inner"></div></div>
    <div class="scroll-bar-text">Go To Top</div>
  </div></div>
</div>

</div>
{scripts}
{TOC_JS}
</body>
</html>"""


# ════════════════════════════════════════════════════════════════════════════
# ARTICLE — blog-details.html
# "The CISO's Guide to Cloud Security Posture Management"
# ════════════════════════════════════════════════════════════════════════════
CSPM_BODY = """
<section class="ba-hero">
  <div class="ba-hero-inner">
    <div class="ba-meta-row">
      <span class="ba-cat compliance"><i class="fas fa-cloud"></i>&nbsp;Cloud Security</span>
      <span class="ba-read-time"><i class="far fa-clock"></i>&nbsp;11 min read</span>
      <span class="ba-read-time">April 18, 2025</span>
    </div>
    <h1 class="ba-hero-title" id="top">The CISO's Guide to Cloud Security Posture Management</h1>
    <p class="ba-hero-lead">Multi-cloud adoption is outpacing traditional security controls. CSPM gives CISOs the continuous visibility, risk context, and compliance evidence they need to govern cloud environments with confidence.</p>
    <div class="ba-author-row">
      <div class="ba-author-avatar"><img src="assets/images/logo/aivric.svg" alt="AiVRIC"></div>
      <div>
        <div class="ba-author-name">AiVRIC Team</div>
        <div class="ba-author-role">Security &amp; Compliance Innovation</div>
      </div>
    </div>
  </div>
  <div class="ba-hero-visual">
    <img src="assets/images/blog/digital-cloud-grid.avif" alt="Cloud security posture management">
  </div>
</section>

<div class="ba-layout">
  <article class="ba-body">

    <p>Cloud environments change fast. Developers spin up resources, IAM policies are modified, new integrations are added — often without a security review. Traditional perimeter-based security doesn't scale to this pace. Cloud Security Posture Management (CSPM) was built specifically for this challenge: giving security teams continuous, automated visibility into how cloud resources are configured and whether they meet security and compliance requirements.</p>

    <div class="ba-stats">
      <div class="ba-stat">
        <div class="ba-stat-val">99%</div>
        <div class="ba-stat-label">of cloud security failures through 2025 will be the customer's fault, not the cloud provider's (Gartner)</div>
      </div>
      <div class="ba-stat">
        <div class="ba-stat-val green">68%</div>
        <div class="ba-stat-label">of organizations report a cloud misconfiguration incident in the last year</div>
      </div>
      <div class="ba-stat">
        <div class="ba-stat-val amber">200+</div>
        <div class="ba-stat-label">misconfiguration types that AiVRIC CloudSignals detects across AWS, Azure, GCP, and OCI</div>
      </div>
    </div>

    <h2 id="what-is-cspm">What Is CSPM — and Why Does It Matter Now?</h2>

    <p>CSPM tools continuously evaluate the configuration of cloud resources — compute, storage, networking, identity, and managed services — against security best practices and compliance frameworks. When something drifts from a safe baseline, CSPM surfaces the issue, estimates the risk, and maps it to the relevant control or framework requirement.</p>

    <div class="ba-callout">
      <div class="ba-callout-label">Why CSPM Is a Board-Level Issue</div>
      <p>A single misconfigured S3 bucket or an overpermissive IAM role can expose sensitive customer data, violate GDPR or HIPAA, and trigger regulatory investigation. CSPM is the first line of defense against the most common root cause of cloud breaches: human configuration error.</p>
    </div>

    <h2 id="what-cspm-covers">What CSPM Covers Across Your Cloud Estate</h2>

    <p>Modern CSPM platforms monitor configuration across every layer of the cloud stack:</p>

    <ul class="ba-checklist">
      <li><strong>Identity and access management</strong> — overpermissive roles, unused credentials, missing MFA, and cross-account trust relationships.</li>
      <li><strong>Storage and data exposure</strong> — public buckets, unencrypted volumes, missing versioning, and data residency violations.</li>
      <li><strong>Networking and perimeter</strong> — open security groups, unrestricted ingress rules, missing VPC flow logs, and exposed management ports.</li>
      <li><strong>Encryption and key management</strong> — unencrypted databases, weak key rotation policies, and CMK configuration gaps.</li>
      <li><strong>Logging and monitoring</strong> — missing CloudTrail coverage, disabled audit logs, and insufficient alerting configurations.</li>
      <li><strong>Managed services and serverless</strong> — Lambda permission boundaries, API Gateway exposure, and container registry access controls.</li>
    </ul>

    <h2 id="cspm-vs-ciem">CSPM vs. CIEM vs. CNAPP — Cutting Through the Acronyms</h2>

    <p>The cloud security market has fragmented into overlapping categories. Here's how to think about where each fits:</p>

    <div class="ba-callout amber">
      <div class="ba-callout-label">Quick Reference</div>
      <p><strong>CSPM</strong> — cloud configuration posture (what is misconfigured?) &bull; <strong>CIEM</strong> — cloud identity entitlements (who has too much access?) &bull; <strong>CWPP</strong> — workload protection (is runtime behavior safe?) &bull; <strong>CNAPP</strong> — unified platform combining all of the above. AiVRIC CloudSignals+RiskOps covers CSPM and CIEM with GRC-grade compliance mapping.</p>
    </div>

    <h2 id="framework-mapping">CSPM and Compliance: Framework-Aware Posture</h2>

    <p>The most powerful aspect of modern CSPM is its ability to translate technical findings into compliance language. When AiVRIC detects that CloudTrail logging is disabled in an AWS account, it doesn't just flag a misconfiguration — it maps the finding to SOC 2 CC7.2, PCI DSS Requirement 10, ISO 27001 A.12.4, and CMMC Practice AU.2.042 simultaneously.</p>

    <h3 id="soc2">SOC 2</h3>
    <p>AiVRIC continuously validates the technical controls underpinning SOC 2 Trust Service Criteria — logging, access control, change management, availability, and encryption — and captures time-stamped evidence suitable for Type 2 audit packages.</p>

    <h3 id="pci-dss">PCI DSS 4.0</h3>
    <p>For organizations processing cardholder data in cloud environments, AiVRIC monitors network segmentation, encryption of data in transit and at rest, access controls, and logging — mapping findings directly to PCI DSS 4.0 requirements.</p>

    <h3 id="iso27001">ISO 27001</h3>
    <p>AiVRIC aligns technical cloud checks to Annex A controls and tracks how cloud configuration changes impact your ISMS over time — supporting both initial certification and ongoing surveillance audits.</p>

    <div class="ba-img-block">
      <img src="assets/images/blog/compliance-risk-dashboard.avif" alt="CSPM compliance dashboard">
      <div class="ba-img-caption">Framework-aware dashboards show coverage, gaps, and trending risk across SOC 2, ISO 27001, PCI DSS, and CMMC simultaneously.</div>
    </div>

    <h2 id="aivric-cspm">How AiVRIC CloudSignals+RiskOps Delivers CSPM</h2>

    <p>AiVRIC CloudSignals+RiskOps is the platform's CSPM and compliance engine. It connects to cloud accounts via read-only API access, runs continuous assessments, and surfaces findings with full framework context and risk scoring.</p>

    <div class="ba-steps">
      <div class="ba-step">
        <div class="ba-step-num">1</div>
        <div class="ba-step-body">
          <h5>Connect in minutes</h5>
          <p>AiVRIC connects to AWS, Azure, GCP, and OCI via read-only IAM roles. No agents, no network changes, no credentials stored in the platform.</p>
        </div>
      </div>
      <div class="ba-step">
        <div class="ba-step-num">2</div>
        <div class="ba-step-body">
          <h5>Baseline your posture</h5>
          <p>An initial scan surfaces all current misconfigurations, maps them to frameworks, and establishes a risk-scored baseline across every account and region.</p>
        </div>
      </div>
      <div class="ba-step">
        <div class="ba-step-num">3</div>
        <div class="ba-step-body">
          <h5>Monitor continuously</h5>
          <p>Scheduled and event-driven scans detect new drift as it happens — whether from a developer change, a Terraform apply, or a manual console action.</p>
        </div>
      </div>
      <div class="ba-step">
        <div class="ba-step-num">4</div>
        <div class="ba-step-body">
          <h5>Remediate and prove it</h5>
          <p>Findings route to Jira, ServiceNow, or Azure DevOps. Once remediated, AiVRIC re-scans and captures updated evidence — closing the loop for auditors.</p>
        </div>
      </div>
    </div>

    <h2 id="risk-prioritization">Moving Beyond Findings: Risk-Based Prioritization</h2>

    <p>The biggest challenge with CSPM isn't detection — it's prioritization. A typical multi-cloud environment can surface hundreds of findings per week. Without context, teams either ignore low-severity noise or — worse — miss a critical exposure buried in the queue.</p>

    <div class="ba-quote">
      <p>The question isn't "what's misconfigured?" — it's "which misconfigurations actually threaten the business?" Risk-based prioritization is what separates a CSPM tool from a CSPM program.</p>
    </div>

    <p>AiVRIC scores findings using multiple context signals:</p>

    <ul class="ba-checklist green">
      <li><strong>Asset criticality</strong> — production workloads and data stores are scored higher than development environments.</li>
      <li><strong>Data classification</strong> — findings affecting resources storing PII, PHI, or cardholder data are elevated automatically.</li>
      <li><strong>Exposure path</strong> — internet-facing resources with misconfigurations rank above internal-only assets.</li>
      <li><strong>Framework impact</strong> — findings that break multiple controls across multiple frameworks are weighted accordingly.</li>
      <li><strong>Trend analysis</strong> — recurring issues in the same account or team signal a systemic problem, not a one-off.</li>
    </ul>

    <h2 id="building-program">Building a Mature CSPM Program</h2>

    <p>CSPM is not a tool you deploy and forget. The most effective programs treat it as a continuous operating discipline:</p>

    <div class="ba-callout green">
      <div class="ba-callout-label">Program Maturity Framework</div>
      <p><strong>Level 1 — Visibility:</strong> all accounts connected, baseline established, critical findings identified. <strong>Level 2 — Remediation:</strong> findings routed to owners, MTTR tracked, recurring issues addressed. <strong>Level 3 — Prevention:</strong> CI/CD gates, policy-as-code, developer self-service. <strong>Level 4 — Assurance:</strong> continuous evidence, executive reporting, audit-ready always.</p>
    </div>

    <div class="ba-tags">
      <a href="blog-portal.html" class="ba-tag">CSPM</a>
      <a href="blog-portal.html" class="ba-tag">Cloud Security</a>
      <a href="blog-portal.html" class="ba-tag">Compliance</a>
      <a href="blog-portal.html" class="ba-tag">Multi-Cloud</a>
      <a href="blog-portal.html" class="ba-tag">SOC 2</a>
      <a href="blog-portal.html" class="ba-tag">Risk Management</a>
      <a href="blog-portal.html" class="ba-tag">GRC</a>
    </div>

    <div class="ba-author-card">
      <div class="ba-author-card-avatar"><img src="assets/images/logo/aivric.svg" alt="AiVRIC"></div>
      <div>
        <div class="ba-author-card-name">AiVRIC Team</div>
        <div class="ba-author-card-role">Security &amp; Compliance Innovation</div>
        <p class="ba-author-card-bio">The AiVRIC Team brings together cloud-security architects, compliance specialists, and DevSecOps practitioners focused on building practical, automation-first ways to manage risk in modern digital environments.</p>
      </div>
    </div>

  </article>

  <aside class="ba-sidebar">
    <div class="ba-sidebar-card">
      <div class="ba-sidebar-title">In This Article</div>
      <ul class="ba-toc">
        <li><a href="#what-is-cspm">What Is CSPM?</a></li>
        <li><a href="#what-cspm-covers">What CSPM Covers</a></li>
        <li><a href="#cspm-vs-ciem">CSPM vs. CIEM vs. CNAPP</a></li>
        <li><a href="#framework-mapping">Framework Mapping</a></li>
        <li><a href="#soc2">SOC 2</a></li>
        <li><a href="#pci-dss">PCI DSS 4.0</a></li>
        <li><a href="#iso27001">ISO 27001</a></li>
        <li><a href="#aivric-cspm">AiVRIC CloudSignals</a></li>
        <li><a href="#risk-prioritization">Risk Prioritization</a></li>
        <li><a href="#building-program">Building a Program</a></li>
      </ul>
    </div>

    <div class="ba-sidebar-cta">
      <div class="ba-sidebar-cta-icon"><i class="fas fa-cloud"></i></div>
      <h4>Start Your CSPM Baseline</h4>
      <p>Connect your cloud accounts and get a risk-scored posture baseline across all frameworks in minutes.</p>
      <a href="https://gcp-defense.aivric.com/sign-up?plan=pkg-cloudsignals-free&source=blog_cspm">Try CloudSignals Free &rarr;</a>
    </div>

    <div class="ba-sidebar-card">
      <div class="ba-sidebar-title">Related Articles</div>
      <div class="ba-related">
        <a href="blog-why-continuous-compliance-matters.html" class="ba-related-item">
          <img class="ba-related-img" src="assets/images/blog/SOC-2-compliance.avif" alt="">
          <div>
            <div class="ba-related-title">Why Continuous Compliance Matters in 2025</div>
            <div class="ba-related-date">April 13, 2025</div>
          </div>
        </a>
        <a href="blog-future-of-cloud-security.html" class="ba-related-item">
          <img class="ba-related-img" src="assets/images/blog/cloud-security-poster.avif" alt="">
          <div>
            <div class="ba-related-title">AI-Powered Compliance: The Future of Cloud Security</div>
            <div class="ba-related-date">April 15, 2025</div>
          </div>
        </a>
      </div>
    </div>

    <div class="ba-sidebar-card">
      <div class="ba-sidebar-title">Topics</div>
      <div class="ba-sidebar-tags">
        <a href="blog-portal.html" class="ba-tag">CSPM</a>
        <a href="blog-portal.html" class="ba-tag">Cloud Security</a>
        <a href="blog-portal.html" class="ba-tag">Multi-Cloud</a>
        <a href="blog-portal.html" class="ba-tag">Compliance</a>
        <a href="blog-portal.html" class="ba-tag">GRC</a>
        <a href="blog-portal.html" class="ba-tag">Risk</a>
      </div>
    </div>
  </aside>
</div>

<section class="ba-cta-banner">
  <div class="ba-cta-banner-eyebrow">CloudSignals+RiskOps&trade;</div>
  <h2>Your cloud estate, always in posture.<br>Always audit-ready.</h2>
  <p>AiVRIC CloudSignals+RiskOps connects to every cloud account, continuously evaluates posture across 200+ checks, and maps every finding to SOC 2, PCI DSS, ISO 27001, and CMMC automatically.</p>
  <div class="ba-cta-banner-actions">
    <a href="https://gcp-defense.aivric.com/sign-up?plan=pkg-cloudsignals-free&source=blog_cspm" class="ba-btn-primary"><i class="fas fa-rocket"></i>&nbsp;Start Free</a>
    <a href="request-demo.html" class="ba-btn-ghost">Request a Demo</a>
  </div>
</section>
"""

# ════════════════════════════════════════════════════════════════════════════
# ARTICLE — assets/blog-managing-healthcare-risk/index.html
# "Managing AI Risk in Healthcare"  (subdirectory — ../../ paths)
# ════════════════════════════════════════════════════════════════════════════
HEALTHCARE_BODY = """
<section class="ba-hero">
  <div class="ba-hero-inner">
    <div class="ba-meta-row">
      <span class="ba-cat healthcare"><i class="fas fa-heartbeat"></i>&nbsp;Healthcare &amp; Life Sciences</span>
      <span class="ba-read-time"><i class="far fa-clock"></i>&nbsp;9 min read</span>
      <span class="ba-read-time">January 18, 2025</span>
    </div>
    <h1 class="ba-hero-title" id="top">Managing AI Risk in Healthcare</h1>
    <p class="ba-hero-lead">Healthcare organizations are deploying AI faster than their governance frameworks can keep up. Here's how to manage model risk, PHI exposure, and cloud configuration gaps without sacrificing clinical innovation.</p>
    <div class="ba-author-row">
      <div class="ba-author-avatar"><img src="../../assets/images/logo/aivric.svg" alt="AiVRIC"></div>
      <div>
        <div class="ba-author-name">AiVRIC Team</div>
        <div class="ba-author-role">Security &amp; Compliance Innovation</div>
      </div>
    </div>
  </div>
  <div class="ba-hero-visual">
    <img src="../../assets/images/blog/cloud-security-poster.avif" alt="Healthcare cloud risk governance">
  </div>
</section>

<div class="ba-layout">
  <article class="ba-body">

    <p>Healthcare organizations are adopting AI for clinical decision support, revenue cycle automation, patient engagement, and operational optimization. These gains introduce new exposure: PHI handling, model safety, and cloud configuration drift can create compliance gaps and patient safety risk if not governed continuously.</p>

    <p>Managing AI risk in healthcare demands more than point-in-time audits. Teams need continuous evidence, model inspection, and posture monitoring across hybrid and multi-cloud environments. AiVRIC is purpose-built for regulated industries that require strong data controls, audit-ready documentation, and clear accountability.</p>

    <div class="ba-stats">
      <div class="ba-stat">
        <div class="ba-stat-val">$10.9M</div>
        <div class="ba-stat-label">average cost of a healthcare data breach in 2024 — highest of any industry (IBM)</div>
      </div>
      <div class="ba-stat">
        <div class="ba-stat-val orange">73%</div>
        <div class="ba-stat-label">of healthcare AI deployments lack formal model risk governance, per recent industry surveys</div>
      </div>
      <div class="ba-stat">
        <div class="ba-stat-val green">3×</div>
        <div class="ba-stat-label">more likely to face regulatory action if PHI is involved in a cloud misconfiguration incident</div>
      </div>
    </div>

    <h2 id="risk-drivers">Healthcare Cloud Risk Drivers</h2>

    <p>Three forces are creating compounding risk for healthcare security and compliance teams:</p>

    <ul class="ba-checklist orange">
      <li><strong>PHI exposure and residency</strong> — Data sovereignty and encryption requirements must be enforced across every workload and storage tier, from EHR integrations to AI inference pipelines.</li>
      <li><strong>Third-party integrations</strong> — EHR, imaging, lab, and remote monitoring systems expand the attack surface and demand continuous vendor and access validation.</li>
      <li><strong>Model safety and drift</strong> — Clinical and operational AI models must be evaluated for accuracy, bias, and hallucination risk over time — not just at deployment.</li>
    </ul>

    <div class="ba-callout orange">
      <div class="ba-callout-label">Regulatory Context</div>
      <p>HIPAA requires ongoing risk analysis — not a one-time assessment. The HHS Office for Civil Rights (OCR) has consistently found that organizations lacking continuous monitoring failed to meet the Security Rule's risk management standard. AI adds a new dimension: FDA guidance on AI-based Software as a Medical Device (SaMD) requires post-market performance monitoring.</p>
    </div>

    <h2 id="aivric-approach">The AiVRIC Approach to Regulated AI</h2>

    <p>AiVRIC connects cloud telemetry, AI evaluations, and compliance evidence into a single fabric so healthcare security and risk leaders can manage both technical controls and procurement-ready requirements from one platform.</p>

    <h3 id="cloudsignals">CloudSignals+RiskOps™ for Continuous Posture</h3>

    <p>CloudSignals continuously evaluates cloud configurations across AWS, Azure, and GCP against healthcare-aligned controls. It maps misconfigurations to HIPAA Security Rule requirements, NIST SP 800-66 Rev. 2, SOC 2, and ISO 27001 simultaneously — giving compliance teams a single view of technical risk across their entire cloud estate.</p>

    <ul class="ba-checklist green">
      <li>PHI storage encryption (S3, Azure Blob, GCS) validated continuously</li>
      <li>Network segmentation and VPC flow log coverage for ePHI workloads</li>
      <li>IAM access controls and privileged account monitoring</li>
      <li>Audit logging completeness across every connected account</li>
    </ul>

    <h3 id="ai-signals">AI Signals™ for Model Inspection and Controls</h3>

    <p>AI Signals provides observability, prompt governance, and evaluation workflows for AI applications deployed in healthcare environments. Security and compliance teams gain governance-ready reporting that supports clinical leadership review, board-level risk discussions, and regulatory inquiries.</p>

    <div class="ba-img-block">
      <img src="../../assets/images/blog/ai-active-scanning.avif" alt="AI model inspection in healthcare">
      <div class="ba-img-caption">AI Signals™ tracks model behavior, prompt governance, and evaluation scores over time — providing the audit trail regulators expect.</div>
    </div>

    <h3 id="grc">GRC Management and Cyber RiskOps</h3>

    <p>AiVRIC unifies evidence collection, exceptions, POA&amp;Ms, and risk registers so compliance teams can track remediation and audit readiness in real time. Risk records are linked directly to cloud findings and model evaluation results — creating a traceable chain from technical control to business risk.</p>

    <h2 id="deployment">Deployment Models Built for Healthcare</h2>

    <p>Healthcare data sovereignty requirements are non-negotiable. AiVRIC supports customer-hosted SaaS on Kubernetes, enabling full data control, private networking, and BYO-AI integration.</p>

    <div class="ba-callout">
      <div class="ba-callout-label">Data Control Guarantee</div>
      <p>AiVRIC never stores PHI or scan results outside your own infrastructure. Your data stays in your cloud, in your region. AiVRIC operates as a read-only assessment layer with no persistent data retention in shared infrastructure.</p>
    </div>

    <p>Organizations can isolate workloads by region, facility, or business unit while maintaining consistent governance policies and a unified risk dashboard across the entire health system.</p>

    <h2 id="procurement-outcomes">Procurement-Ready Outcomes</h2>

    <p>Healthcare technology procurement requires demonstrating security posture to health system security officers, privacy officers, and procurement committees. AiVRIC delivers documentation and evidence that directly supports these evaluations:</p>

    <ul class="ba-checklist green">
      <li>Audit-ready evidence mapped to HIPAA, SOC 2, ISO 27001, and HITRUST</li>
      <li>Data residency, retention, and access controls documented and continuously validated</li>
      <li>Model risk scoring and AI evaluation reports suitable for executive and board review</li>
      <li>Unified dashboards for security, compliance, and clinical leadership</li>
      <li>Business Associate Agreement (BAA) support and third-party risk documentation</li>
    </ul>

    <h2 id="getting-started">Getting Started in Healthcare Environments</h2>

    <div class="ba-steps">
      <div class="ba-step">
        <div class="ba-step-num">1</div>
        <div class="ba-step-body">
          <h5>Classify and connect PHI workloads first</h5>
          <p>Begin by connecting cloud accounts that host ePHI workloads. A scoped initial assessment focused on HIPAA Security Rule controls delivers immediate value for compliance teams.</p>
        </div>
      </div>
      <div class="ba-step">
        <div class="ba-step-num">2</div>
        <div class="ba-step-body">
          <h5>Instrument AI applications with AI Signals™</h5>
          <p>Add OpenTelemetry-compatible instrumentation to AI applications to begin capturing prompt-level observability and model evaluation metrics.</p>
        </div>
      </div>
      <div class="ba-step">
        <div class="ba-step-num">3</div>
        <div class="ba-step-body">
          <h5>Establish a unified risk register</h5>
          <p>Map cloud findings and model risk scores to a single risk register visible to security, compliance, and clinical leadership — eliminating siloed spreadsheets.</p>
        </div>
      </div>
      <div class="ba-step">
        <div class="ba-step-num">4</div>
        <div class="ba-step-body">
          <h5>Build toward continuous evidence</h5>
          <p>Configure automated evidence collection for your highest-priority frameworks (HIPAA, SOC 2) so audit preparation becomes a continuous process, not an annual sprint.</p>
        </div>
      </div>
    </div>

    <div class="ba-tags">
      <a href="/blog-portal.html" class="ba-tag">AI Risk</a>
      <a href="/blog-portal.html" class="ba-tag">Healthcare</a>
      <a href="/blog-portal.html" class="ba-tag">HIPAA</a>
      <a href="/blog-portal.html" class="ba-tag">Cloud Security</a>
      <a href="/blog-portal.html" class="ba-tag">Data Residency</a>
      <a href="/blog-portal.html" class="ba-tag">Model Safety</a>
      <a href="/blog-portal.html" class="ba-tag">Compliance</a>
    </div>

    <div class="ba-author-card">
      <div class="ba-author-card-avatar"><img src="../../assets/images/logo/aivric.svg" alt="AiVRIC"></div>
      <div>
        <div class="ba-author-card-name">AiVRIC Team</div>
        <div class="ba-author-card-role">Security &amp; Compliance Innovation</div>
        <p class="ba-author-card-bio">The AiVRIC Team brings together cloud-security architects, compliance specialists, and DevSecOps practitioners focused on building practical, automation-first ways to manage risk in modern digital environments.</p>
      </div>
    </div>

  </article>

  <aside class="ba-sidebar">
    <div class="ba-sidebar-card">
      <div class="ba-sidebar-title">In This Article</div>
      <ul class="ba-toc">
        <li><a href="#risk-drivers">Healthcare Risk Drivers</a></li>
        <li><a href="#aivric-approach">The AiVRIC Approach</a></li>
        <li><a href="#cloudsignals">CloudSignals+RiskOps™</a></li>
        <li><a href="#ai-signals">AI Signals™</a></li>
        <li><a href="#grc">GRC &amp; RiskOps</a></li>
        <li><a href="#deployment">Deployment Models</a></li>
        <li><a href="#procurement-outcomes">Procurement Outcomes</a></li>
        <li><a href="#getting-started">Getting Started</a></li>
      </ul>
    </div>

    <div class="ba-sidebar-cta">
      <div class="ba-sidebar-cta-icon"><i class="fas fa-heartbeat"></i></div>
      <h4>Built for Regulated Industries</h4>
      <p>See how AiVRIC governs AI and cloud risk in healthcare environments with full data control.</p>
      <a href="https://gcp-defense.aivric.com/sign-up?plan=pkg-cloudsignals-free&source=blog_healthcare">Try CloudSignals Free &rarr;</a>
    </div>

    <div class="ba-sidebar-card">
      <div class="ba-sidebar-title">Related Articles</div>
      <div class="ba-related">
        <a href="/blog-future-of-cloud-security.html" class="ba-related-item">
          <img class="ba-related-img" src="../../assets/images/blog/cloud-security-poster.avif" alt="">
          <div>
            <div class="ba-related-title">AI-Powered Compliance: The Future of Cloud Security</div>
            <div class="ba-related-date">April 15, 2025</div>
          </div>
        </a>
        <a href="/blog-why-continuous-compliance-matters.html" class="ba-related-item">
          <img class="ba-related-img" src="../../assets/images/blog/SOC-2-compliance.avif" alt="">
          <div>
            <div class="ba-related-title">Why Continuous Compliance Matters in 2025</div>
            <div class="ba-related-date">April 13, 2025</div>
          </div>
        </a>
      </div>
    </div>

    <div class="ba-sidebar-card">
      <div class="ba-sidebar-title">Topics</div>
      <div class="ba-sidebar-tags">
        <a href="/blog-portal.html" class="ba-tag">Healthcare</a>
        <a href="/blog-portal.html" class="ba-tag">HIPAA</a>
        <a href="/blog-portal.html" class="ba-tag">AI Risk</a>
        <a href="/blog-portal.html" class="ba-tag">Cloud Security</a>
        <a href="/blog-portal.html" class="ba-tag">PHI</a>
        <a href="/blog-portal.html" class="ba-tag">Compliance</a>
      </div>
    </div>
  </aside>
</div>

<section class="ba-cta-banner">
  <div class="ba-cta-banner-eyebrow">Healthcare &amp; Life Sciences</div>
  <h2>Govern AI and cloud risk<br>without slowing innovation.</h2>
  <p>AiVRIC gives healthcare organizations the continuous posture monitoring, AI model governance, and audit-ready evidence needed to deploy AI with confidence — fully hosted in your own environment.</p>
  <div class="ba-cta-banner-actions">
    <a href="https://gcp-defense.aivric.com/sign-up?plan=pkg-cloudsignals-free&source=blog_healthcare" class="ba-btn-primary"><i class="fas fa-rocket"></i>&nbsp;Start Free</a>
    <a href="/request-demo.html" class="ba-btn-ghost">Request a Demo</a>
  </div>
</section>
"""

# ── Write files ──────────────────────────────────────────────────────────────

# 1. blog-details.html (root level)
out1 = SITE / "blog-details.html"
out1.write_text(
    page(
        "The CISO's Guide to Cloud Security Posture Management",
        "Multi-cloud adoption is outpacing traditional security controls. Learn how CSPM gives CISOs continuous visibility, risk context, and compliance evidence to govern cloud environments with confidence.",
        CSPM_BODY,
    ),
    encoding="utf-8"
)
print(f"  wrote: blog-details.html  ({out1.stat().st_size // 1024} KB)")

# 2. assets/blog-managing-healthcare-risk/index.html (subdirectory — ../../ paths)
out2 = SITE / "assets" / "blog-managing-healthcare-risk" / "index.html"
out2.write_text(
    page(
        "Managing AI Risk in Healthcare",
        "Healthcare organizations are deploying AI faster than their governance frameworks can keep up. Learn how AiVRIC manages model risk, PHI exposure, and cloud configuration gaps.",
        HEALTHCARE_BODY,
        asset_prefix="../../assets/",
        nav=NAV_SUB,
        footer=FOOTER_SUB,
        scripts=SCRIPTS_SUB,
    ),
    encoding="utf-8"
)
print(f"  wrote: assets/blog-managing-healthcare-risk/index.html  ({out2.stat().st_size // 1024} KB)")

print("\nDone — 2 blog pages rebuilt.")
