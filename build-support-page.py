#!/usr/bin/env python3
"""
Build support.html — reimagined enterprise support portal for AiVRIC.
Extracts shared NAV and FOOTER from cloudsignals-findings.html.
"""
from pathlib import Path

SITE = Path(r"C:\Projects\AiVRIC-Website")
TEMPLATE = SITE / "cloudsignals-findings.html"
OUT = SITE / "support.html"

raw_t = TEMPLATE.read_text(encoding="utf-8", errors="replace")

# ── Extract shared blocks ──────────────────────────────────────────────────
NAV_START = "<!-- page wrapper -->"
NAV_END   = "<!-- End Mobile Menu -->"
FOOT_START = "<!-- main-footer -->"
FOOT_END   = "<!-- main-footer end -->"

nav_s  = raw_t.find(NAV_START)
nav_e  = raw_t.find(NAV_END) + len(NAV_END)
foot_s = raw_t.find(FOOT_START)
foot_e = raw_t.find(FOOT_END) + len(FOOT_END)

assert nav_s  != -1, "NAV_START not found"
assert nav_e  != -1, "NAV_END not found"
assert foot_s != -1, "FOOT_START not found"
assert foot_e != -1, "FOOT_END not found"

NAV    = raw_t[nav_s : nav_e]
FOOTER = raw_t[foot_s : foot_e]

# ── CSS ────────────────────────────────────────────────────────────────────
CSS = """
<style id="su-styles">
/* ── AiVRIC Support Page ──────────────────────────────────────────────── */
body.su-page {
  font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Arial, sans-serif;
  background:
    radial-gradient(1400px 900px at 65% -8%, rgba(0,209,255,.10), transparent 52%),
    radial-gradient(900px 700px at 2% 22%, rgba(46,113,229,.08), transparent 55%),
    linear-gradient(180deg,#060b14 0%,#07101c 40%,#050810 100%);
  color: #e5e7eb;
}

/* ── Hero ──────────────────────────────────────────────────────────────── */
.su-hero {
  padding: 88px 0 64px;
  text-align: center;
  position: relative;
}
.su-hero-inner { max-width: 700px; margin: 0 auto; }
.su-eyebrow {
  display: inline-flex; align-items: center; gap: 8px;
  font-size: 11px; font-weight: 900; letter-spacing: 2.5px; text-transform: uppercase;
  color: #00d1ff; margin-bottom: 20px;
}
.su-eyebrow::before { content:''; width:22px; height:2px; background:#00d1ff; border-radius:2px; }
.su-eyebrow::after  { content:''; width:22px; height:2px; background:#00d1ff; border-radius:2px; }
.su-hero-title {
  font-family: 'Jost', 'Inter', sans-serif;
  font-size: 52px; font-weight: 800; letter-spacing: -1.2px;
  color: #f8fafc; line-height: 1.06; margin: 0 0 16px;
}
@media(max-width:640px){ .su-hero-title { font-size: 36px; } }
.su-hero-sub {
  font-size: 17px; line-height: 1.75; color: #94a3b8; margin: 0 0 36px;
}
/* Hero search */
.su-search-wrap { max-width: 560px; margin: 0 auto; position: relative; }
.su-search-box {
  display: flex; align-items: center; gap: 12px;
  background: rgba(255,255,255,.06);
  border: 1px solid rgba(148,163,184,.22);
  border-radius: 16px; padding: 14px 20px;
  transition: border-color .2s, background .2s;
}
.su-search-box:focus-within {
  border-color: rgba(0,209,255,.45);
  background: rgba(0,209,255,.04);
}
.su-search-box i { color: #64748b; font-size: 15px; flex-shrink: 0; }
.su-search-box input {
  flex: 1; background: transparent; border: none; outline: none;
  color: #f8fafc; font-size: 15px; font-family: inherit;
}
.su-search-box input::placeholder { color: #475569; }
.su-search-box a.su-search-btn {
  background: #00d1ff; color: #060b14; font-size: 13px; font-weight: 800;
  padding: 8px 18px; border-radius: 10px; white-space: nowrap;
  text-decoration: none; flex-shrink: 0; transition: background .18s;
}
.su-search-box a.su-search-btn:hover { background: #20d8ff; }
.su-search-note {
  font-size: 12px; color: #475569; margin-top: 10px;
}
.su-search-note a { color: #64748b; }
.su-search-note a:hover { color: #00d1ff; }

/* ── Section wrapper ───────────────────────────────────────────────────── */
.su-section { padding: 0 0 72px; }
.su-container { max-width: 1200px; margin: 0 auto; padding: 0 28px; }
.su-section-label {
  font-size: 11px; font-weight: 800; letter-spacing: 2px; text-transform: uppercase;
  color: #64748b; margin: 0 0 20px;
  display: flex; align-items: center; gap: 12px;
}
.su-section-label::after {
  content: ''; flex: 1; height: 1px; background: rgba(148,163,184,.12);
}

/* ── Channel cards ─────────────────────────────────────────────────────── */
.su-channels {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 72px;
}
@media(max-width:900px){ .su-channels { grid-template-columns: repeat(2,1fr); } }
@media(max-width:540px){ .su-channels { grid-template-columns: 1fr; } }

.su-channel-card {
  display: flex; flex-direction: column; gap: 12px;
  padding: 24px 22px 20px;
  background: rgba(255,255,255,.03);
  border: 1px solid rgba(148,163,184,.12);
  border-radius: 16px;
  text-decoration: none;
  color: inherit;
  transition: border-color .2s, background .2s, transform .2s;
  cursor: pointer;
}
.su-channel-card:hover {
  border-color: rgba(0,209,255,.28);
  background: rgba(0,209,255,.04);
  transform: translateY(-2px);
  color: inherit;
}
.su-channel-icon {
  width: 44px; height: 44px; border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 19px; flex-shrink: 0;
}
.su-channel-icon.cyan   { background: rgba(0,209,255,.12);  color: #00d1ff;  }
.su-channel-icon.green  { background: rgba(46,229,157,.12); color: #2ee59d;  }
.su-channel-icon.amber  { background: rgba(255,214,58,.12); color: #ffd63a;  }
.su-channel-icon.purple { background: rgba(167,139,250,.12);color: #a78bfa;  }
.su-channel-label {
  font-size: 15px; font-weight: 700; color: #f8fafc; line-height: 1.3;
}
.su-channel-desc {
  font-size: 13.5px; color: #94a3b8; line-height: 1.6; flex: 1;
}
.su-channel-arrow {
  font-size: 12.5px; font-weight: 700; color: #00d1ff; margin-top: 4px;
}

/* ── Topics grid ───────────────────────────────────────────────────────── */
.su-topics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}
@media(max-width:900px){ .su-topics { grid-template-columns: 1fr 1fr; } }
@media(max-width:540px){ .su-topics { grid-template-columns: 1fr; } }

.su-topic-group {
  background: rgba(255,255,255,.03);
  border: 1px solid rgba(148,163,184,.1);
  border-radius: 14px;
  padding: 20px 20px 16px;
}
.su-topic-title {
  font-size: 12px; font-weight: 800; letter-spacing: 1.2px; text-transform: uppercase;
  margin: 0 0 14px;
  display: flex; align-items: center; gap: 8px;
}
.su-topic-title i { font-size: 13px; }
.su-topic-title.cyan   { color: #00d1ff; }
.su-topic-title.green  { color: #2ee59d; }
.su-topic-title.amber  { color: #ffd63a; }
.su-topic-title.purple { color: #a78bfa; }
.su-topic-title.orange { color: #fb923c; }
.su-topic-title.red    { color: #f87171; }

.su-topic-links {
  list-style: none; padding: 0; margin: 0;
  display: flex; flex-direction: column; gap: 6px;
}
.su-topic-links li a {
  font-size: 13.5px; color: #94a3b8; text-decoration: none;
  display: flex; align-items: center; gap: 6px;
  transition: color .15s;
}
.su-topic-links li a::before {
  content: '→'; font-size: 11px; color: #475569; flex-shrink: 0; transition: color .15s;
}
.su-topic-links li a:hover { color: #f8fafc; }
.su-topic-links li a:hover::before { color: #00d1ff; }

/* ── SLA tiers ─────────────────────────────────────────────────────────── */
.su-tiers {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
@media(max-width:800px){ .su-tiers { grid-template-columns: 1fr; } }

.su-tier-card {
  padding: 26px 24px 22px;
  background: rgba(255,255,255,.03);
  border: 1px solid rgba(148,163,184,.1);
  border-radius: 16px;
  position: relative;
  overflow: hidden;
}
.su-tier-card.su-tier-featured {
  border-color: rgba(0,209,255,.3);
  background: rgba(0,209,255,.04);
}
.su-tier-badge {
  display: inline-flex; align-items: center; gap: 5px;
  font-size: 10px; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase;
  padding: 3px 10px; border-radius: 999px; margin-bottom: 12px;
}
.su-tier-badge.starter   { background: rgba(148,163,184,.1); color: #94a3b8; }
.su-tier-badge.pro       { background: rgba(0,209,255,.1);   color: #00d1ff; border: 1px solid rgba(0,209,255,.25); }
.su-tier-badge.enterprise{ background: rgba(167,139,250,.1); color: #a78bfa; border: 1px solid rgba(167,139,250,.25); }
.su-tier-name {
  font-family: 'Jost', 'Inter', sans-serif;
  font-size: 20px; font-weight: 800; color: #f8fafc; margin: 0 0 6px;
}
.su-tier-desc { font-size: 13.5px; color: #94a3b8; line-height: 1.6; margin: 0 0 18px; }
.su-tier-list {
  list-style: none; padding: 0; margin: 0;
  display: flex; flex-direction: column; gap: 8px;
}
.su-tier-list li {
  display: flex; align-items: flex-start; gap: 9px;
  font-size: 13.5px; color: #cbd5e1; line-height: 1.5;
}
.su-tier-list li i { font-size: 11px; flex-shrink: 0; margin-top: 3px; }
.su-tier-list li i.fa-check-circle { color: #2ee59d; }
.su-tier-list li i.fa-circle { color: #475569; font-size: 7px; margin-top: 6px; }
.su-tier-cta {
  display: inline-block; margin-top: 20px;
  font-size: 13px; font-weight: 700;
  padding: 9px 18px; border-radius: 10px;
  text-decoration: none; transition: background .18s, color .18s;
  border: 1px solid;
}
.su-tier-cta.outline {
  border-color: rgba(148,163,184,.22);
  color: #94a3b8;
  background: transparent;
}
.su-tier-cta.outline:hover { border-color: rgba(0,209,255,.3); color: #00d1ff; background: rgba(0,209,255,.05); }
.su-tier-cta.filled {
  border-color: #00d1ff;
  color: #060b14;
  background: #00d1ff;
}
.su-tier-cta.filled:hover { background: #20d8ff; border-color: #20d8ff; }
.su-tier-cta.purple-fill {
  border-color: rgba(167,139,250,.5);
  color: #a78bfa;
  background: rgba(167,139,250,.08);
}
.su-tier-cta.purple-fill:hover { background: rgba(167,139,250,.16); }

/* ── Support form ──────────────────────────────────────────────────────── */
.su-form-wrap {
  display: grid;
  grid-template-columns: 1fr 1.55fr;
  gap: 40px;
  align-items: start;
}
@media(max-width:900px){ .su-form-wrap { grid-template-columns: 1fr; } }

.su-form-info {}
.su-form-title {
  font-family: 'Jost', 'Inter', sans-serif;
  font-size: 28px; font-weight: 800; letter-spacing: -.5px;
  color: #f8fafc; margin: 0 0 12px; line-height: 1.2;
}
.su-form-body { font-size: 15px; color: #94a3b8; line-height: 1.75; margin: 0 0 24px; }

.su-contact-stack { display: flex; flex-direction: column; gap: 12px; }
.su-contact-row {
  display: flex; align-items: center; gap: 12px;
  padding: 14px 16px;
  background: rgba(255,255,255,.03);
  border: 1px solid rgba(148,163,184,.1);
  border-radius: 12px;
  text-decoration: none;
  transition: border-color .18s, background .18s;
}
.su-contact-row:hover { border-color: rgba(0,209,255,.28); background: rgba(0,209,255,.04); }
.su-contact-row-icon {
  width: 36px; height: 36px; border-radius: 9px;
  display: flex; align-items: center; justify-content: center;
  font-size: 15px; flex-shrink: 0;
}
.su-contact-row-icon.cyan   { background: rgba(0,209,255,.12);  color: #00d1ff;  }
.su-contact-row-icon.green  { background: rgba(46,229,157,.12); color: #2ee59d;  }
.su-contact-row-icon.amber  { background: rgba(255,214,58,.12); color: #ffd63a;  }
.su-contact-row-icon.purple { background: rgba(167,139,250,.12);color: #a78bfa;  }
.su-contact-row-text { flex: 1; }
.su-contact-row-label { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: .8px; color: #64748b; }
.su-contact-row-value { font-size: 14px; color: #cbd5e1; font-weight: 500; margin-top: 1px; }
.su-contact-row-arrow { color: #475569; font-size: 12px; }

/* Urgency note */
.su-urgent-note {
  margin-top: 14px; padding: 12px 16px;
  background: rgba(248,113,113,.05);
  border: 1px solid rgba(248,113,113,.18);
  border-left: 3px solid #f87171;
  border-radius: 10px;
  font-size: 13px; color: #fca5a5; line-height: 1.6;
}
.su-urgent-note strong { color: #f8fafc; }
.su-urgent-note a { color: #f87171; }

/* Form panel */
.su-form-panel {
  background: rgba(255,255,255,.03);
  border: 1px solid rgba(148,163,184,.12);
  border-radius: 20px;
  padding: 32px 32px 28px;
}
@media(max-width:540px){ .su-form-panel { padding: 20px 16px; } }
.su-form-panel-title {
  font-family: 'Jost', 'Inter', sans-serif;
  font-size: 20px; font-weight: 800; color: #f8fafc; margin: 0 0 6px;
}
.su-form-panel-sub { font-size: 13.5px; color: #64748b; margin: 0 0 24px; }

.su-form {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px 16px;
}
.su-form .su-full { grid-column: 1 / -1; }

.su-form-group { display: flex; flex-direction: column; gap: 5px; }
.su-form-group label {
  font-size: 12px; font-weight: 700; color: #64748b;
  text-transform: uppercase; letter-spacing: .7px;
}
.su-form-group input,
.su-form-group select,
.su-form-group textarea {
  padding: 10px 14px;
  background: rgba(255,255,255,.04);
  border: 1px solid rgba(148,163,184,.18);
  border-radius: 10px;
  color: #f8fafc;
  font-size: 14px;
  font-family: inherit;
  outline: none;
  transition: border-color .2s, background .2s;
  width: 100%;
  box-sizing: border-box;
}
.su-form-group input:focus,
.su-form-group select:focus,
.su-form-group textarea:focus {
  border-color: rgba(0,209,255,.4);
  background: rgba(0,209,255,.03);
}
.su-form-group select option { background: #0f1b2e; color: #f8fafc; }
.su-form-group textarea { min-height: 120px; resize: vertical; line-height: 1.6; }
.su-form-group input::placeholder,
.su-form-group textarea::placeholder { color: #334155; }

.su-form-consent {
  font-size: 12px; color: #475569; line-height: 1.6;
}
.su-form-consent a { color: #64748b; }
.su-form-consent a:hover { color: #00d1ff; }

.su-submit-row {
  display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap;
  grid-column: 1 / -1; margin-top: 4px;
}
.su-submit-btn {
  padding: 12px 32px;
  background: #00d1ff;
  color: #060b14;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 800;
  cursor: pointer;
  font-family: inherit;
  transition: background .18s, transform .18s;
  letter-spacing: .2px;
}
.su-submit-btn:hover { background: #20d8ff; transform: translateY(-1px); }

/* ── Status strip ──────────────────────────────────────────────────────── */
.su-status-strip {
  display: flex; align-items: center; justify-content: center; gap: 28px;
  flex-wrap: wrap;
  padding: 18px 28px;
  background: rgba(255,255,255,.02);
  border: 1px solid rgba(148,163,184,.08);
  border-radius: 14px;
  margin-bottom: 72px;
  font-size: 13.5px;
}
.su-status-item { display: flex; align-items: center; gap: 8px; color: #64748b; }
.su-status-dot {
  width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0;
}
.su-status-dot.green { background: #2ee59d; box-shadow: 0 0 6px #2ee59d; animation: su-pulse 2.4s ease-in-out infinite; }
.su-status-dot.amber { background: #ffd63a; }
.su-status-dot.gray  { background: #475569; }
@keyframes su-pulse { 0%,100%{opacity:1}50%{opacity:.3} }
.su-status-value { color: #cbd5e1; font-weight: 600; }

/* ── Resources strip ───────────────────────────────────────────────────── */
.su-resources {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
}
@media(max-width:900px){ .su-resources { grid-template-columns: 1fr 1fr; } }
@media(max-width:540px){ .su-resources { grid-template-columns: 1fr; } }

.su-resource-card {
  padding: 18px 18px 16px;
  background: rgba(255,255,255,.02);
  border: 1px solid rgba(148,163,184,.09);
  border-radius: 14px;
  text-decoration: none;
  display: flex; flex-direction: column; gap: 6px;
  transition: border-color .18s, background .18s;
}
.su-resource-card:hover { border-color: rgba(0,209,255,.22); background: rgba(0,209,255,.03); }
.su-resource-icon { font-size: 20px; margin-bottom: 2px; }
.su-resource-label { font-size: 14px; font-weight: 700; color: #f8fafc; }
.su-resource-desc  { font-size: 12.5px; color: #64748b; line-height: 1.55; }
.su-resource-arrow { font-size: 12px; color: #00d1ff; margin-top: 2px; }

@media(max-width:600px){
  .su-form { grid-template-columns: 1fr; }
}
</style>
"""

# ── Page content ───────────────────────────────────────────────────────────
CONTENT = """
  <!-- ── Support Page ──────────────────────────────────────────────────── -->
  <div class="su-container">

    <!-- Hero -->
    <div class="su-hero">
      <div class="su-hero-inner">
        <div class="su-eyebrow">AiVRIC Platform Support</div>
        <h1 class="su-hero-title">How can we help?</h1>
        <p class="su-hero-sub">Browse the Platform Guide, open a support ticket, or reach the AiVRIC team directly. We're here every step of your security and compliance journey.</p>
        <div class="su-search-wrap">
          <div class="su-search-box">
            <i class="fas fa-search"></i>
            <input type="text" placeholder="Search the Platform Guide…" id="su-search-input" autocomplete="off">
            <a href="AiVRIC-UserGuide/index.html" class="su-search-btn">Browse Docs &rarr;</a>
          </div>
          <p class="su-search-note">
            Search across onboarding, connectors, compliance policies, and more in the
            <a href="AiVRIC-UserGuide/index.html">Platform Guide &rarr;</a>
          </p>
        </div>
      </div>
    </div>

    <!-- Status strip -->
    <div class="su-status-strip">
      <div class="su-status-item">
        <span class="su-status-dot green"></span>
        <span>Platform status:</span>
        <span class="su-status-value">All systems operational</span>
      </div>
      <div class="su-status-item">
        <span class="su-status-dot green"></span>
        <span>API:</span>
        <span class="su-status-value">Operational</span>
      </div>
      <div class="su-status-item">
        <span class="su-status-dot green"></span>
        <span>CloudSignals+RiskOps:</span>
        <span class="su-status-value">Operational</span>
      </div>
      <div class="su-status-item">
        <i class="fas fa-clock" style="color:#475569;font-size:12px"></i>
        <span>Support hours:</span>
        <span class="su-status-value">Mon&ndash;Fri, 8am&ndash;6pm ET</span>
      </div>
    </div>

    <!-- Channel cards -->
    <div class="su-channels">
      <a class="su-channel-card" href="AiVRIC-UserGuide/index.html">
        <div class="su-channel-icon cyan"><i class="fas fa-book-open"></i></div>
        <div class="su-channel-label">Platform Guide</div>
        <div class="su-channel-desc">Browse documentation for onboarding, connectors, compliance policies, and governance.</div>
        <div class="su-channel-arrow">Browse docs &rarr;</div>
      </a>
      <a class="su-channel-card" href="#submit-ticket">
        <div class="su-channel-icon green"><i class="fas fa-ticket-alt"></i></div>
        <div class="su-channel-label">Submit a Ticket</div>
        <div class="su-channel-desc">Open a support request for technical issues, onboarding help, or integration questions.</div>
        <div class="su-channel-arrow">Open ticket &rarr;</div>
      </a>
      <a class="su-channel-card" href="mailto:support@aivric.com">
        <div class="su-channel-icon amber"><i class="fas fa-envelope"></i></div>
        <div class="su-channel-label">Email Support</div>
        <div class="su-channel-desc">Reach us at support@aivric.com — initial response within one business day for standard plans.</div>
        <div class="su-channel-arrow">Send email &rarr;</div>
      </a>
      <a class="su-channel-card" href="https://calendly.com/aivric-sales/aivric-walkthrough-demo">
        <div class="su-channel-icon purple"><i class="fas fa-calendar-check"></i></div>
        <div class="su-channel-label">Book a Session</div>
        <div class="su-channel-desc">Schedule a live working session with an AiVRIC engineer for hands-on setup or advisory help.</div>
        <div class="su-channel-arrow">Book now &rarr;</div>
      </a>
    </div>

    <!-- Topics grid -->
    <div class="su-section">
      <p class="su-section-label">Popular topics</p>
      <div class="su-topics">

        <div class="su-topic-group">
          <div class="su-topic-title cyan"><i class="fas fa-rocket"></i> Getting Started</div>
          <ul class="su-topic-links">
            <li><a href="AiVRIC-UserGuide/getting-started.html">Onboarding checklist</a></li>
            <li><a href="AiVRIC-UserGuide/getting-started.html#connect">Connect your first cloud account</a></li>
            <li><a href="AiVRIC-UserGuide/getting-started.html#collaborate">Invite your team &amp; set roles</a></li>
            <li><a href="AiVRIC-UserGuide/platform-overview.html">Platform architecture overview</a></li>
            <li><a href="AiVRIC-UserGuide/getting-started.html#guardrails">Apply your first guardrails</a></li>
          </ul>
        </div>

        <div class="su-topic-group">
          <div class="su-topic-title green"><i class="fas fa-plug"></i> Connectors</div>
          <ul class="su-topic-links">
            <li><a href="AiVRIC-UserGuide/connectors.html#aws">AWS IAM role setup</a></li>
            <li><a href="AiVRIC-UserGuide/connectors.html#azure">Azure App Registration</a></li>
            <li><a href="AiVRIC-UserGuide/connectors.html#gcp">GCP Service Account setup</a></li>
            <li><a href="AiVRIC-UserGuide/connectors.html#k8s">Kubernetes RBAC manifest</a></li>
            <li><a href="AiVRIC-UserGuide/connectors.html#m365">Microsoft 365 / Entra ID</a></li>
          </ul>
        </div>

        <div class="su-topic-group">
          <div class="su-topic-title amber"><i class="fas fa-shield-alt"></i> CloudSignals+RiskOps</div>
          <ul class="su-topic-links">
            <li><a href="AiVRIC-UserGuide/cloudsignals-riskops.html">Module overview</a></li>
            <li><a href="AiVRIC-UserGuide/cloudsignals-riskops.html#compliance">Framework mapping (SOC 2, ISO 27001)</a></li>
            <li><a href="AiVRIC-UserGuide/cloudsignals-riskops.html#findings">Understanding findings &amp; risk scores</a></li>
            <li><a href="AiVRIC-UserGuide/cloudsignals-riskops.html#remediation">Remediation workflows</a></li>
            <li><a href="AiVRIC-UserGuide/integrations.html">SIEM &amp; ticketing integrations</a></li>
          </ul>
        </div>

        <div class="su-topic-group">
          <div class="su-topic-title purple"><i class="fas fa-brain"></i> AI Governance</div>
          <ul class="su-topic-links">
            <li><a href="AiVRIC-UserGuide/ai-governance.html">Governance guide</a></li>
            <li><a href="AiVRIC-UserGuide/ai-autonomous-technologies.html">AI &amp; autonomous tech policy</a></li>
            <li><a href="AiVRIC-UserGuide/platform-overview.html#guardrails">Guardrail modes (Detect, Prevent, Remediate)</a></li>
            <li><a href="AiVRIC-UserGuide/ai-governance.html#approvals">Approval workflows</a></li>
            <li><a href="AiVRIC-UserGuide/ai-governance.html#lifecycle">AI model lifecycle controls</a></li>
          </ul>
        </div>

        <div class="su-topic-group">
          <div class="su-topic-title orange"><i class="fas fa-lock"></i> Security &amp; Compliance</div>
          <ul class="su-topic-links">
            <li><a href="AiVRIC-UserGuide/security-trust.html">Platform security overview</a></li>
            <li><a href="AiVRIC-UserGuide/data-privacy.html">Data privacy policy</a></li>
            <li><a href="AiVRIC-UserGuide/data-classification-handling.html">Data classification</a></li>
            <li><a href="AiVRIC-UserGuide/compliance.html">Compliance overview</a></li>
            <li><a href="trust.html">Trust Center</a></li>
          </ul>
        </div>

        <div class="su-topic-group">
          <div class="su-topic-title red"><i class="fas fa-exclamation-circle"></i> Incidents &amp; Escalations</div>
          <ul class="su-topic-links">
            <li><a href="AiVRIC-UserGuide/incident-response-operations.html">Incident response policy</a></li>
            <li><a href="mailto:security@aivric.com">Report a security incident &rarr;</a></li>
            <li><a href="AiVRIC-UserGuide/faq.html#security">Security FAQ</a></li>
            <li><a href="AiVRIC-UserGuide/threat-management.html">Threat management guide</a></li>
            <li><a href="#submit-ticket">Open an urgent ticket</a></li>
          </ul>
        </div>

      </div>
    </div>

    <!-- SLA tiers -->
    <div class="su-section">
      <p class="su-section-label">Support plans</p>
      <div class="su-tiers">

        <div class="su-tier-card">
          <div class="su-tier-badge starter">Starter</div>
          <div class="su-tier-name">Standard Support</div>
          <div class="su-tier-desc">Included with all AiVRIC plans. Community docs and email ticketing.</div>
          <ul class="su-tier-list">
            <li><i class="fas fa-check-circle"></i> Platform Guide access (24/7)</li>
            <li><i class="fas fa-check-circle"></i> Email: <a href="mailto:support@aivric.com" style="color:#2ee59d">support@aivric.com</a></li>
            <li><i class="fas fa-check-circle"></i> Response target: 1 business day</li>
            <li><i class="fas fa-check-circle"></i> FAQ &amp; self-service resources</li>
            <li><i class="fas fa-circle"></i> Dedicated CSM</li>
            <li><i class="fas fa-circle"></i> Phone support</li>
          </ul>
          <a href="#submit-ticket" class="su-tier-cta outline">Open a ticket &rarr;</a>
        </div>

        <div class="su-tier-card su-tier-featured">
          <div class="su-tier-badge pro">Professional</div>
          <div class="su-tier-name">Priority Support</div>
          <div class="su-tier-desc">Enhanced SLAs, phone access, and guided working sessions for Professional and AiVRIC+ customers.</div>
          <ul class="su-tier-list">
            <li><i class="fas fa-check-circle"></i> Everything in Standard</li>
            <li><i class="fas fa-check-circle"></i> Phone: <a href="tel:+19543426637" style="color:#2ee59d">+1-954-342-6637</a></li>
            <li><i class="fas fa-check-circle"></i> Response target: 4 business hours</li>
            <li><i class="fas fa-check-circle"></i> Live working sessions (Calendly)</li>
            <li><i class="fas fa-check-circle"></i> Prioritized ticket queue</li>
            <li><i class="fas fa-circle"></i> Dedicated CSM</li>
          </ul>
          <a href="https://calendly.com/aivric-sales/aivric-walkthrough-demo" class="su-tier-cta filled">Book a session &rarr;</a>
        </div>

        <div class="su-tier-card">
          <div class="su-tier-badge enterprise">Enterprise</div>
          <div class="su-tier-name">Managed &amp; Enterprise</div>
          <div class="su-tier-desc">White-glove support for Enterprise and Managed GRC customers — dedicated CSM, agreed SLAs, and 24/7 critical coverage.</div>
          <ul class="su-tier-list">
            <li><i class="fas fa-check-circle"></i> Everything in Priority</li>
            <li><i class="fas fa-check-circle"></i> Dedicated Customer Success Manager</li>
            <li><i class="fas fa-check-circle"></i> Critical SLA: 1-hour response</li>
            <li><i class="fas fa-check-circle"></i> 24/7 coverage for P0 incidents</li>
            <li><i class="fas fa-check-circle"></i> GRC advisory sessions</li>
            <li><i class="fas fa-check-circle"></i> Custom onboarding &amp; training</li>
          </ul>
          <a href="mailto:sales@aivric.com" class="su-tier-cta purple-fill">Talk to sales &rarr;</a>
        </div>

      </div>
    </div>

    <!-- Submit ticket + contact info -->
    <div class="su-section" id="submit-ticket">
      <p class="su-section-label">Contact &amp; submit a request</p>
      <div class="su-form-wrap">

        <!-- Left: contact info -->
        <div class="su-form-info">
          <h2 class="su-form-title">Reach the<br>AiVRIC team</h2>
          <p class="su-form-body">Use the form to open a support request, or reach us directly via email, phone, or a live session booking. For security incidents, contact <a href="mailto:security@aivric.com" style="color:#f87171">security@aivric.com</a> immediately.</p>

          <div class="su-contact-stack">
            <a href="mailto:support@aivric.com" class="su-contact-row">
              <div class="su-contact-row-icon cyan"><i class="fas fa-envelope"></i></div>
              <div class="su-contact-row-text">
                <div class="su-contact-row-label">Email</div>
                <div class="su-contact-row-value">support@aivric.com</div>
              </div>
              <i class="fas fa-chevron-right su-contact-row-arrow"></i>
            </a>
            <a href="tel:+19543426637" class="su-contact-row">
              <div class="su-contact-row-icon green"><i class="fas fa-phone-alt"></i></div>
              <div class="su-contact-row-text">
                <div class="su-contact-row-label">Phone</div>
                <div class="su-contact-row-value">+1-954-342-6637 &mdash; Mon&ndash;Fri, 8am&ndash;6pm ET</div>
              </div>
              <i class="fas fa-chevron-right su-contact-row-arrow"></i>
            </a>
            <a href="https://calendly.com/aivric-sales/aivric-walkthrough-demo" class="su-contact-row">
              <div class="su-contact-row-icon amber"><i class="fas fa-calendar-alt"></i></div>
              <div class="su-contact-row-text">
                <div class="su-contact-row-label">Live session</div>
                <div class="su-contact-row-value">Book a guided working session with an engineer</div>
              </div>
              <i class="fas fa-chevron-right su-contact-row-arrow"></i>
            </a>
            <a href="mailto:sales@aivric.com" class="su-contact-row">
              <div class="su-contact-row-icon purple"><i class="fas fa-user-tie"></i></div>
              <div class="su-contact-row-text">
                <div class="su-contact-row-label">Sales</div>
                <div class="su-contact-row-value">sales@aivric.com &mdash; pricing, enterprise plans, POC</div>
              </div>
              <i class="fas fa-chevron-right su-contact-row-arrow"></i>
            </a>
          </div>

          <div class="su-urgent-note">
            <strong>Critical incident?</strong> Mark your ticket as <em>Urgent</em> and email
            <a href="mailto:security@aivric.com">security@aivric.com</a> simultaneously for fastest triage.
          </div>
        </div>

        <!-- Right: form -->
        <div class="su-form-panel">
          <div class="su-form-panel-title">Submit a support request</div>
          <div class="su-form-panel-sub">We typically respond within one business day for standard plans.</div>

          <form id="support-form" class="su-form" onsubmit="return false;">

            <div class="su-form-group">
              <label for="su-name">Full Name</label>
              <input type="text" id="su-name" name="name" placeholder="Your full name" required>
            </div>

            <div class="su-form-group">
              <label for="su-email">Work Email</label>
              <input type="email" id="su-email" name="email" placeholder="you@company.com" required>
            </div>

            <div class="su-form-group">
              <label for="su-company">Organization</label>
              <input type="text" id="su-company" name="company" placeholder="Company or team name">
            </div>

            <div class="su-form-group">
              <label for="su-plan">Plan / Service</label>
              <select id="su-plan" name="plan">
                <option value="">Select your plan</option>
                <option value="defense-starter">AiVRIC Defense &mdash; Starter</option>
                <option value="defense-professional">AiVRIC Defense &mdash; Professional</option>
                <option value="defense-enterprise">AiVRIC Defense &mdash; Enterprise</option>
                <option value="aivric-plus">AiVRIC+ Services Platform</option>
                <option value="managed-grc">Managed GRC Services</option>
                <option value="other">Other / Evaluating</option>
              </select>
            </div>

            <div class="su-form-group">
              <label for="su-priority">Priority</label>
              <select id="su-priority" name="priority">
                <option value="normal">Normal</option>
                <option value="high">High &mdash; Production Impact</option>
                <option value="urgent">Urgent &mdash; Security or Compliance Risk</option>
              </select>
            </div>

            <div class="su-form-group">
              <label for="su-category">Request Type</label>
              <select id="su-category" name="category">
                <option value="">Select type</option>
                <option value="onboarding">Onboarding &amp; Setup</option>
                <option value="technical">Technical Issue / Error</option>
                <option value="integrations">Integrations &amp; APIs</option>
                <option value="compliance">Compliance &amp; Reporting</option>
                <option value="billing">Billing &amp; Subscription</option>
                <option value="other">Other Question</option>
              </select>
            </div>

            <div class="su-form-group su-full">
              <label for="su-subject">Subject</label>
              <input type="text" id="su-subject" name="subject" placeholder="Short summary of your request" required>
            </div>

            <div class="su-form-group su-full">
              <label for="su-message">Details</label>
              <textarea id="su-message" name="message" placeholder="Describe what you need help with. Include impact, relevant environments, recent changes, and any error messages." required></textarea>
            </div>

            <div class="su-submit-row">
              <button type="submit" class="su-submit-btn">Submit Support Request</button>
              <span class="su-form-consent">By submitting you agree to our <a href="privacy-policy.html">Privacy Policy</a>.</span>
            </div>

          </form>
        </div>
      </div>
    </div>

    <!-- Resources -->
    <div class="su-section">
      <p class="su-section-label">Helpful resources</p>
      <div class="su-resources">
        <a class="su-resource-card" href="AiVRIC-UserGuide/index.html">
          <div class="su-resource-icon">📖</div>
          <div class="su-resource-label">Platform Guide</div>
          <div class="su-resource-desc">Complete documentation for AiVRIC — onboarding, connectors, and policies.</div>
          <div class="su-resource-arrow">Browse &rarr;</div>
        </a>
        <a class="su-resource-card" href="AiVRIC-UserGuide/faq.html">
          <div class="su-resource-icon">❓</div>
          <div class="su-resource-label">FAQ</div>
          <div class="su-resource-desc">Answers to the most common setup, security, and billing questions.</div>
          <div class="su-resource-arrow">Read FAQs &rarr;</div>
        </a>
        <a class="su-resource-card" href="trust.html">
          <div class="su-resource-icon">🔐</div>
          <div class="su-resource-label">Trust Center</div>
          <div class="su-resource-desc">SOC 2 readiness, pen-test summaries, data handling, and compliance posture.</div>
          <div class="su-resource-arrow">View Trust Center &rarr;</div>
        </a>
        <a class="su-resource-card" href="https://calendly.com/aivric-sales/aivric-walkthrough-demo">
          <div class="su-resource-icon">🗓️</div>
          <div class="su-resource-label">Book a Session</div>
          <div class="su-resource-desc">30-minute working session with an AiVRIC engineer — setup, advisory, or deep-dive.</div>
          <div class="su-resource-arrow">Book now &rarr;</div>
        </a>
      </div>
    </div>

  </div>
  <!-- ── /Support Page ───────────────────────────────────────────────────── -->
"""

# ── Scroll-to-top + JS blocks ──────────────────────────────────────────────
SCROLL_TOP = """
        <!--Scroll to top-->
        <div class="scroll-to-top">
            <div>
                <div class="scroll-top-inner">
                    <div class="scroll-bar">
                        <div class="bar-inner"></div>
                    </div>
                    <div class="scroll-bar-text">Go To Top</div>
                </div>
            </div>
        </div>
        <!-- Scroll to top end -->"""

JS_BLOCK = """
<!-- JS -->
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
<script src="assets/js/support-form.js"></script>
<script src="assets/js/theme-toggle.js"></script>
<script src="assets/js/mega-hover.js"></script>
<script src="assets/js/mega-tabs.js"></script>
<script>
  // Redirect hero search to Platform Guide
  (function(){
    var inp = document.getElementById('su-search-input');
    if(!inp) return;
    inp.addEventListener('keydown', function(e){
      if(e.key === 'Enter' && inp.value.trim()){
        window.location.href = 'AiVRIC-UserGuide/index.html';
      }
    });
  })();
</script>
"""

# ── Head block ─────────────────────────────────────────────────────────────
HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
    <title>Support | AiVRIC Platform</title>
    <meta name="description" content="AiVRIC platform support — browse the Platform Guide, submit a ticket, contact our team, or book a live working session.">
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
    <link href="assets/css/custom.css?v=20250115" rel="stylesheet">"""

GTAG = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-EG2Q8GD30V"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-EG2Q8GD30V');
</script>"""

# ── Assemble ───────────────────────────────────────────────────────────────
output = (
    HEAD
    + CSS
    + "\n</head>"
    + GTAG
    + '\n<body class="su-page">\n<div class="boxed_wrapper">\n'
    + "    <!-- preloader -->\n"
    + "    <div class=\"loader-wrap\"><div class=\"preloader\"><div class=\"preloader-close\">x</div>"
    + "<div id=\"handle-preloader\" class=\"handle-preloader\"><div class=\"animation-preloader\">"
    + "<div class=\"spinner\"></div><div class=\"txt-loading\">"
    + "<span data-text-preloader=\"A\" class=\"letters-loading\">A</span>"
    + "<span data-text-preloader=\"I\" class=\"letters-loading\">I</span>"
    + "<span data-text-preloader=\"V\" class=\"letters-loading\">V</span>"
    + "<span data-text-preloader=\"r\" class=\"letters-loading\">r</span>"
    + "<span data-text-preloader=\"i\" class=\"letters-loading\">i</span>"
    + "<span data-text-preloader=\"c\" class=\"letters-loading\">c</span>"
    + "</div></div></div></div></div>\n    <!-- preloader end -->\n"
    + NAV
    + "\n\n"
    + CONTENT
    + "\n\n"
    + "        " + FOOTER
    + "\n"
    + SCROLL_TOP
    + "\n    </div>\n"
    + JS_BLOCK
    + "\n</body>\n</html>"
)

OUT.write_text(output, encoding="utf-8")
print(f"Built: support.html  ({len(output.splitlines())} lines)")
