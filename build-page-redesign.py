#!/usr/bin/env python3
"""
AiVRIC Website - Page Redesign Pass
Rebuilds 9 marketing pages + upgrades 25 UserGuide stub pages + darkens guide header CSS.
"""

import re
from pathlib import Path

SITE = Path(r"C:\Projects\AiVRIC-Website")
TEMPLATE = SITE / "cspm-cloudsignals.html"
UG = SITE / "AiVRIC-UserGuide"

# ── Extract header/footer from cspm template ──────────────────────────────────
def get_templates():
    raw = TEMPLATE.read_text(encoding="utf-8")
    mobile_end = "        </div><!-- End Mobile Menu -->"
    ftr_start = "        </div><!-- /cs-product-page -->"
    hdr_end = raw.index(mobile_end) + len(mobile_end)
    ftr_idx  = raw.index(ftr_start)
    return raw[:hdr_end], raw[ftr_idx:]

# ── Shared page builder ───────────────────────────────────────────────────────
def make_page(title, description, content_html):
    hdr, ftr = get_templates()
    hdr = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", hdr, flags=re.DOTALL)
    hdr = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{description}">', hdr)
    return hdr + "\n" + content_html + "\n" + ftr

# ── Guide sidebar (shared across UserGuide pages) ─────────────────────────────
def guide_sidebar(active=""):
    def lnk(target, href, label, sub):
        cls = "nav-link active" if active == target else "nav-link"
        return f'        <a class="{cls}" data-page-target="{target}" href="{href}">{label} <small>{sub}</small></a>'
    return f"""    <aside class="guide-sidebar" id="sidebar">
      <div class="nav-section">
        <p class="nav-label">Essentials</p>
{lnk("home","index.html","Overview","Start here")}
{lnk("getting-started","getting-started.html","Getting started","Setup")}
{lnk("platform","platform-overview.html","Platform overview","How AiVRIC works")}
      </div>
      <div class="nav-section">
        <p class="nav-label">CloudSignals+RiskOps</p>
{lnk("cloudsignals","cloudsignals-riskops.html","Module overview","How it works")}
{lnk("connectors","connectors.html","Connectors","Connect cloud accounts")}
{lnk("integrations","integrations.html","Integrations","SIEM, ticketing &amp; alerts")}
      </div>
      <div class="nav-section">
        <p class="nav-label">Assurance</p>
{lnk("security","security-trust.html","Security &amp; Trust","Controls")}
{lnk("governance","ai-governance.html","AI Governance","Policies")}
{lnk("faq","faq.html","FAQ &amp; Support","Answers")}
      </div>
    </aside>"""

# ── Standard guide-shell JS footer ────────────────────────────────────────────
GUIDE_SCRIPT = """  <script>
    (function(){
      var p = document.body.dataset.page;
      document.querySelectorAll('[data-page-target]').forEach(function(a){
        if(a.dataset.pageTarget === p){ a.classList.add('active'); }
      });
      var toggle = document.querySelector('.nav-toggle');
      var sidebar = document.getElementById('sidebar');
      if(toggle && sidebar){
        toggle.addEventListener('click', function(){ sidebar.classList.toggle('open'); });
      }
    })();
  </script>"""

# ─────────────────────────────────────────────────────────────────────────────
# PART 1 — MARKETING PAGES
# ─────────────────────────────────────────────────────────────────────────────

# ── Shared hero/module/cap/fw builders ───────────────────────────────────────
def hero(badge_color, badge_text, badge_dot_class, title, sub, cta1_href, cta1_text, cta2_href, cta2_text, quick_items, rb_items):
    ql = "\n".join(f'        <li><i class="fas fa-check-circle"></i> {x}</li>' for x in quick_items)
    rb = "\n".join(
        f'        <div class="csp-rb-item"><span class="csp-rb-label">{a}</span>'
        f'<span class="csp-rb-val {c}">{v}</span></div>'
        for a, v, c in rb_items
    )
    return f"""<div class="cs-product-page">
  <section class="csp-hero">
    <div class="auto-container">
      <div class="csp-hero-grid">
        <div>
          <div class="csp-badge">
            <span class="{badge_dot_class}"></span>
            {badge_text}
          </div>
          <h1 class="csp-title">{title}</h1>
          <p class="csp-sub">{sub}</p>
          <div class="csp-actions">
            <a href="{cta1_href}" class="cs-btn primary">{cta1_text}</a>
            <a href="{cta2_href}" class="cs-btn secondary">{cta2_text}</a>
          </div>
          <div class="csp-release-band">
{rb}
          </div>
        </div>
        <div class="csp-hero-aside">
          <div class="csp-quick-card">
            <h4>Key Capabilities</h4>
            <ul class="csp-quick-list">
{ql}
            </ul>
          </div>
          <a class="csp-quick-link" href="cloudsignals-pricing.html">
            <span>CloudSignals+RiskOps Pricing</span>
            <i class="fas fa-arrow-right"></i>
          </a>
        </div>
      </div>
    </div>
  </section>"""


def modules_section(eyebrow, section_title, section_sub, cards):
    def card(icon, color, name, desc, feats):
        fl = "\n".join(f'          <li>{f}</li>' for f in feats)
        return f"""        <div class="csp-module-card">
          <div class="csp-module-icon {color}"><i class="{icon}"></i></div>
          <h3>{name}</h3>
          <p>{desc}</p>
          <ul class="csp-module-feats">
{fl}
          </ul>
        </div>"""
    cards_html = "\n".join(card(*c) for c in cards)
    return f"""  <section class="csp-section">
    <div class="auto-container">
      <span class="csp-eyebrow">{eyebrow}</span>
      <h2 class="csp-section-title">{section_title}</h2>
      <p class="csp-section-sub">{section_sub}</p>
      <div class="csp-modules-grid">
{cards_html}
      </div>
    </div>
  </section>"""


def caps_section(eyebrow, section_title, caps):
    def cap(icon, name, desc):
        return f"""        <div class="csp-cap">
          <div class="csp-cap-icon"><i class="{icon}"></i></div>
          <h4>{name}</h4>
          <p>{desc}</p>
        </div>"""
    caps_html = "\n".join(cap(*c) for c in caps)
    return f"""  <section class="csp-section">
    <div class="auto-container">
      <span class="csp-eyebrow">{eyebrow}</span>
      <h2 class="csp-section-title">{section_title}</h2>
      <div class="csp-cap-grid">
{caps_html}
      </div>
    </div>
  </section>"""


def frameworks_section(eyebrow, title, frameworks):
    def fw(icon_class, name, badge, items):
        li_html = "\n".join(f'                <li>{i}</li>' for i in items)
        return f"""        <details class="csp-fw-card">
          <summary class="csp-fw-head">
            <div class="csp-fw-head-left">
              <div class="csp-fw-logo"><i class="{icon_class}"></i></div>
              <span class="csp-fw-name">{name}</span>
            </div>
            <span class="csp-fw-badge">{badge}</span>
          </summary>
          <div class="csp-fw-body">
            <ul class="csp-fw-list">
{li_html}
            </ul>
          </div>
        </details>"""
    fws_html = "\n".join(fw(*f) for f in frameworks)
    return f"""  <section class="csp-section">
    <div class="auto-container">
      <span class="csp-eyebrow">{eyebrow}</span>
      <h2 class="csp-section-title">{title}</h2>
      <div class="csp-fw-grid">
{fws_html}
      </div>
    </div>
  </section>"""


def bottom_cta_section(headline, sub, cta_href, cta_text):
    return f"""  <section class="csp-section csp-bottom-cta">
    <div class="auto-container">
      <div class="csp-fw-grid" style="display:flex;flex-direction:column;align-items:center;text-align:center;gap:14px;padding:40px 0 20px;">
        <h2 class="csp-section-title" style="margin:0">{headline}</h2>
        <p class="csp-section-sub" style="margin:0">{sub}</p>
        <div class="csp-actions" style="justify-content:center">
          <a href="{cta_href}" class="cs-btn primary">{cta_text}</a>
          <a href="cloudsignals-pricing.html" class="cs-btn secondary">Compare plans</a>
        </div>
      </div>
    </div>
  </section>
</div>"""


# ─────────────────────────────────────────────────────────────────────────────
# SOC 2
# ─────────────────────────────────────────────────────────────────────────────
def page_soc2():
    h = hero(
        badge_color="green", badge_text="SOC 2 Automation &mdash; CloudSignals+RiskOps&#x2122;",
        badge_dot_class="avail-dot",
        title="SOC 2 Readiness.<br>Automated.",
        sub="Transform SOC 2 from an annual scramble into a continuous, automated operation. Cut audit prep time, eliminate evidence gaps, and give auditors exactly what they need.",
        cta1_href="https://calendly.com/aivric/cloudsignals-demo", cta1_text="Request a SOC 2 Demo",
        cta2_href="cloudsignals-pricing.html", cta2_text="View Pricing",
        quick_items=[
            "Continuous controls monitoring across AWS, Azure, GCP, K8s, GitHub &amp; M365",
            "Automated evidence collection tied to SOC 2 criteria",
            "Lighthouse AI narratives — audit-ready prose from your live posture",
            "Risk register with prioritized remediation guidance",
            "SOC 2 Type I &amp; Type II readiness scoring",
            "Executive and auditor dashboards",
        ],
        rb_items=[
            ("CloudSignals+RiskOps", "Available Now", "avail"),
            ("Audit Cycle", "Continuous", ""),
            ("Frameworks", "SOC 2, NIST CSF, ISO 27001", ""),
        ]
    )
    m = modules_section(
        "How it works", "Four modules that run the whole SOC 2 lifecycle",
        "CloudSignals+RiskOps handles continuous controls monitoring, evidence, AI narratives, and risk — so your team can focus on remediation and stakeholder readiness.",
        [
            ("fas fa-heartbeat", "cyan", "Continuous Controls Monitoring",
             "Real-time visibility into the state of every SOC 2 control across all connected environments.",
             ["24-hour automated audits across all providers", "Policy-to-control mapping for all Trust Services Criteria", "Drift detection with alerting"]),
            ("fas fa-file-alt", "green", "Automated Evidence Collection",
             "Every finding, remediation action, and configuration state is logged as evidence — no manual screenshots.",
             ["Timestamped evidence bundles per control", "Exportable audit packs (PDF + JSON)", "Evidence linked to SOC 2 criteria IDs"]),
            ("fas fa-robot", "gold", "Lighthouse AI Narratives",
             "Generative AI converts your live posture data into clear, auditor-ready control narratives.",
             ["Plain-language control descriptions", "Contextualized risk explanations", "Exportable narrative packs"]),
            ("fas fa-chart-line", "purple", "Risk Register Intelligence",
             "Prioritized risk register with business-context scoring to guide where to fix first.",
             ["Severity scoring with business impact overlay", "Remediation tracking with ownership", "Trend reporting for leadership"]),
        ]
    )
    c = caps_section(
        "Capabilities", "Everything you need across the SOC 2 lifecycle",
        [
            ("fas fa-map", "Control Mapping", "Map every cloud configuration and SaaS setting to SOC 2 Trust Services Criteria automatically."),
            ("fas fa-archive", "Evidence Automation", "Collect, timestamp, and package evidence from all connected providers without manual effort."),
            ("fas fa-pen-fancy", "AI Narratives", "Generate audit-ready control descriptions and risk narratives using Lighthouse AI."),
            ("fas fa-search", "Gap Analysis", "Identify control gaps against SOC 2 criteria with remediation guidance ranked by risk."),
            ("fas fa-clipboard-check", "Audit Reporting", "Produce auditor-ready evidence packs and status reports on demand."),
            ("fas fa-tachometer-alt", "Executive Dashboards", "Track SOC 2 readiness posture, trend lines, and open items in real time."),
        ]
    )
    fw = frameworks_section(
        "Compliance", "Frameworks covered by this use case",
        [
            ("fas fa-shield-alt", "SOC 2 Type I &amp; Type II", "Fully mapped",
             ["All five Trust Services Criteria (Security, Availability, Confidentiality, Processing Integrity, Privacy)", "Automated evidence mapped to criterion IDs", "Supports both Type I point-in-time and Type II period readiness"]),
            ("fas fa-sitemap", "NIST Cybersecurity Framework", "Covered",
             ["Identify &rarr; Protect &rarr; Detect &rarr; Respond &rarr; Recover alignment", "CloudSignals findings mapped to CSF categories", "CSF coverage dashboard"]),
            ("fas fa-globe", "ISO/IEC 27001", "Covered",
             ["Annex A control mapping", "Information Security Management System evidence support", "Cross-walk to SOC 2 controls"]),
            ("fas fa-cog", "CIS Benchmarks", "Covered",
             ["CIS Level 1 &amp; Level 2 checks across AWS, Azure, GCP, and K8s", "Hardening status per benchmark section", "Deviation tracking"]),
        ]
    )
    cta = bottom_cta_section(
        "Ready to automate SOC 2?",
        "See how AiVRIC CloudSignals+RiskOps replaces manual SOC 2 prep with a continuous, automated operation.",
        "https://calendly.com/aivric/cloudsignals-demo", "Schedule a SOC 2 Demo"
    )
    return h + "\n" + m + "\n" + c + "\n" + fw + "\n" + cta


# ─────────────────────────────────────────────────────────────────────────────
# PCI-DSS
# ─────────────────────────────────────────────────────────────────────────────
def page_pcidss():
    h = hero(
        badge_color="green", badge_text="PCI-DSS Compliance &mdash; CloudSignals+RiskOps&#x2122;",
        badge_dot_class="avail-dot",
        title="PCI-DSS Compliance.<br>Continuously.",
        sub="Reduce cardholder data environment risk with automated scope discovery, continuous control monitoring, and audit-ready evidence that makes your QSA's job easier.",
        cta1_href="https://calendly.com/aivric/cloudsignals-demo", cta1_text="Request a PCI-DSS Demo",
        cta2_href="cloudsignals-pricing.html", cta2_text="View Pricing",
        quick_items=[
            "Automated CDE scope and asset discovery",
            "PCI-DSS v4.0 requirement-to-control mapping",
            "Continuous posture monitoring for cardholder environments",
            "Automated evidence collection for QSA review",
            "Executive and auditor reporting on demand",
            "Risk-aware prioritization for faster remediation",
        ],
        rb_items=[
            ("CloudSignals+RiskOps", "Available Now", "avail"),
            ("Standard", "PCI-DSS v4.0", ""),
            ("Providers", "AWS, Azure, GCP, M365 &amp; more", ""),
        ]
    )
    m = modules_section(
        "How it works", "Four modules across the PCI-DSS readiness lifecycle",
        "CloudSignals+RiskOps automates the most time-consuming parts of PCI-DSS compliance — scope, evidence, mapping, and reporting.",
        [
            ("fas fa-crosshairs", "cyan", "Scope &amp; Asset Discovery",
             "Automatically discover and classify assets within cardholder data environments.",
             ["CDE boundary detection and mapping", "Service and data flow identification", "Scope change alerting"]),
            ("fas fa-file-alt", "green", "Evidence &amp; Reporting Automation",
             "Collect and package PCI-DSS evidence without manual screenshots or spreadsheets.",
             ["Timestamped control evidence bundles", "QSA-ready audit packs", "Exportable in PDF and JSON"]),
            ("fas fa-link", "gold", "Requirement-to-Control Mapping",
             "Every cloud configuration and SaaS setting is mapped to PCI-DSS requirements automatically.",
             ["PCI-DSS v4.0 full requirement coverage", "Sub-requirement level mapping", "Cross-walk to other frameworks"]),
            ("fas fa-shield-alt", "purple", "Risk-Aware PCI Posture",
             "Risk scores prioritized by business impact — fix what matters most for your CDE first.",
             ["Severity scoring with remediation guidance", "Trend reporting for leadership", "Open findings ownership tracking"]),
        ]
    )
    c = caps_section(
        "Capabilities", "Full lifecycle PCI-DSS capabilities",
        [
            ("fas fa-search", "CDE Asset Discovery", "Automatically identify and classify all assets within cardholder data environment boundaries."),
            ("fas fa-compress-arrows-alt", "Scope Reduction", "Identify out-of-scope assets and configuration gaps that unnecessarily expand CDE scope."),
            ("fas fa-archive", "Control Evidence", "Capture timestamped control evidence from all connected cloud and SaaS providers."),
            ("fas fa-map-signs", "Requirement Mapping", "Map findings and configurations directly to PCI-DSS v4.0 requirements and sub-requirements."),
            ("fas fa-file-contract", "QSA Reporting", "Generate QSA-ready evidence packs and summary reports on demand."),
            ("fas fa-eye", "Continuous Monitoring", "Run automated 24-hour posture audits across all CDE-connected providers."),
        ]
    )
    fw = frameworks_section(
        "Compliance", "Frameworks covered",
        [
            ("fas fa-credit-card", "PCI-DSS v4.0", "Fully mapped",
             ["All 12 PCI-DSS requirements covered", "Sub-requirement level control checks", "Supports SAQ and full ROC workflows"]),
            ("fas fa-shield-alt", "SOC 2", "Cross-walk available",
             ["Overlapping control evidence reduces dual-framework effort", "SOC 2 TSC cross-walk for shared controls", "Combined audit evidence packs"]),
            ("fas fa-sitemap", "NIST Cybersecurity Framework", "Covered",
             ["PCI-DSS controls aligned to CSF categories", "CDE posture mapped to Identify, Protect, Detect"]),
            ("fas fa-cog", "CIS Benchmarks", "Covered",
             ["CIS checks for all cloud providers in scope", "Hardening status for CDE workloads"]),
        ]
    )
    cta = bottom_cta_section(
        "Ready to simplify PCI-DSS?",
        "Automate scope, evidence, and reporting for your next PCI-DSS assessment with CloudSignals+RiskOps.",
        "https://calendly.com/aivric/cloudsignals-demo", "Schedule a PCI-DSS Demo"
    )
    return h + "\n" + m + "\n" + c + "\n" + fw + "\n" + cta


# ─────────────────────────────────────────────────────────────────────────────
# CMMC
# ─────────────────────────────────────────────────────────────────────────────
def page_cmmc():
    h = hero(
        badge_color="cyan", badge_text="CMMC Readiness &mdash; CloudSignals+RiskOps&#x2122;",
        badge_dot_class="beta-dot",
        title="CMMC Level 2 Readiness.<br>Continuously verified.",
        sub="Operationalize CMMC Level 2 compliance for defense contractors with automated NIST SP 800-171 mapping, continuous technical monitoring, and dynamic SSP and POA&amp;M support.",
        cta1_href="https://calendly.com/aivric/cloudsignals-demo", cta1_text="Request a CMMC Demo",
        cta2_href="cloudsignals-pricing.html", cta2_text="View Pricing",
        quick_items=[
            "Automated mapping to all 110 NIST SP 800-171 practices",
            "Continuous technical control verification (not just self-assessment)",
            "Dynamic SSP and POA&amp;M with live posture data",
            "CMMC Level 2 readiness scoring for leadership and assessors",
            "CUI protection posture across cloud and SaaS",
            "DFARS alignment and evidence packs",
        ],
        rb_items=[
            ("CloudSignals+RiskOps", "Available Now", "avail"),
            ("Level", "CMMC Level 2", ""),
            ("Alignment", "NIST SP 800-171 + DFARS", ""),
        ]
    )
    m = modules_section(
        "How it works", "Four modules for CMMC Level 2 readiness",
        "CloudSignals+RiskOps replaces fragile spreadsheet-based CMMC tracking with live, technically verified posture data.",
        [
            ("fas fa-map", "cyan", "NIST SP 800-171 Mapping",
             "Every technical control check is automatically mapped to the applicable NIST 800-171 practice.",
             ["All 110 practices covered", "Finding-to-practice traceability", "Cross-walk to CMMC Level 2 domains"]),
            ("fas fa-heartbeat", "green", "Continuous Technical Monitoring",
             "Move beyond self-assessment — CloudSignals continuously verifies technical controls in your CUI environment.",
             ["24-hour automated posture checks", "CUI environment boundary monitoring", "Drift detection with alerting"]),
            ("fas fa-file-alt", "gold", "SSP &amp; POA&amp;M Support",
             "Dynamic System Security Plan and POA&amp;M updated with live posture data, not quarterly snapshots.",
             ["Live SSP status per practice", "POA&amp;M with milestones and ownership", "Exportable for assessor review"]),
            ("fas fa-chart-bar", "purple", "Readiness Reporting",
             "Leadership and C3PAO-ready readiness reports showing practice coverage, gaps, and trend lines.",
             ["Practice-level status dashboard", "Gap analysis with risk ranking", "Evidence packs for assessors"]),
        ]
    )
    c = caps_section(
        "Capabilities", "End-to-end CMMC Level 2 capabilities",
        [
            ("fas fa-search", "Control Gap Analysis", "Identify which NIST 800-171 practices are not met and what's needed to close the gap."),
            ("fas fa-heartbeat", "Continuous Verification", "Automatically verify technical controls in your environment — not self-reported status."),
            ("fas fa-file-contract", "SSP Generation", "Maintain a live System Security Plan that reflects actual posture, not point-in-time snapshots."),
            ("fas fa-tasks", "POA&amp;M Tracking", "Track remediation milestones and ownership for every open CMMC finding."),
            ("fas fa-archive", "Evidence Collection", "Collect and package timestamped technical evidence for each NIST 800-171 practice."),
            ("fas fa-clipboard-check", "Assessor Reporting", "Generate C3PAO-ready evidence bundles and readiness summaries on demand."),
        ]
    )
    fw = frameworks_section(
        "Compliance", "Frameworks and standards covered",
        [
            ("fas fa-shield-alt", "CMMC Level 2", "Fully mapped",
             ["All 110 NIST SP 800-171 practices", "CMMC Level 2 domain coverage", "C3PAO-ready evidence packs"]),
            ("fas fa-cog", "NIST SP 800-171", "Fully mapped",
             ["Practice-level control checks across 14 domains", "Automated technical verification", "Self-assessment score (SPRS) support"]),
            ("fas fa-gavel", "DFARS / ITAR", "Covered",
             ["DFARS 252.204-7012 alignment", "CUI handling evidence", "Supplier and contractor posture tracking"]),
            ("fas fa-sitemap", "NIST CSF", "Cross-walk available",
             ["CSF category alignment for CMMC domains", "Shared evidence across NIST frameworks"]),
        ]
    )
    cta = bottom_cta_section(
        "Ready to operationalize CMMC readiness?",
        "Replace spreadsheet-based CMMC tracking with continuously verified, audit-ready posture data.",
        "https://calendly.com/aivric/cloudsignals-demo", "Schedule a CMMC Demo"
    )
    return h + "\n" + m + "\n" + c + "\n" + fw + "\n" + cta


# ─────────────────────────────────────────────────────────────────────────────
# ISSUES & POA&Ms — uses csfp-* feature page design
# ─────────────────────────────────────────────────────────────────────────────
ISSUES_CONTENT = """<style>
  :root{--fp-cyan:#00d1ff;--fp-green:#2ee59d;--fp-gold:#ffd63a;--fp-purple:#a78bfa;
    --fp-text:#f8fafc;--fp-muted:#cbd5e1;--fp-surf:rgba(255,255,255,0.06);--fp-line:rgba(148,163,184,0.22);}
  .fpp-hero{padding:90px 0 48px;position:relative;}
  .fpp-badge{display:inline-flex;align-items:center;gap:8px;padding:6px 14px;border-radius:999px;
    background:rgba(46,229,157,0.12);border:1px solid rgba(46,229,157,0.32);
    color:var(--fp-text);font-size:12px;font-weight:700;margin-bottom:14px;}
  .fpp-badge .avail-dot{width:7px;height:7px;border-radius:50%;background:var(--fp-green);
    box-shadow:0 0 6px rgba(46,229,157,0.6);}
  .fpp-title{font-family:Jost,Inter,sans-serif;font-size:48px;font-weight:800;
    line-height:1.05;letter-spacing:-1px;color:var(--fp-text);margin:0 0 12px;}
  .fpp-sub{font-size:16px;color:var(--fp-muted);line-height:1.75;max-width:60ch;margin:0 0 24px;}
  .fpp-actions{display:flex;gap:12px;flex-wrap:wrap;}
  .fpp-section{padding:48px 0 0;}
  .fpp-eyebrow{display:block;font-size:11.5px;font-weight:700;letter-spacing:1.5px;
    text-transform:uppercase;color:var(--fp-cyan);margin-bottom:8px;}
  .fpp-section-title{font-family:Jost,Inter,sans-serif;font-size:28px;font-weight:800;
    color:var(--fp-text);margin:0 0 8px;}
  .fpp-section-sub{font-size:14.5px;color:var(--fp-muted);line-height:1.7;max-width:72ch;margin:0 0 24px;}
  .fpp-cap-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;}
  @media(max-width:768px){.fpp-cap-grid{grid-template-columns:1fr;}}
  .fpp-cap{border-radius:16px;background:var(--fp-surf);border:1px solid var(--fp-line);padding:20px;}
  .fpp-cap-icon{width:40px;height:40px;border-radius:11px;background:rgba(0,209,255,0.1);
    border:1px solid rgba(0,209,255,0.22);display:flex;align-items:center;justify-content:center;
    color:var(--fp-cyan);font-size:16px;margin-bottom:12px;}
  .fpp-cap h4{font-size:15px;font-weight:700;color:var(--fp-text);margin:0 0 6px;}
  .fpp-cap p{font-size:13.5px;color:var(--fp-muted);line-height:1.65;margin:0;}
  .fpp-outcome-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:0;}
  @media(max-width:768px){.fpp-outcome-grid{grid-template-columns:1fr;}}
  .fpp-outcome{border-radius:14px;background:var(--fp-surf);border:1px solid var(--fp-line);
    padding:18px;text-align:center;}
  .fpp-outcome-num{font-family:Jost,Inter,sans-serif;font-size:32px;font-weight:800;
    color:var(--fp-green);display:block;margin-bottom:4px;}
  .fpp-outcome p{font-size:13.5px;color:var(--fp-muted);line-height:1.6;margin:0;}
  .fpp-cta{padding:44px 0 28px;text-align:center;}
  .fpp-cta h2{font-family:Jost,Inter,sans-serif;font-size:28px;font-weight:800;color:var(--fp-text);margin:0 0 10px;}
  .fpp-cta p{font-size:15px;color:var(--fp-muted);margin:0 0 20px;}
</style>
<div class="cs-product-page">
  <section class="fpp-hero">
    <div class="auto-container">
      <div class="fpp-badge"><span class="avail-dot"></span> CloudSignals+RiskOps &mdash; Available Now</div>
      <h1 class="fpp-title">Issues &amp; POA&amp;Ms.<br>Accountable workflows.</h1>
      <p class="fpp-sub">Track remediation issues and Plans of Action &amp; Milestones with clear ownership, approval workflows, and audit-ready reporting — all inside CloudSignals+RiskOps.</p>
      <div class="fpp-actions">
        <a href="https://calendly.com/aivric/cloudsignals-demo" class="cs-btn primary">Book a Demo</a>
        <a href="cloudsignals-pricing.html" class="cs-btn secondary">View Pricing</a>
        <a href="cspm-cloudsignals.html" class="cs-btn ghost">CloudSignals+RiskOps</a>
      </div>
    </div>
  </section>

  <section class="fpp-section">
    <div class="auto-container">
      <span class="fpp-eyebrow">Capabilities</span>
      <h2 class="fpp-section-title">Everything issues and POA&amp;Ms need</h2>
      <p class="fpp-section-sub">From open finding to closed ticket, CloudSignals+RiskOps manages the full remediation lifecycle with accountability at every step.</p>
      <div class="fpp-cap-grid">
        <div class="fpp-cap">
          <div class="fpp-cap-icon"><i class="fas fa-list-alt"></i></div>
          <h4>Issue Tracking</h4>
          <p>Centralized issue registry linked to CloudSignals findings. Every issue has an owner, severity, due date, and status — no spreadsheets.</p>
        </div>
        <div class="fpp-cap">
          <div class="fpp-cap-icon"><i class="fas fa-road"></i></div>
          <h4>Remediation Plans</h4>
          <p>Define milestone-based remediation plans with intermediate checkpoints. Attach evidence at each stage to satisfy auditor and leadership review.</p>
        </div>
        <div class="fpp-cap">
          <div class="fpp-cap-icon"><i class="fas fa-user-check"></i></div>
          <h4>Ownership &amp; Approvals</h4>
          <p>Assign issues to teams or individuals. Approval workflows ensure changes are reviewed before closure — with a complete audit trail.</p>
        </div>
        <div class="fpp-cap">
          <div class="fpp-cap-icon"><i class="fas fa-file-export"></i></div>
          <h4>Audit-Ready Reporting</h4>
          <p>Export POA&amp;M reports formatted for auditors, executives, and compliance frameworks (SOC 2, CMMC, NIST). On-demand and scheduled.</p>
        </div>
        <div class="fpp-cap">
          <div class="fpp-cap-icon"><i class="fas fa-plug"></i></div>
          <h4>ITSM Integration</h4>
          <p>Bidirectional sync with Jira and ServiceNow. Issues opened in CloudSignals become tickets in your ITSM; status flows back automatically.</p>
        </div>
        <div class="fpp-cap">
          <div class="fpp-cap-icon"><i class="fas fa-bell"></i></div>
          <h4>SLA Alerting</h4>
          <p>Define remediation SLAs by severity. Receive alerts when issues are approaching or breaching their target closure date.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="fpp-section">
    <div class="auto-container">
      <span class="fpp-eyebrow">Outcomes</span>
      <h2 class="fpp-section-title">What teams report after deployment</h2>
      <div class="fpp-outcome-grid">
        <div class="fpp-outcome">
          <span class="fpp-outcome-num">60%</span>
          <p>Reduction in average remediation cycle time vs. spreadsheet-based tracking</p>
        </div>
        <div class="fpp-outcome">
          <span class="fpp-outcome-num">100%</span>
          <p>Audit trail coverage — every issue state change logged with user and timestamp</p>
        </div>
        <div class="fpp-outcome">
          <span class="fpp-outcome-num">On-demand</span>
          <p>POA&amp;M and remediation reports for auditors — no manual compilation required</p>
        </div>
      </div>
    </div>
  </section>

  <section class="fpp-section fpp-cta">
    <div class="auto-container">
      <h2>Ready to close findings faster?</h2>
      <p>See how CloudSignals+RiskOps manages issues and POA&amp;Ms from discovery to evidence to closure.</p>
      <div class="fpp-actions" style="justify-content:center">
        <a href="https://calendly.com/aivric/cloudsignals-demo" class="cs-btn primary">Book a Demo</a>
        <a href="cloudsignals-pricing.html" class="cs-btn secondary">Compare plans</a>
      </div>
    </div>
  </section>
</div>"""


# ─────────────────────────────────────────────────────────────────────────────
# SECURITY EXCEPTIONS
# ─────────────────────────────────────────────────────────────────────────────
EXCEPTIONS_CONTENT = ISSUES_CONTENT.replace(
    "Issues &amp; POA&amp;Ms.<br>Accountable workflows.",
    "Security Exceptions.<br>Governed lifecycle."
).replace(
    "Track remediation issues and Plans of Action &amp; Milestones with clear ownership, approval workflows, and audit-ready reporting — all inside CloudSignals+RiskOps.",
    "Govern security exceptions with policy-aligned approvals, evidence requirements, risk scoring, and time-bound controls — so every accepted risk is documented and auditable."
).replace(
    "Everything issues and POA&amp;Ms need",
    "Full exception lifecycle governance"
).replace(
    "From open finding to closed ticket, CloudSignals+RiskOps manages the full remediation lifecycle with accountability at every step.",
    "From exception request to approval, review, and expiry — CloudSignals+RiskOps governs the complete exception lifecycle."
).replace(
    """        <div class="fpp-cap">
          <div class="fpp-cap-icon"><i class="fas fa-list-alt"></i></div>
          <h4>Issue Tracking</h4>
          <p>Centralized issue registry linked to CloudSignals findings. Every issue has an owner, severity, due date, and status — no spreadsheets.</p>
        </div>
        <div class="fpp-cap">
          <div class="fpp-cap-icon"><i class="fas fa-road"></i></div>
          <h4>Remediation Plans</h4>
          <p>Define milestone-based remediation plans with intermediate checkpoints. Attach evidence at each stage to satisfy auditor and leadership review.</p>
        </div>
        <div class="fpp-cap">
          <div class="fpp-cap-icon"><i class="fas fa-user-check"></i></div>
          <h4>Ownership &amp; Approvals</h4>
          <p>Assign issues to teams or individuals. Approval workflows ensure changes are reviewed before closure — with a complete audit trail.</p>
        </div>
        <div class="fpp-cap">
          <div class="fpp-cap-icon"><i class="fas fa-file-export"></i></div>
          <h4>Audit-Ready Reporting</h4>
          <p>Export POA&amp;M reports formatted for auditors, executives, and compliance frameworks (SOC 2, CMMC, NIST). On-demand and scheduled.</p>
        </div>
        <div class="fpp-cap">
          <div class="fpp-cap-icon"><i class="fas fa-plug"></i></div>
          <h4>ITSM Integration</h4>
          <p>Bidirectional sync with Jira and ServiceNow. Issues opened in CloudSignals become tickets in your ITSM; status flows back automatically.</p>
        </div>
        <div class="fpp-cap">
          <div class="fpp-cap-icon"><i class="fas fa-bell"></i></div>
          <h4>SLA Alerting</h4>
          <p>Define remediation SLAs by severity. Receive alerts when issues are approaching or breaching their target closure date.</p>
        </div>""",
    """        <div class="fpp-cap">
          <div class="fpp-cap-icon"><i class="fas fa-book-open"></i></div>
          <h4>Exception Registry</h4>
          <p>A centralized exception log with full request history — who requested it, why, the risk accepted, and when it expires.</p>
        </div>
        <div class="fpp-cap">
          <div class="fpp-cap-icon"><i class="fas fa-check-double"></i></div>
          <h4>Approval Workflow</h4>
          <p>Multi-stage approval flows with mandatory reviewer sign-off. Approvals are logged with identity, timestamp, and rationale.</p>
        </div>
        <div class="fpp-cap">
          <div class="fpp-cap-icon"><i class="fas fa-exclamation-triangle"></i></div>
          <h4>Risk Scoring</h4>
          <p>Every exception carries an automated risk score based on the underlying finding severity, asset criticality, and exception duration.</p>
        </div>
        <div class="fpp-cap">
          <div class="fpp-cap-icon"><i class="fas fa-box"></i></div>
          <h4>Evidence Packs</h4>
          <p>Attach supporting documentation to each exception. Evidence packs are formatted for auditor consumption — ready for SOC 2, PCI-DSS, or CMMC review.</p>
        </div>
        <div class="fpp-cap">
          <div class="fpp-cap-icon"><i class="fas fa-clock"></i></div>
          <h4>Time-Bound Controls</h4>
          <p>Set expiration dates on every exception. Automated reminders prompt owners to review, renew, or close before exceptions lapse silently.</p>
        </div>
        <div class="fpp-cap">
          <div class="fpp-cap-icon"><i class="fas fa-chart-pie"></i></div>
          <h4>Exception Reporting</h4>
          <p>Exception dashboards show open count, aging, risk exposure, and owner accountability — ready for leadership and audit committee review.</p>
        </div>"""
).replace(
    "What teams report after deployment",
    "Governance outcomes"
).replace(
    """        <div class="fpp-outcome">
          <span class="fpp-outcome-num">60%</span>
          <p>Reduction in average remediation cycle time vs. spreadsheet-based tracking</p>
        </div>
        <div class="fpp-outcome">
          <span class="fpp-outcome-num">100%</span>
          <p>Audit trail coverage — every issue state change logged with user and timestamp</p>
        </div>
        <div class="fpp-outcome">
          <span class="fpp-outcome-num">On-demand</span>
          <p>POA&amp;M and remediation reports for auditors — no manual compilation required</p>
        </div>""",
    """        <div class="fpp-outcome">
          <span class="fpp-outcome-num">Zero</span>
          <p>Undocumented exceptions — every accepted risk has an owner, evidence, and expiry</p>
        </div>
        <div class="fpp-outcome">
          <span class="fpp-outcome-num">100%</span>
          <p>Audit trail on all exception approvals — identity, timestamp, and rationale captured</p>
        </div>
        <div class="fpp-outcome">
          <span class="fpp-outcome-num">On-demand</span>
          <p>Exception posture reports for auditors and risk committees — no manual compilation</p>
        </div>"""
).replace(
    "Ready to close findings faster?",
    "Ready to govern exceptions properly?"
).replace(
    "See how CloudSignals+RiskOps manages issues and POA&amp;Ms from discovery to evidence to closure.",
    "See how CloudSignals+RiskOps replaces spreadsheet-based exception tracking with a governed, auditable workflow."
)


# ─────────────────────────────────────────────────────────────────────────────
# THREAT ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
THREAT_CONTENT = """<style>
  :root{--fp-cyan:#00d1ff;--fp-green:#2ee59d;--fp-gold:#ffd63a;--fp-purple:#a78bfa;
    --fp-text:#f8fafc;--fp-muted:#cbd5e1;--fp-surf:rgba(255,255,255,0.06);--fp-line:rgba(148,163,184,0.22);}
  .fpp-hero{padding:90px 0 48px;}
  .fpp-badge{display:inline-flex;align-items:center;gap:8px;padding:6px 14px;border-radius:999px;
    background:rgba(255,214,58,0.12);border:1px solid rgba(255,214,58,0.32);
    color:#f8fafc;font-size:12px;font-weight:700;margin-bottom:14px;}
  .fpp-badge .gold-dot{width:7px;height:7px;border-radius:50%;background:#ffd63a;
    box-shadow:0 0 6px rgba(255,214,58,0.6);}
  .fpp-title{font-family:Jost,Inter,sans-serif;font-size:48px;font-weight:800;
    line-height:1.05;letter-spacing:-1px;color:#f8fafc;margin:0 0 12px;}
  .fpp-sub{font-size:16px;color:#cbd5e1;line-height:1.75;max-width:60ch;margin:0 0 24px;}
  .fpp-actions{display:flex;gap:12px;flex-wrap:wrap;}
  .fpp-section{padding:48px 0 0;}
  .fpp-eyebrow{display:block;font-size:11.5px;font-weight:700;letter-spacing:1.5px;
    text-transform:uppercase;color:var(--fp-cyan);margin-bottom:8px;}
  .fpp-section-title{font-family:Jost,Inter,sans-serif;font-size:28px;font-weight:800;
    color:#f8fafc;margin:0 0 8px;}
  .fpp-section-sub{font-size:14.5px;color:#cbd5e1;line-height:1.7;max-width:72ch;margin:0 0 24px;}
  .fpp-cap-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;}
  @media(max-width:768px){.fpp-cap-grid{grid-template-columns:1fr;}}
  .fpp-cap{border-radius:16px;background:rgba(255,255,255,0.06);border:1px solid rgba(148,163,184,0.22);padding:20px;}
  .fpp-cap-icon{width:40px;height:40px;border-radius:11px;background:rgba(255,214,58,0.1);
    border:1px solid rgba(255,214,58,0.22);display:flex;align-items:center;justify-content:center;
    color:#ffd63a;font-size:16px;margin-bottom:12px;}
  .fpp-cap h4{font-size:15px;font-weight:700;color:#f8fafc;margin:0 0 6px;}
  .fpp-cap p{font-size:13.5px;color:#cbd5e1;line-height:1.65;margin:0;}
  .fpp-outcome-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;}
  @media(max-width:768px){.fpp-outcome-grid{grid-template-columns:1fr;}}
  .fpp-outcome{border-radius:14px;background:rgba(255,255,255,0.06);border:1px solid rgba(148,163,184,0.22);
    padding:18px;text-align:center;}
  .fpp-outcome-num{font-family:Jost,Inter,sans-serif;font-size:32px;font-weight:800;
    color:#ffd63a;display:block;margin-bottom:4px;}
  .fpp-outcome p{font-size:13.5px;color:#cbd5e1;line-height:1.6;margin:0;}
  .fpp-cta{padding:44px 0 28px;text-align:center;}
  .fpp-cta h2{font-family:Jost,Inter,sans-serif;font-size:28px;font-weight:800;color:#f8fafc;margin:0 0 10px;}
  .fpp-cta p{font-size:15px;color:#cbd5e1;margin:0 0 20px;}
</style>
<div class="cs-product-page">
  <section class="fpp-hero">
    <div class="auto-container">
      <div class="fpp-badge"><span class="gold-dot"></span> CloudSignals+RiskOps &mdash; Available Now</div>
      <h1 class="fpp-title">Threat Analysis.<br>Prioritized by business impact.</h1>
      <p class="fpp-sub">Correlate threats, apply business-context risk scoring, and deliver executive-ready intelligence — so your team knows exactly where to focus remediation effort.</p>
      <div class="fpp-actions">
        <a href="https://calendly.com/aivric/cloudsignals-demo" class="cs-btn primary">Book a Demo</a>
        <a href="cloudsignals-pricing.html" class="cs-btn secondary">View Pricing</a>
        <a href="cspm-cloudsignals.html" class="cs-btn ghost">CloudSignals+RiskOps</a>
      </div>
    </div>
  </section>

  <section class="fpp-section">
    <div class="auto-container">
      <span class="fpp-eyebrow">Capabilities</span>
      <h2 class="fpp-section-title">From raw signals to actionable intelligence</h2>
      <p class="fpp-section-sub">CloudSignals+RiskOps correlates findings across all connected providers and layers on business context to surface the threats that matter most.</p>
      <div class="fpp-cap-grid">
        <div class="fpp-cap">
          <div class="fpp-cap-icon"><i class="fas fa-random"></i></div>
          <h4>Threat Correlation</h4>
          <p>Automatically correlate related findings across cloud providers, identities, and assets to surface attack paths and multi-vector exposures.</p>
        </div>
        <div class="fpp-cap">
          <div class="fpp-cap-icon"><i class="fas fa-thermometer-half"></i></div>
          <h4>Risk Scoring</h4>
          <p>Business-context risk scoring combines technical severity, asset criticality, and exposure to rank threats by real-world impact — not just CVSS.</p>
        </div>
        <div class="fpp-cap">
          <div class="fpp-cap-icon"><i class="fas fa-chart-bar"></i></div>
          <h4>Executive Reports</h4>
          <p>Auto-generated threat intelligence reports formatted for C-suite and board — risk posture, top threats, trend lines, and remediation status.</p>
        </div>
        <div class="fpp-cap">
          <div class="fpp-cap-icon"><i class="fas fa-directions"></i></div>
          <h4>Action Guidance</h4>
          <p>Each threat surfaces with step-by-step remediation guidance, affected asset list, and compliance impact — no manual triage required.</p>
        </div>
        <div class="fpp-cap">
          <div class="fpp-cap-icon"><i class="fas fa-satellite-dish"></i></div>
          <h4>Threat Intelligence Integration</h4>
          <p>Enrich findings with external threat intelligence feeds to contextualize exposure against active threat actors and known vulnerabilities.</p>
        </div>
        <div class="fpp-cap">
          <div class="fpp-cap-icon"><i class="fas fa-cogs"></i></div>
          <h4>SOC Workflow Integration</h4>
          <p>Push prioritized threats directly to your SIEM, SOAR, or ticketing system via native integrations with Jira, ServiceNow, Splunk, and more.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="fpp-section">
    <div class="auto-container">
      <span class="fpp-eyebrow">Outcomes</span>
      <h2 class="fpp-section-title">What threat analysis delivers</h2>
      <div class="fpp-outcome-grid">
        <div class="fpp-outcome">
          <span class="fpp-outcome-num">Faster</span>
          <p>Mean time to response — threats surfaced with context and guidance, not raw logs</p>
        </div>
        <div class="fpp-outcome">
          <span class="fpp-outcome-num">Fewer</span>
          <p>Alert fatigue incidents — business-context scoring cuts noise before it reaches the SOC</p>
        </div>
        <div class="fpp-outcome">
          <span class="fpp-outcome-num">Ready</span>
          <p>Executive and board-level threat reporting — on demand, no manual prep required</p>
        </div>
      </div>
    </div>
  </section>

  <section class="fpp-section fpp-cta">
    <div class="auto-container">
      <h2>Ready to prioritize what matters?</h2>
      <p>See how CloudSignals+RiskOps turns raw security signals into business-prioritized threat intelligence.</p>
      <div class="fpp-actions" style="justify-content:center">
        <a href="https://calendly.com/aivric/cloudsignals-demo" class="cs-btn primary">Book a Demo</a>
        <a href="cloudsignals-pricing.html" class="cs-btn secondary">Compare plans</a>
      </div>
    </div>
  </section>
</div>"""


# ─────────────────────────────────────────────────────────────────────────────
# GITHUB SECURITY
# ─────────────────────────────────────────────────────────────────────────────
def page_github():
    h = hero(
        badge_color="cyan", badge_text="GitHub Security &mdash; CloudSignals+RiskOps&#x2122;",
        badge_dot_class="avail-dot",
        title="GitHub Security.<br>Proven to auditors.",
        sub="Secure GitHub repositories, CI/CD pipelines, and dependencies — and generate the evidence your auditors actually need. Continuously.",
        cta1_href="https://calendly.com/aivric/cloudsignals-demo", cta1_text="Request a GitHub Demo",
        cta2_href="cloudsignals-pricing.html", cta2_text="View Pricing",
        quick_items=[
            "Repository &amp; org posture baselines across all repos",
            "Branch protection, MFA, and secret detection checks",
            "Least-privilege access and PAT governance",
            "CI/CD pipeline and supply chain risk scanning",
            "Compliance evidence mapped to SOC 2, ISO 27001, CMMC",
            "Executive reporting on GitHub security posture",
        ],
        rb_items=[
            ("CloudSignals+RiskOps", "Available Now", "avail"),
            ("Connector", "GitHub (PAT, OAuth, GitHub App)", ""),
            ("Scan Frequency", "Every 24 hours", ""),
        ]
    )
    m = modules_section(
        "How it works", "Four areas of GitHub security coverage",
        "CloudSignals+RiskOps continuously monitors your GitHub organization across four key risk areas — from org-level settings to CI/CD supply chain.",
        [
            ("fab fa-github", "cyan", "Repo &amp; Org Posture Baselines",
             "Continuously scan all repositories and org-level settings for security drift and misconfigurations.",
             ["Branch protection enforcement across all repos", "MFA status and admin access reviews", "Public vs. private repo exposure tracking"]),
            ("fas fa-id-badge", "green", "Access Governance &amp; Least Privilege",
             "Identify over-privileged accounts, stale PATs, and outside collaborators with excessive access.",
             ["PAT age, scope, and revocation tracking", "Outside collaborator access reviews", "Bot and service account inventory"]),
            ("fas fa-code-branch", "gold", "Branch Protection &amp; Change Controls",
             "Verify branch protection rules, required reviews, and status checks are enforced across all critical branches.",
             ["Forced push protection status", "Required reviewer and CI check enforcement", "Change approval audit trails"]),
            ("fas fa-boxes", "purple", "CI/CD &amp; Supply Chain Risk",
             "Scan GitHub Actions workflows and dependencies for unpinned actions, vulnerable packages, and exposed secrets.",
             ["Action pinning and version drift", "Dependency vulnerability status (Dependabot)", "Secret scanner findings and exposure"]),
        ]
    )
    c = caps_section(
        "Capabilities", "End-to-end GitHub security capabilities",
        [
            ("fas fa-sliders-h", "Posture Baselines", "Define and continuously enforce GitHub security baselines across repositories and org settings."),
            ("fas fa-user-shield", "Access Reviews", "Automated access reviews for admins, outside collaborators, and service accounts — with evidence."),
            ("fas fa-code-branch", "Branch Protection", "Verify branch protection rules are configured and enforced on all critical branches."),
            ("fas fa-key", "Secret Detection", "Surface secret scanner findings and track remediation — before credentials become incidents."),
            ("fas fa-box-open", "Supply Chain Audit", "Scan dependencies and GitHub Actions for vulnerable versions and unpinned references."),
            ("fas fa-clipboard-check", "Compliance Evidence", "Map GitHub security checks directly to SOC 2, ISO 27001, and CMMC control requirements."),
        ]
    )
    fw = frameworks_section(
        "Compliance", "Frameworks evidenced by GitHub security checks",
        [
            ("fas fa-shield-alt", "SOC 2 (Change Management &amp; CC6)", "Mapped",
             ["CC6.2 — Logical access and MFA enforcement", "CC6.7 — Branch protection and change approval", "CC7.2 — Secret detection and response"]),
            ("fas fa-globe", "ISO/IEC 27001 (A.12, A.14)", "Mapped",
             ["A.12.1.2 — Change management controls", "A.14.2.5 — Secure software development", "A.14.2.8 — Testing of security functionality"]),
            ("fas fa-shield-alt", "CMMC Level 2 / NIST 800-171", "Mapped",
             ["3.4.2 — Establish configuration baselines", "3.4.5 — Define and document access restrictions", "3.13.13 — Control and monitor use of mobile code"]),
            ("fas fa-cog", "CIS Software Supply Chain", "Covered",
             ["Branch protection and review requirements", "Action pinning and version controls", "Token and secret hygiene"]),
        ]
    )
    cta = bottom_cta_section(
        "Ready to secure GitHub end to end?",
        "Connect CloudSignals+RiskOps to GitHub and get continuous posture monitoring, evidence, and executive reporting.",
        "https://calendly.com/aivric/cloudsignals-demo", "Schedule a GitHub Security Demo"
    )
    return h + "\n" + m + "\n" + c + "\n" + fw + "\n" + cta


# ─────────────────────────────────────────────────────────────────────────────
# ABOUT
# ─────────────────────────────────────────────────────────────────────────────
ABOUT_CONTENT = """<style>
  :root{--ab-cyan:#00d1ff;--ab-green:#2ee59d;--ab-gold:#ffd63a;--ab-purple:#a78bfa;
    --ab-text:#f8fafc;--ab-muted:#cbd5e1;--ab-faint:#94a3b8;
    --ab-surf:rgba(255,255,255,0.06);--ab-line:rgba(148,163,184,0.22);}
  .abp-hero{padding:100px 0 56px;text-align:center;}
  .abp-badge{display:inline-flex;align-items:center;gap:8px;padding:7px 16px;border-radius:999px;
    background:rgba(0,209,255,0.12);border:1px solid rgba(0,209,255,0.3);
    color:var(--ab-text);font-size:12px;font-weight:700;margin-bottom:18px;}
  .abp-title{font-family:Jost,Inter,sans-serif;font-size:52px;font-weight:800;
    line-height:1.04;letter-spacing:-1.2px;color:var(--ab-text);margin:0 0 16px;}
  @media(max-width:768px){.abp-title{font-size:36px;}}
  .abp-sub{font-size:18px;color:var(--ab-muted);line-height:1.75;max-width:66ch;margin:0 auto 28px;}
  .abp-actions{display:flex;gap:12px;flex-wrap:wrap;justify-content:center;}
  .abp-section{padding:52px 0 0;}
  .abp-eyebrow{display:block;font-size:12px;font-weight:700;letter-spacing:1.5px;
    text-transform:uppercase;color:var(--ab-cyan);margin-bottom:8px;text-align:center;}
  .abp-section-title{font-family:Jost,Inter,sans-serif;font-size:30px;font-weight:800;
    color:var(--ab-text);margin:0 0 8px;text-align:center;}
  .abp-section-sub{font-size:15px;color:var(--ab-muted);line-height:1.75;max-width:72ch;
    margin:0 auto 28px;text-align:center;}
  .abp-what-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;}
  @media(max-width:900px){.abp-what-grid{grid-template-columns:1fr;}}
  .abp-what-card{border-radius:18px;background:var(--ab-surf);border:1px solid var(--ab-line);
    padding:24px;display:flex;flex-direction:column;gap:12px;}
  .abp-what-icon{width:48px;height:48px;border-radius:14px;
    display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0;}
  .abp-what-icon.cyan{background:rgba(0,209,255,0.12);border:1px solid rgba(0,209,255,0.28);color:var(--ab-cyan);}
  .abp-what-icon.green{background:rgba(46,229,157,0.12);border:1px solid rgba(46,229,157,0.28);color:var(--ab-green);}
  .abp-what-icon.gold{background:rgba(255,214,58,0.12);border:1px solid rgba(255,214,58,0.28);color:var(--ab-gold);}
  .abp-what-card h3{font-size:18px;font-weight:700;color:var(--ab-text);margin:0;}
  .abp-what-card p{font-size:14px;color:var(--ab-muted);line-height:1.7;margin:0;flex:1;}
  .abp-value-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;}
  @media(max-width:768px){.abp-value-grid{grid-template-columns:1fr;}}
  .abp-value-card{border-radius:16px;background:var(--ab-surf);border:1px solid var(--ab-line);padding:20px;}
  .abp-value-card h4{font-size:15px;font-weight:700;color:var(--ab-text);margin:0 0 8px;
    display:flex;align-items:center;gap:10px;}
  .abp-value-card h4 i{color:var(--ab-cyan);font-size:14px;}
  .abp-value-card p{font-size:13.5px;color:var(--ab-muted);line-height:1.7;margin:0;}
  .abp-mission{border-radius:18px;
    background:linear-gradient(135deg,rgba(0,89,255,0.12) 0%,rgba(0,209,255,0.06) 100%);
    border:1px solid rgba(0,89,255,0.2);padding:36px 40px;text-align:center;margin-top:24px;}
  .abp-mission p{font-size:17px;color:var(--ab-muted);line-height:1.8;max-width:72ch;margin:0 auto;}
  .abp-mission strong{color:var(--ab-text);}
  .abp-cta{padding:52px 0 24px;text-align:center;}
  .abp-cta h2{font-family:Jost,Inter,sans-serif;font-size:28px;font-weight:800;color:var(--ab-text);margin:0 0 10px;}
  .abp-cta p{font-size:15px;color:var(--ab-muted);margin:0 0 20px;}
</style>
<div class="cs-product-page">
  <section class="abp-hero">
    <div class="auto-container">
      <div class="abp-badge"><i class="fas fa-building"></i> Company</div>
      <h1 class="abp-title">We built AiVRIC because<br>security deserved better.</h1>
      <p class="abp-sub">AiVRIC is an enterprise security operations platform that unifies cloud security, AI governance, compliance automation, and offensive security into one continuously operating system.</p>
      <div class="abp-actions">
        <a href="why-aivric.html" class="cs-btn primary">Why AiVRIC</a>
        <a href="cspm-cloudsignals.html" class="cs-btn secondary">Our Platform</a>
      </div>
    </div>
  </section>

  <section class="abp-section">
    <div class="auto-container">
      <div class="abp-mission">
        <p><strong>Our mission</strong> is to make autonomous, continuous security and compliance accessible to every organization that runs in the cloud &mdash; so that security teams spend their energy on decisions, not documentation.</p>
      </div>
    </div>
  </section>

  <section class="abp-section">
    <div class="auto-container">
      <span class="abp-eyebrow">What we do</span>
      <h2 class="abp-section-title">Three capabilities. One platform.</h2>
      <p class="abp-section-sub">AiVRIC brings together the capabilities that modern security and compliance teams need — built to work together, not bolted together.</p>
      <div class="abp-what-grid">
        <div class="abp-what-card">
          <div class="abp-what-icon cyan"><i class="fas fa-cloud"></i></div>
          <h3>Cloud Security &amp; GRC</h3>
          <p>CloudSignals+RiskOps delivers continuous cloud security posture management, automated compliance evidence, risk register intelligence, and AI-generated audit narratives across AWS, Azure, GCP, Kubernetes, and more.</p>
          <a href="cspm-cloudsignals.html" style="font-size:13px;font-weight:700;color:#00d1ff;">Explore CloudSignals &rarr;</a>
        </div>
        <div class="abp-what-card">
          <div class="abp-what-icon green"><i class="fas fa-robot"></i></div>
          <h3>AI Signal Intelligence</h3>
          <p>AI Signals&trade; monitors AI models, agents, and pipelines for security and compliance risk. REDTEAM testing, MCP governance, OWASP LLM TOP 10 compliance, and real-time observability for your AI stack.</p>
          <a href="ai-inspector.html" style="font-size:13px;font-weight:700;color:#2ee59d;">Explore AI Signals &rarr;</a>
        </div>
        <div class="abp-what-card">
          <div class="abp-what-icon gold"><i class="fas fa-crosshairs"></i></div>
          <h3>Offensive Security</h3>
          <p>RogueAgent ASPM&trade; maps your enterprise attack surface continuously, identifies exploitable paths, and delivers evidence your teams can act on — without waiting for an annual pen test.</p>
          <a href="rogueagent.html" style="font-size:13px;font-weight:700;color:#ffd63a;">Explore RogueAgent &rarr;</a>
        </div>
      </div>
    </div>
  </section>

  <section class="abp-section">
    <div class="auto-container">
      <span class="abp-eyebrow">Why we're different</span>
      <h2 class="abp-section-title">Built for the way security teams actually work</h2>
      <p class="abp-section-sub">AiVRIC was designed by practitioners who ran security programs at scale. Every design decision reflects real-world trade-offs.</p>
      <div class="abp-value-grid">
        <div class="abp-value-card">
          <h4><i class="fas fa-infinity"></i> Continuous by default</h4>
          <p>Everything in AiVRIC runs continuously — posture monitoring, evidence collection, compliance scoring, threat analysis. No manual cycles, no point-in-time snapshots.</p>
        </div>
        <div class="abp-value-card">
          <h4><i class="fas fa-brain"></i> AI-powered throughout</h4>
          <p>Lighthouse AI generates audit narratives, prioritizes risk by business context, and surfaces intelligence that would take analysts hours to produce manually.</p>
        </div>
        <div class="abp-value-card">
          <h4><i class="fas fa-layer-group"></i> Unified data layer</h4>
          <p>One shared data layer connects cloud posture, AI risk, offensive findings, and compliance state — so your teams work from a single source of truth.</p>
        </div>
        <div class="abp-value-card">
          <h4><i class="fas fa-users-cog"></i> Built by practitioners</h4>
          <p>AiVRIC was founded by 3HUE Security, a security advisory firm that has led security programs at enterprise scale. Every feature solves a problem we lived.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="abp-section abp-cta">
    <div class="auto-container">
      <h2>Let's talk.</h2>
      <p>Whether you're exploring CloudSignals+RiskOps, AI Signals, or the full platform — we'd like to show you what it does.</p>
      <div class="abp-actions">
        <a href="https://calendly.com/aivric/cloudsignals-demo" class="cs-btn primary">Book a Demo</a>
        <a href="contact.html" class="cs-btn secondary">Contact us</a>
      </div>
    </div>
  </section>
</div>"""


# ─────────────────────────────────────────────────────────────────────────────
# WHY AIVRIC
# ─────────────────────────────────────────────────────────────────────────────
WHY_CONTENT = """<style>
  :root{--wy-cyan:#00d1ff;--wy-green:#2ee59d;--wy-gold:#ffd63a;--wy-purple:#a78bfa;
    --wy-text:#f8fafc;--wy-muted:#cbd5e1;--wy-faint:#94a3b8;
    --wy-surf:rgba(255,255,255,0.06);--wy-line:rgba(148,163,184,0.22);}
  .wyp-hero{padding:100px 0 56px;text-align:center;}
  .wyp-badge{display:inline-flex;align-items:center;gap:8px;padding:7px 16px;border-radius:999px;
    background:rgba(46,229,157,0.12);border:1px solid rgba(46,229,157,0.3);
    color:var(--wy-text);font-size:12px;font-weight:700;margin-bottom:18px;}
  .wyp-title{font-family:Jost,Inter,sans-serif;font-size:52px;font-weight:800;
    line-height:1.04;letter-spacing:-1.2px;color:var(--wy-text);margin:0 0 16px;}
  @media(max-width:768px){.wyp-title{font-size:36px;}}
  .wyp-sub{font-size:18px;color:var(--wy-muted);line-height:1.75;max-width:66ch;margin:0 auto 28px;}
  .wyp-actions{display:flex;gap:12px;flex-wrap:wrap;justify-content:center;}
  .wyp-section{padding:52px 0 0;}
  .wyp-eyebrow{display:block;font-size:12px;font-weight:700;letter-spacing:1.5px;
    text-transform:uppercase;color:var(--wy-cyan);margin-bottom:8px;text-align:center;}
  .wyp-section-title{font-family:Jost,Inter,sans-serif;font-size:30px;font-weight:800;
    color:var(--wy-text);margin:0 0 10px;text-align:center;}
  .wyp-section-sub{font-size:15px;color:var(--wy-muted);line-height:1.75;max-width:72ch;
    margin:0 auto 28px;text-align:center;}
  .wyp-adv-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;}
  @media(max-width:768px){.wyp-adv-grid{grid-template-columns:1fr;}}
  .wyp-adv{border-radius:18px;background:var(--wy-surf);border:1px solid var(--wy-line);padding:24px;}
  .wyp-adv-num{font-family:Jost,Inter,sans-serif;font-size:13px;font-weight:800;
    color:var(--wy-cyan);text-transform:uppercase;letter-spacing:0.8px;margin-bottom:10px;display:block;}
  .wyp-adv h3{font-size:18px;font-weight:700;color:var(--wy-text);margin:0 0 8px;}
  .wyp-adv p{font-size:14px;color:var(--wy-muted);line-height:1.7;margin:0;}
  .wyp-problem{border-radius:18px;
    background:linear-gradient(135deg,rgba(167,139,250,0.10) 0%,rgba(0,209,255,0.06) 100%);
    border:1px solid rgba(167,139,250,0.2);padding:36px 40px;margin-top:0;}
  .wyp-problem h3{font-family:Jost,Inter,sans-serif;font-size:22px;font-weight:800;
    color:var(--wy-text);margin:0 0 12px;}
  .wyp-problem p{font-size:15px;color:var(--wy-muted);line-height:1.75;margin:0 0 12px;}
  .wyp-problem p:last-child{margin:0;}
  .wyp-targets{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:0;}
  @media(max-width:768px){.wyp-targets{grid-template-columns:1fr;}}
  .wyp-target{border-radius:14px;background:var(--wy-surf);border:1px solid var(--wy-line);
    padding:16px;display:flex;align-items:center;gap:12px;}
  .wyp-target i{color:var(--wy-green);font-size:18px;flex-shrink:0;}
  .wyp-target span{font-size:14px;color:var(--wy-muted);line-height:1.5;}
  .wyp-cta{padding:52px 0 24px;text-align:center;}
  .wyp-cta h2{font-family:Jost,Inter,sans-serif;font-size:28px;font-weight:800;color:var(--wy-text);margin:0 0 10px;}
  .wyp-cta p{font-size:15px;color:var(--wy-muted);margin:0 0 20px;}
</style>
<div class="cs-product-page">
  <section class="wyp-hero">
    <div class="auto-container">
      <div class="wyp-badge"><i class="fas fa-star"></i> The AiVRIC Difference</div>
      <h1 class="wyp-title">Security and compliance<br>should work as one.</h1>
      <p class="wyp-sub">Most organizations run security and compliance as two separate, largely manual operations. AiVRIC unifies them into a single, continuously operating, AI-powered platform.</p>
      <div class="wyp-actions">
        <a href="cspm-cloudsignals.html" class="cs-btn primary">Explore the platform</a>
        <a href="https://calendly.com/aivric/cloudsignals-demo" class="cs-btn secondary">Book a demo</a>
      </div>
    </div>
  </section>

  <section class="wyp-section">
    <div class="auto-container">
      <div class="wyp-problem">
        <h3>The problem we set out to solve</h3>
        <p>Security operations are fragmented. Cloud posture tools, compliance platforms, evidence trackers, pen testing services, and AI monitoring tools — each working in isolation, each generating its own findings, each requiring its own workflow.</p>
        <p>The result is teams that spend more time correlating tools than acting on intelligence. Auditors that wait weeks for evidence that should be available in seconds. Leadership that can't get a clear answer on overall risk posture without a two-week project.</p>
        <p>AiVRIC exists to fix that. One platform. Continuous operation. Unified intelligence.</p>
      </div>
    </div>
  </section>

  <section class="wyp-section">
    <div class="auto-container">
      <span class="wyp-eyebrow">The AiVRIC Advantage</span>
      <h2 class="wyp-section-title">Four principles behind every decision</h2>
      <p class="wyp-section-sub">Every product decision, every feature, and every integration is built against these four principles.</p>
      <div class="wyp-adv-grid">
        <div class="wyp-adv">
          <span class="wyp-adv-num">01</span>
          <h3>Unified offense, defense, and compliance</h3>
          <p>AiVRIC connects cloud security posture, AI model risk, offensive security findings, and compliance state into a single data layer. What one module discovers, all modules act on.</p>
        </div>
        <div class="wyp-adv">
          <span class="wyp-adv-num">02</span>
          <h3>AI-powered risk &amp; compliance intelligence</h3>
          <p>Lighthouse AI generates audit narratives, risk summaries, and remediation guidance automatically. Intelligence that would take your team hours is ready in seconds — and gets better over time.</p>
        </div>
        <div class="wyp-adv">
          <span class="wyp-adv-num">03</span>
          <h3>Continuous, autonomous evidence collection</h3>
          <p>Evidence is collected continuously and automatically from every connected provider — timestamped, mapped to controls, and packaged for auditors. No manual screenshots. No last-minute scrambles.</p>
        </div>
        <div class="wyp-adv">
          <span class="wyp-adv-num">04</span>
          <h3>Security as a business enabler</h3>
          <p>AiVRIC translates technical risk into business language — so CISOs can brief the board, auditors can get what they need, and developers can ship with confidence. Security that accelerates, not blocks.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="wyp-section">
    <div class="auto-container">
      <span class="wyp-eyebrow">Who it's for</span>
      <h2 class="wyp-section-title">Designed for modern environments</h2>
      <p class="wyp-section-sub">AiVRIC is purpose-built for organizations that operate in the cloud, use AI in production, and need security and compliance to scale with them.</p>
      <div class="wyp-targets">
        <div class="wyp-target"><i class="fas fa-cloud"></i><span>Multi-cloud organizations (AWS, Azure, GCP)</span></div>
        <div class="wyp-target"><i class="fas fa-robot"></i><span>Teams running AI models or agents in production</span></div>
        <div class="wyp-target"><i class="fas fa-shield-alt"></i><span>Security teams under SOC 2, PCI-DSS, or CMMC requirements</span></div>
        <div class="wyp-target"><i class="fas fa-code-branch"></i><span>Engineering-led organizations with GitHub and CI/CD pipelines</span></div>
        <div class="wyp-target"><i class="fas fa-chart-line"></i><span>Companies scaling fast and needing compliance to keep pace</span></div>
        <div class="wyp-target"><i class="fas fa-user-tie"></i><span>CISOs who need board-level risk reporting without manual prep</span></div>
      </div>
    </div>
  </section>

  <section class="wyp-section wyp-cta">
    <div class="auto-container">
      <h2>Ready to see it in action?</h2>
      <p>Explore what AiVRIC looks like for your cloud, compliance, and AI environment.</p>
      <div class="wyp-actions">
        <a href="https://calendly.com/aivric/cloudsignals-demo" class="cs-btn primary">Book a Demo</a>
        <a href="cspm-cloudsignals.html" class="cs-btn secondary">Explore the platform</a>
      </div>
    </div>
  </section>
</div>"""


# ─────────────────────────────────────────────────────────────────────────────
# PART 2 — USER GUIDE
# ─────────────────────────────────────────────────────────────────────────────

GUIDE_SIDEBAR_HTML = guide_sidebar()  # no active item (set per-page via JS)

def upgrade_policy_page(filepath):
    """Convert a policy-main page to guide-shell layout with sidebar."""
    raw = filepath.read_text(encoding="utf-8")
    if "guide-shell" in raw:
        return False  # already upgraded

    # Fix header brand (add logo image if missing)
    raw = raw.replace(
        '<a class="brand" href="index.html"><span class="dot"></span>AiVRIC User Guide</a>',
        '<a class="brand" href="index.html"><img src="../assets/images/logo/aivric.svg" alt="AiVRIC logo"><span>Platform Guide</span></a>'
    )

    # Replace policy-main with guide-shell + sidebar + guide-content
    # Extract: everything inside <main class="policy-main">...</main>
    m = re.search(r'<main class="policy-main">(.*?)</main>', raw, re.DOTALL)
    if not m:
        return False
    inner = m.group(1)

    # Build new body structure
    new_main = f"""  <div class="guide-shell">
{GUIDE_SIDEBAR_HTML}

    <main class="guide-content">
{inner}    </main>
  </div>"""

    raw = raw[:m.start()] + new_main + raw[m.end():]

    # Patch the policy classes to guide classes for better styling
    raw = raw.replace('class="policy-hero"', 'class="policy-hero" style="margin-bottom:16px"')
    raw = raw.replace('class="policy-section"', 'class="guide-section"')
    raw = raw.replace('class="policy-card"', 'class="guide-card"')
    raw = raw.replace('class="policy-list"', 'class="policy-list guide-content-list"')

    # Add the nav active JS before </body>
    raw = raw.replace("</body>", GUIDE_SCRIPT + "\n</body>")
    filepath.write_text(raw, encoding="utf-8")
    return True


def update_guide_header(filepath):
    """Update guide-shell pages that are missing the logo image in the brand."""
    raw = filepath.read_text(encoding="utf-8")
    if '<img' in raw[:3000]:
        return False  # already has logo
    raw = raw.replace(
        '<a class="brand" href="index.html"><span class="dot"></span>AiVRIC User Guide</a>',
        '<a class="brand" href="index.html"><img src="../assets/images/logo/aivric.svg" alt="AiVRIC logo"><span>Platform Guide</span></a>'
    )
    if raw.startswith(raw):  # no-op guard
        filepath.write_text(raw, encoding="utf-8")
        return True
    return False


DARK_HEADER_CSS = """
/* ─── Dark guide header (design-system update 2026-05) ─── */
.guide-header {
  background: rgba(5, 10, 20, 0.96) !important;
  backdrop-filter: blur(18px);
  border-bottom: 1px solid rgba(148,163,184,0.12) !important;
  box-shadow: 0 4px 24px rgba(0,0,0,0.4) !important;
}
.brand { color: var(--text) !important; }
.brand span { color: var(--text) !important; }
.top-links a { color: var(--muted) !important; border-color: transparent !important; }
.top-links a:hover {
  color: var(--accent) !important;
  border-color: rgba(9,211,251,0.3) !important;
  background: rgba(9,211,251,0.07) !important;
}
.guide-search {
  background: rgba(255,255,255,0.05) !important;
  border-color: rgba(255,255,255,0.1) !important;
  color: var(--text) !important;
}
.guide-search input { color: var(--text) !important; }
.guide-search input::placeholder { color: var(--muted) !important; }
.guide-search i { color: var(--muted) !important; }
.nav-toggle {
  background: rgba(255,255,255,0.06) !important;
  border-color: rgba(255,255,255,0.12) !important;
  color: var(--text) !important;
}
/* guide-content heading colors */
.guide-content h1, .guide-content h2, .guide-content h3 { color: #f4f8ff; }
"""


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    # ── Part 1: Marketing pages ────────────────────────────────────────────────
    pages = [
        ("streamline-soc2.html",
         "SOC 2 Automation | Continuous Controls &amp; Evidence | AiVRIC CloudSignals",
         "Automate SOC 2 readiness with continuous controls monitoring, automated evidence collection, and AI-generated audit narratives from AiVRIC CloudSignals+RiskOps.",
         page_soc2()),
        ("achieve-pci-dss.html",
         "PCI-DSS Compliance Automation | Continuous Monitoring | AiVRIC CloudSignals",
         "Automate PCI-DSS compliance with scope discovery, continuous monitoring, and QSA-ready evidence from AiVRIC CloudSignals+RiskOps.",
         page_pcidss()),
        ("cmmc-readiness.html",
         "CMMC Level 2 Readiness | NIST 800-171 Automation | AiVRIC CloudSignals",
         "Operationalize CMMC Level 2 readiness with continuous NIST SP 800-171 verification, dynamic SSP and POA&M support from AiVRIC CloudSignals+RiskOps.",
         page_cmmc()),
        ("issues-poams.html",
         "Issues &amp; POA&amp;Ms | Accountable Remediation Workflows | AiVRIC",
         "Track remediation issues and POA&Ms with accountable workflows, ITSM integration, and audit-ready reporting inside AiVRIC CloudSignals+RiskOps.",
         ISSUES_CONTENT),
        ("security-exceptions.html",
         "Security Exceptions | Governed Exception Lifecycle | AiVRIC",
         "Govern security exceptions with policy-aligned approvals, risk scoring, evidence packs, and time-bound controls in AiVRIC CloudSignals+RiskOps.",
         EXCEPTIONS_CONTENT),
        ("threat-analysis.html",
         "Threat Analysis | Business-Prioritized Risk Intelligence | AiVRIC",
         "Correlate threats and prioritize remediation by business impact with threat analysis from AiVRIC CloudSignals+RiskOps.",
         THREAT_CONTENT),
        ("use-case-github-security.html",
         "GitHub Security | Continuous Posture &amp; Compliance Evidence | AiVRIC",
         "Secure GitHub repositories, access, branch protections, and CI/CD pipelines — with continuous posture monitoring and auditor-ready evidence from AiVRIC.",
         page_github()),
        ("about.html",
         "About AiVRIC | Autonomous Security, Compliance &amp; AI Risk Platform",
         "AiVRIC is an enterprise security operations platform unifying cloud security, AI governance, compliance automation, and offensive security.",
         ABOUT_CONTENT),
        ("why-aivric.html",
         "Why AiVRIC | Unified Security &amp; Compliance Platform",
         "Why AiVRIC exists: unified offense, defense, and compliance into one AI-powered platform for modern cloud environments.",
         WHY_CONTENT),
    ]

    for filename, title, desc, content in pages:
        path = SITE / filename
        html = make_page(title, desc, content)
        path.write_text(html, encoding="utf-8")
        print(f"[OK] Rebuilt: {filename}")

    # ── Part 2: UserGuide CSS dark header ─────────────────────────────────────
    ug_css = UG / "userguide.css"
    css_content = ug_css.read_text(encoding="utf-8-sig")
    if "Dark guide header" not in css_content:
        css_content += DARK_HEADER_CSS
        ug_css.write_text(css_content, encoding="utf-8")
        print("[OK] userguide.css: dark header CSS appended")
    else:
        print("[--] userguide.css: dark header already present")

    # ── Part 3: UserGuide stub pages → guide-shell ────────────────────────────
    ug_pages = sorted(UG.glob("*.html"))
    upgraded = 0
    logo_fixed = 0

    for p in ug_pages:
        content = p.read_text(encoding="utf-8", errors="replace")
        if "policy-main" in content:
            if upgrade_policy_page(p):
                upgraded += 1
                print(f"  Upgraded: {p.name}")
        elif "guide-shell" in content or "handbook-main" in content:
            # Fix missing logo in brand
            raw = p.read_text(encoding="utf-8")
            if '<span class="dot"></span>' in raw:
                raw = raw.replace(
                    '<a class="brand" href="index.html"><span class="dot"></span>AiVRIC User Guide</a>',
                    '<a class="brand" href="index.html"><img src="../assets/images/logo/aivric.svg" alt="AiVRIC logo"><span>Platform Guide</span></a>'
                )
                p.write_text(raw, encoding="utf-8")
                logo_fixed += 1

    print(f"[OK] UserGuide: {upgraded} stub pages upgraded to guide-shell")
    print(f"[OK] UserGuide: {logo_fixed} pages logo-brand fixed")
    print("\n[OK] All done.")


if __name__ == "__main__":
    main()
