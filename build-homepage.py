#!/usr/bin/env python3
"""
AiVRIC Homepage Reimagination
Replaces all body content between header and footer with a full-dark,
animated, market-leading design centered on CloudSignals+RiskOps (live)
while showcasing Vision Platform as the unified data backbone.
"""
from pathlib import Path

SITE = Path(r"C:\Projects\AiVRIC-Website")
INDEX = SITE / "index.html"

raw = INDEX.read_text(encoding="utf-8", errors="replace")

BANNER_ANCHOR = "        <!-- banner-section -->"
FOOTER_ANCHOR = "        <!-- main-footer -->"

bi = raw.find(BANNER_ANCHOR)
fi = raw.find(FOOTER_ANCHOR)
assert bi != -1 and fi != -1, "Anchors not found"

HEAD = raw[:bi]
TAIL = raw[fi:]

# ── HP Inline CSS ─────────────────────────────────────────────────────────────
HP_CSS = """
<style id="hp-styles">
/* ── tokens ─────────────────────────────────────────────────────────── */
:root {
  --hp-bg:    #080f1c;
  --hp-bg2:   #0d1829;
  --hp-bg3:   #060d18;
  --hp-cyan:  #00d1ff;
  --hp-green: #2ee59d;
  --hp-gold:  #ffd63a;
  --hp-purp:  #a78bfa;
  --hp-red:   #f87171;
  --hp-amber: #fb923c;
  --hp-text:  #e2e8f0;
  --hp-muted: #94a3b8;
  --hp-bdr:   rgba(0,209,255,0.12);
}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.001ms!important;transition-duration:.001ms!important}}

/* ── shared helpers ──────────────────────────────────────────────────── */
.hp-avail-dot{width:8px;height:8px;border-radius:50%;background:var(--hp-green);display:inline-block;box-shadow:0 0 8px var(--hp-green);animation:hp-blink 2s ease-in-out infinite;flex-shrink:0}
.hp-dot-lg{width:12px;height:12px;box-shadow:0 0 14px var(--hp-green)}
@keyframes hp-blink{0%,100%{opacity:1}50%{opacity:.35}}
.hp-hero-gradient{background:linear-gradient(90deg,var(--hp-cyan),var(--hp-green));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.hp-vision-gradient{background:linear-gradient(90deg,var(--hp-gold),var(--hp-purp));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.hp-section-label,.hp-section-label-c{display:inline-flex;align-items:center;gap:8px;font-size:11px;font-weight:800;letter-spacing:2.5px;text-transform:uppercase;color:var(--hp-cyan);margin-bottom:16px}
.hp-section-label-c{display:flex;justify-content:center}
.hp-h2{font-family:'Jost',sans-serif;font-size:clamp(28px,3.5vw,46px);font-weight:800;line-height:1.15;color:#f0f8ff;margin-bottom:20px}
.hp-h2.centred{text-align:center}
.hp-sub{font-size:16px;line-height:1.75;color:var(--hp-muted);margin-bottom:40px;max-width:640px}
.hp-sub.centred{text-align:center;margin-left:auto;margin-right:auto}
.hp-btn-primary{display:inline-flex;align-items:center;gap:8px;padding:14px 28px;border-radius:8px;font-size:15px;font-weight:700;background:var(--hp-cyan);color:#050c18;text-decoration:none;transition:all .2s;white-space:nowrap}
.hp-btn-primary:hover{background:#00e8ff;color:#050c18;transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,209,255,.35)}
.hp-btn-ghost{display:inline-flex;align-items:center;gap:8px;padding:14px 28px;border-radius:8px;font-size:15px;font-weight:600;border:1px solid rgba(0,209,255,.3);color:var(--hp-cyan);text-decoration:none;transition:all .2s;white-space:nowrap}
.hp-btn-ghost:hover{background:rgba(0,209,255,.08);border-color:var(--hp-cyan);transform:translateY(-2px)}
.hp-btn-vision{display:inline-flex;align-items:center;gap:8px;padding:14px 32px;border-radius:8px;font-size:15px;font-weight:700;background:linear-gradient(135deg,var(--hp-gold),var(--hp-purp));color:#070e1a;text-decoration:none;transition:all .2s}
.hp-btn-vision:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(167,139,250,.35);color:#070e1a}
.hp-btn-xl{padding:18px 40px;font-size:17px}

/* ═══════════════════════════════════════════════════════════════════════
   SECTION 1 — HERO
═══════════════════════════════════════════════════════════════════════ */
.hp-hero{position:relative;min-height:100vh;background:var(--hp-bg);overflow:hidden;display:flex;align-items:center;padding:140px 0 80px}
/* animated grid overlay */
.hp-hero-grid{position:absolute;inset:0;background-image:linear-gradient(rgba(0,209,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(0,209,255,.035) 1px,transparent 1px);background-size:64px 64px;animation:hp-grid-pulse 9s ease-in-out infinite;pointer-events:none}
@keyframes hp-grid-pulse{0%,100%{opacity:.3}50%{opacity:.8}}
/* vertical scan beam */
.hp-hero-scan{position:absolute;left:0;right:0;height:1.5px;background:linear-gradient(90deg,transparent 0%,rgba(0,209,255,.85) 50%,transparent 100%);top:0;animation:hp-scan 8s linear infinite;pointer-events:none;z-index:1}
@keyframes hp-scan{0%{top:0;opacity:0}4%{opacity:.9}96%{opacity:.9}100%{top:100%;opacity:0}}
/* radial glows */
.hp-hero-glow{position:absolute;border-radius:50%;pointer-events:none}
.hp-glow-l{width:700px;height:700px;background:radial-gradient(circle,rgba(0,209,255,.07) 0%,transparent 70%);left:-200px;top:50%;transform:translateY(-50%);animation:hp-gp-l 6s ease-in-out infinite}
.hp-glow-r{width:600px;height:600px;background:radial-gradient(circle,rgba(46,229,157,.05) 0%,transparent 70%);right:-150px;top:20%;animation:hp-gp-r 7s ease-in-out infinite}
@keyframes hp-gp-l{0%,100%{opacity:.6;transform:translateY(-50%) scale(1)}50%{opacity:1;transform:translateY(-50%) scale(1.07)}}
@keyframes hp-gp-r{0%,100%{opacity:.5;transform:scale(1)}50%{opacity:.9;transform:scale(1.1)}}
/* layout */
.hp-hero-inner{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center;position:relative;z-index:2}
@media(max-width:991px){.hp-hero-inner{grid-template-columns:1fr}.hp-hero-ui-wrap{display:none}}
/* copy entry animation */
.hp-hero-copy{animation:hp-fade-l .9s cubic-bezier(.16,1,.3,1) both}
@keyframes hp-fade-l{from{opacity:0;transform:translateX(-32px)}to{opacity:1;transform:translateX(0)}}
.hp-hero-badge{display:inline-flex;align-items:center;gap:8px;background:rgba(0,209,255,.08);border:1px solid rgba(0,209,255,.25);border-radius:100px;padding:7px 18px;font-size:12px;font-weight:700;color:var(--hp-cyan);letter-spacing:.8px;margin-bottom:28px;text-transform:uppercase}
.hp-h1{font-family:'Jost',sans-serif;font-size:clamp(34px,4.5vw,58px);font-weight:900;line-height:1.1;color:#f0f8ff;margin-bottom:24px}
.hp-hero-sub{font-size:17px;line-height:1.75;color:var(--hp-muted);margin-bottom:36px;max-width:520px}
.hp-hero-actions{display:flex;gap:16px;flex-wrap:wrap;margin-bottom:28px}
.hp-hero-chips{display:flex;flex-wrap:wrap;gap:10px}
.hp-chip{display:inline-flex;align-items:center;gap:6px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:6px;padding:6px 12px;font-size:12px;color:var(--hp-muted)}
.hp-chip i{color:var(--hp-cyan);font-size:11px}
/* ── hero UI mockup ── */
.hp-hero-ui-wrap{position:relative;animation:hp-slide-r .95s cubic-bezier(.16,1,.3,1) both;animation-delay:.15s}
@keyframes hp-slide-r{from{opacity:0;transform:translateX(40px)}to{opacity:1;transform:translateX(0)}}
.hp-ui-card{background:rgba(11,20,38,.97);border:1px solid var(--hp-bdr);border-radius:16px;backdrop-filter:blur(20px);overflow:hidden;box-shadow:0 36px 80px rgba(0,0,0,.65),0 0 0 1px rgba(0,209,255,.05)}
.hp-ui-titlebar{display:flex;align-items:center;gap:6px;padding:13px 16px;background:rgba(0,0,0,.3);border-bottom:1px solid rgba(255,255,255,.06)}
.hp-ui-dot{width:11px;height:11px;border-radius:50%;display:inline-block}
.hp-r{background:#f87171}.hp-y{background:#fbbf24}.hp-g{background:#34d399}
.hp-ui-name{flex:1;font-size:12px;color:var(--hp-muted);margin-left:8px;font-family:monospace}
.hp-ui-live{display:flex;align-items:center;gap:5px;font-size:10px;font-weight:800;letter-spacing:1.2px;color:var(--hp-green)}
.hp-live-dot{width:6px;height:6px;border-radius:50%;background:var(--hp-green);animation:hp-blink 1.4s ease-in-out infinite}
.hp-ui-stats{display:flex}
.hp-ui-stat{flex:1;text-align:center;padding:14px 10px;border-right:1px solid rgba(255,255,255,.05)}
.hp-ui-stat:last-child{border-right:none}
.hp-stat-n{display:block;font-size:26px;font-weight:900;font-family:'Jost',sans-serif;line-height:1;margin-bottom:4px}
.hp-stat-n.good{color:var(--hp-green)}.hp-stat-n.warn{color:var(--hp-amber)}.hp-stat-n.crit{color:var(--hp-red)}
.hp-stat-l{font-size:10.5px;color:var(--hp-muted)}
.hp-ui-findings{padding:12px 14px;display:flex;flex-direction:column;gap:8px}
.hp-finding{display:flex;align-items:center;gap:10px;padding:9px 10px;border-radius:8px;background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.05)}
.hp-f-crit{border-left:3px solid var(--hp-red)!important}
.hp-f-high{border-left:3px solid var(--hp-amber)!important}
.hp-f-med{border-left:3px solid #facc15!important}
.hp-finding>i{font-size:14px;flex-shrink:0}
.hp-f-crit>i{color:var(--hp-red)}.hp-f-high>i{color:var(--hp-amber)}.hp-f-med>i{color:#facc15}
.hp-finding-info{flex:1;display:flex;flex-direction:column;gap:2px;min-width:0}
.hp-finding-name{font-size:12px;font-weight:600;color:#e2e8f0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.hp-finding-meta{font-size:10px;color:var(--hp-muted)}
.hp-sev{font-size:9px;font-weight:800;letter-spacing:.8px;padding:3px 7px;border-radius:4px;white-space:nowrap}
.hp-sv-c{background:rgba(248,113,113,.14);color:var(--hp-red)}
.hp-sv-h{background:rgba(251,146,60,.13);color:var(--hp-amber)}
.hp-sv-m{background:rgba(250,204,21,.11);color:#facc15}
.hp-ui-compliance{display:flex;align-items:center;gap:10px;padding:12px 14px;border-top:1px solid rgba(255,255,255,.05)}
.hp-comp-label{font-size:11px;color:var(--hp-muted);white-space:nowrap}
.hp-comp-track{flex:1;height:5px;background:rgba(255,255,255,.08);border-radius:10px;overflow:hidden}
.hp-comp-fill{height:100%;background:linear-gradient(90deg,var(--hp-cyan),var(--hp-green));border-radius:10px;position:relative;overflow:hidden}
.hp-comp-fill::after{content:'';position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(255,255,255,.3),transparent);animation:hp-shimmer 2s linear infinite}
@keyframes hp-shimmer{from{transform:translateX(-100%)}to{transform:translateX(100%)}}
.hp-comp-pct{font-size:12px;font-weight:700;color:var(--hp-green);white-space:nowrap}
.hp-ui-frameworks{display:flex;flex-wrap:wrap;gap:6px;padding:8px 14px 14px}
.hp-fw-pill{font-size:10px;padding:3px 8px;border-radius:4px;background:rgba(0,209,255,.07);border:1px solid rgba(0,209,255,.15);color:var(--hp-cyan)}
/* floating signal chips */
.hp-float-chip{position:absolute;display:flex;align-items:center;gap:7px;padding:8px 14px;border-radius:50px;font-size:12px;font-weight:700;backdrop-filter:blur(12px);animation:hp-float 3s ease-in-out infinite;white-space:nowrap;z-index:3}
@keyframes hp-float{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
.hp-fc-1{background:rgba(46,229,157,.11);border:1px solid rgba(46,229,157,.3);color:var(--hp-green);top:-18px;right:24px;animation-delay:0s}
.hp-fc-2{background:rgba(251,146,60,.09);border:1px solid rgba(251,146,60,.3);color:var(--hp-amber);bottom:60px;right:-28px;animation-delay:-1s}
.hp-fc-3{background:rgba(0,209,255,.09);border:1px solid rgba(0,209,255,.25);color:var(--hp-cyan);bottom:-16px;left:24px;animation-delay:-2s}

/* ═══════════════════════════════════════════════════════════════════════
   SECTION 2 — TICKER
═══════════════════════════════════════════════════════════════════════ */
.hp-ticker-wrap{background:rgba(0,209,255,.04);border-top:1px solid rgba(0,209,255,.1);border-bottom:1px solid rgba(0,209,255,.1);display:flex;align-items:center;height:38px;overflow:hidden}
.hp-ticker-label{display:flex;align-items:center;gap:6px;padding:0 18px;font-size:10px;font-weight:800;letter-spacing:1.8px;color:var(--hp-green);background:rgba(0,0,0,.35);height:100%;border-right:1px solid rgba(0,209,255,.1);white-space:nowrap;flex-shrink:0;text-transform:uppercase}
.hp-ticker-label i{animation:hp-blink 1.4s infinite;font-size:8px}
.hp-ticker-outer{flex:1;overflow:hidden}
.hp-ticker-track{display:flex;align-items:center;gap:20px;white-space:nowrap;animation:hp-tick 42s linear infinite;font-size:12px;color:var(--hp-muted)}
.hp-t-sep{color:rgba(0,209,255,.4)}
@keyframes hp-tick{from{transform:translateX(0)}to{transform:translateX(-50%)}}

/* ═══════════════════════════════════════════════════════════════════════
   SECTION 3 — CLOUDSIGNALS SPOTLIGHT
═══════════════════════════════════════════════════════════════════════ */
.hp-cs-spotlight{background:var(--hp-bg2);padding:100px 0;position:relative;overflow:hidden}
.hp-cs-spotlight::after{content:'';position:absolute;width:700px;height:700px;border-radius:50%;background:radial-gradient(circle,rgba(46,229,157,.055) 0%,transparent 70%);right:-250px;top:50%;transform:translateY(-50%);pointer-events:none}
.hp-cs-caps{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-bottom:44px}
@media(max-width:768px){.hp-cs-caps{grid-template-columns:1fr 1fr}}
@media(max-width:480px){.hp-cs-caps{grid-template-columns:1fr}}
.hp-cs-cap{background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.07);border-radius:12px;padding:26px;transition:all .22s}
.hp-cs-cap:hover{background:rgba(0,209,255,.05);border-color:rgba(0,209,255,.2);transform:translateY(-3px);box-shadow:0 12px 32px rgba(0,0,0,.3)}
.hp-cs-cap-icon{width:44px;height:44px;border-radius:10px;background:rgba(0,209,255,.1);border:1px solid rgba(0,209,255,.2);display:flex;align-items:center;justify-content:center;margin-bottom:14px}
.hp-cs-cap-icon i{color:var(--hp-cyan);font-size:18px}
.hp-cs-cap h4{font-size:15px;font-weight:700;color:#e2e8f0;margin-bottom:8px}
.hp-cs-cap p{font-size:13px;line-height:1.6;color:var(--hp-muted);margin:0}
.hp-cs-actions{display:flex;gap:16px;flex-wrap:wrap}

/* ═══════════════════════════════════════════════════════════════════════
   SECTION 4 — VISION ARCHITECTURE
═══════════════════════════════════════════════════════════════════════ */
.hp-arch-section{background:var(--hp-bg);padding:100px 0;position:relative;overflow:hidden}
.hp-arch-section::before{content:'';position:absolute;inset:0;background-image:linear-gradient(rgba(0,209,255,.022) 1px,transparent 1px),linear-gradient(90deg,rgba(0,209,255,.022) 1px,transparent 1px);background-size:80px 80px;pointer-events:none}
.hp-arch-diagram{display:grid;grid-template-columns:1fr 56px 180px 56px 1fr;gap:0;align-items:center;margin-bottom:44px}
@media(max-width:991px){.hp-arch-diagram{grid-template-columns:1fr;gap:20px}.hp-arch-connectors-l,.hp-arch-connectors-r{display:none}}
.hp-arch-sources,.hp-arch-outputs{display:flex;flex-direction:column;gap:14px}
.hp-arch-node,.hp-arch-out{display:flex;align-items:center;gap:14px;background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.07);border-radius:12px;padding:16px 18px;transition:all .2s}
.hp-arch-node:hover,.hp-arch-out:hover{background:rgba(0,209,255,.04);border-color:rgba(0,209,255,.16)}
.hp-an-icon,.hp-ao-icon{width:40px;height:40px;border-radius:9px;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.hp-an-def .hp-an-icon{background:rgba(0,209,255,.12)}.hp-an-def .hp-an-icon i{color:var(--hp-cyan)}
.hp-an-off .hp-an-icon{background:rgba(248,113,113,.1)}.hp-an-off .hp-an-icon i{color:var(--hp-red)}
.hp-an-sig .hp-an-icon{background:rgba(167,139,250,.1)}.hp-an-sig .hp-an-icon i{color:var(--hp-purp)}
.hp-ao-chat .hp-ao-icon{background:rgba(0,209,255,.1)}.hp-ao-chat .hp-ao-icon i{color:var(--hp-cyan)}
.hp-ao-aire .hp-ao-icon{background:rgba(46,229,157,.1)}.hp-ao-aire .hp-ao-icon i{color:var(--hp-green)}
.hp-ao-anal .hp-ao-icon{background:rgba(255,214,58,.1)}.hp-ao-anal .hp-ao-icon i{color:var(--hp-gold)}
.hp-an-icon i,.hp-ao-icon i{font-size:17px}
.hp-an-info,.hp-ao-info{display:flex;flex-direction:column;gap:3px;min-width:0}
.hp-an-badge{font-size:9px;font-weight:800;letter-spacing:.8px;text-transform:uppercase;padding:2px 7px;border-radius:4px;display:inline-block;width:fit-content;margin-bottom:3px}
.hp-an-badge.live{background:rgba(46,229,157,.14);color:var(--hp-green)}
.hp-an-badge.road{background:rgba(148,163,184,.1);color:var(--hp-muted)}
.hp-an-info strong,.hp-ao-info strong{font-size:13px;color:#e2e8f0;font-weight:700}
.hp-an-info span,.hp-ao-info span{font-size:11px;color:var(--hp-muted)}
/* flow connectors */
.hp-arch-connectors-l,.hp-arch-connectors-r{display:flex;flex-direction:column;justify-content:space-between;height:210px;padding:24px 0}
.hp-arch-line{flex:1;position:relative;overflow:hidden}
.hp-arch-connectors-l .hp-arch-line{border-top:1px dashed rgba(0,209,255,.18)}
.hp-arch-connectors-r .hp-arch-line{border-top:1px dashed rgba(46,229,157,.18)}
.hp-arch-line::after{content:'';position:absolute;top:-3px;width:14px;height:6px;border-radius:3px;animation:hp-flow 2.2s linear infinite}
.hp-arch-connectors-l .hp-arch-line::after{background:var(--hp-cyan);box-shadow:0 0 7px var(--hp-cyan)}
.hp-arch-connectors-r .hp-arch-line::after{background:var(--hp-green);box-shadow:0 0 7px var(--hp-green)}
.hp-arch-connectors-l .hp-arch-line:nth-child(2)::after{animation-delay:-.73s}
.hp-arch-connectors-l .hp-arch-line:nth-child(3)::after{animation-delay:-1.46s}
.hp-arch-connectors-r .hp-arch-line:nth-child(2)::after{animation-delay:-.73s}
.hp-arch-connectors-r .hp-arch-line:nth-child(3)::after{animation-delay:-1.46s}
@keyframes hp-flow{0%{left:0;opacity:0}5%{opacity:1}95%{opacity:1}100%{left:calc(100% - 14px);opacity:0}}
/* hub */
.hp-arch-hub{position:relative;display:flex;align-items:center;justify-content:center;width:180px;height:180px}
.hp-hub-ring{position:absolute;border-radius:50%;border:1px solid}
.hp-hub-r1{inset:0;border-color:rgba(255,214,58,.2);animation:hp-ring 3.5s ease-in-out infinite}
.hp-hub-r2{inset:15%;border-color:rgba(255,214,58,.35);animation:hp-ring 3.5s ease-in-out infinite;animation-delay:-1.75s}
@keyframes hp-ring{0%,100%{transform:scale(1);opacity:.6}50%{transform:scale(1.05);opacity:1}}
.hp-hub-core{position:relative;z-index:2;background:linear-gradient(135deg,rgba(255,214,58,.1),rgba(167,139,250,.1));border:1.5px solid rgba(255,214,58,.35);border-radius:50%;width:55%;height:55%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:10px;gap:2px}
.hp-hub-core i{color:var(--hp-gold);font-size:20px;margin-bottom:3px}
.hp-hub-core strong{font-size:8.5px;font-weight:900;color:#e2e8f0;text-transform:uppercase;letter-spacing:.5px;line-height:1.3;display:block}
.hp-hub-core em{font-size:7.5px;color:var(--hp-gold);opacity:.85;font-style:normal;display:block}
.hp-arch-cta{text-align:center}

/* ═══════════════════════════════════════════════════════════════════════
   SECTION 5 — PLATFORM SUITES
═══════════════════════════════════════════════════════════════════════ */
.hp-suites-section{background:var(--hp-bg2);padding:100px 0}
.hp-suites-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
@media(max-width:991px){.hp-suites-grid{grid-template-columns:1fr}}
.hp-suite-card{background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.07);border-radius:16px;padding:32px 28px;display:flex;flex-direction:column;position:relative;overflow:hidden;transition:all .25s}
.hp-suite-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px}
.hp-sc-def::before{background:linear-gradient(90deg,var(--hp-cyan),var(--hp-green))}
.hp-sc-off::before{background:linear-gradient(90deg,var(--hp-red),var(--hp-amber))}
.hp-sc-vis::before{background:linear-gradient(90deg,var(--hp-gold),var(--hp-purp))}
.hp-suite-card:hover{background:rgba(255,255,255,.04);border-color:rgba(255,255,255,.12);transform:translateY(-5px);box-shadow:0 24px 56px rgba(0,0,0,.45)}
.hp-sc-hdr{display:flex;align-items:center;justify-content:space-between;margin-bottom:22px}
.hp-sc-icon{width:50px;height:50px;border-radius:12px;display:flex;align-items:center;justify-content:center}
.hp-sc-def .hp-sc-icon{background:rgba(0,209,255,.12)}.hp-sc-def .hp-sc-icon i{color:var(--hp-cyan);font-size:22px}
.hp-sc-off .hp-sc-icon{background:rgba(248,113,113,.1)}.hp-sc-off .hp-sc-icon i{color:var(--hp-red);font-size:22px}
.hp-sc-vis .hp-sc-icon{background:rgba(255,214,58,.1)}.hp-sc-vis .hp-sc-icon i{color:var(--hp-gold);font-size:22px}
.hp-sc-status{font-size:11px;font-weight:700;padding:5px 11px;border-radius:50px;display:flex;align-items:center;gap:5px}
.hp-sc-live{background:rgba(46,229,157,.11);color:var(--hp-green);border:1px solid rgba(46,229,157,.25)}
.hp-sc-road{background:rgba(148,163,184,.08);color:var(--hp-muted);border:1px solid rgba(148,163,184,.15)}
.hp-suite-card h3{font-size:21px;font-weight:800;color:#f0f8ff;margin-bottom:12px;font-family:'Jost',sans-serif}
.hp-suite-card>p{font-size:13px;color:var(--hp-muted);line-height:1.65;margin-bottom:22px}
.hp-sc-list{list-style:none;padding:0;margin:0 0 28px;display:flex;flex-direction:column;gap:9px}
.hp-sc-list li{font-size:13px;color:#cbd5e1;display:flex;align-items:flex-start;gap:8px}
.hp-sc-list li i{color:var(--hp-green);font-size:11px;margin-top:3px;flex-shrink:0}
.hp-sc-cta{margin-top:auto;display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:700;text-decoration:none;transition:gap .2s}
.hp-sc-def .hp-sc-cta{color:var(--hp-cyan)}.hp-sc-off .hp-sc-cta{color:var(--hp-amber)}.hp-sc-vis .hp-sc-cta{color:var(--hp-gold)}
.hp-sc-cta:hover{gap:11px}

/* ═══════════════════════════════════════════════════════════════════════
   SECTION 6 — STATS
═══════════════════════════════════════════════════════════════════════ */
.hp-stats-section{background:var(--hp-bg);padding:70px 0;border-top:1px solid rgba(255,255,255,.04);border-bottom:1px solid rgba(255,255,255,.04)}
.hp-stats-grid{display:grid;grid-template-columns:repeat(4,1fr)}
@media(max-width:768px){.hp-stats-grid{grid-template-columns:repeat(2,1fr)}}
.hp-stat-block{text-align:center;padding:28px 20px;border-right:1px solid rgba(255,255,255,.05)}
.hp-stat-block:last-child{border-right:none}
.hp-stat-num{display:block;font-family:'Jost',sans-serif;font-size:clamp(40px,5vw,60px);font-weight:900;color:#f0f8ff;line-height:1;margin-bottom:8px}
.hp-stat-plus,.hp-stat-pct{color:var(--hp-cyan);font-size:.65em}
.hp-stat-lbl{font-size:12px;color:var(--hp-muted);line-height:1.5}

/* ═══════════════════════════════════════════════════════════════════════
   SECTION 7 — HOW IT WORKS
═══════════════════════════════════════════════════════════════════════ */
.hp-how-section{background:var(--hp-bg3);padding:100px 0}
.hp-how-steps{display:flex;align-items:stretch;gap:0}
@media(max-width:768px){.hp-how-steps{flex-direction:column}.hp-how-arrow{transform:rotate(90deg)}}
.hp-how-step{flex:1;text-align:center;padding:40px 28px;background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.07);border-radius:16px;display:flex;flex-direction:column;align-items:center;transition:all .22s}
.hp-how-step:hover{background:rgba(0,209,255,.04);border-color:rgba(0,209,255,.15);transform:translateY(-3px)}
.hp-how-num{font-family:'Jost',sans-serif;font-size:52px;font-weight:900;background:linear-gradient(90deg,var(--hp-cyan),var(--hp-green));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1;margin-bottom:14px}
.hp-how-icon{width:58px;height:58px;border-radius:14px;background:rgba(0,209,255,.1);border:1px solid rgba(0,209,255,.2);display:flex;align-items:center;justify-content:center;margin-bottom:16px}
.hp-how-icon i{color:var(--hp-cyan);font-size:24px}
.hp-how-step h4{font-size:17px;font-weight:700;color:#e2e8f0;margin-bottom:10px}
.hp-how-step p{font-size:13px;color:var(--hp-muted);line-height:1.65;margin:0;flex:1}
.hp-how-arrow{width:56px;text-align:center;color:rgba(0,209,255,.25);font-size:22px;display:flex;align-items:center;justify-content:center;flex-shrink:0}

/* ═══════════════════════════════════════════════════════════════════════
   SECTION 8 — DATA SOVEREIGNTY
═══════════════════════════════════════════════════════════════════════ */
.hp-deploy-section{background:var(--hp-bg2);padding:100px 0}
.hp-deploy-inner{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center}
@media(max-width:991px){.hp-deploy-inner{grid-template-columns:1fr}.hp-deploy-visual{display:none}}
.hp-deploy-opts{display:flex;flex-direction:column;gap:14px;margin-bottom:36px}
.hp-deploy-opt{display:flex;align-items:flex-start;gap:14px;padding:16px;background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.07);border-radius:10px}
.hp-do-icon{width:38px;height:38px;border-radius:8px;background:rgba(0,209,255,.1);display:flex;align-items:center;justify-content:center;flex-shrink:0}
.hp-do-icon i{color:var(--hp-cyan);font-size:16px}
.hp-deploy-opt strong{display:block;font-size:14px;font-weight:700;color:#e2e8f0;margin-bottom:3px}
.hp-deploy-opt span{font-size:12.5px;color:var(--hp-muted);line-height:1.5}
.hp-dv-card{background:rgba(10,18,34,.98);border:1px solid rgba(0,209,255,.14);border-radius:16px;overflow:hidden}
.hp-dv-hdr{background:rgba(0,209,255,.07);border-bottom:1px solid rgba(0,209,255,.1);padding:11px 20px;font-size:11px;font-weight:800;color:var(--hp-cyan);letter-spacing:.6px;font-family:monospace;text-transform:uppercase}
.hp-dv-body{padding:18px 18px 6px;display:flex;flex-direction:column;gap:9px}
.hp-dv-pod{display:flex;align-items:center;gap:10px;padding:9px 13px;background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.055);border-radius:8px;font-size:12.5px;color:#94a3b8;font-family:monospace}
.hp-dv-pod i{color:var(--hp-cyan);font-size:13px}
.hp-dv-db{border-color:rgba(46,229,157,.15)!important;color:var(--hp-green)!important}
.hp-dv-db i{color:var(--hp-green)!important}
.hp-dv-foot{margin:12px 18px 18px;padding:10px 14px;background:rgba(46,229,157,.06);border:1px solid rgba(46,229,157,.15);border-radius:8px;font-size:11.5px;color:var(--hp-green);font-weight:700;display:flex;align-items:center;gap:7px}

/* ═══════════════════════════════════════════════════════════════════════
   SECTION 9 — BLOG
═══════════════════════════════════════════════════════════════════════ */
.hp-blog-section{background:var(--hp-bg);padding:100px 0}
.hp-blog-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
@media(max-width:768px){.hp-blog-grid{grid-template-columns:1fr}}
.hp-blog-card{background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.07);border-radius:14px;overflow:hidden;text-decoration:none;display:flex;flex-direction:column;transition:all .22s}
.hp-blog-card:hover{transform:translateY(-5px);border-color:rgba(0,209,255,.2);box-shadow:0 20px 48px rgba(0,0,0,.45)}
.hp-blog-img{height:176px;background-size:cover;background-position:center;position:relative}
.hp-blog-img::after{content:'';position:absolute;inset:0;background:linear-gradient(to bottom,transparent 40%,rgba(8,15,28,.8))}
.hp-blog-body{padding:20px;flex:1;display:flex;flex-direction:column;gap:8px}
.hp-blog-tag{font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:1.5px;color:var(--hp-cyan)}
.hp-blog-body h4{font-size:15px;font-weight:700;color:#e2e8f0;line-height:1.4;margin:0}
.hp-blog-body p{font-size:12.5px;color:var(--hp-muted);line-height:1.6;margin:0;flex:1}
.hp-blog-read{font-size:12px;font-weight:700;color:var(--hp-cyan);display:flex;align-items:center;gap:5px;margin-top:4px}
.hp-blog-read i{transition:transform .15s}
.hp-blog-card:hover .hp-blog-read i{transform:translateX(4px)}

/* ═══════════════════════════════════════════════════════════════════════
   SECTION 10 — FINAL CTA
═══════════════════════════════════════════════════════════════════════ */
.hp-final-cta{background:var(--hp-bg);position:relative;padding:120px 0;text-align:center;overflow:hidden}
.hp-cta-grid{position:absolute;inset:0;background-image:linear-gradient(rgba(0,209,255,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(0,209,255,.04) 1px,transparent 1px);background-size:64px 64px;animation:hp-grid-pulse 9s ease-in-out infinite;pointer-events:none}
.hp-cta-glow{position:absolute;width:900px;height:400px;border-radius:50%;background:radial-gradient(ellipse,rgba(0,209,255,.07) 0%,transparent 70%);left:50%;top:50%;transform:translate(-50%,-50%);pointer-events:none}
.hp-cta-inner{position:relative;z-index:2;display:flex;flex-direction:column;align-items:center}
.hp-cta-h2{font-family:'Jost',sans-serif;font-size:clamp(32px,4vw,54px);font-weight:900;color:#f0f8ff;margin:16px 0 22px;line-height:1.12}
.hp-cta-sub{font-size:17px;color:var(--hp-muted);max-width:560px;line-height:1.75;margin-bottom:36px}
.hp-cta-actions{display:flex;gap:16px;flex-wrap:wrap;justify-content:center;margin-bottom:28px}
.hp-cta-chips{display:flex;gap:24px;flex-wrap:wrap;justify-content:center}
.hp-cta-chips span{font-size:13px;color:var(--hp-muted);display:flex;align-items:center;gap:6px}
.hp-cta-chips i{color:var(--hp-green)}
</style>
"""

# ── New body content ────────────────────────────────────────────────────────────
NEW_BODY = r"""
        <!-- ═══════════════════════ HERO ═══════════════════════ -->
        <section class="hp-hero">
          <div class="hp-hero-grid"></div>
          <div class="hp-hero-scan"></div>
          <div class="hp-hero-glow hp-glow-l"></div>
          <div class="hp-hero-glow hp-glow-r"></div>
          <div class="auto-container">
            <div class="hp-hero-inner">

              <!-- COPY -->
              <div class="hp-hero-copy">
                <div class="hp-hero-badge">
                  <span class="hp-avail-dot"></span>
                  CloudSignals+RiskOps&trade; &mdash; Available Now
                </div>
                <h1 class="hp-h1">AI-native cloud security.<br>Hosted in your environment.<br><span class="hp-hero-gradient">One data truth.</span></h1>
                <p class="hp-hero-sub">Detect misconfigurations, enforce continuous compliance, and run autonomous risk operations across AWS, Azure, GCP, and OCI &mdash; with full data sovereignty.</p>
                <div class="hp-hero-actions">
                  <a href="cspm-cloudsignals.html" class="hp-btn-primary">Explore CloudSignals+RiskOps</a>
                  <a href="services.html" class="hp-btn-ghost">Full platform overview <i class="fas fa-arrow-right"></i></a>
                </div>
                <div class="hp-hero-chips">
                  <span class="hp-chip"><i class="fas fa-server"></i> Customer-hosted SaaS</span>
                  <span class="hp-chip"><i class="fas fa-shield-alt"></i> 350+ cloud checks</span>
                  <span class="hp-chip"><i class="fas fa-file-alt"></i> 20+ frameworks</span>
                  <span class="hp-chip"><i class="fas fa-robot"></i> AIRE Agentic Mesh&trade;</span>
                </div>
              </div>

              <!-- UI MOCKUP -->
              <div class="hp-hero-ui-wrap">
                <div class="hp-ui-card">
                  <div class="hp-ui-titlebar">
                    <span class="hp-ui-dot hp-r"></span><span class="hp-ui-dot hp-y"></span><span class="hp-ui-dot hp-g"></span>
                    <span class="hp-ui-name">cloudsignals &mdash; live-scan &mdash; prod-aws-us-east-1</span>
                    <span class="hp-ui-live"><span class="hp-live-dot"></span>LIVE</span>
                  </div>
                  <div class="hp-ui-stats">
                    <div class="hp-ui-stat"><span class="hp-stat-n good">847</span><span class="hp-stat-l">Controls Passed</span></div>
                    <div class="hp-ui-stat"><span class="hp-stat-n warn">23</span><span class="hp-stat-l">Findings</span></div>
                    <div class="hp-ui-stat"><span class="hp-stat-n crit">3</span><span class="hp-stat-l">Critical</span></div>
                  </div>
                  <div class="hp-ui-findings">
                    <div class="hp-finding hp-f-crit">
                      <i class="fas fa-exclamation-circle"></i>
                      <div class="hp-finding-info">
                        <span class="hp-finding-name">S3 bucket public read ACL enabled</span>
                        <span class="hp-finding-meta">AWS us-east-1 &middot; CIS 2.1.5 &middot; SOC 2 CC6.1</span>
                      </div>
                      <span class="hp-sev hp-sv-c">CRITICAL</span>
                    </div>
                    <div class="hp-finding hp-f-high">
                      <i class="fas fa-exclamation-triangle"></i>
                      <div class="hp-finding-info">
                        <span class="hp-finding-name">IAM root access key active</span>
                        <span class="hp-finding-meta">AWS us-east-1 &middot; CIS 1.4 &middot; PCI 8.3</span>
                      </div>
                      <span class="hp-sev hp-sv-h">HIGH</span>
                    </div>
                    <div class="hp-finding hp-f-med">
                      <i class="fas fa-info-circle"></i>
                      <div class="hp-finding-info">
                        <span class="hp-finding-name">MFA not enforced for IAM user</span>
                        <span class="hp-finding-meta">AWS us-west-2 &middot; SOC 2 CC6.1 &middot; NIST AC-2</span>
                      </div>
                      <span class="hp-sev hp-sv-m">MEDIUM</span>
                    </div>
                  </div>
                  <div class="hp-ui-compliance">
                    <span class="hp-comp-label">SOC 2 Readiness</span>
                    <div class="hp-comp-track"><div class="hp-comp-fill" style="width:78%"></div></div>
                    <span class="hp-comp-pct">78%</span>
                  </div>
                  <div class="hp-ui-frameworks">
                    <span class="hp-fw-pill">CIS AWS 1.5</span>
                    <span class="hp-fw-pill">SOC 2</span>
                    <span class="hp-fw-pill">PCI DSS 4.0</span>
                    <span class="hp-fw-pill">NIST CSF</span>
                    <span class="hp-fw-pill">+16 more</span>
                  </div>
                </div>
                <div class="hp-float-chip hp-fc-1"><i class="fas fa-check-circle"></i>&nbsp;Policy enforced</div>
                <div class="hp-float-chip hp-fc-2"><i class="fas fa-bell"></i>&nbsp;Alert &rarr; Jira</div>
                <div class="hp-float-chip hp-fc-3"><i class="fas fa-database"></i>&nbsp;Evidence captured</div>
              </div>

            </div>
          </div>
        </section>

        <!-- ═══════════════════════ SIGNAL TICKER ═══════════════════════ -->
        <div class="hp-ticker-wrap" aria-hidden="true">
          <div class="hp-ticker-label"><i class="fas fa-circle"></i>&nbsp; LIVE</div>
          <div class="hp-ticker-outer">
            <div class="hp-ticker-track">
              <span>CIS AWS 1.5 scan completed &mdash; 847 controls evaluated</span><span class="hp-t-sep">&bull;</span>
              <span>Critical: S3 public ACL detected &mdash; us-east-1</span><span class="hp-t-sep">&bull;</span>
              <span>SOC 2 evidence package updated &mdash; 4 new controls mapped</span><span class="hp-t-sep">&bull;</span>
              <span>AIRE agent executed remediation &mdash; IAM policy applied</span><span class="hp-t-sep">&bull;</span>
              <span>PCI DSS 4.0 assessment: 94% compliant</span><span class="hp-t-sep">&bull;</span>
              <span>Cyber Risk Index updated &mdash; 7.2 (&#8595;0.4 this week)</span><span class="hp-t-sep">&bull;</span>
              <span>Azure posture scan complete &mdash; 312 resources evaluated</span><span class="hp-t-sep">&bull;</span>
              <span>New POAM generated &mdash; assigned to remediation team</span><span class="hp-t-sep">&bull;</span>
              <span>CMMC Level 2 gap analysis complete &mdash; 3 controls require action</span><span class="hp-t-sep">&bull;</span>
              <!-- duplicate for seamless loop -->
              <span>CIS AWS 1.5 scan completed &mdash; 847 controls evaluated</span><span class="hp-t-sep">&bull;</span>
              <span>Critical: S3 public ACL detected &mdash; us-east-1</span><span class="hp-t-sep">&bull;</span>
              <span>SOC 2 evidence package updated &mdash; 4 new controls mapped</span><span class="hp-t-sep">&bull;</span>
              <span>AIRE agent executed remediation &mdash; IAM policy applied</span><span class="hp-t-sep">&bull;</span>
              <span>PCI DSS 4.0 assessment: 94% compliant</span><span class="hp-t-sep">&bull;</span>
              <span>Cyber Risk Index updated &mdash; 7.2 (&#8595;0.4 this week)</span><span class="hp-t-sep">&bull;</span>
              <span>Azure posture scan complete &mdash; 312 resources evaluated</span><span class="hp-t-sep">&bull;</span>
              <span>New POAM generated &mdash; assigned to remediation team</span><span class="hp-t-sep">&bull;</span>
              <span>CMMC Level 2 gap analysis complete &mdash; 3 controls require action</span><span class="hp-t-sep">&bull;</span>
            </div>
          </div>
        </div>

        <!-- ═══════════════════════ CLOUDSIGNALS SPOTLIGHT ═══════════════════════ -->
        <section class="hp-cs-spotlight">
          <div class="auto-container">
            <div class="hp-section-label"><span class="hp-avail-dot"></span>&nbsp;The only cloud security platform you host yourself</div>
            <h2 class="hp-h2">CloudSignals+RiskOps&trade; &mdash;<br><span class="hp-hero-gradient">AI-native. Customer-hosted. Live today.</span></h2>
            <p class="hp-sub">A unified cloud security platform combining AI-native posture management, continuous compliance, and autonomous risk operations. Deployed in your Kubernetes environment with complete data sovereignty &mdash; your findings never leave your infrastructure.</p>
            <div class="hp-cs-caps">
              <div class="hp-cs-cap">
                <div class="hp-cs-cap-icon"><i class="fas fa-cloud"></i></div>
                <h4>Multi-Cloud CSPM</h4>
                <p>Continuous posture scanning across AWS, Azure, GCP, and OCI with 350+ security checks and real-time drift detection.</p>
              </div>
              <div class="hp-cs-cap">
                <div class="hp-cs-cap-icon"><i class="fas fa-exclamation-triangle"></i></div>
                <h4>Risk Signals &amp; Findings</h4>
                <p>Business-context risk scoring with prioritized findings, ownership assignment, and SLA tracking across your cloud estate.</p>
              </div>
              <div class="hp-cs-cap">
                <div class="hp-cs-cap-icon"><i class="fas fa-clipboard-check"></i></div>
                <h4>Continuous Compliance</h4>
                <p>Automated control mapping for SOC 2, PCI DSS, NIST, CMMC, ISO 27001, and 16+ frameworks with audit-ready evidence.</p>
              </div>
              <div class="hp-cs-cap">
                <div class="hp-cs-cap-icon"><i class="fas fa-robot"></i></div>
                <h4>AIRE Agentic Mesh&trade;</h4>
                <p>AI agents that auto-remediate findings, update evidence, route tasks, and close loops through your existing workflows.</p>
              </div>
              <div class="hp-cs-cap">
                <div class="hp-cs-cap-icon"><i class="fas fa-list-alt"></i></div>
                <h4>Issues, POAMs &amp; Exceptions</h4>
                <p>Centralized risk register with POAMs, control exceptions, owner tracking, and executive-ready evidence packages.</p>
              </div>
              <div class="hp-cs-cap">
                <div class="hp-cs-cap-icon"><i class="fas fa-chart-bar"></i></div>
                <h4>AI Signals&trade;</h4>
                <p>LLM observability and evaluation for your AI applications &mdash; traces, scores, prompt governance, and model risk.</p>
              </div>
            </div>
            <div class="hp-cs-actions">
              <a href="cspm-cloudsignals.html" class="hp-btn-primary">Full platform breakdown</a>
              <a href="cloudsignals-pricing.html" class="hp-btn-ghost">Compare plans &amp; pricing <i class="fas fa-arrow-right"></i></a>
            </div>
          </div>
        </section>

        <!-- ═══════════════════════ VISION ARCHITECTURE ═══════════════════════ -->
        <section class="hp-arch-section">
          <div class="auto-container">
            <div class="hp-section-label-c">Platform Architecture</div>
            <h2 class="hp-h2 centred">AiVRIC Vision Platform &mdash;<br><span class="hp-vision-gradient">The unified intelligence backbone.</span></h2>
            <p class="hp-sub centred">Every AiVRIC solution feeds into Vision&rsquo;s unified data layer with tight tenant segmentation. Vision aggregates, normalizes, and surfaces intelligence across the entire platform &mdash; powering AI Chat, Data Analytics &amp; Modelling, and the AIRE Agentic Mesh from one authoritative data truth.</p>
            <div class="hp-arch-diagram">

              <!-- SOURCES -->
              <div class="hp-arch-sources">
                <div class="hp-arch-node hp-an-def">
                  <div class="hp-an-icon"><i class="fas fa-shield-alt"></i></div>
                  <div class="hp-an-info">
                    <span class="hp-an-badge live">Live</span>
                    <strong>CloudSignals+RiskOps&trade;</strong>
                    <span>Posture, compliance &amp; risk signals</span>
                  </div>
                </div>
                <div class="hp-arch-node hp-an-off">
                  <div class="hp-an-icon"><i class="fas fa-user-secret"></i></div>
                  <div class="hp-an-info">
                    <span class="hp-an-badge road">Roadmap</span>
                    <strong>RogueAgent ASPM&trade;</strong>
                    <span>Adversarial signals &amp; ASPM data</span>
                  </div>
                </div>
                <div class="hp-arch-node hp-an-sig">
                  <div class="hp-an-icon"><i class="fas fa-microchip"></i></div>
                  <div class="hp-an-info">
                    <span class="hp-an-badge live">Live</span>
                    <strong>AI Signals&trade;</strong>
                    <span>LLM traces, evals &amp; prompt data</span>
                  </div>
                </div>
              </div>

              <!-- LEFT FLOW LINES -->
              <div class="hp-arch-connectors-l">
                <div class="hp-arch-line"></div>
                <div class="hp-arch-line"></div>
                <div class="hp-arch-line"></div>
              </div>

              <!-- VISION HUB -->
              <div class="hp-arch-hub">
                <div class="hp-hub-ring hp-hub-r1"></div>
                <div class="hp-hub-ring hp-hub-r2"></div>
                <div class="hp-hub-core">
                  <i class="fas fa-eye"></i>
                  <strong>AiVRIC Vision</strong>
                  <em>Unified Data Layer</em>
                </div>
              </div>

              <!-- RIGHT FLOW LINES -->
              <div class="hp-arch-connectors-r">
                <div class="hp-arch-line"></div>
                <div class="hp-arch-line"></div>
                <div class="hp-arch-line"></div>
              </div>

              <!-- OUTPUTS -->
              <div class="hp-arch-outputs">
                <div class="hp-arch-out hp-ao-chat">
                  <div class="hp-ao-icon"><i class="fas fa-comments"></i></div>
                  <div class="hp-ao-info">
                    <strong>AI Chat</strong>
                    <span>Query your security data in natural language across all solutions</span>
                  </div>
                </div>
                <div class="hp-arch-out hp-ao-aire">
                  <div class="hp-ao-icon"><i class="fas fa-robot"></i></div>
                  <div class="hp-ao-info">
                    <strong>AIRE Agentic Mesh&trade;</strong>
                    <span>Autonomous agents acting on unified intelligence</span>
                  </div>
                </div>
                <div class="hp-arch-out hp-ao-anal">
                  <div class="hp-ao-icon"><i class="fas fa-chart-line"></i></div>
                  <div class="hp-ao-info">
                    <strong>Data Analytics &amp; Modelling</strong>
                    <span>AI-driven risk models, trend analysis &amp; predictive insights</span>
                  </div>
                </div>
              </div>

            </div>
            <div class="hp-arch-cta">
              <a href="aivric-vision-professional.html" class="hp-btn-vision">Explore AiVRIC Vision Platform &rarr;</a>
            </div>
          </div>
        </section>

        <!-- ═══════════════════════ PLATFORM SUITES ═══════════════════════ -->
        <section class="hp-suites-section">
          <div class="auto-container">
            <div class="hp-section-label-c">The AiVRIC Platform</div>
            <h2 class="hp-h2 centred">Defense, Offense, and Intelligence.<br><span class="hp-hero-gradient">Built as one unified system.</span></h2>
            <div class="hp-suites-grid">

              <div class="hp-suite-card hp-sc-def">
                <div class="hp-sc-hdr">
                  <div class="hp-sc-icon"><i class="fas fa-shield-alt"></i></div>
                  <span class="hp-sc-status hp-sc-live"><span class="hp-avail-dot"></span>&nbsp;Available Now</span>
                </div>
                <h3>AiVRIC Defense Suite</h3>
                <p>The complete cloud security platform for SOC, GRC, and compliance teams. Powered by CloudSignals+RiskOps&trade; and AI Signals&trade;.</p>
                <ul class="hp-sc-list">
                  <li><i class="fas fa-check"></i> Multi-Cloud CSPM (AWS, Azure, GCP, OCI)</li>
                  <li><i class="fas fa-check"></i> Continuous compliance &amp; evidence collection</li>
                  <li><i class="fas fa-check"></i> Cyber RiskOps, POAMs &amp; risk register</li>
                  <li><i class="fas fa-check"></i> AI Signals&trade; LLM observability</li>
                  <li><i class="fas fa-check"></i> AIRE Agentic Mesh&trade; auto-remediation</li>
                </ul>
                <a href="cspm-cloudsignals.html" class="hp-sc-cta">Explore Defense Suite <i class="fas fa-arrow-right"></i></a>
              </div>

              <div class="hp-suite-card hp-sc-off">
                <div class="hp-sc-hdr">
                  <div class="hp-sc-icon"><i class="fas fa-user-secret"></i></div>
                  <span class="hp-sc-status hp-sc-road"><i class="fas fa-clock"></i>&nbsp;Roadmap</span>
                </div>
                <h3>AiVRIC Offense Suite</h3>
                <p>Adversarial validation and attack surface management. RogueAgent ASPM&trade; tests your defenses against real-world techniques.</p>
                <ul class="hp-sc-list">
                  <li><i class="fas fa-check"></i> Application Security Posture Management</li>
                  <li><i class="fas fa-check"></i> Red team automation &amp; scenario playbooks</li>
                  <li><i class="fas fa-check"></i> Digital risk scans &amp; external exposure</li>
                  <li><i class="fas fa-check"></i> Defense-offense correlation via Vision</li>
                  <li><i class="fas fa-check"></i> Findings feed directly into AIRE agents</li>
                </ul>
                <a href="rogueagent.html" class="hp-sc-cta">Learn about RogueAgent <i class="fas fa-arrow-right"></i></a>
              </div>

              <div class="hp-suite-card hp-sc-vis">
                <div class="hp-sc-hdr">
                  <div class="hp-sc-icon"><i class="fas fa-eye"></i></div>
                  <span class="hp-sc-status hp-sc-road"><i class="fas fa-clock"></i>&nbsp;Roadmap</span>
                </div>
                <h3>AiVRIC Vision Platform</h3>
                <p>The intelligence backbone. The only security platform with a truly unified data layer that aggregates all solutions into one authoritative truth.</p>
                <ul class="hp-sc-list">
                  <li><i class="fas fa-check"></i> Unified data layer &mdash; all solutions, one truth</li>
                  <li><i class="fas fa-check"></i> Tenant-segmented private AI datastore</li>
                  <li><i class="fas fa-check"></i> AI Chat across all security contexts</li>
                  <li><i class="fas fa-check"></i> Data Analytics &amp; AI Modelling</li>
                  <li><i class="fas fa-check"></i> AIRE Agentic Mesh&trade; full integration</li>
                </ul>
                <a href="aivric-vision-professional.html" class="hp-sc-cta">Explore Vision Platform <i class="fas fa-arrow-right"></i></a>
              </div>

            </div>
          </div>
        </section>

        <!-- ═══════════════════════ STATS ═══════════════════════ -->
        <section class="hp-stats-section">
          <div class="auto-container">
            <div class="hp-stats-grid">
              <div class="hp-stat-block">
                <span class="hp-stat-num">350<span class="hp-stat-plus">+</span></span>
                <span class="hp-stat-lbl">Cloud security checks across 4 providers</span>
              </div>
              <div class="hp-stat-block">
                <span class="hp-stat-num">20<span class="hp-stat-plus">+</span></span>
                <span class="hp-stat-lbl">Compliance frameworks natively mapped</span>
              </div>
              <div class="hp-stat-block">
                <span class="hp-stat-num">3</span>
                <span class="hp-stat-lbl">Integrated platform suites sharing one data layer</span>
              </div>
              <div class="hp-stat-block">
                <span class="hp-stat-num">100<span class="hp-stat-pct">%</span></span>
                <span class="hp-stat-lbl">Customer-hosted &mdash; your data, your cluster</span>
              </div>
            </div>
          </div>
        </section>

        <!-- ═══════════════════════ HOW IT WORKS ═══════════════════════ -->
        <section class="hp-how-section">
          <div class="auto-container">
            <div class="hp-section-label-c">How It Works</div>
            <h2 class="hp-h2 centred">From cloud telemetry to agentic action<br><span class="hp-hero-gradient">in three steps.</span></h2>
            <div class="hp-how-steps">
              <div class="hp-how-step">
                <div class="hp-how-num">01</div>
                <div class="hp-how-icon"><i class="fas fa-plug"></i></div>
                <h4>Connect your cloud</h4>
                <p>Deploy CloudSignals into your Kubernetes cluster in minutes. Connect your AWS, Azure, GCP, and OCI accounts &mdash; no data leaves your environment from day one.</p>
              </div>
              <div class="hp-how-arrow"><i class="fas fa-chevron-right"></i></div>
              <div class="hp-how-step">
                <div class="hp-how-num">02</div>
                <div class="hp-how-icon"><i class="fas fa-search"></i></div>
                <h4>Detect, score &amp; map</h4>
                <p>CloudSignals scans your posture continuously, prioritizes findings with business-context scoring, and maps controls to every compliance framework you need.</p>
              </div>
              <div class="hp-how-arrow"><i class="fas fa-chevron-right"></i></div>
              <div class="hp-how-step">
                <div class="hp-how-num">03</div>
                <div class="hp-how-icon"><i class="fas fa-robot"></i></div>
                <h4>Act with AIRE agents</h4>
                <p>AIRE Agentic Mesh&trade; autonomously remediates findings, captures evidence, routes tasks to owners, and closes compliance gaps in real time without manual effort.</p>
              </div>
            </div>
          </div>
        </section>

        <!-- ═══════════════════════ DATA SOVEREIGNTY ═══════════════════════ -->
        <section class="hp-deploy-section">
          <div class="auto-container">
            <div class="hp-deploy-inner">
              <div class="hp-deploy-copy">
                <div class="hp-section-label">Data Sovereignty</div>
                <h2 class="hp-h2">Your findings never leave<br><span class="hp-hero-gradient">your environment.</span></h2>
                <p class="hp-sub">Unlike cloud-native SaaS tools that ingest your security findings into their infrastructure, AiVRIC deploys directly into your Kubernetes cluster. You own the data, the encryption keys, and the compute.</p>
                <div class="hp-deploy-opts">
                  <div class="hp-deploy-opt">
                    <div class="hp-do-icon"><i class="fas fa-cloud-download-alt"></i></div>
                    <div>
                      <strong>Customer-hosted SaaS</strong>
                      <span>Full AiVRIC stack in your Kubernetes environment. Managed updates, your data stays sovereign.</span>
                    </div>
                  </div>
                  <div class="hp-deploy-opt">
                    <div class="hp-do-icon"><i class="fas fa-globe"></i></div>
                    <div>
                      <strong>AiVRIC Online SaaS</strong>
                      <span>Hosted by AiVRIC with SOC 2 compliance, strict data isolation, and zero cross-tenant exposure.</span>
                    </div>
                  </div>
                  <div class="hp-deploy-opt">
                    <div class="hp-do-icon"><i class="fas fa-download"></i></div>
                    <div>
                      <strong>Downloadable Executable</strong>
                      <span>Run scans directly from your terminal for air-gapped, edge, and offline environments.</span>
                    </div>
                  </div>
                </div>
                <a href="why-aivric.html" class="hp-btn-primary">Why AiVRIC for data sovereignty</a>
              </div>
              <div class="hp-deploy-visual">
                <div class="hp-dv-card">
                  <div class="hp-dv-hdr">YOUR KUBERNETES CLUSTER</div>
                  <div class="hp-dv-body">
                    <div class="hp-dv-pod"><i class="fas fa-cube"></i>&nbsp; aivric-api</div>
                    <div class="hp-dv-pod"><i class="fas fa-cube"></i>&nbsp; cloudsignals-scanner</div>
                    <div class="hp-dv-pod"><i class="fas fa-cube"></i>&nbsp; aire-agent-mesh</div>
                    <div class="hp-dv-pod"><i class="fas fa-cube"></i>&nbsp; compliance-engine</div>
                    <div class="hp-dv-pod hp-dv-db"><i class="fas fa-database"></i>&nbsp; private-datastore</div>
                  </div>
                  <div class="hp-dv-foot"><i class="fas fa-lock"></i> Your data. Your keys. Your cluster.</div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- ═══════════════════════ BLOG ═══════════════════════ -->
        <section class="hp-blog-section">
          <div class="auto-container">
            <div class="hp-section-label-c">AiVRIC Insights</div>
            <h2 class="hp-h2 centred">Stay ahead of the threat<br><span class="hp-hero-gradient">with expert intelligence.</span></h2>
            <div class="hp-blog-grid">
              <a href="blog-future-of-cloud-security.html" class="hp-blog-card">
                <div class="hp-blog-img" style="background-image:url(assets/images/app/VISION-Chat-QandA.jpg)"></div>
                <div class="hp-blog-body">
                  <span class="hp-blog-tag">Cloud Security</span>
                  <h4>AI-Powered Compliance: The Future of Cloud Security</h4>
                  <p>How AI is transforming compliance, managing risk, and optimizing cloud environments at enterprise scale.</p>
                  <span class="hp-blog-read">Read article <i class="fas fa-arrow-right"></i></span>
                </div>
              </a>
              <a href="blog-integrating-into-DevOps.html" class="hp-blog-card">
                <div class="hp-blog-img" style="background-image:url(assets/images/app/Service-watchlist-LineGraph-1.jpg)"></div>
                <div class="hp-blog-body">
                  <span class="hp-blog-tag">DevSecOps</span>
                  <h4>Integrating Security Automation into DevOps</h4>
                  <p>Seamless security automation that accelerates pipelines and ensures compliance from code to cloud.</p>
                  <span class="hp-blog-read">Read article <i class="fas fa-arrow-right"></i></span>
                </div>
              </a>
              <a href="blog-why-continuous-compliance-matters.html" class="hp-blog-card">
                <div class="hp-blog-img" style="background-image:url(assets/images/app/Compliance-HIPPA-Chart.jpg)"></div>
                <div class="hp-blog-body">
                  <span class="hp-blog-tag">GRC</span>
                  <h4>Why Continuous Compliance Matters in 2025</h4>
                  <p>The importance of ongoing compliance monitoring and staying audit-ready year-round.</p>
                  <span class="hp-blog-read">Read article <i class="fas fa-arrow-right"></i></span>
                </div>
              </a>
            </div>
          </div>
        </section>

        <!-- ═══════════════════════ FINAL CTA ═══════════════════════ -->
        <section class="hp-final-cta">
          <div class="hp-cta-grid"></div>
          <div class="hp-cta-glow"></div>
          <div class="auto-container">
            <div class="hp-cta-inner">
              <span class="hp-avail-dot hp-dot-lg"></span>
              <h2 class="hp-cta-h2">Ready to govern risk<br><span class="hp-hero-gradient">at the speed of AI?</span></h2>
              <p class="hp-cta-sub">CloudSignals+RiskOps is live and deployable in your environment today. Start with a personalized walkthrough &mdash; no pressure, no commitment required.</p>
              <div class="hp-cta-actions">
                <a href="https://calendly.com/aivric-sales/aivric-walkthrough-demo" class="hp-btn-primary hp-btn-xl">Book a walkthrough demo</a>
                <a href="cspm-cloudsignals.html" class="hp-btn-ghost">Explore the platform <i class="fas fa-arrow-right"></i></a>
              </div>
              <div class="hp-cta-chips">
                <span><i class="fas fa-check-circle"></i> No credit card required</span>
                <span><i class="fas fa-check-circle"></i> Deploys in your environment</span>
                <span><i class="fas fa-check-circle"></i> Full platform access on day one</span>
              </div>
            </div>
          </div>
        </section>

"""

# ── Inject CSS into <head> ─────────────────────────────────────────────────────
if 'id="hp-styles"' not in HEAD:
    HEAD = HEAD.replace("</head>", HP_CSS + "\n</head>", 1)

# ── Assemble ─────────────────────────────────────────────────────────────────
NEW_RAW = HEAD + NEW_BODY + "\n        " + TAIL

INDEX.write_text(NEW_RAW, encoding="utf-8")
print(f"[OK] index.html written — {len(NEW_RAW)} chars")
print("[OK] New sections: Hero | Ticker | CS Spotlight | Vision Architecture | Suites | Stats | How It Works | Data Sovereignty | Blog | Final CTA")
