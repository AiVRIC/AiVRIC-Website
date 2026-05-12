#!/usr/bin/env python3
"""Build the modernized AiVRIC blog portal page."""
from pathlib import Path

SITE     = Path(r"C:\Projects\AiVRIC-Website")
TEMPLATE = SITE / "cloudsignals-findings.html"

raw_t    = TEMPLATE.read_text(encoding="utf-8", errors="replace")
NAV      = raw_t[raw_t.find("<!-- page wrapper -->") : raw_t.find("<!-- End Mobile Menu -->") + len("<!-- End Mobile Menu -->")]
FOOTER   = raw_t[raw_t.find("<!-- main-footer -->") : raw_t.find("<!-- main-footer end -->") + len("<!-- main-footer end -->")]

# ── Category color map ────────────────────────────────────────────────────────
CAT_COLOR = {
    "Company":        ("#f8fafc",  "rgba(248,250,252,.13)",  "rgba(248,250,252,.35)"),
    "Cloud Security": ("#00d1ff",  "rgba(0,209,255,.13)",    "rgba(0,209,255,.35)"),
    "Compliance":     ("#2ee59d",  "rgba(46,229,157,.13)",   "rgba(46,229,157,.35)"),
    "AI & Security":  ("#a78bfa",  "rgba(167,139,250,.13)",  "rgba(167,139,250,.35)"),
    "Risk Mgmt":      ("#fb923c",  "rgba(251,146,60,.13)",   "rgba(251,146,60,.35)"),
    "DevSecOps":      ("#ffd63a",  "rgba(255,214,58,.13)",   "rgba(255,214,58,.35)"),
}

# ── Article data ──────────────────────────────────────────────────────────────
FEATURED = {
    "href":     "why-aivric-exists.html",
    "img":      "assets/images/blog/aivric-vision-human-ai.avif",
    "category": "Company",
    "date":     "Feb 2, 2026",
    "read":     "8 min read",
    "title":    "Why AiVRIC Exists: A Founder's Thesis on Security That Endures",
    "excerpt":  "Most enterprise security tools are designed to pass audits, not survive incidents. This is the story of why we built AiVRIC — and what we believe a security platform actually owes to the organizations that depend on it when things go wrong.",
}

POSTS = [
    {
        "href":     "blog-why-continuous-compliance-matters.html",
        "img":      "assets/images/blog/SOC-2-compliance.avif",
        "category": "Compliance",
        "date":     "Apr 13, 2025",
        "read":     "6 min read",
        "title":    "Why Continuous Compliance Matters in 2025",
        "excerpt":  "Continuous compliance reduces audit fatigue, improves risk posture, and keeps cloud environments aligned with SOC 2, ISO 27001, PCI DSS, and CMMC — automatically.",
        "soon":     False,
    },
    {
        "href":     "blog-future-of-cloud-security.html",
        "img":      "assets/images/blog/cloud-security-poster.avif",
        "category": "AI & Security",
        "date":     "Apr 11, 2025",
        "read":     "5 min read",
        "title":    "AI-Powered Compliance: The Future of Cloud Security",
        "excerpt":  "How artificial intelligence is transforming compliance monitoring, managing risk at scale, and turning configuration data into decision-ready intelligence.",
        "soon":     False,
    },
    {
        "href":     "blog-integrating-into-DevOps.html",
        "img":      "assets/images/blog/SOC-analyst-1.avif",
        "category": "DevSecOps",
        "date":     "Apr 9, 2025",
        "read":     "7 min read",
        "title":    "Integrating Security Automation into DevOps",
        "excerpt":  "Seamless security automation accelerates your pipeline, surfaces vulnerabilities earlier, and ensures compliance from code commit to cloud deployment.",
        "soon":     False,
    },
    {
        "href":     "#",
        "img":      "assets/images/blog/compliance-risk-dashboard.avif",
        "category": "Cloud Security",
        "date":     "Coming Soon",
        "read":     "",
        "title":    "The Anatomy of a Multi-Cloud Posture Failure",
        "excerpt":  "A forensic look at how configuration drift, untracked accounts, and stale IAM roles combine into real incidents — and how continuous scanning prevents them.",
        "soon":     True,
    },
    {
        "href":     "#",
        "img":      "assets/images/blog/threat-detected.avif",
        "category": "Risk Mgmt",
        "date":     "Coming Soon",
        "read":     "",
        "title":    "Threat Detection Without the Noise: How Scoring Changes Everything",
        "excerpt":  "When every finding is critical, nothing is critical. Business-context scoring is the difference between a signal and a noise complaint.",
        "soon":     True,
    },
    {
        "href":     "#",
        "img":      "assets/images/blog/aivric-vision-ai.avif",
        "category": "AI & Security",
        "date":     "Coming Soon",
        "read":     "",
        "title":    "What GRC Automation Looks Like When AI Does the Heavy Lifting",
        "excerpt":  "GRC platforms have been spreadsheets with better branding for a decade. Here is what changes when a purpose-built AI model runs the control monitoring layer.",
        "soon":     True,
    },
]

# ── HTML generators ───────────────────────────────────────────────────────────
def cat_badge(cat, small=False):
    col, bg, bdr = CAT_COLOR.get(cat, CAT_COLOR["Company"])
    size = "bp-cat-sm" if small else "bp-cat"
    return f'<span class="{size}" style="color:{col};background:{bg};border-color:{bdr}">{cat}</span>'

def featured_html(p):
    col, bg, bdr = CAT_COLOR.get(p["category"], CAT_COLOR["Company"])
    return f"""
          <!-- ── FEATURED ─────────────────────────────────────────────── -->
          <section class="bp-featured-wrap">
            <div class="auto-container">
              <div class="bp-section-label">
                <span class="bp-eyebrow">Featured</span>
              </div>
              <a href="{p['href']}" class="bp-featured-card">
                <div class="bp-featured-img">
                  <img src="{p['img']}" alt="{p['title']}">
                  <div class="bp-featured-img-overlay"></div>
                </div>
                <div class="bp-featured-content">
                  <div class="bp-featured-meta">
                    {cat_badge(p['category'])}
                    <span class="bp-meta-sep">·</span>
                    <span class="bp-date">{p['date']}</span>
                    <span class="bp-meta-sep">·</span>
                    <span class="bp-read">{p['read']}</span>
                  </div>
                  <h2 class="bp-featured-title">{p['title']}</h2>
                  <p class="bp-featured-excerpt">{p['excerpt']}</p>
                  <span class="bp-read-cta">Read article <i class="fas fa-arrow-right"></i></span>
                </div>
              </a>
            </div>
          </section>"""

def post_card(p):
    col, bg, bdr = CAT_COLOR.get(p["category"], CAT_COLOR["Company"])
    soon_overlay = '<div class="bp-soon-overlay"><span>Coming Soon</span></div>' if p["soon"] else ""
    wrap_open  = f'<a href="{p["href"]}" class="bp-card">' if not p["soon"] else '<div class="bp-card bp-card-soon">'
    wrap_close = "</a>" if not p["soon"] else "</div>"
    meta_date  = f'<span class="bp-date">{p["date"]}</span>'
    meta_read  = f'<span class="bp-meta-sep">·</span><span class="bp-read">{p["read"]}</span>' if p["read"] else ""
    cta        = '' if p["soon"] else '<span class="bp-card-cta">Read more <i class="fas fa-arrow-right"></i></span>'
    return f"""              {wrap_open}
                <div class="bp-card-img">
                  <img src="{p['img']}" alt="{p['title']}" loading="lazy">
                  {cat_badge(p['category'], small=True)}
                  {soon_overlay}
                </div>
                <div class="bp-card-body">
                  <div class="bp-card-meta">{meta_date}{meta_read}</div>
                  <h3 class="bp-card-title">{p['title']}</h3>
                  <p class="bp-card-excerpt">{p['excerpt']}</p>
                  {cta}
                </div>
              {wrap_close}"""

CARDS_HTML = "\n".join(post_card(p) for p in POSTS)

# ── CSS ───────────────────────────────────────────────────────────────────────
BP_CSS = """\
<style id="bp-styles">
/* ── Blog Portal ── */
body.bp-page{
  font-family:Inter,system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
  background:radial-gradient(1400px 900px at 60% -10%,rgba(0,209,255,.14),transparent 55%),
    radial-gradient(900px 700px at 5% 20%,rgba(46,113,229,.10),transparent 60%),
    linear-gradient(180deg,#070b14 0%,#060a12 35%,#050814 100%);
  color:#e5e7eb;
}
/* hero */
.bp-hero{
  padding:100px 0 48px;
  border-bottom:1px solid rgba(148,163,184,.15);
  position:relative;
}
.bp-hero-inner{max-width:680px;}
.bp-hero-eyebrow{
  display:inline-flex;align-items:center;gap:8px;
  font-size:11px;font-weight:900;letter-spacing:2.5px;text-transform:uppercase;
  color:#00d1ff;margin-bottom:20px;
}
.bp-hero-eyebrow::before{
  content:'';width:24px;height:2px;background:#00d1ff;border-radius:2px;
}
.bp-hero-title{
  font-family:Jost,Inter,sans-serif;font-size:52px;font-weight:800;
  line-height:1.05;letter-spacing:-1.2px;color:#f8fafc;margin:0 0 14px;
}
@media(max-width:768px){.bp-hero-title{font-size:36px;}}
.bp-hero-sub{
  font-size:17px;line-height:1.75;color:#94a3b8;max-width:58ch;margin:0 0 32px;
}
.bp-search-row{
  display:flex;align-items:center;gap:0;max-width:440px;
  background:rgba(255,255,255,.05);border:1px solid rgba(148,163,184,.22);
  border-radius:12px;overflow:hidden;transition:border-color .2s;
}
.bp-search-row:focus-within{border-color:rgba(0,209,255,.4);}
.bp-search-row input{
  flex:1;background:transparent;border:none;outline:none;
  padding:12px 18px;font-size:14px;color:#e2e8f0;font-family:Inter,sans-serif;
}
.bp-search-row input::placeholder{color:#3d5268;}
.bp-search-row button{
  background:rgba(0,209,255,.10);border:none;padding:12px 18px;
  color:#00d1ff;cursor:pointer;font-size:14px;transition:background .2s;flex-shrink:0;
}
.bp-search-row button:hover{background:rgba(0,209,255,.18);}
/* filter tabs */
.bp-filters{padding:20px 0;border-bottom:1px solid rgba(148,163,184,.12);}
.bp-filter-inner{display:flex;align-items:center;gap:8px;flex-wrap:wrap;}
.bp-filter-btn{
  background:transparent;border:1px solid rgba(255,255,255,.10);
  border-radius:999px;padding:7px 16px;font-size:13px;font-weight:600;
  color:#64748b;cursor:pointer;transition:all .2s;
}
.bp-filter-btn:hover{border-color:rgba(0,209,255,.3);color:#cbd5e1;}
.bp-filter-btn.active{background:rgba(0,209,255,.10);border-color:rgba(0,209,255,.35);color:#00d1ff;}
/* category badges */
.bp-cat{
  display:inline-flex;align-items:center;
  padding:5px 12px;border-radius:999px;border:1px solid;
  font-size:12px;font-weight:700;letter-spacing:.2px;flex-shrink:0;
}
.bp-cat-sm{
  display:inline-flex;align-items:center;
  padding:4px 10px;border-radius:999px;border:1px solid;
  font-size:11px;font-weight:700;letter-spacing:.2px;flex-shrink:0;
  position:absolute;top:12px;left:12px;
  backdrop-filter:blur(8px);
}
/* eyebrow */
.bp-eyebrow{
  font-size:11px;font-weight:800;letter-spacing:2px;text-transform:uppercase;
  color:#00d1ff;
}
.bp-section-label{margin-bottom:16px;}
/* featured card */
.bp-featured-wrap{padding:52px 0 0;}
.bp-featured-card{
  display:grid;grid-template-columns:1.1fr 0.9fr;
  border-radius:20px;overflow:hidden;
  background:rgba(255,255,255,.04);border:1px solid rgba(148,163,184,.18);
  box-shadow:0 20px 60px rgba(0,0,0,.32);
  text-decoration:none;transition:border-color .25s,box-shadow .25s;
}
.bp-featured-card:hover{border-color:rgba(0,209,255,.3);box-shadow:0 28px 72px rgba(0,0,0,.38);}
@media(max-width:880px){.bp-featured-card{grid-template-columns:1fr;}}
.bp-featured-img{position:relative;overflow:hidden;min-height:340px;}
.bp-featured-img img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s;}
.bp-featured-card:hover .bp-featured-img img{transform:scale(1.03);}
.bp-featured-img-overlay{
  position:absolute;inset:0;
  background:linear-gradient(90deg,rgba(7,11,20,.0) 50%,rgba(7,11,20,.55) 100%),
    linear-gradient(0deg,rgba(7,11,20,.35) 0%,transparent 50%);
}
.bp-featured-content{
  padding:36px 38px;display:flex;flex-direction:column;justify-content:center;gap:0;
}
.bp-featured-meta{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:18px;}
.bp-meta-sep{color:#3d5268;font-size:12px;}
.bp-date{font-size:13px;color:#64748b;font-weight:500;}
.bp-read{font-size:13px;color:#64748b;}
.bp-featured-title{
  font-family:Jost,Inter,sans-serif;font-size:28px;font-weight:800;
  color:#f8fafc;line-height:1.2;letter-spacing:-.4px;margin:0 0 14px;
}
.bp-featured-excerpt{font-size:15px;line-height:1.75;color:#94a3b8;margin:0 0 22px;flex:1;}
.bp-read-cta{
  display:inline-flex;align-items:center;gap:8px;
  font-size:14px;font-weight:700;color:#00d1ff;
  transition:gap .2s;
}
.bp-featured-card:hover .bp-read-cta{gap:12px;}
/* article grid */
.bp-grid-wrap{padding:52px 0 72px;}
.bp-grid-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:24px;}
.bp-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;}
@media(max-width:1024px){.bp-grid{grid-template-columns:repeat(2,1fr);}}
@media(max-width:640px){.bp-grid{grid-template-columns:1fr;}}
/* article card */
.bp-card{
  display:flex;flex-direction:column;
  border-radius:16px;overflow:hidden;
  background:rgba(255,255,255,.04);border:1px solid rgba(148,163,184,.16);
  box-shadow:0 8px 28px rgba(0,0,0,.22);
  text-decoration:none;transition:border-color .22s,box-shadow .22s,transform .22s;
}
.bp-card:hover{border-color:rgba(0,209,255,.28);box-shadow:0 14px 44px rgba(0,0,0,.3);transform:translateY(-2px);}
.bp-card-soon{cursor:default;}
.bp-card-img{
  position:relative;overflow:hidden;aspect-ratio:16/9;
}
.bp-card-img img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s;}
.bp-card:hover .bp-card-img img{transform:scale(1.04);}
.bp-card-soon .bp-card-img img{filter:grayscale(60%) brightness(.65);}
.bp-soon-overlay{
  position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
}
.bp-soon-overlay span{
  font-size:12px;font-weight:800;letter-spacing:2px;text-transform:uppercase;
  color:#f8fafc;background:rgba(7,11,20,.65);backdrop-filter:blur(8px);
  padding:7px 16px;border-radius:999px;border:1px solid rgba(255,255,255,.18);
}
.bp-card-body{padding:20px 22px 22px;display:flex;flex-direction:column;flex:1;}
.bp-card-meta{display:flex;align-items:center;gap:8px;margin-bottom:10px;}
.bp-card-title{
  font-family:Jost,Inter,sans-serif;font-size:17px;font-weight:700;
  color:#f1f5f9;line-height:1.3;margin:0 0 8px;
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;
}
.bp-card-soon .bp-card-title{color:#64748b;}
.bp-card-excerpt{
  font-size:13.5px;color:#64748b;line-height:1.65;margin:0 0 14px;flex:1;
  display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;
}
.bp-card-cta{
  display:inline-flex;align-items:center;gap:7px;
  font-size:13px;font-weight:700;color:#00d1ff;margin-top:auto;
  transition:gap .2s;
}
.bp-card:hover .bp-card-cta{gap:10px;}
/* newsletter strip */
.bp-newsletter{
  margin:0 0 80px;
  border-radius:20px;
  background:linear-gradient(135deg,rgba(0,209,255,.08),rgba(46,229,157,.04));
  border:1px solid rgba(0,209,255,.22);
  box-shadow:0 20px 56px rgba(0,209,255,.07);
  padding:52px 56px;
  display:grid;grid-template-columns:1fr auto;gap:40px;align-items:center;
}
@media(max-width:768px){.bp-newsletter{grid-template-columns:1fr;padding:36px 28px;}}
.bp-nl-title{
  font-family:Jost,Inter,sans-serif;font-size:28px;font-weight:800;
  color:#f8fafc;margin:0 0 8px;letter-spacing:-.4px;
}
.bp-nl-sub{font-size:15px;color:#94a3b8;margin:0;line-height:1.6;}
.bp-nl-form{display:flex;gap:0;max-width:380px;width:100%;}
.bp-nl-form input{
  flex:1;background:rgba(255,255,255,.06);border:1px solid rgba(148,163,184,.25);
  border-right:none;border-radius:10px 0 0 10px;
  padding:13px 18px;font-size:14px;color:#e2e8f0;font-family:Inter,sans-serif;outline:none;
  transition:border-color .2s;
}
.bp-nl-form input:focus{border-color:rgba(0,209,255,.4);}
.bp-nl-form input::placeholder{color:#3d5268;}
.bp-nl-form button{
  background:#00d1ff;color:#030a12;border:none;
  padding:13px 22px;border-radius:0 10px 10px 0;
  font-size:14px;font-weight:700;cursor:pointer;white-space:nowrap;
  transition:background .2s;flex-shrink:0;
}
.bp-nl-form button:hover{background:#24ddff;}
.bp-nl-note{font-size:11.5px;color:#3d5268;margin-top:7px;}
</style>"""

GF_CSS = """\
<style id="gf-styles">
.gf-footer{background:#050b17;position:relative;overflow:hidden;font-family:'Inter',sans-serif}
.gf-footer::before{content:'';position:absolute;inset:0;background-image:radial-gradient(rgba(0,209,255,.045) 1px,transparent 1px);background-size:28px 28px;pointer-events:none}
.gf-top-rule{height:1px;background:linear-gradient(90deg,transparent 0%,rgba(0,209,255,.55) 30%,rgba(46,229,157,.4) 70%,transparent 100%);position:relative;z-index:1}
.gf-body{padding:72px 0 52px;position:relative;z-index:1}
.gf-grid{display:grid;grid-template-columns:1.45fr 1fr 1fr 1fr;gap:52px}
@media(max-width:991px){.gf-grid{grid-template-columns:1fr 1fr;gap:36px 40px}}
@media(max-width:599px){.gf-grid{grid-template-columns:1fr;gap:32px}}
.gf-logo-link{display:inline-block;margin-bottom:14px}
.gf-logo{height:34px;width:auto;display:block}
.gf-tagline{font-size:13px;color:#4e637a;line-height:1.7;margin-bottom:22px;max-width:255px}
.gf-subscribe-row{display:flex;gap:0;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);border-radius:8px;overflow:hidden;margin-bottom:7px;transition:border-color .2s}
.gf-subscribe-row:focus-within{border-color:rgba(0,209,255,.35)}
.gf-subscribe-row input{flex:1;background:transparent;border:none;outline:none;padding:10px 14px;font-size:13px;color:#e2e8f0;font-family:'Inter',sans-serif}
.gf-subscribe-row input::placeholder{color:#3d5268}
.gf-subscribe-row button{background:#00d1ff;border:none;padding:10px 15px;color:#030a12;cursor:pointer;font-size:13px;transition:background .2s;flex-shrink:0}
.gf-subscribe-row button:hover{background:#33daff}
.gf-subscribe-note{font-size:11px;color:#3d5268;margin:0 0 22px}
.gf-social{display:flex;gap:8px}
.gf-social-link{width:33px;height:33px;border-radius:8px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);display:flex;align-items:center;justify-content:center;color:#4e637a;font-size:13px;text-decoration:none;transition:all .2s}
.gf-social-link:hover{background:rgba(0,209,255,.09);border-color:rgba(0,209,255,.28);color:#00d1ff}
.gf-col-title{font-size:10.5px;font-weight:800;letter-spacing:2px;text-transform:uppercase;color:#94a3b8;margin-bottom:16px;padding-bottom:11px;border-bottom:1px solid rgba(255,255,255,.06)}
.gf-links{list-style:none;padding:0;margin:0 0 22px;display:flex;flex-direction:column;gap:9px}
.gf-links li a{font-size:13.5px;color:#4e637a;text-decoration:none;transition:color .18s;display:inline-block}
.gf-links li a:hover{color:#cbd5e1}
.gf-contact-block{display:flex;flex-direction:column;gap:9px;margin-top:4px}
.gf-contact-link{display:flex;align-items:center;gap:8px;font-size:13px;color:#4e637a;text-decoration:none;transition:color .18s}
.gf-contact-link i{color:#00d1ff;font-size:12px;width:14px;text-align:center;flex-shrink:0}
.gf-contact-link:hover{color:#cbd5e1}
.gf-bottom{border-top:1px solid rgba(255,255,255,.055);padding:16px 0;position:relative;z-index:1}
.gf-bottom-inner{display:flex;align-items:center;justify-content:space-between;gap:18px;flex-wrap:wrap}
.gf-copy{font-size:12px;color:#3d5268;margin:0}
.gf-copy a{color:#4e637a;text-decoration:none;transition:color .18s}
.gf-copy a:hover{color:#94a3b8}
.gf-bottom-right{display:flex;align-items:center;gap:18px;flex-wrap:wrap}
.gf-trust-pill{display:inline-flex;align-items:center;gap:6px;font-size:11px;font-weight:700;color:#2ee59d;background:rgba(46,229,157,.07);border:1px solid rgba(46,229,157,.18);border-radius:100px;padding:4px 12px;letter-spacing:.3px}
.gf-trust-dot{width:6px;height:6px;border-radius:50%;background:#2ee59d;box-shadow:0 0 6px #2ee59d;animation:gf-blink 2s ease-in-out infinite}
@keyframes gf-blink{0%,100%{opacity:1}50%{opacity:.25}}
.gf-bottom-nav{display:flex;gap:18px}
.gf-bottom-nav a{font-size:12px;color:#3d5268;text-decoration:none;transition:color .18s}
.gf-bottom-nav a:hover{color:#94a3b8}
.gf-footer .pattern-layer{display:none!important}
.gf-footer .links-list,.gf-footer .footer-widget,.gf-footer .widget-section,.gf-footer .footer-bottom{display:none!important}
</style>"""

# ── Assemble page ─────────────────────────────────────────────────────────────
HEAD = f"""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
<title>AiVRIC Insights | Security Intelligence Blog</title>
<meta name="description" content="Security intelligence, cloud compliance, and AI-driven risk management — written by the team building AiVRIC.">
<link rel="icon" href="assets/images/Aivric-favicon-logo.ico" type="image/x-icon">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Jost:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap" rel="stylesheet">
<link href="assets/css/font-awesome-all.css" rel="stylesheet">
<link href="assets/css/flaticon.css" rel="stylesheet">
<link href="assets/css/owl.css" rel="stylesheet">
<link href="assets/css/bootstrap.css" rel="stylesheet">
<link href="assets/css/jquery.fancybox.min.css" rel="stylesheet">
<link href="assets/css/animate.css" rel="stylesheet">
<link href="assets/css/nice-select.css" rel="stylesheet">
<link href="assets/css/color.css" rel="stylesheet">
<link href="assets/css/elpath.css" rel="stylesheet">
<link href="assets/css/style.css?v=20250115" rel="stylesheet">
<link href="assets/css/responsive.css" rel="stylesheet">
<link href="assets/css/custom.css?v=20250115" rel="stylesheet">
{BP_CSS}
{GF_CSS}
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-EG2Q8GD30V"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-EG2Q8GD30V');
</script>
</head>"""

BODY_OPEN = NAV.replace('class="portal-page"', 'class="bp-page"').replace('class="cf-page"', 'class="bp-page"')

CONTENT = f"""
        <div class="bp-outer">

          <!-- ── HERO ──────────────────────────────────────────────────── -->
          <section class="bp-hero">
            <div class="auto-container">
              <div class="bp-hero-inner">
                <div class="bp-hero-eyebrow">AiVRIC Insights</div>
                <h1 class="bp-hero-title">Security intelligence.<br>From the people building it.</h1>
                <p class="bp-hero-sub">In-depth writing on cloud security, compliance automation, AI-driven risk management, and the future of the security operations function.</p>
                <form class="bp-search-row" action="#" onsubmit="return false;">
                  <input type="search" placeholder="Search articles..." aria-label="Search articles">
                  <button type="submit" aria-label="Search"><i class="fas fa-search"></i></button>
                </form>
              </div>
            </div>
          </section>

          <!-- ── CATEGORY FILTERS ──────────────────────────────────────── -->
          <div class="bp-filters">
            <div class="auto-container">
              <div class="bp-filter-inner" id="bp-filters">
                <button class="bp-filter-btn active" data-filter="all">All Topics</button>
                <button class="bp-filter-btn" data-filter="Cloud Security">Cloud Security</button>
                <button class="bp-filter-btn" data-filter="Compliance">Compliance</button>
                <button class="bp-filter-btn" data-filter="AI &amp; Security">AI &amp; Security</button>
                <button class="bp-filter-btn" data-filter="Risk Mgmt">Risk Management</button>
                <button class="bp-filter-btn" data-filter="DevSecOps">DevSecOps</button>
                <button class="bp-filter-btn" data-filter="Company">Company</button>
              </div>
            </div>
          </div>

          {featured_html(FEATURED)}

          <!-- ── ARTICLE GRID ───────────────────────────────────────────── -->
          <section class="bp-grid-wrap">
            <div class="auto-container">
              <div class="bp-grid-header">
                <span class="bp-eyebrow">Latest Articles</span>
              </div>
              <div class="bp-grid">
{CARDS_HTML}
              </div>
            </div>
          </section>

          <!-- ── NEWSLETTER ─────────────────────────────────────────────── -->
          <div class="auto-container">
            <div class="bp-newsletter">
              <div>
                <h2 class="bp-nl-title">Stay ahead of the threat landscape.</h2>
                <p class="bp-nl-sub">New articles on cloud security, compliance automation, and AI-driven risk management — delivered to your inbox.</p>
              </div>
              <div>
                <form class="bp-nl-form" action="contact.html" method="post" onsubmit="return false;">
                  <input type="email" name="email" placeholder="Work email address" required>
                  <button type="submit">Subscribe</button>
                </form>
                <p class="bp-nl-note">No spam. Unsubscribe any time.</p>
              </div>
            </div>
          </div>

        </div><!-- /bp-outer -->"""

TAIL = f"""
        {FOOTER}

        <div class="scroll-to-top">
            <div><div class="scroll-top-inner">
                <div class="scroll-bar"><div class="bar-inner"></div></div>
                <div class="scroll-bar-text">Go To Top</div>
            </div></div>
        </div>

    </div>

    <script src="assets/js/jquery.js"></script>
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
    <script src="assets/js/script.js"></script>
    <script src="assets/js/theme-toggle.js"></script>
    <script src="assets/js/mega-hover.js"></script>
    <script src="assets/js/mega-tabs.js"></script>
    <script>
    /* Category filter tab highlight */
    document.addEventListener('DOMContentLoaded', function() {{
      var btns = document.querySelectorAll('.bp-filter-btn');
      btns.forEach(function(btn) {{
        btn.addEventListener('click', function() {{
          btns.forEach(function(b) {{ b.classList.remove('active'); }});
          btn.classList.add('active');
        }});
      }});
    }});
    </script>
</body>
</html>"""

html = HEAD + "\n" + BODY_OPEN + CONTENT + TAIL
out  = SITE / "blog-portal.html"
out.write_text(html, encoding="utf-8")
print(f"Built: blog-portal.html  ({len(html.splitlines())} lines)")
