#!/usr/bin/env python3
"""Build platform pages: services.html (Fabric hub) + 6 sub-pages."""
from pathlib import Path
import re

SITE = Path(r"C:\Projects\AiVRIC-Website")
MOBILE_END_TAG = "<!-- End Mobile Menu -->"
FOOTER_ANCHOR  = "        <!-- main-footer -->"

PLAT_CSS = """<style id="plat-styles">
:root{
  --plat-bg:#080f1c;--plat-bg2:#0d1829;--plat-bg3:#060d18;--plat-card:#0d1a2e;
  --plat-cyan:#00d1ff;--plat-green:#2ee59d;--plat-gold:#ffd63a;
  --plat-purp:#a78bfa;--plat-red:#f87171;--plat-amber:#fb923c;
  --plat-text:#e2e8f0;--plat-muted:#94a3b8;--plat-dim:#64748b;
}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.001ms!important;transition-duration:.001ms!important}}
@keyframes plat-scan{0%{top:0;opacity:0}4%{opacity:.9}96%{opacity:.9}100%{top:100%;opacity:0}}
@keyframes plat-grid{0%,100%{opacity:.35}50%{opacity:.8}}
@keyframes plat-pulse{0%,100%{opacity:.5;transform:scale(1)}50%{opacity:1;transform:scale(1.04)}}
@keyframes plat-fade-up{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}

/* shared layout */
.plat-auto{max-width:1260px;margin:0 auto;padding:0 24px}
.plat-section{background:var(--plat-bg);padding:80px 0}
.plat-section-alt{background:var(--plat-bg2);padding:80px 0}
.plat-label{display:inline-flex;align-items:center;gap:8px;font-size:11px;font-weight:800;letter-spacing:2.5px;text-transform:uppercase;color:var(--plat-cyan);margin-bottom:18px;background:rgba(0,209,255,.07);border:1px solid rgba(0,209,255,.18);border-radius:100px;padding:5px 16px}
.plat-section-hdr{text-align:center;margin-bottom:56px}
.plat-section-title{font-family:'Jost',sans-serif;font-size:clamp(28px,3.5vw,40px);font-weight:900;color:#f0f8ff;line-height:1.15;margin-bottom:12px}
.plat-section-sub{font-size:16px;line-height:1.75;color:var(--plat-muted);max-width:560px;margin:0 auto}

/* hero */
.plat-hero{position:relative;background:var(--plat-bg3);overflow:hidden;padding:110px 0 76px}
.plat-hero-grid{position:absolute;inset:0;background-image:linear-gradient(rgba(0,209,255,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(0,209,255,.03) 1px,transparent 1px);background-size:64px 64px;animation:plat-grid 12s ease-in-out infinite;pointer-events:none}
.plat-hero-scan{position:absolute;left:0;right:0;height:1.5px;background:linear-gradient(90deg,transparent,rgba(0,209,255,.75) 50%,transparent);top:0;animation:plat-scan 9s linear infinite;pointer-events:none;z-index:1}
.plat-hero-glow{position:absolute;border-radius:50%;pointer-events:none;width:900px;height:600px;background:radial-gradient(ellipse,rgba(0,209,255,.05) 0%,transparent 70%);left:50%;top:50%;transform:translate(-50%,-60%);animation:plat-pulse 8s ease-in-out infinite}
.plat-hero-inner{position:relative;z-index:2;text-align:center;max-width:860px;margin:0 auto}
.plat-h1{font-family:'Jost',sans-serif;font-size:clamp(34px,5vw,60px);font-weight:900;line-height:1.1;color:#f0f8ff;margin-bottom:20px}
.plat-h1 .grad{background:linear-gradient(90deg,var(--plat-cyan),var(--plat-green));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.plat-hero-sub{font-size:17px;line-height:1.75;color:var(--plat-muted);margin-bottom:44px;max-width:660px;margin-left:auto;margin-right:auto}
.plat-crumb{display:flex;align-items:center;justify-content:center;gap:8px;font-size:13px;color:var(--plat-dim);margin-bottom:26px;position:relative;z-index:2}
.plat-crumb a{color:var(--plat-muted);text-decoration:none}.plat-crumb a:hover{color:var(--plat-cyan)}
.plat-crumb-sep{color:var(--plat-dim)}.plat-crumb-cur{color:var(--plat-cyan);font-weight:600}

/* quick links */
.plat-quicklinks{display:flex;flex-wrap:wrap;gap:10px;justify-content:center}
.plat-ql{display:inline-flex;align-items:center;gap:7px;padding:9px 18px;border-radius:100px;font-size:13px;font-weight:600;text-decoration:none;transition:all .2s;border:1px solid}
.plat-ql-cyan{background:rgba(0,209,255,.07);border-color:rgba(0,209,255,.22);color:var(--plat-cyan)}
.plat-ql-green{background:rgba(46,229,157,.06);border-color:rgba(46,229,157,.2);color:var(--plat-green)}
.plat-ql-purp{background:rgba(167,139,250,.06);border-color:rgba(167,139,250,.2);color:var(--plat-purp)}
.plat-ql-amber{background:rgba(251,146,60,.06);border-color:rgba(251,146,60,.2);color:var(--plat-amber)}
.plat-ql-red{background:rgba(248,113,113,.06);border-color:rgba(248,113,113,.2);color:var(--plat-red)}
.plat-ql-gold{background:rgba(255,214,58,.06);border-color:rgba(255,214,58,.2);color:var(--plat-gold)}
.plat-ql:hover{transform:translateY(-2px);box-shadow:0 8px 20px rgba(0,0,0,.3)}

/* capability cards (hub) */
.plat-caps-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
@media(max-width:991px){.plat-caps-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:599px){.plat-caps-grid{grid-template-columns:1fr}}
.plat-cap-card{background:var(--plat-card);border:1px solid rgba(255,255,255,.06);border-radius:16px;padding:30px;transition:all .25s;position:relative;overflow:hidden;display:flex;flex-direction:column}
.plat-cap-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;border-radius:16px 16px 0 0}
.plat-cap-card.c-cyan::before{background:var(--plat-cyan)}
.plat-cap-card.c-green::before{background:var(--plat-green)}
.plat-cap-card.c-purp::before{background:var(--plat-purp)}
.plat-cap-card.c-amber::before{background:var(--plat-amber)}
.plat-cap-card.c-red::before{background:var(--plat-red)}
.plat-cap-card.c-gold::before{background:var(--plat-gold)}
.plat-cap-card:hover{transform:translateY(-4px);border-color:rgba(255,255,255,.12)}
.plat-cap-card:hover.c-cyan{box-shadow:0 20px 50px rgba(0,209,255,.08)}
.plat-cap-card:hover.c-green{box-shadow:0 20px 50px rgba(46,229,157,.07)}
.plat-cap-card:hover.c-purp{box-shadow:0 20px 50px rgba(167,139,250,.07)}
.plat-cap-card:hover.c-amber{box-shadow:0 20px 50px rgba(251,146,60,.07)}
.plat-cap-card:hover.c-red{box-shadow:0 20px 50px rgba(248,113,113,.07)}
.plat-cap-card:hover.c-gold{box-shadow:0 20px 50px rgba(255,214,58,.07)}
.plat-cap-icon{width:46px;height:46px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:19px;margin-bottom:18px;flex-shrink:0}
.plat-cap-icon.c-cyan{background:rgba(0,209,255,.12);color:var(--plat-cyan)}
.plat-cap-icon.c-green{background:rgba(46,229,157,.12);color:var(--plat-green)}
.plat-cap-icon.c-purp{background:rgba(167,139,250,.12);color:var(--plat-purp)}
.plat-cap-icon.c-amber{background:rgba(251,146,60,.12);color:var(--plat-amber)}
.plat-cap-icon.c-red{background:rgba(248,113,113,.12);color:var(--plat-red)}
.plat-cap-icon.c-gold{background:rgba(255,214,58,.12);color:var(--plat-gold)}
.plat-cap-name{font-family:'Jost',sans-serif;font-size:19px;font-weight:700;color:#f0f8ff;margin-bottom:10px}
.plat-cap-desc{font-size:14px;line-height:1.65;color:var(--plat-muted);margin-bottom:18px;flex:1}
.plat-cap-feats{list-style:none;padding:0;margin:0 0 22px;display:flex;flex-direction:column;gap:6px}
.plat-cap-feats li{font-size:13px;color:var(--plat-muted);display:flex;align-items:center;gap:8px}
.plat-cap-feats li::before{content:'';width:5px;height:5px;border-radius:50%;flex-shrink:0}
.plat-cap-feats.c-cyan li::before{background:var(--plat-cyan)}
.plat-cap-feats.c-green li::before{background:var(--plat-green)}
.plat-cap-feats.c-purp li::before{background:var(--plat-purp)}
.plat-cap-feats.c-amber li::before{background:var(--plat-amber)}
.plat-cap-feats.c-red li::before{background:var(--plat-red)}
.plat-cap-feats.c-gold li::before{background:var(--plat-gold)}
.plat-cap-link{display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:700;text-decoration:none;letter-spacing:.4px;transition:gap .18s;margin-top:auto}
.plat-cap-link.c-cyan{color:var(--plat-cyan)}.plat-cap-link.c-green{color:var(--plat-green)}
.plat-cap-link.c-purp{color:var(--plat-purp)}.plat-cap-link.c-amber{color:var(--plat-amber)}
.plat-cap-link.c-red{color:var(--plat-red)}.plat-cap-link.c-gold{color:var(--plat-gold)}
.plat-cap-link:hover{gap:10px}

/* suite powers section */
.plat-suite-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
@media(max-width:767px){.plat-suite-grid{grid-template-columns:1fr}}
.plat-suite-card{background:var(--plat-card);border-radius:16px;padding:30px;border:1px solid rgba(255,255,255,.06)}
.plat-suite-card.s-def{border-top:3px solid var(--plat-cyan)}
.plat-suite-card.s-off{border-top:3px solid var(--plat-red)}
.plat-suite-card.s-vis{border-top:3px solid var(--plat-gold)}
.plat-suite-name{font-family:'Jost',sans-serif;font-size:18px;font-weight:800;margin-bottom:8px}
.plat-suite-name.s-def{color:var(--plat-cyan)}.plat-suite-name.s-off{color:var(--plat-red)}.plat-suite-name.s-vis{color:var(--plat-gold)}
.plat-suite-desc{font-size:13px;color:var(--plat-muted);line-height:1.6;margin-bottom:18px}
.plat-suite-tags{display:flex;flex-wrap:wrap;gap:7px;margin-bottom:20px}
.plat-suite-tag{font-size:11px;font-weight:600;padding:3px 10px;border-radius:100px;letter-spacing:.3px}
.plat-suite-tag.s-def{background:rgba(0,209,255,.08);color:var(--plat-cyan);border:1px solid rgba(0,209,255,.18)}
.plat-suite-tag.s-off{background:rgba(248,113,113,.07);color:var(--plat-red);border:1px solid rgba(248,113,113,.16)}
.plat-suite-tag.s-vis{background:rgba(255,214,58,.07);color:var(--plat-gold);border:1px solid rgba(255,214,58,.16)}
.plat-suite-link{display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:700;text-decoration:none;transition:gap .18s}
.plat-suite-link.s-def{color:var(--plat-cyan)}.plat-suite-link.s-off{color:var(--plat-red)}.plat-suite-link.s-vis{color:var(--plat-gold)}
.plat-suite-link:hover{gap:10px}

/* integrations strip */
.plat-integ-strip{background:var(--plat-bg3);padding:60px 0;border-top:1px solid rgba(255,255,255,.04);border-bottom:1px solid rgba(255,255,255,.04)}
.plat-integ-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:16px}
@media(max-width:767px){.plat-integ-grid{grid-template-columns:repeat(2,1fr)}}
.plat-integ-item{display:flex;flex-direction:column;align-items:center;gap:10px;padding:22px 16px;background:var(--plat-card);border-radius:12px;border:1px solid rgba(255,255,255,.05);transition:border-color .2s;text-align:center}
.plat-integ-item:hover{border-color:rgba(0,209,255,.2)}
.plat-integ-icon{width:38px;height:38px;border-radius:9px;background:rgba(0,209,255,.1);color:var(--plat-cyan);display:flex;align-items:center;justify-content:center;font-size:15px}
.plat-integ-name{font-size:12px;font-weight:700;color:var(--plat-text)}
.plat-integ-desc{font-size:11px;color:var(--plat-dim);line-height:1.5}

/* final CTA */
.plat-final-cta{position:relative;background:var(--plat-bg3);overflow:hidden;padding:90px 0;text-align:center}
.plat-final-cta-grid{position:absolute;inset:0;background-image:linear-gradient(rgba(0,209,255,.025) 1px,transparent 1px),linear-gradient(90deg,rgba(0,209,255,.025) 1px,transparent 1px);background-size:64px 64px;pointer-events:none}
.plat-final-cta-inner{position:relative;z-index:2}
.plat-cta-title{font-family:'Jost',sans-serif;font-size:clamp(24px,3.5vw,38px);font-weight:900;color:#f0f8ff;margin-bottom:12px}
.plat-cta-sub{font-size:16px;color:var(--plat-muted);margin-bottom:34px}
.plat-cta-btns{display:flex;gap:14px;justify-content:center;flex-wrap:wrap}
.plat-btn-primary{display:inline-flex;align-items:center;gap:8px;padding:14px 30px;border-radius:8px;background:linear-gradient(135deg,var(--plat-cyan),#0099cc);color:#03080e;font-weight:800;font-size:14px;text-decoration:none;transition:all .2s}
.plat-btn-primary:hover{transform:translateY(-2px);box-shadow:0 12px 30px rgba(0,209,255,.3);color:#03080e}
.plat-btn-ghost{display:inline-flex;align-items:center;gap:8px;padding:14px 30px;border-radius:8px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.15);color:#f0f8ff;font-weight:700;font-size:14px;text-decoration:none;transition:all .2s}
.plat-btn-ghost:hover{background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.25);color:#f0f8ff;transform:translateY(-2px)}

/* ── SUB-PAGE ── */
.plat-sub-hero{position:relative;background:var(--plat-bg3);overflow:hidden;padding:80px 0 60px;border-bottom:1px solid rgba(255,255,255,.05)}
.plat-sub-hero-inner{position:relative;z-index:2;text-align:center}
.plat-sub-icon{width:64px;height:64px;border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:26px;margin:0 auto 22px}
.plat-sub-icon.c-cyan{background:rgba(0,209,255,.13);color:var(--plat-cyan);box-shadow:0 0 30px rgba(0,209,255,.15)}
.plat-sub-icon.c-green{background:rgba(46,229,157,.13);color:var(--plat-green);box-shadow:0 0 30px rgba(46,229,157,.15)}
.plat-sub-icon.c-purp{background:rgba(167,139,250,.13);color:var(--plat-purp);box-shadow:0 0 30px rgba(167,139,250,.15)}
.plat-sub-icon.c-amber{background:rgba(251,146,60,.13);color:var(--plat-amber);box-shadow:0 0 30px rgba(251,146,60,.15)}
.plat-sub-icon.c-red{background:rgba(248,113,113,.13);color:var(--plat-red);box-shadow:0 0 30px rgba(248,113,113,.15)}
.plat-sub-icon.c-gold{background:rgba(255,214,58,.13);color:var(--plat-gold);box-shadow:0 0 30px rgba(255,214,58,.15)}
.plat-sub-h1{font-family:'Jost',sans-serif;font-size:clamp(30px,4.5vw,50px);font-weight:900;color:#f0f8ff;margin-bottom:14px;line-height:1.15}
.plat-sub-hero-sub{font-size:16px;line-height:1.75;color:var(--plat-muted);max-width:620px;margin:0 auto}

/* sub-page body layout */
.plat-sub-body{background:var(--plat-bg);padding:70px 0}
.plat-sub-layout{display:grid;grid-template-columns:270px 1fr;gap:48px;align-items:start}
@media(max-width:991px){.plat-sub-layout{grid-template-columns:1fr}}

/* sidebar */
.plat-sidebar-nav{background:var(--plat-card);border:1px solid rgba(255,255,255,.07);border-radius:16px;padding:26px;margin-bottom:22px;position:sticky;top:96px}
.plat-sidebar-nav-title{font-size:10px;font-weight:800;letter-spacing:2.2px;text-transform:uppercase;color:var(--plat-dim);margin-bottom:14px;padding-bottom:12px;border-bottom:1px solid rgba(255,255,255,.06)}
.plat-sidebar-nav-list{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:3px}
.plat-sidebar-nav-list li a{display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:8px;font-size:13.5px;color:var(--plat-muted);text-decoration:none;transition:all .2s;font-weight:500}
.plat-sidebar-nav-list li a:hover{background:rgba(255,255,255,.05);color:var(--plat-text)}
.plat-sidebar-nav-list li a.current{background:rgba(0,209,255,.08);color:var(--plat-cyan);font-weight:700;border-left:2px solid var(--plat-cyan);padding-left:10px}
.plat-sidebar-nav-list li a i{font-size:12px;width:15px;text-align:center;opacity:.7}
.plat-sidebar-cta{background:linear-gradient(135deg,rgba(0,209,255,.07),rgba(46,229,157,.04));border:1px solid rgba(0,209,255,.14);border-radius:16px;padding:26px;text-align:center}
.plat-sidebar-cta h4{font-size:14px;font-weight:700;color:#f0f8ff;margin-bottom:7px}
.plat-sidebar-cta p{font-size:12px;color:var(--plat-muted);line-height:1.6;margin-bottom:14px}
.plat-btn-sm{display:inline-flex;align-items:center;gap:6px;padding:10px 18px;border-radius:7px;background:var(--plat-cyan);color:#03080e;font-size:13px;font-weight:800;text-decoration:none;transition:all .2s}
.plat-btn-sm:hover{background:#33daff;transform:translateY(-1px);color:#03080e}

/* sub content */
.plat-sub-intro{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);border-radius:16px;padding:30px 34px;margin-bottom:40px}
.plat-sub-intro h2{font-family:'Jost',sans-serif;font-size:21px;font-weight:800;color:#f0f8ff;margin-bottom:10px;line-height:1.35}
.plat-sub-intro p{font-size:15px;line-height:1.75;color:var(--plat-muted);margin:0}
.plat-sub-caps-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:18px;margin-bottom:40px}
@media(max-width:599px){.plat-sub-caps-grid{grid-template-columns:1fr}}
.plat-sub-cap-item{background:var(--plat-card);border:1px solid rgba(255,255,255,.06);border-radius:12px;padding:22px;transition:border-color .2s}
.plat-sub-cap-item:hover{border-color:rgba(255,255,255,.12)}
.plat-sub-cap-item .cap-icon{font-size:18px;margin-bottom:12px}
.plat-sub-cap-item h4{font-size:14px;font-weight:700;color:#f0f8ff;margin-bottom:7px}
.plat-sub-cap-item p{font-size:13px;line-height:1.6;color:var(--plat-muted);margin:0}
.plat-how-title{font-family:'Jost',sans-serif;font-size:19px;font-weight:800;color:#f0f8ff;margin-bottom:20px}
.plat-steps{display:flex;flex-direction:column;gap:14px;margin-bottom:40px}
.plat-step{display:flex;align-items:flex-start;gap:16px;padding:18px 22px;background:var(--plat-card);border-radius:12px;border:1px solid rgba(255,255,255,.05)}
.plat-step-num{width:30px;height:30px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:800;flex-shrink:0;background:rgba(0,209,255,.1);color:var(--plat-cyan)}
.plat-step-body h5{font-size:14px;font-weight:700;color:#f0f8ff;margin-bottom:4px}
.plat-step-body p{font-size:13px;color:var(--plat-muted);line-height:1.6;margin:0}
.plat-outcomes{background:rgba(46,229,157,.04);border:1px solid rgba(46,229,157,.12);border-radius:16px;padding:26px 30px;margin-bottom:36px}
.plat-outcomes h3{font-size:16px;font-weight:700;color:var(--plat-green);margin-bottom:14px}
.plat-outcomes ul{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:9px}
.plat-outcomes ul li{font-size:14px;color:var(--plat-muted);display:flex;align-items:flex-start;gap:10px;line-height:1.55}
.plat-outcomes ul li::before{content:'\\2713';color:var(--plat-green);font-weight:700;flex-shrink:0;margin-top:1px}
.plat-sub-cta-block{background:linear-gradient(135deg,rgba(0,209,255,.06),rgba(46,229,157,.04));border:1px solid rgba(0,209,255,.14);border-radius:16px;padding:30px;text-align:center}
.plat-sub-cta-block h3{font-family:'Jost',sans-serif;font-size:19px;font-weight:800;color:#f0f8ff;margin-bottom:9px}
.plat-sub-cta-block p{font-size:14px;color:var(--plat-muted);margin-bottom:18px}
</style>"""


# ── helpers ───────────────────────────────────────────────────────────────────

def build_page(filepath, new_body, title=None):
    raw = filepath.read_text(encoding="utf-8", errors="replace")
    mobile_end = raw.find(MOBILE_END_TAG)
    assert mobile_end != -1, f"Mobile end tag not found in {filepath.name}"
    bi = raw.find("\n", mobile_end) + 1
    while bi < len(raw) and raw[bi] in (" ", "\n", "\r", "\t"):
        bi += 1
    bi = raw.rfind("\n", 0, bi) + 1
    fi = raw.find(FOOTER_ANCHOR)
    assert fi != -1, f"Footer anchor not found in {filepath.name}"
    HEAD = raw[:bi]
    TAIL = raw[fi:]
    if title:
        HEAD = re.sub(r'<title>[^<]*</title>', f'<title>{title}</title>', HEAD)
    head_css = HEAD.replace('</head>', PLAT_CSS + '\n</head>', 1)
    output = head_css + new_body + "\n" + TAIL
    filepath.write_text(output, encoding="utf-8")
    print(f"  OK  {filepath.name}")


NAV_ITEMS = [
    ("genai-chat.html",         "fa-comments",  "GenAI Chat"),
    ("shared-data-layer.html",  "fa-database",  "Shared Data Layer"),
    ("agentic-design.html",     "fa-robot",     "Agentic Design"),
    ("efficient-compute.html",  "fa-microchip", "Efficient Compute"),
    ("data-localization.html",  "fa-globe",     "Data Localization"),
    ("ai-model-inspection.html","fa-search",    "AI Model Inspection"),
]

def sidebar(current_href):
    lis = []
    for href, icon, name in NAV_ITEMS:
        cls = ' class="current"' if href == current_href else ''
        lis.append(f'<li><a href="{href}"{cls}><i class="fas {icon}"></i>{name}</a></li>')
    items_html = "\n            ".join(lis)
    return f"""
        <aside>
          <div class="plat-sidebar-nav">
            <div class="plat-sidebar-nav-title">Platform Capabilities</div>
            <ul class="plat-sidebar-nav-list">
            {items_html}
            </ul>
          </div>
          <div class="plat-sidebar-cta">
            <h4>See the Fabric in action</h4>
            <p>Book a 30-minute walkthrough with the AiVRIC engineering team.</p>
            <a href="https://calendly.com/aivric-sales/aivric-walkthrough-demo" class="plat-btn-sm"><i class="fas fa-calendar-alt"></i>Book a Demo</a>
          </div>
        </aside>"""


def subpage_body(*, color, icon, title, hero_sub, intro_h2, intro_p, caps, steps, outcomes, current_href):
    cap_items = ""
    for cap_name, cap_desc in caps:
        cap_items += f"""
          <div class="plat-sub-cap-item">
            <h4>{cap_name}</h4>
            <p>{cap_desc}</p>
          </div>"""

    step_items = ""
    for i, (s_title, s_desc) in enumerate(steps, 1):
        step_items += f"""
          <div class="plat-step">
            <div class="plat-step-num">{i}</div>
            <div class="plat-step-body">
              <h5>{s_title}</h5>
              <p>{s_desc}</p>
            </div>
          </div>"""

    outcome_items = "\n".join(f"<li>{o}</li>" for o in outcomes)

    sb = sidebar(current_href)

    return f"""
        <section class="plat-sub-hero">
          <div class="plat-hero-grid"></div>
          <div class="plat-hero-scan"></div>
          <div class="plat-hero-glow"></div>
          <div class="plat-auto">
            <div class="plat-crumb">
              <a href="index.html">Home</a>
              <span class="plat-crumb-sep">&#8250;</span>
              <a href="services.html">Platform</a>
              <span class="plat-crumb-sep">&#8250;</span>
              <span class="plat-crumb-cur">{title}</span>
            </div>
            <div class="plat-sub-hero-inner">
              <div class="plat-sub-icon c-{color}"><i class="fas {icon}"></i></div>
              <div class="plat-label"><i class="fas fa-layer-group"></i>AIVRIC PLATFORM FABRIC</div>
              <h1 class="plat-sub-h1">{title}</h1>
              <p class="plat-sub-hero-sub">{hero_sub}</p>
            </div>
          </div>
        </section>

        <section class="plat-sub-body">
          <div class="plat-auto">
            <div class="plat-sub-layout">
              {sb}
              <main>
                <div class="plat-sub-intro">
                  <h2>{intro_h2}</h2>
                  <p>{intro_p}</p>
                </div>

                <div class="plat-sub-caps-grid">{cap_items}
                </div>

                <div class="plat-how-title">How it works</div>
                <div class="plat-steps">{step_items}
                </div>

                <div class="plat-outcomes">
                  <h3>Outcomes you can expect</h3>
                  <ul>{outcome_items}</ul>
                </div>

                <div class="plat-sub-cta-block">
                  <h3>Ready to see {title} in action?</h3>
                  <p>Join a live platform walkthrough and see the Fabric at work across your environment.</p>
                  <a href="https://calendly.com/aivric-sales/aivric-walkthrough-demo" class="plat-btn-primary"><i class="fas fa-play-circle"></i>Request a Live Demo</a>
                </div>
              </main>
            </div>
          </div>
        </section>"""


# ── HUB PAGE (services.html) ──────────────────────────────────────────────────

HUB_BODY = """
        <section class="plat-hero">
          <div class="plat-hero-grid"></div>
          <div class="plat-hero-scan"></div>
          <div class="plat-hero-glow"></div>
          <div class="plat-auto">
            <div class="plat-hero-inner">
              <div class="plat-label"><i class="fas fa-layer-group"></i>AIVRIC PLATFORM FABRIC</div>
              <h1 class="plat-h1">Six capabilities.<br><span class="grad">One unified intelligence layer.</span></h1>
              <p class="plat-hero-sub">The AiVRIC Fabric is the shared foundation powering every suite &mdash; unified data, AI, compute, governance, and privacy across your entire security ecosystem.</p>
              <div class="plat-quicklinks">
                <a class="plat-ql plat-ql-cyan" href="genai-chat.html"><i class="fas fa-comments"></i>GenAI Chat</a>
                <a class="plat-ql plat-ql-green" href="shared-data-layer.html"><i class="fas fa-database"></i>Shared Data Layer</a>
                <a class="plat-ql plat-ql-purp" href="agentic-design.html"><i class="fas fa-robot"></i>Agentic Design</a>
                <a class="plat-ql plat-ql-amber" href="efficient-compute.html"><i class="fas fa-microchip"></i>Efficient Compute</a>
                <a class="plat-ql plat-ql-red" href="data-localization.html"><i class="fas fa-globe"></i>Data Localization</a>
                <a class="plat-ql plat-ql-gold" href="ai-model-inspection.html"><i class="fas fa-search"></i>AI Model Inspection</a>
              </div>
            </div>
          </div>
        </section>

        <section class="plat-section">
          <div class="plat-auto">
            <div class="plat-section-hdr">
              <div class="plat-label"><i class="fas fa-th-large"></i>PLATFORM CAPABILITIES</div>
              <h2 class="plat-section-title">Everything your suites need, built in.</h2>
              <p class="plat-section-sub">Six foundational capabilities that every AiVRIC suite inherits automatically &mdash; no integrations required.</p>
            </div>
            <div class="plat-caps-grid">

              <a class="plat-cap-card c-cyan" href="genai-chat.html" style="text-decoration:none;">
                <div class="plat-cap-icon c-cyan"><i class="fas fa-comments"></i></div>
                <div class="plat-cap-name">GenAI Chat</div>
                <div class="plat-cap-desc">Secure, context-aware intelligence chat that turns telemetry, evidence, and assessments into clear, cited answers for any role.</div>
                <ul class="plat-cap-feats c-cyan">
                  <li>Contextual retrieval with source citations</li>
                  <li>Role-aware responses for analysts &amp; executives</li>
                  <li>Launch investigations from chat</li>
                </ul>
                <span class="plat-cap-link c-cyan">Explore GenAI Chat <i class="fas fa-arrow-right"></i></span>
              </a>

              <a class="plat-cap-card c-green" href="shared-data-layer.html" style="text-decoration:none;">
                <div class="plat-cap-icon c-green"><i class="fas fa-database"></i></div>
                <div class="plat-cap-name">Shared Data Layer</div>
                <div class="plat-cap-desc">One normalized schema that unifies telemetry, compliance evidence, and AI signals across every suite &mdash; eliminating data silos permanently.</div>
                <ul class="plat-cap-feats c-green">
                  <li>Unified ingestion from all suites</li>
                  <li>Real-time cross-suite querying</li>
                  <li>Evidence normalization &amp; tagging</li>
                </ul>
                <span class="plat-cap-link c-green">Explore Data Layer <i class="fas fa-arrow-right"></i></span>
              </a>

              <a class="plat-cap-card c-purp" href="agentic-design.html" style="text-decoration:none;">
                <div class="plat-cap-icon c-purp"><i class="fas fa-robot"></i></div>
                <div class="plat-cap-name">Agentic Design</div>
                <div class="plat-cap-desc">Policy-gated AIRE agents that orchestrate autonomous remediation and investigation workflows with full audit trails and human-in-the-loop controls.</div>
                <ul class="plat-cap-feats c-purp">
                  <li>Multi-agent orchestration across suites</li>
                  <li>Policy-gated autonomous actions</li>
                  <li>Complete audit trail for every action</li>
                </ul>
                <span class="plat-cap-link c-purp">Explore Agentic Design <i class="fas fa-arrow-right"></i></span>
              </a>

              <a class="plat-cap-card c-amber" href="efficient-compute.html" style="text-decoration:none;">
                <div class="plat-cap-icon c-amber"><i class="fas fa-microchip"></i></div>
                <div class="plat-cap-name">Efficient Compute</div>
                <div class="plat-cap-desc">Intelligent model routing, token optimization, and cost monitoring that maximize AI throughput while minimizing infrastructure spend across every workload.</div>
                <ul class="plat-cap-feats c-amber">
                  <li>Intelligent model routing per request type</li>
                  <li>Token &amp; batch optimization</li>
                  <li>Per-workload cost visibility</li>
                </ul>
                <span class="plat-cap-link c-amber">Explore Efficient Compute <i class="fas fa-arrow-right"></i></span>
              </a>

              <a class="plat-cap-card c-red" href="data-localization.html" style="text-decoration:none;">
                <div class="plat-cap-icon c-red"><i class="fas fa-globe"></i></div>
                <div class="plat-cap-name">Data Localization</div>
                <div class="plat-cap-desc">Precise data residency controls that govern where data is stored, processed, and transmitted &mdash; meeting GDPR, ITAR, and sovereign cloud mandates.</div>
                <ul class="plat-cap-feats c-red">
                  <li>Region pinning per dataset or tenant</li>
                  <li>Cross-border governance policies</li>
                  <li>Residency audit reports on demand</li>
                </ul>
                <span class="plat-cap-link c-red">Explore Data Localization <i class="fas fa-arrow-right"></i></span>
              </a>

              <a class="plat-cap-card c-gold" href="ai-model-inspection.html" style="text-decoration:none;">
                <div class="plat-cap-icon c-gold"><i class="fas fa-search"></i></div>
                <div class="plat-cap-name">AI Model Inspection</div>
                <div class="plat-cap-desc">Continuous safety evaluations, bias detection, and hallucination monitoring across every AI model in use &mdash; generating governance-ready evidence automatically.</div>
                <ul class="plat-cap-feats c-gold">
                  <li>Model safety &amp; bias evaluations</li>
                  <li>Hallucination risk monitoring</li>
                  <li>AI governance evidence export</li>
                </ul>
                <span class="plat-cap-link c-gold">Explore AI Inspection <i class="fas fa-arrow-right"></i></span>
              </a>

            </div>
          </div>
        </section>

        <section class="plat-section-alt">
          <div class="plat-auto">
            <div class="plat-section-hdr">
              <div class="plat-label"><i class="fas fa-sitemap"></i>FABRIC POWERS EVERY SUITE</div>
              <h2 class="plat-section-title">The intelligence layer behind each suite.</h2>
              <p class="plat-section-sub">Every AiVRIC suite is built on the Fabric. Here is what that means for each one.</p>
            </div>
            <div class="plat-suite-grid">

              <div class="plat-suite-card s-def">
                <div class="plat-suite-name s-def">Defense Suite</div>
                <div class="plat-suite-desc">CloudSignals, AI Signals, and AIRE use the Fabric to correlate posture findings, compliance evidence, and AI risk signals in one workflow.</div>
                <div class="plat-suite-tags">
                  <span class="plat-suite-tag s-def">GenAI Chat</span>
                  <span class="plat-suite-tag s-def">Shared Data Layer</span>
                  <span class="plat-suite-tag s-def">Agentic Design</span>
                  <span class="plat-suite-tag s-def">AI Model Inspection</span>
                </div>
                <a class="plat-suite-link s-def" href="solutions-portal.html#defense">View Defense products <i class="fas fa-arrow-right"></i></a>
              </div>

              <div class="plat-suite-card s-off">
                <div class="plat-suite-name s-off">Offense Suite</div>
                <div class="plat-suite-desc">RogueAgent ASPM uses the Fabric to route adversary simulations through optimized compute and store attack-path evidence in the shared data layer.</div>
                <div class="plat-suite-tags">
                  <span class="plat-suite-tag s-off">Efficient Compute</span>
                  <span class="plat-suite-tag s-off">Shared Data Layer</span>
                  <span class="plat-suite-tag s-off">Agentic Design</span>
                </div>
                <a class="plat-suite-link s-off" href="solutions-portal.html#offense">View Offense products <i class="fas fa-arrow-right"></i></a>
              </div>

              <div class="plat-suite-card s-vis">
                <div class="plat-suite-name s-vis">Vision Suite</div>
                <div class="plat-suite-desc">Vision AI Optics draws on all six Fabric capabilities to surface cross-suite risk narratives, dashboards, and governance-ready reports from one interface.</div>
                <div class="plat-suite-tags">
                  <span class="plat-suite-tag s-vis">GenAI Chat</span>
                  <span class="plat-suite-tag s-vis">Shared Data Layer</span>
                  <span class="plat-suite-tag s-vis">Data Localization</span>
                  <span class="plat-suite-tag s-vis">AI Model Inspection</span>
                </div>
                <a class="plat-suite-link s-vis" href="solutions-portal.html#vision">View Vision products <i class="fas fa-arrow-right"></i></a>
              </div>

            </div>
          </div>
        </section>

        <section class="plat-integ-strip">
          <div class="plat-auto">
            <div class="plat-section-hdr" style="margin-bottom:36px;">
              <div class="plat-label"><i class="fas fa-plug"></i>ENTERPRISE INTEGRATIONS</div>
              <h2 class="plat-section-title" style="font-size:clamp(22px,3vw,32px);">Connects to your existing stack.</h2>
            </div>
            <div class="plat-integ-grid">
              <div class="plat-integ-item">
                <div class="plat-integ-icon"><i class="fas fa-ticket-alt"></i></div>
                <div class="plat-integ-name">Ticketing</div>
                <div class="plat-integ-desc">Jira &amp; ServiceNow remediation workflows</div>
              </div>
              <div class="plat-integ-item">
                <div class="plat-integ-icon"><i class="fas fa-shield-alt"></i></div>
                <div class="plat-integ-name">SIEM / SOC</div>
                <div class="plat-integ-desc">Splunk &amp; Sentinel alert routing</div>
              </div>
              <div class="plat-integ-item">
                <div class="plat-integ-icon"><i class="fas fa-code-branch"></i></div>
                <div class="plat-integ-name">CI / CD</div>
                <div class="plat-integ-desc">GitHub Actions pipeline policy gates</div>
              </div>
              <div class="plat-integ-item">
                <div class="plat-integ-icon"><i class="fas fa-file-export"></i></div>
                <div class="plat-integ-name">Evidence Export</div>
                <div class="plat-integ-desc">PDF, CSV, JSON audit bundles</div>
              </div>
              <div class="plat-integ-item">
                <div class="plat-integ-icon"><i class="fas fa-code"></i></div>
                <div class="plat-integ-name">API &amp; Webhooks</div>
                <div class="plat-integ-desc">Enterprise APIs for custom automations</div>
              </div>
            </div>
          </div>
        </section>

        <section class="plat-final-cta">
          <div class="plat-final-cta-grid"></div>
          <div class="plat-auto plat-final-cta-inner">
            <div class="plat-label" style="justify-content:center;"><i class="fas fa-play-circle"></i>GET STARTED</div>
            <div class="plat-cta-title">See the Fabric in action.</div>
            <div class="plat-cta-sub">Walk through every capability with the AiVRIC team in 30 minutes.</div>
            <div class="plat-cta-btns">
              <a href="https://calendly.com/aivric-sales/aivric-walkthrough-demo" class="plat-btn-primary"><i class="fas fa-calendar-alt"></i>Book a Platform Demo</a>
              <a href="solutions-portal.html" class="plat-btn-ghost"><i class="fas fa-th-large"></i>Explore All Products</a>
            </div>
          </div>
        </section>"""


# ── SUB-PAGE DATA ─────────────────────────────────────────────────────────────

SUBPAGES = [
    dict(
        file="genai-chat.html",
        title="GenAI Chat | AiVRIC Fabric",
        color="cyan", icon="fa-comments",
        display_title="GenAI Chat",
        hero_sub="Secure, context-aware chat that turns telemetry, evidence, and assessments into clear answers — with citations — for analysts, executives, and auditors.",
        intro_h2="AiVRIC Fabric GenAI Chat unifies risk, compliance, and AI signals into a single intelligent interface.",
        intro_p="Security and compliance data lives across tools, dashboards, and teams. The Fabric GenAI Chat closes the gap by providing a single place to ask questions, verify evidence, and trigger actions without hunting across systems. Every response comes with verifiable source citations from the shared data layer.",
        caps=[
            ("Contextual Retrieval", "Retrieve verified evidence, controls, and telemetry with source citations pulled directly from the Fabric data layer."),
            ("Role-Aware Responses", "Deliver tailored answers for analysts, auditors, and executives — each sees the level of detail they need."),
            ("Actionable Prompts", "Launch investigations, create tasks, or trigger remediation workflows directly from a chat prompt."),
            ("Conversation Memory", "Maintain ongoing investigation context so follow-up questions build on prior answers without repetition."),
        ],
        steps=[
            ("Ingest & Index", "Telemetry, controls, and AI evaluation results are continuously ingested and indexed in the Fabric data layer."),
            ("Tag & Map", "Policy tags, identity context, and evidence mappings are applied so every data point is safe to retrieve."),
            ("Route & Respond", "Requests are routed to specialized Fabric agents for analysis, validation, and synthesized responses."),
        ],
        outcomes=[
            "Reduce time to answer audit and executive questions from hours to minutes.",
            "Improve analyst productivity by eliminating multi-tool pivots for a single answer.",
            "Standardize security and compliance narratives across every team and stakeholder.",
        ],
        current_href="genai-chat.html",
    ),
    dict(
        file="shared-data-layer.html",
        title="Shared Data Layer | AiVRIC Fabric",
        color="green", icon="fa-database",
        display_title="Shared Data Layer",
        hero_sub="One schema, one index, one truth — enabling every AiVRIC capability to query, correlate, and act on the same verified security and compliance data.",
        intro_h2="The AiVRIC Fabric Shared Data Layer is the normalized backbone that eliminates data silos across every suite.",
        intro_p="Without a shared data layer, security teams maintain separate stores for CSPM findings, GRC evidence, AI evaluation results, and incident data. The Fabric collapses these into one normalized index — so queries, correlations, and investigations work across all of them simultaneously.",
        caps=[
            ("Unified Ingestion", "Continuously collect findings, evidence, and telemetry from every AiVRIC suite and third-party integration into one pipeline."),
            ("Evidence Normalization", "Apply a consistent schema to security findings, compliance controls, AI signals, and risk records for cross-suite querying."),
            ("Cross-Suite Querying", "Run a single query that spans CSPM posture, GRC evidence, AI risk scores, and offense findings simultaneously."),
            ("Real-Time Sync", "Changes in any suite propagate to the shared layer within seconds, keeping dashboards and agents operating on current data."),
        ],
        steps=[
            ("Collect", "Findings, evidence, and telemetry stream into the Fabric ingestion pipeline from every connected suite and integration."),
            ("Normalize & Tag", "Each record is mapped to the Fabric schema, tagged by policy, control framework, and identity context."),
            ("Index & Serve", "Normalized records are indexed for low-latency retrieval by GenAI Chat, dashboards, agents, and export workflows."),
        ],
        outcomes=[
            "Eliminate data silos that cause inconsistent findings across security and compliance tools.",
            "Accelerate cross-suite investigations from hours to seconds with unified querying.",
            "Ensure every evidence package, dashboard, and AI response draws from the same verified source.",
        ],
        current_href="shared-data-layer.html",
    ),
    dict(
        file="agentic-design.html",
        title="Agentic Design | AiVRIC Fabric",
        color="purp", icon="fa-robot",
        display_title="Agentic Design",
        hero_sub="Policy-gated AIRE agents that orchestrate autonomous remediation and investigation across every suite — with full audit trails and human-in-the-loop controls.",
        intro_h2="The AiVRIC Fabric Agentic Design layer powers autonomous agents that act with bounded authority across your entire security ecosystem.",
        intro_p="AIRE (AI-driven Remediation Engine) agents coordinate actions across CloudSignals, AI Signals, RogueAgent, and Vision. Each agent operates within explicit policy boundaries, escalates when confidence is low, and generates a complete audit trail for every action taken — so you retain control while automation handles scale.",
        caps=[
            ("Multi-Agent Orchestration", "Coordinate specialized sub-agents across suites — CSPM, GRC, AI risk, and offense — to complete compound workflows autonomously."),
            ("Policy-Gated Actions", "Every agent action is validated against defined policies before execution, preventing unauthorized changes in any environment."),
            ("Audit Trail", "A tamper-evident log captures every agent decision, action, and outcome for compliance review and retrospective investigation."),
            ("Human-in-the-Loop Controls", "Configure approval thresholds so high-impact actions pause for human review before proceeding — at any granularity."),
        ],
        steps=[
            ("Receive Trigger", "An agent workflow is triggered by a finding, scheduled scan, chat prompt, or API call from a connected suite."),
            ("Plan Actions", "The orchestrator agent evaluates available sub-agents and composes an action plan within the bounds of defined policies."),
            ("Execute & Log", "Actions execute with real-time policy validation; every step is written to the audit log with timestamps and actor context."),
        ],
        outcomes=[
            "Remediate misconfigurations and compliance gaps up to 10x faster than manual workflows.",
            "Enforce consistent policy across thousands of resources without analyst overhead.",
            "Produce a complete, board-ready audit trail for every automated action taken.",
        ],
        current_href="agentic-design.html",
    ),
    dict(
        file="efficient-compute.html",
        title="Efficient Compute | AiVRIC Fabric",
        color="amber", icon="fa-microchip",
        display_title="Efficient Compute",
        hero_sub="Intelligent model routing and token optimization that maximize AI throughput while minimizing infrastructure cost across every workload in the Fabric.",
        intro_h2="The AiVRIC Fabric Efficient Compute layer ensures every AI workload uses the right model at the right cost — automatically.",
        intro_p="Not every AI request needs the most powerful model. The Fabric routes low-complexity queries to lightweight models, caches repeated patterns, and batches high-volume workloads — so your infrastructure scales efficiently without sacrificing response quality. Full cost visibility comes standard.",
        caps=[
            ("Intelligent Model Routing", "Classify each request by complexity and route it to the optimal model — balancing quality, latency, and cost automatically."),
            ("Token Optimization", "Compress, cache, and deduplicate prompts and context windows to reduce token consumption across high-volume pipelines."),
            ("Batch Processing", "Group compatible workloads into batches for asynchronous processing, reducing per-unit compute cost at scale."),
            ("Cost Monitoring", "Track AI inference spend per suite, per tenant, and per workload type with real-time dashboards and budget alerts."),
        ],
        steps=[
            ("Analyze Request", "Each incoming AI request is classified by type, urgency, and complexity before routing begins."),
            ("Select Optimal Model", "The compute layer selects the best-fit model from the registered pool, applying caching and batching rules."),
            ("Execute & Track", "The request executes with full telemetry; token usage, latency, and cost are written to the Fabric data layer."),
        ],
        outcomes=[
            "Reduce AI inference costs by 40-60% through intelligent routing and caching without degrading quality.",
            "Improve P95 response latency for high-volume evaluation and chat workloads.",
            "Gain full visibility into AI spend across teams, suites, and cost centers.",
        ],
        current_href="efficient-compute.html",
    ),
    dict(
        file="data-localization.html",
        title="Data Localization | AiVRIC Fabric",
        color="red", icon="fa-globe",
        display_title="Data Localization",
        hero_sub="Precise data residency controls that govern where data is stored, processed, and transmitted — meeting GDPR, ITAR, and sovereign cloud mandates.",
        intro_h2="The AiVRIC Fabric Data Localization layer gives organizations exact control over the geographic and jurisdictional boundaries of every dataset.",
        intro_p="Regulated industries, government customers, and multinational organizations face strict rules about where security data can reside and be processed. The Fabric enforces residency at the record level — not just at the infrastructure tier — so every finding, evidence package, and AI evaluation result stays within its mandated boundary.",
        caps=[
            ("Region Pinning", "Assign storage and processing regions to individual tenants, data types, or control frameworks with granular policy controls."),
            ("Encryption Controls", "Enforce customer-managed encryption keys (CMEK) and bring-your-own-key (BYOK) policies per data classification tier."),
            ("Residency Auditing", "Generate on-demand reports that prove every data record was stored and processed within its mandated geographic boundary."),
            ("Cross-Border Governance", "Define policies that block cross-border data flows, with exception workflows for approved transfers and full logging."),
        ],
        steps=[
            ("Tag by Policy", "Every record ingested into the Fabric is tagged with its applicable residency policy, control framework, and jurisdiction."),
            ("Apply Constraints", "Storage routing, processing assignment, and access controls enforce the residency policy automatically at write time."),
            ("Monitor & Report", "Continuous monitoring detects policy violations; on-demand residency reports provide audit-ready evidence of compliance."),
        ],
        outcomes=[
            "Meet GDPR Article 46, ITAR, and sovereign cloud requirements with verifiable, auditable evidence.",
            "Pass residency audits without manual data inventory — reports generate automatically from the Fabric.",
            "Reduce breach liability by ensuring sensitive security data never leaves its mandated jurisdiction.",
        ],
        current_href="data-localization.html",
    ),
    dict(
        file="ai-model-inspection.html",
        title="AI Model Inspection | AiVRIC Fabric",
        color="gold", icon="fa-search",
        display_title="AI Model Inspection",
        hero_sub="Continuous safety evaluations, bias detection, and hallucination monitoring across every AI model in use — with governance-ready evidence generated automatically.",
        intro_h2="The AiVRIC Fabric AI Model Inspection layer continuously monitors every AI model for safety, bias, and hallucination risk.",
        intro_p="As organizations deploy more AI models, the attack surface for unsafe outputs, biased decisions, and hallucinated facts grows. The Fabric runs continuous, repeatable evaluations against every registered model and feeds the results directly into GRC workflows, compliance evidence packages, and executive dashboards — so AI governance is an ongoing practice, not a quarterly audit.",
        caps=[
            ("Safety Evaluations", "Run repeatable red-team and safety test suites against registered models to detect unsafe outputs before they reach users."),
            ("Bias Detection", "Evaluate models across demographic and domain dimensions to surface systematic bias in outputs and recommendations."),
            ("Hallucination Monitoring", "Continuously measure hallucination rates in production against grounded truth datasets, with trend tracking and alerts."),
            ("Risk Scoring", "Aggregate evaluation results into a model risk score that integrates directly into the GRC risk register and dashboard."),
        ],
        steps=[
            ("Connect Models", "Register AI models — internal, third-party, or open-source — with the Fabric inspection pipeline via API or native integration."),
            ("Run Evaluations", "Scheduled and on-demand evaluation suites execute against each model using standardized and custom test cases."),
            ("Score & Export", "Results are scored, trended over time, and exported as governance-ready evidence mapped to AI policies and control frameworks."),
        ],
        outcomes=[
            "Produce AI governance evidence for SOC 2, ISO 42001, and NIST AI RMF audits automatically.",
            "Reduce hallucination-related incidents by detecting model drift before it impacts users.",
            "Give boards and executives a continuously updated AI risk score with supporting evidence.",
        ],
        current_href="ai-model-inspection.html",
    ),
]


# ── BUILD ─────────────────────────────────────────────────────────────────────

print("Building platform pages...")

build_page(SITE / "services.html", HUB_BODY, title="Platform Fabric | AiVRIC")

for sp in SUBPAGES:
    body = subpage_body(
        color=sp["color"],
        icon=sp["icon"],
        title=sp["display_title"],
        hero_sub=sp["hero_sub"],
        intro_h2=sp["intro_h2"],
        intro_p=sp["intro_p"],
        caps=sp["caps"],
        steps=sp["steps"],
        outcomes=sp["outcomes"],
        current_href=sp["current_href"],
    )
    build_page(SITE / sp["file"], body, title=sp["title"])

print("Done — 7 pages built.")
