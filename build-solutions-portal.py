#!/usr/bin/env python3
"""
AiVRIC Solutions Portal — Full Re-imagination
Replaces body content between mobile-menu-end and footer with a dark,
animated, market-leading all-products page matching the hp- design system.
"""
from pathlib import Path
import re as _re

SITE  = Path(r"C:\Projects\AiVRIC-Website")
PAGE  = SITE / "solutions-portal.html"

raw = PAGE.read_text(encoding="utf-8", errors="replace")

FOOTER_ANCHOR  = "        <!-- main-footer -->"
MOBILE_END_TAG = "<!-- End Mobile Menu -->"

mobile_end = raw.find(MOBILE_END_TAG)
assert mobile_end != -1, "Mobile Menu end not found"
bi = raw.find("\n", mobile_end) + 1
while bi < len(raw) and raw[bi] in (" ", "\n", "\r", "\t"):
    bi += 1
bi = raw.rfind("\n", 0, bi) + 1

fi = raw.find(FOOTER_ANCHOR)
assert fi != -1, "Footer anchor not found"

HEAD = raw[:bi]
TAIL = raw[fi:]

# ── Inline CSS ────────────────────────────────────────────────────────────────
SP_CSS = """
<style id="sp-styles">
/* ── tokens ── */
:root{
  --sp-bg:#080f1c;--sp-bg2:#0d1829;--sp-bg3:#060d18;
  --sp-cyan:#00d1ff;--sp-green:#2ee59d;--sp-gold:#ffd63a;
  --sp-purp:#a78bfa;--sp-red:#f87171;--sp-amber:#fb923c;
  --sp-text:#e2e8f0;--sp-muted:#94a3b8;
  --sp-bdr-c:rgba(0,209,255,0.12);
  --sp-bdr-r:rgba(248,113,113,0.14);
  --sp-bdr-v:rgba(255,214,58,0.14);
}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.001ms!important;transition-duration:.001ms!important}}

/* ── shared ── */
.sp-grad-def{background:linear-gradient(90deg,var(--sp-cyan),var(--sp-green));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.sp-grad-off{background:linear-gradient(90deg,var(--sp-red),var(--sp-amber));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.sp-grad-vis{background:linear-gradient(90deg,var(--sp-gold),var(--sp-purp));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
@keyframes sp-blink{0%,100%{opacity:1}50%{opacity:.35}}
@keyframes sp-scan{0%{top:0;opacity:0}4%{opacity:.9}96%{opacity:.9}100%{top:100%;opacity:0}}
@keyframes sp-grid{0%,100%{opacity:.3}50%{opacity:.75}}
@keyframes sp-float{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}
@keyframes sp-pulse{0%,100%{opacity:.5;transform:scale(1)}50%{opacity:1;transform:scale(1.04)}}
.sp-dot-live{width:7px;height:7px;border-radius:50%;background:var(--sp-green);box-shadow:0 0 7px var(--sp-green);display:inline-block;animation:sp-blink 2s ease-in-out infinite}

/* ═══ HERO ═══ */
.sp-hero{position:relative;background:var(--sp-bg);overflow:hidden;padding:120px 0 80px}
.sp-hero-grid{position:absolute;inset:0;background-image:linear-gradient(rgba(0,209,255,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(0,209,255,.03) 1px,transparent 1px);background-size:64px 64px;animation:sp-grid 10s ease-in-out infinite;pointer-events:none}
.sp-hero-scan{position:absolute;left:0;right:0;height:1.5px;background:linear-gradient(90deg,transparent,rgba(0,209,255,.7) 50%,transparent);top:0;animation:sp-scan 9s linear infinite;pointer-events:none;z-index:1}
.sp-hero-glow{position:absolute;border-radius:50%;pointer-events:none;width:800px;height:500px;background:radial-gradient(ellipse,rgba(0,209,255,.06) 0%,transparent 70%);left:50%;top:50%;transform:translate(-50%,-50%);animation:sp-pulse 7s ease-in-out infinite}
.sp-hero-inner{position:relative;z-index:2;text-align:center;max-width:820px;margin:0 auto}
.sp-hero-label{display:inline-flex;align-items:center;gap:7px;font-size:11px;font-weight:800;letter-spacing:2.5px;text-transform:uppercase;color:var(--sp-cyan);margin-bottom:20px;background:rgba(0,209,255,.07);border:1px solid rgba(0,209,255,.18);border-radius:100px;padding:6px 18px}
.sp-hero-label i{font-size:10px}
.sp-h1{font-family:'Jost',sans-serif;font-size:clamp(36px,5vw,62px);font-weight:900;line-height:1.1;color:#f0f8ff;margin-bottom:22px}
.sp-hero-sub{font-size:17px;line-height:1.75;color:var(--sp-muted);margin-bottom:44px;max-width:640px;margin-left:auto;margin-right:auto}

/* suite pills */
.sp-suite-pills{display:flex;flex-wrap:wrap;gap:12px;justify-content:center}
.sp-suite-pill{display:inline-flex;align-items:center;gap:8px;padding:12px 22px;border-radius:100px;font-size:14px;font-weight:700;text-decoration:none;transition:all .2s;border:1px solid}
.sp-pill-def{background:rgba(0,209,255,.07);border-color:rgba(0,209,255,.25);color:var(--sp-cyan)}
.sp-pill-off{background:rgba(248,113,113,.06);border-color:rgba(248,113,113,.2);color:var(--sp-red)}
.sp-pill-vis{background:rgba(255,214,58,.06);border-color:rgba(255,214,58,.2);color:var(--sp-gold)}
.sp-suite-pill:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.3)}
.sp-pill-def:hover{background:rgba(0,209,255,.13);border-color:var(--sp-cyan);color:var(--sp-cyan)}
.sp-pill-off:hover{background:rgba(248,113,113,.12);border-color:var(--sp-red);color:var(--sp-red)}
.sp-pill-vis:hover{background:rgba(255,214,58,.12);border-color:var(--sp-gold);color:var(--sp-gold)}
.sp-pill-count{font-size:11px;font-weight:600;opacity:.75;margin-left:2px}
.sp-suite-pill-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.sp-dot-def{background:var(--sp-cyan);box-shadow:0 0 6px var(--sp-cyan)}
.sp-dot-off{background:var(--sp-red);box-shadow:0 0 6px var(--sp-red)}
.sp-dot-vis{background:var(--sp-gold);box-shadow:0 0 6px var(--sp-gold)}

/* ═══ HOW THEY CONNECT ═══ */
.sp-connect-section{background:var(--sp-bg2);padding:70px 0;border-top:1px solid rgba(255,255,255,.04)}
.sp-connect-inner{display:flex;align-items:stretch;gap:0;max-width:860px;margin:0 auto}
.sp-connect-card{flex:1;text-align:center;padding:32px 24px;background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.07);border-radius:16px;display:flex;flex-direction:column;align-items:center;gap:14px}
.sp-connect-icon{width:52px;height:52px;border-radius:13px;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.sp-ci-def{background:rgba(0,209,255,.12);border:1px solid rgba(0,209,255,.2)}.sp-ci-def i{color:var(--sp-cyan);font-size:22px}
.sp-ci-off{background:rgba(248,113,113,.1);border:1px solid rgba(248,113,113,.2)}.sp-ci-off i{color:var(--sp-red);font-size:22px}
.sp-ci-vis{background:rgba(255,214,58,.1);border:1px solid rgba(255,214,58,.2)}.sp-ci-vis i{color:var(--sp-gold);font-size:22px}
.sp-connect-card h4{font-size:16px;font-weight:800;color:#e2e8f0;font-family:'Jost',sans-serif;margin:0}
.sp-connect-card p{font-size:13px;color:var(--sp-muted);line-height:1.6;margin:0;flex:1}
.sp-connect-arrow{display:flex;align-items:center;padding:0 10px;color:rgba(0,209,255,.25);font-size:20px;flex-shrink:0}
@media(max-width:768px){.sp-connect-inner{flex-direction:column}.sp-connect-arrow{transform:rotate(90deg)}}

/* ═══ SUITE SECTIONS ═══ */
.sp-suite-section{background:var(--sp-bg)}
.sp-suite-section:nth-child(even){background:var(--sp-bg2)}

.sp-suite-hdr{padding:64px 0 0}
.sp-suite-hdr-band{padding:22px 0;margin-bottom:0}
.sp-suite-hdr-inner{display:flex;align-items:flex-start;justify-content:space-between;gap:24px;flex-wrap:wrap;margin-bottom:16px}
.sp-suite-hdr-left{display:flex;align-items:center;gap:18px}
.sp-suite-icon{width:54px;height:54px;border-radius:14px;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.sp-si-def{background:rgba(0,209,255,.12);border:1px solid rgba(0,209,255,.22)}.sp-si-def i{color:var(--sp-cyan);font-size:24px}
.sp-si-off{background:rgba(248,113,113,.1);border:1px solid rgba(248,113,113,.2)}.sp-si-off i{color:var(--sp-red);font-size:24px}
.sp-si-vis{background:rgba(255,214,58,.1);border:1px solid rgba(255,214,58,.2)}.sp-si-vis i{color:var(--sp-gold);font-size:24px}
.sp-suite-kicker{font-size:10px;font-weight:800;letter-spacing:2px;text-transform:uppercase;margin-bottom:5px}
.sp-kicker-def{color:var(--sp-cyan)}.sp-kicker-off{color:var(--sp-red)}.sp-kicker-vis{color:var(--sp-gold)}
.sp-suite-hdr h2{font-family:'Jost',sans-serif;font-size:clamp(22px,3vw,34px);font-weight:800;color:#f0f8ff;margin:0;line-height:1.15}
.sp-suite-hdr-right{display:flex;align-items:center;gap:16px;flex-shrink:0}
.sp-suite-count{text-align:center;padding:12px 20px;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);border-radius:10px}
.sp-suite-count-n{display:block;font-family:'Jost',sans-serif;font-size:28px;font-weight:900;line-height:1;color:#f0f8ff}
.sp-suite-count-l{font-size:10px;color:var(--sp-muted);letter-spacing:.5px}
.sp-btn-def{display:inline-flex;align-items:center;gap:7px;padding:12px 22px;border-radius:8px;font-size:13px;font-weight:700;background:var(--sp-cyan);color:#050c18;text-decoration:none;transition:all .2s;white-space:nowrap}
.sp-btn-def:hover{background:#00e8ff;color:#050c18;transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,209,255,.3)}
.sp-btn-off{display:inline-flex;align-items:center;gap:7px;padding:12px 22px;border-radius:8px;font-size:13px;font-weight:700;background:var(--sp-red);color:#fff;text-decoration:none;transition:all .2s;white-space:nowrap}
.sp-btn-off:hover{background:#ff8888;color:#fff;transform:translateY(-2px);box-shadow:0 8px 24px rgba(248,113,113,.3)}
.sp-btn-vis{display:inline-flex;align-items:center;gap:7px;padding:12px 22px;border-radius:8px;font-size:13px;font-weight:700;background:linear-gradient(135deg,var(--sp-gold),var(--sp-purp));color:#070e1a;text-decoration:none;transition:all .2s;white-space:nowrap}
.sp-btn-vis:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(167,139,250,.3);color:#070e1a}

.sp-suite-desc{font-size:15px;color:var(--sp-muted);line-height:1.7;margin-bottom:24px;max-width:680px}
.sp-suite-rule{height:1px;background:rgba(255,255,255,.06);margin:0 0 28px}
.sp-highlights{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:0}
.sp-highlight{display:inline-flex;align-items:center;gap:7px;font-size:12.5px;color:#cbd5e1;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);border-radius:7px;padding:7px 13px}
.sp-highlight-def i{color:var(--sp-cyan);font-size:11px}
.sp-highlight-off i{color:var(--sp-amber);font-size:11px}
.sp-highlight-vis i{color:var(--sp-gold);font-size:11px}

/* ═══ PRODUCT GRID ═══ */
.sp-product-body{padding:32px 0 72px}
.sp-product-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
@media(max-width:991px){.sp-product-grid{grid-template-columns:1fr 1fr}}
@media(max-width:600px){.sp-product-grid{grid-template-columns:1fr}}

.sp-product-card{background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.07);border-radius:16px;padding:28px;display:flex;flex-direction:column;gap:16px;position:relative;overflow:hidden;transition:all .25s}
.sp-product-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px}
.sp-pc-def::before{background:linear-gradient(90deg,var(--sp-cyan),var(--sp-green))}
.sp-pc-off::before{background:linear-gradient(90deg,var(--sp-red),var(--sp-amber))}
.sp-pc-vis::before{background:linear-gradient(90deg,var(--sp-gold),var(--sp-purp))}
.sp-product-card:hover{transform:translateY(-4px);box-shadow:0 20px 52px rgba(0,0,0,.45)}
.sp-pc-def:hover{border-color:rgba(0,209,255,.18);background:rgba(0,209,255,.03)}
.sp-pc-off:hover{border-color:rgba(248,113,113,.16);background:rgba(248,113,113,.03)}
.sp-pc-vis:hover{border-color:rgba(255,214,58,.16);background:rgba(255,214,58,.03)}

.sp-pc-top{display:flex;align-items:center;justify-content:space-between;gap:10px}
.sp-pc-icon{width:44px;height:44px;border-radius:11px;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.sp-pi-def{background:rgba(0,209,255,.12);border:1px solid rgba(0,209,255,.2)}.sp-pi-def i{color:var(--sp-cyan);font-size:18px}
.sp-pi-off{background:rgba(248,113,113,.1);border:1px solid rgba(248,113,113,.18)}.sp-pi-off i{color:var(--sp-red);font-size:18px}
.sp-pi-vis{background:rgba(255,214,58,.1);border:1px solid rgba(255,214,58,.18)}.sp-pi-vis i{color:var(--sp-gold);font-size:18px}
.sp-pc-badges{display:flex;flex-wrap:wrap;gap:5px;justify-content:flex-end}
.sp-badge{font-size:9px;font-weight:800;letter-spacing:.8px;padding:3px 8px;border-radius:4px}
.sp-badge-live{background:rgba(46,229,157,.13);color:var(--sp-green);border:1px solid rgba(46,229,157,.25)}
.sp-badge-road{background:rgba(148,163,184,.08);color:var(--sp-muted);border:1px solid rgba(148,163,184,.15)}
.sp-badge-def{background:rgba(0,209,255,.08);color:var(--sp-cyan);border:1px solid rgba(0,209,255,.15)}
.sp-badge-off{background:rgba(248,113,113,.08);color:var(--sp-red);border:1px solid rgba(248,113,113,.15)}
.sp-badge-vis{background:rgba(255,214,58,.08);color:var(--sp-gold);border:1px solid rgba(255,214,58,.15)}

.sp-pc-name{font-family:'Jost',sans-serif;font-size:17px;font-weight:800;color:#f0f8ff;margin:0;line-height:1.25}
.sp-pc-desc{font-size:13px;color:var(--sp-muted);line-height:1.65;margin:0;flex:1}
.sp-pc-features{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:7px}
.sp-pc-features li{font-size:12.5px;color:#cbd5e1;display:flex;align-items:flex-start;gap:7px}
.sp-pc-features li i{font-size:10px;margin-top:3px;flex-shrink:0}
.sp-pc-def .sp-pc-features li i{color:var(--sp-green)}
.sp-pc-off .sp-pc-features li i{color:var(--sp-amber)}
.sp-pc-vis .sp-pc-features li i{color:var(--sp-gold)}
.sp-pc-foot{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-top:auto;padding-top:4px;border-top:1px solid rgba(255,255,255,.05)}
.sp-pc-link{font-size:13px;font-weight:700;text-decoration:none;display:inline-flex;align-items:center;gap:5px;transition:gap .15s}
.sp-pc-link i{transition:transform .15s;font-size:11px}
.sp-pc-link:hover i{transform:translateX(3px)}
.sp-pc-def .sp-pc-link{color:var(--sp-cyan)}
.sp-pc-off .sp-pc-link{color:var(--sp-amber)}
.sp-pc-vis .sp-pc-link{color:var(--sp-gold)}
.sp-pc-pricing{font-size:11.5px;font-weight:600;color:var(--sp-muted);text-decoration:none;transition:color .15s}
.sp-pc-pricing:hover{color:var(--sp-cyan)}

/* ═══ VISION PLATFORM CALLOUT ═══ */
.sp-vision-callout{background:rgba(255,214,58,.04);border:1px solid rgba(255,214,58,.12);border-radius:16px;padding:28px;margin-top:8px;display:flex;align-items:flex-start;gap:18px}
.sp-vcall-icon{width:44px;height:44px;border-radius:11px;background:rgba(255,214,58,.1);border:1px solid rgba(255,214,58,.2);display:flex;align-items:center;justify-content:center;flex-shrink:0}
.sp-vcall-icon i{color:var(--sp-gold);font-size:18px}
.sp-vcall-body strong{display:block;font-size:14px;font-weight:700;color:#e2e8f0;margin-bottom:5px}
.sp-vcall-body p{font-size:13px;color:var(--sp-muted);line-height:1.6;margin:0}

/* ═══ FINAL CTA ═══ */
.sp-final-cta{background:var(--sp-bg);padding:100px 0;text-align:center;position:relative;overflow:hidden;border-top:1px solid rgba(255,255,255,.04)}
.sp-cta-grid{position:absolute;inset:0;background-image:linear-gradient(rgba(0,209,255,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(0,209,255,.04) 1px,transparent 1px);background-size:64px 64px;animation:sp-grid 9s ease-in-out infinite;pointer-events:none}
.sp-cta-glow{position:absolute;width:900px;height:400px;border-radius:50%;background:radial-gradient(ellipse,rgba(0,209,255,.07) 0%,transparent 70%);left:50%;top:50%;transform:translate(-50%,-50%);pointer-events:none}
.sp-cta-inner{position:relative;z-index:2}
.sp-cta-h2{font-family:'Jost',sans-serif;font-size:clamp(30px,4vw,50px);font-weight:900;color:#f0f8ff;margin:14px 0 18px;line-height:1.12}
.sp-cta-sub{font-size:16px;color:var(--sp-muted);max-width:540px;line-height:1.75;margin:0 auto 32px}
.sp-cta-actions{display:flex;gap:14px;flex-wrap:wrap;justify-content:center}
.sp-btn-primary{display:inline-flex;align-items:center;gap:8px;padding:14px 30px;border-radius:8px;font-size:15px;font-weight:700;background:var(--sp-cyan);color:#050c18;text-decoration:none;transition:all .2s}
.sp-btn-primary:hover{background:#00e8ff;color:#050c18;transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,209,255,.35)}
.sp-btn-ghost{display:inline-flex;align-items:center;gap:8px;padding:14px 30px;border-radius:8px;font-size:15px;font-weight:600;border:1px solid rgba(0,209,255,.3);color:var(--sp-cyan);text-decoration:none;transition:all .2s}
.sp-btn-ghost:hover{background:rgba(0,209,255,.08);border-color:var(--sp-cyan);transform:translateY(-2px)}
</style>"""

# ── Body content ──────────────────────────────────────────────────────────────
NEW_BODY = r"""
        <!-- ═══ PAGE HERO ═══ -->
        <section class="sp-hero">
          <div class="sp-hero-grid"></div>
          <div class="sp-hero-scan"></div>
          <div class="sp-hero-glow"></div>
          <div class="auto-container">
            <div class="sp-hero-inner">
              <div class="sp-hero-label"><i class="fas fa-th"></i> All Products</div>
              <h1 class="sp-h1">Three suites.<br><span class="sp-grad-def">One unified platform.</span></h1>
              <p class="sp-hero-sub">CloudSignals+RiskOps is live today. Offense and Vision bring autonomous attack simulation and cross-suite intelligence. Together they form the complete AiVRIC security operations stack &mdash; all sharing one data layer.</p>
              <div class="sp-suite-pills">
                <a href="#defense" class="sp-suite-pill sp-pill-def">
                  <span class="sp-suite-pill-dot sp-dot-def"></span>
                  Defense Suite
                  <span class="sp-pill-count">&middot; 3 products</span>
                </a>
                <a href="#offense" class="sp-suite-pill sp-pill-off">
                  <span class="sp-suite-pill-dot sp-dot-off"></span>
                  Offense Suite
                  <span class="sp-pill-count">&middot; 3 products</span>
                </a>
                <a href="#vision" class="sp-suite-pill sp-pill-vis">
                  <span class="sp-suite-pill-dot sp-dot-vis"></span>
                  Vision Suite
                  <span class="sp-pill-count">&middot; 3 products</span>
                </a>
              </div>
            </div>
          </div>
        </section>

        <!-- ═══ HOW THEY CONNECT ═══ -->
        <section class="sp-connect-section">
          <div class="auto-container">
            <div class="sp-connect-inner">
              <div class="sp-connect-card">
                <div class="sp-connect-icon sp-ci-def"><i class="fas fa-shield-alt"></i></div>
                <h4><span class="sp-grad-def">Defense</span></h4>
                <p>Detect misconfigurations, evaluate AI systems, and enforce continuous compliance across your cloud and infrastructure.</p>
              </div>
              <div class="sp-connect-arrow"><i class="fas fa-arrow-right"></i></div>
              <div class="sp-connect-card">
                <div class="sp-connect-icon sp-ci-off"><i class="fas fa-crosshairs"></i></div>
                <h4><span class="sp-grad-off">Offense</span></h4>
                <p>Continuously simulate adversary attacks to validate controls, discover exposure, and surface risks before attackers find them.</p>
              </div>
              <div class="sp-connect-arrow"><i class="fas fa-arrow-right"></i></div>
              <div class="sp-connect-card">
                <div class="sp-connect-icon sp-ci-vis"><i class="fas fa-eye"></i></div>
                <h4><span class="sp-grad-vis">Vision</span></h4>
                <p>Aggregate Defense and Offense signal into unified dashboards, AI chat, and executive intelligence with one data truth.</p>
              </div>
            </div>
          </div>
        </section>

        <!-- ═══ DEFENSE SUITE ═══ -->
        <section id="defense" class="sp-suite-section">
          <div class="sp-suite-hdr">
            <div class="auto-container">
              <div class="sp-suite-hdr-inner">
                <div class="sp-suite-hdr-left">
                  <div class="sp-suite-icon sp-si-def"><i class="fas fa-shield-alt"></i></div>
                  <div>
                    <div class="sp-suite-kicker sp-kicker-def">Defense Suite</div>
                    <h2 class="sp-suite-hdr h2">Protect cloud, AI &amp; enterprise infrastructure</h2>
                  </div>
                </div>
                <div class="sp-suite-hdr-right">
                  <div class="sp-suite-count">
                    <span class="sp-suite-count-n">3</span>
                    <span class="sp-suite-count-l">Products</span>
                  </div>
                  <a href="defense-suite.html" class="sp-btn-def">Explore Suite <i class="fas fa-arrow-right"></i></a>
                </div>
              </div>
              <p class="sp-suite-desc">Continuous posture management, AI evaluations, and agentic remediation for regulated enterprises. From misconfiguration detection to automated fix &mdash; all with evidence mapped to your compliance frameworks.</p>
              <div class="sp-suite-rule"></div>
              <div class="sp-highlights">
                <div class="sp-highlight sp-highlight-def"><i class="fas fa-check"></i><span>Unified evidence for SOC 2, ISO 27001, PCI-DSS, CMMC, HIPAA</span></div>
                <div class="sp-highlight sp-highlight-def"><i class="fas fa-check"></i><span>Agent-driven remediation with approvals and audit trails</span></div>
                <div class="sp-highlight sp-highlight-def"><i class="fas fa-check"></i><span>SaaS, customer-hosted SaaS, or executable deployment</span></div>
                <div class="sp-highlight sp-highlight-def"><i class="fas fa-check"></i><span>AWS, Azure, GCP, OCI coverage</span></div>
              </div>
            </div>
          </div>
          <div class="sp-product-body">
            <div class="auto-container">
              <div class="sp-product-grid">

                <div class="sp-product-card sp-pc-def">
                  <div class="sp-pc-top">
                    <div class="sp-pc-icon sp-pi-def"><i class="fas fa-cloud"></i></div>
                    <div class="sp-pc-badges">
                      <span class="sp-badge sp-badge-live"><span class="sp-dot-live" style="width:5px;height:5px;margin-right:3px;display:inline-block;border-radius:50%;background:#2ee59d;vertical-align:middle"></span>LIVE</span>
                      <span class="sp-badge sp-badge-def">Defense</span>
                    </div>
                  </div>
                  <h3 class="sp-pc-name">CloudSignals+ RiskOps&trade;</h3>
                  <p class="sp-pc-desc">AI-native cloud security posture, risk operations, and continuous compliance across AWS, Azure, GCP, and OCI.</p>
                  <ul class="sp-pc-features">
                    <li><i class="fas fa-check-circle"></i>Real-time misconfiguration detection</li>
                    <li><i class="fas fa-check-circle"></i>GRC-grade risk register &amp; RiskOps</li>
                    <li><i class="fas fa-check-circle"></i>Continuous compliance with evidence packs</li>
                    <li><i class="fas fa-check-circle"></i>Third-party risk (TPRM) management</li>
                  </ul>
                  <div class="sp-pc-foot">
                    <a href="cspm-cloudsignals.html" class="sp-pc-link">View product details <i class="fas fa-arrow-right"></i></a>
                    <a href="cloudsignals-pricing.html" class="sp-pc-pricing">Compare pricing</a>
                  </div>
                </div>

                <div class="sp-product-card sp-pc-def">
                  <div class="sp-pc-top">
                    <div class="sp-pc-icon sp-pi-def"><i class="fas fa-satellite-dish"></i></div>
                    <div class="sp-pc-badges">
                      <span class="sp-badge sp-badge-live"><span style="width:5px;height:5px;margin-right:3px;display:inline-block;border-radius:50%;background:#2ee59d;vertical-align:middle"></span>LIVE</span>
                      <span class="sp-badge sp-badge-def">Defense</span>
                    </div>
                  </div>
                  <h3 class="sp-pc-name">AI Signals&trade;</h3>
                  <p class="sp-pc-desc">LLM observability, evaluations, and prompt management for production AI applications. Security and compliance for AI.</p>
                  <ul class="sp-pc-features">
                    <li><i class="fas fa-check-circle"></i>OTEL-native LLM signal collection</li>
                    <li><i class="fas fa-check-circle"></i>Repeatable AI control testing &amp; evals</li>
                    <li><i class="fas fa-check-circle"></i>Governance-ready compliance reporting</li>
                  </ul>
                  <div class="sp-pc-foot">
                    <a href="ai-inspector.html" class="sp-pc-link">View product details <i class="fas fa-arrow-right"></i></a>
                  </div>
                </div>

                <div class="sp-product-card sp-pc-def">
                  <div class="sp-pc-top">
                    <div class="sp-pc-icon sp-pi-def"><i class="fas fa-robot"></i></div>
                    <div class="sp-pc-badges">
                      <span class="sp-badge sp-badge-road">ROADMAP</span>
                      <span class="sp-badge sp-badge-def">Defense</span>
                    </div>
                  </div>
                  <h3 class="sp-pc-name">AIRE Agentic Mesh&trade;</h3>
                  <p class="sp-pc-desc">Role-aware remediation agents that detect misconfigurations, execute approved fixes, and verify outcomes end-to-end.</p>
                  <ul class="sp-pc-features">
                    <li><i class="fas fa-check-circle"></i>Automated remediation workflows</li>
                    <li><i class="fas fa-check-circle"></i>Role-based approval gates</li>
                    <li><i class="fas fa-check-circle"></i>Audit-ready verification logs</li>
                  </ul>
                  <div class="sp-pc-foot">
                    <a href="air-remediation.html" class="sp-pc-link">View product details <i class="fas fa-arrow-right"></i></a>
                  </div>
                </div>

              </div>
            </div>
          </div>
        </section>

        <!-- ═══ OFFENSE SUITE ═══ -->
        <section id="offense" class="sp-suite-section" style="background:var(--sp-bg2)">
          <div class="sp-suite-hdr">
            <div class="auto-container">
              <div class="sp-suite-hdr-inner">
                <div class="sp-suite-hdr-left">
                  <div class="sp-suite-icon sp-si-off"><i class="fas fa-crosshairs"></i></div>
                  <div>
                    <div class="sp-suite-kicker sp-kicker-off">Offense Suite</div>
                    <h2 class="sp-suite-hdr h2">Simulate attacks and expose digital risk</h2>
                  </div>
                </div>
                <div class="sp-suite-hdr-right">
                  <div class="sp-suite-count">
                    <span class="sp-suite-count-n">3</span>
                    <span class="sp-suite-count-l">Products</span>
                  </div>
                  <a href="offense-suite.html" class="sp-btn-off">Explore Suite <i class="fas fa-arrow-right"></i></a>
                </div>
              </div>
              <p class="sp-suite-desc">Proactive attack simulation and exposure management for continuous control validation. Know your attack surface before adversaries do.</p>
              <div class="sp-suite-rule"></div>
              <div class="sp-highlights">
                <div class="sp-highlight sp-highlight-off"><i class="fas fa-check"></i><span>Continuous attack simulation for risk validation</span></div>
                <div class="sp-highlight sp-highlight-off"><i class="fas fa-check"></i><span>Prioritized exposure reporting for executives</span></div>
                <div class="sp-highlight sp-highlight-off"><i class="fas fa-check"></i><span>SIEM, ITSM, and cloud tool integrations</span></div>
                <div class="sp-highlight sp-highlight-off"><i class="fas fa-check"></i><span>MITRE ATT&amp;CK-aligned scenario coverage</span></div>
              </div>
            </div>
          </div>
          <div class="sp-product-body">
            <div class="auto-container">
              <div class="sp-product-grid">

                <div class="sp-product-card sp-pc-off">
                  <div class="sp-pc-top">
                    <div class="sp-pc-icon sp-pi-off"><i class="fas fa-bug"></i></div>
                    <div class="sp-pc-badges">
                      <span class="sp-badge sp-badge-road">ROADMAP</span>
                      <span class="sp-badge sp-badge-off">Offense</span>
                    </div>
                  </div>
                  <h3 class="sp-pc-name">RogueAgent ASPM&trade;</h3>
                  <p class="sp-pc-desc">Attack surface and posture management with continuous risk scoring. Discover, map, and prioritize external exposure across environments.</p>
                  <ul class="sp-pc-features">
                    <li><i class="fas fa-check-circle"></i>Risk-ranked exposure mapping</li>
                    <li><i class="fas fa-check-circle"></i>Asset discovery across cloud &amp; on-prem</li>
                    <li><i class="fas fa-check-circle"></i>Continuous posture drift alerting</li>
                  </ul>
                  <div class="sp-pc-foot">
                    <a href="rogueagent.html" class="sp-pc-link">View product details <i class="fas fa-arrow-right"></i></a>
                  </div>
                </div>

                <div class="sp-product-card sp-pc-off">
                  <div class="sp-pc-top">
                    <div class="sp-pc-icon sp-pi-off"><i class="fas fa-user-secret"></i></div>
                    <div class="sp-pc-badges">
                      <span class="sp-badge sp-badge-road">ROADMAP</span>
                      <span class="sp-badge sp-badge-off">Offense</span>
                    </div>
                  </div>
                  <h3 class="sp-pc-name">Red Teaming Scans</h3>
                  <p class="sp-pc-desc">Continuous adversary simulation with MITRE ATT&amp;CK-aligned scenarios. Validate defenses before the real thing.</p>
                  <ul class="sp-pc-features">
                    <li><i class="fas fa-check-circle"></i>Control verification at scale</li>
                    <li><i class="fas fa-check-circle"></i>Executive-ready attack reports</li>
                    <li><i class="fas fa-check-circle"></i>MITRE ATT&amp;CK scenario library</li>
                  </ul>
                  <div class="sp-pc-foot">
                    <a href="red-teaming.html" class="sp-pc-link">View product details <i class="fas fa-arrow-right"></i></a>
                  </div>
                </div>

                <div class="sp-product-card sp-pc-off">
                  <div class="sp-pc-top">
                    <div class="sp-pc-icon sp-pi-off"><i class="fas fa-globe"></i></div>
                    <div class="sp-pc-badges">
                      <span class="sp-badge sp-badge-road">ROADMAP</span>
                      <span class="sp-badge sp-badge-off">Offense</span>
                    </div>
                  </div>
                  <h3 class="sp-pc-name">Digital Risk Monitoring</h3>
                  <p class="sp-pc-desc">Track external threats, leaked credentials, brand exposure, and supply chain risk before they escalate.</p>
                  <ul class="sp-pc-features">
                    <li><i class="fas fa-check-circle"></i>Dark web &amp; leaked asset monitoring</li>
                    <li><i class="fas fa-check-circle"></i>Early-warning risk intelligence</li>
                    <li><i class="fas fa-check-circle"></i>Actionable remediation paths</li>
                  </ul>
                  <div class="sp-pc-foot">
                    <a href="digital-risk.html" class="sp-pc-link">View product details <i class="fas fa-arrow-right"></i></a>
                  </div>
                </div>

              </div>
            </div>
          </div>
        </section>

        <!-- ═══ VISION SUITE ═══ -->
        <section id="vision" class="sp-suite-section">
          <div class="sp-suite-hdr">
            <div class="auto-container">
              <div class="sp-suite-hdr-inner">
                <div class="sp-suite-hdr-left">
                  <div class="sp-suite-icon sp-si-vis"><i class="fas fa-eye"></i></div>
                  <div>
                    <div class="sp-suite-kicker sp-kicker-vis">Vision Suite</div>
                    <h2 class="sp-suite-hdr h2">Unified intelligence for every decision</h2>
                  </div>
                </div>
                <div class="sp-suite-hdr-right">
                  <div class="sp-suite-count">
                    <span class="sp-suite-count-n">3</span>
                    <span class="sp-suite-count-l">Products</span>
                  </div>
                  <a href="vision-suite.html" class="sp-btn-vis">Explore Suite <i class="fas fa-arrow-right"></i></a>
                </div>
              </div>
              <p class="sp-suite-desc">A unified intelligence center that connects Defense and Offense signal into cross-suite dashboards, AI chat, and executive reporting &mdash; with full tenant segmentation and data sovereignty.</p>
              <div class="sp-suite-rule"></div>
              <div class="sp-highlights">
                <div class="sp-highlight sp-highlight-vis"><i class="fas fa-check"></i><span>Cross-suite dashboards and custom reporting</span></div>
                <div class="sp-highlight sp-highlight-vis"><i class="fas fa-check"></i><span>GenAI-assisted summaries and risk narratives</span></div>
                <div class="sp-highlight sp-highlight-vis"><i class="fas fa-check"></i><span>Role-based access and data localization controls</span></div>
                <div class="sp-highlight sp-highlight-vis"><i class="fas fa-check"></i><span>AIRE Agentic Mesh integration for autonomous action</span></div>
              </div>
            </div>
          </div>
          <div class="sp-product-body">
            <div class="auto-container">
              <div class="sp-product-grid">

                <div class="sp-product-card sp-pc-vis">
                  <div class="sp-pc-top">
                    <div class="sp-pc-icon sp-pi-vis"><i class="fas fa-chart-bar"></i></div>
                    <div class="sp-pc-badges">
                      <span class="sp-badge sp-badge-road">ROADMAP</span>
                      <span class="sp-badge sp-badge-vis">Vision</span>
                    </div>
                  </div>
                  <h3 class="sp-pc-name">Vision AI Optics&trade;</h3>
                  <p class="sp-pc-desc">Unified dashboards and AI-generated reports for security and compliance leaders. One view of your entire risk posture.</p>
                  <ul class="sp-pc-features">
                    <li><i class="fas fa-check-circle"></i>Pre-built executive reporting</li>
                    <li><i class="fas fa-check-circle"></i>Cross-suite posture visibility</li>
                    <li><i class="fas fa-check-circle"></i>AI-generated risk narratives</li>
                  </ul>
                  <div class="sp-pc-foot">
                    <a href="aivric-vision-professional.html" class="sp-pc-link">View product details <i class="fas fa-arrow-right"></i></a>
                  </div>
                </div>

                <div class="sp-product-card sp-pc-vis">
                  <div class="sp-pc-top">
                    <div class="sp-pc-icon sp-pi-vis"><i class="fas fa-building"></i></div>
                    <div class="sp-pc-badges">
                      <span class="sp-badge sp-badge-road">ROADMAP</span>
                      <span class="sp-badge sp-badge-vis">Vision</span>
                    </div>
                  </div>
                  <h3 class="sp-pc-name">Vision Enterprise</h3>
                  <p class="sp-pc-desc">Enterprise-scale intelligence with multi-tenant governance, custom analytics pipelines, and multi-region data controls.</p>
                  <ul class="sp-pc-features">
                    <li><i class="fas fa-check-circle"></i>Advanced reporting automation</li>
                    <li><i class="fas fa-check-circle"></i>Multi-tenant governance controls</li>
                    <li><i class="fas fa-check-circle"></i>Multi-region data residency</li>
                  </ul>
                  <div class="sp-pc-foot">
                    <a href="aivric-vision-enterprise.html" class="sp-pc-link">View product details <i class="fas fa-arrow-right"></i></a>
                  </div>
                </div>

                <div class="sp-product-card sp-pc-vis">
                  <div class="sp-pc-top">
                    <div class="sp-pc-icon sp-pi-vis"><i class="fas fa-brain"></i></div>
                    <div class="sp-pc-badges">
                      <span class="sp-badge sp-badge-road">ROADMAP</span>
                      <span class="sp-badge sp-badge-vis">Vision</span>
                    </div>
                  </div>
                  <h3 class="sp-pc-name">Fabric Intelligence Center</h3>
                  <p class="sp-pc-desc">AI chat, contextual dashboards, and on-demand intelligence reports in one command interface. Powered by AIRE Agentic Mesh.</p>
                  <ul class="sp-pc-features">
                    <li><i class="fas fa-check-circle"></i>Context-aware AI chat across all suites</li>
                    <li><i class="fas fa-check-circle"></i>Agentic task execution via AIRE</li>
                    <li><i class="fas fa-check-circle"></i>Custom intelligence views</li>
                  </ul>
                  <div class="sp-pc-foot">
                    <a href="fabric-intelligence-center.html" class="sp-pc-link">View product details <i class="fas fa-arrow-right"></i></a>
                  </div>
                </div>

              </div>

              <!-- Vision Platform Callout -->
              <div class="sp-vision-callout">
                <div class="sp-vcall-icon"><i class="fas fa-layer-group"></i></div>
                <div class="sp-vcall-body">
                  <strong>AiVRIC Vision Platform &mdash; The Shared Data Layer</strong>
                  <p>Vision is more than a suite &mdash; it&rsquo;s the unified backend that aggregates telemetry and evidence from every AiVRIC solution. With tight tenant segmentation, all products share one data truth while maintaining complete isolation per customer or business unit.</p>
                </div>
              </div>

            </div>
          </div>
        </section>

        <!-- ═══ FINAL CTA ═══ -->
        <section class="sp-final-cta">
          <div class="sp-cta-grid"></div>
          <div class="sp-cta-glow"></div>
          <div class="auto-container">
            <div class="sp-cta-inner">
              <div class="sp-hero-label" style="justify-content:center;margin-bottom:12px"><i class="fas fa-rocket"></i> Get Started</div>
              <h2 class="sp-cta-h2">Ready to see the platform<br><span class="sp-grad-def">in your environment?</span></h2>
              <p class="sp-cta-sub">CloudSignals+RiskOps is available today. Book a personalized walkthrough and we&rsquo;ll show you exactly how it maps to your cloud estate and compliance requirements.</p>
              <div class="sp-cta-actions">
                <a href="https://calendly.com/aivric-sales/aivric-walkthrough-demo" class="sp-btn-primary">Book a walkthrough demo</a>
                <a href="cspm-cloudsignals.html" class="sp-btn-ghost">Explore CloudSignals+RiskOps <i class="fas fa-arrow-right"></i></a>
              </div>
            </div>
          </div>
        </section>

"""

# ── Inject CSS into <head> ────────────────────────────────────────────────────
if 'id="sp-styles"' in HEAD:
    HEAD = _re.sub(r'\n<style id="sp-styles">.*?</style>', '', HEAD, flags=_re.DOTALL)
HEAD = HEAD.replace("</head>", SP_CSS + "\n</head>", 1)

# ── Update page title ─────────────────────────────────────────────────────────
HEAD = HEAD.replace(
    "<title>Solutions | AiVRIC</title>",
    "<title>All Products | AiVRIC Platform</title>"
)

# ── Assemble ──────────────────────────────────────────────────────────────────
NEW_RAW = HEAD + NEW_BODY + "\n        " + TAIL
PAGE.write_text(NEW_RAW, encoding="utf-8")
print(f"[OK] solutions-portal.html written — {len(NEW_RAW):,} chars")

# ── Verify ────────────────────────────────────────────────────────────────────
checks = [
    ("sp-hero",           "Hero section"),
    ("sp-suite-pills",    "Suite pills"),
    ("sp-connect-section","How They Connect"),
    ('id="defense"',      "Defense anchor"),
    ('id="offense"',      "Offense anchor"),
    ('id="vision"',       "Vision anchor"),
    ("sp-product-card",   "Product cards"),
    ("sp-badge-live",     "LIVE badges"),
    ("sp-badge-road",     "ROADMAP badges"),
    ("sp-vision-callout", "Vision platform callout"),
    ("sp-final-cta",      "Final CTA"),
    ("main-footer",       "Footer preserved"),
    ("sp-grad-def",       "Gradient text"),
    ("sp-suite-hdr",      "Suite headers"),
    ("sp-btn-def",        "Defense CTA button"),
    ("sp-btn-off",        "Offense CTA button"),
    ("sp-btn-vis",        "Vision CTA button"),
]
passed = 0
for needle, label in checks:
    if needle in NEW_RAW:
        print(f"  [OK] {label}")
        passed += 1
    else:
        print(f"  [!!] MISSING: {label}  ({needle!r})")
print(f"\n{passed}/{len(checks)} checks passed")
