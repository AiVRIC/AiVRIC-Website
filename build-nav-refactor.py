#!/usr/bin/env python3
"""
AiVRIC Website – Navigation Refactor
- Appends CloudSignals mega-menu CSS to custom.css
- Creates 6 CloudSignals feature pages from the cspm template
- Renames "Solutions" → "Portfolio" on all pages
- Removes Blogs main-nav <li> block from all pages
- Adds blog links to Resources dropdown
- Inserts CloudSignals+RiskOps mega-menu between Platform and Portfolio
"""

import os, re, sys
from pathlib import Path

SITE = Path(r"C:\Projects\AiVRIC-Website")
TEMPLATE = SITE / "cspm-cloudsignals.html"

# ── 1. CSS ────────────────────────────────────────────────────────────────────
MEGA_CSS = r"""

/* ─────────────────────────────────────────────────────────────────────────────
   CloudSignals+RiskOps Product Mega-menu  (nav refactor 2026-05)
───────────────────────────────────────────────────────────────────────────── */
.cs-product-menu > a { color:#00d1ff !important; font-weight:600 !important; }
.cs-product-megamenu {
  position:absolute; top:100%; left:50%; transform:translateX(-50%);
  width:940px; background:#0d1726;
  border:1px solid rgba(0,209,255,0.25); border-radius:16px;
  box-shadow:0 24px 60px rgba(0,0,0,0.5),0 0 0 1px rgba(0,209,255,0.06);
  padding:0; z-index:200; display:none; overflow:hidden;
}
.cs-product-menu:hover .cs-product-megamenu,
.cs-product-menu.is-open .cs-product-megamenu { display:block; }
.cs-mega-hdr {
  display:flex; align-items:center; justify-content:space-between;
  padding:18px 24px 14px;
  border-bottom:1px solid rgba(0,209,255,0.12);
  background:linear-gradient(135deg,rgba(0,209,255,0.07),rgba(46,229,157,0.03));
}
.cs-mega-hdr-info { flex:1; }
.cs-mega-hdr h3 { font-family:Jost,sans-serif; font-size:16px; font-weight:800; color:#f8fafc; margin:4px 0 2px; }
.cs-mega-hdr p { font-size:12px; color:#94a3b8; margin:0; max-width:42ch; line-height:1.5; }
.cs-mega-status {
  display:inline-flex; align-items:center; gap:6px;
  font-size:10.5px; font-weight:700; letter-spacing:1px;
  text-transform:uppercase; color:#2ee59d; margin-bottom:3px;
}
.cs-avail-dot {
  width:7px; height:7px; background:#2ee59d; border-radius:50%;
  animation:cs-pulse-green 2s infinite; flex-shrink:0;
}
@keyframes cs-pulse-green {
  0%,100%{box-shadow:0 0 0 0 rgba(46,229,157,0.6);}
  50%{box-shadow:0 0 0 5px rgba(46,229,157,0);}
}
.cs-mega-pricing-cta {
  font-size:12px; font-weight:700; color:#00d1ff !important;
  text-decoration:none !important; white-space:nowrap;
  padding:7px 14px; border:1px solid rgba(0,209,255,0.4);
  border-radius:8px; transition:background 0.2s; flex-shrink:0;
}
.cs-mega-pricing-cta:hover { background:rgba(0,209,255,0.12); }
.cs-mega-body {
  display:grid; grid-template-columns:repeat(3,1fr);
  padding:18px 0; border-bottom:1px solid rgba(148,163,184,0.1);
}
.cs-mega-col { padding:0 20px; }
.cs-mega-col+.cs-mega-col { border-left:1px solid rgba(148,163,184,0.1); }
.cs-mega-col-label {
  display:block; font-size:10px; font-weight:700;
  letter-spacing:1.2px; text-transform:uppercase; color:#475569; margin-bottom:10px;
}
.cs-mega-feat-card {
  display:flex; align-items:flex-start; gap:11px;
  padding:9px 10px; border-radius:9px;
  text-decoration:none !important; transition:background 0.15s; margin-bottom:2px;
}
.cs-mega-feat-card:hover { background:rgba(255,255,255,0.06); }
.cs-mega-feat-card>i { font-size:14px; color:#00d1ff; margin-top:2px; flex-shrink:0; width:16px; text-align:center; }
.cs-mega-feat-card strong { display:block; font-size:12.5px; font-weight:700; color:#f1f5f9; line-height:1.3; margin-bottom:1px; }
.cs-mega-feat-card span { display:block; font-size:11px; color:#94a3b8; line-height:1.4; }
.cs-mega-ftr {
  display:flex; align-items:center; justify-content:space-between;
  padding:12px 24px; background:rgba(0,0,0,0.15);
}
.cs-mega-ftr-link { font-size:11.5px; color:#64748b; text-decoration:none; }
.cs-mega-ftr-link:hover { color:#94a3b8; text-decoration:none; }
.cs-mega-ftr-ctas { display:flex; gap:8px; }
.cs-mega-btn-primary {
  font-size:11.5px; font-weight:700; color:#0a1628 !important;
  background:#00d1ff; border-radius:7px; padding:7px 14px;
  text-decoration:none !important; transition:background 0.2s;
}
.cs-mega-btn-primary:hover { background:#24ddff; }
.cs-mega-btn-ghost {
  font-size:11.5px; font-weight:600; color:#e2e8f0 !important;
  border:1px solid rgba(148,163,184,0.28); border-radius:7px; padding:7px 14px;
  text-decoration:none !important; transition:border-color 0.2s;
}
.cs-mega-btn-ghost:hover { border-color:rgba(148,163,184,0.55); }

/* ─────────────────────────────────────────────────────────────────────────────
   CloudSignals Feature Pages (.csfp-*)  (nav refactor 2026-05)
───────────────────────────────────────────────────────────────────────────── */
.csfp-page { background:#080f1c; min-height:60vh; }
.csfp-hero { padding:80px 0 56px; }
.csfp-hero-inner { display:grid; grid-template-columns:1fr 160px; gap:32px; align-items:center; }
@media(max-width:900px){ .csfp-hero-inner{grid-template-columns:1fr;} .csfp-hero-icon-wrap{display:none;} }
.csfp-hero-icon-wrap { font-size:96px; opacity:0.12; text-align:center; }
.csfp-breadcrumb { display:flex; gap:8px; align-items:center; font-size:12px; color:#64748b; margin-bottom:20px; }
.csfp-breadcrumb a { color:#64748b; text-decoration:none; }
.csfp-breadcrumb a:hover { color:#94a3b8; }
.csfp-breadcrumb span { color:#334155; }
.csfp-badge {
  display:inline-flex; align-items:center; gap:8px;
  padding:6px 14px; border-radius:999px; border:1px solid;
  font-size:12px; font-weight:600; margin-bottom:14px;
}
.csfp-avail-dot { width:6px; height:6px; border-radius:50%; }
.csfp-title { font-family:Jost,sans-serif; font-size:42px; font-weight:800; color:#f8fafc; margin:0 0 4px; letter-spacing:-0.5px; line-height:1.15; }
@media(max-width:768px){ .csfp-title{font-size:30px;} }
.csfp-subtitle { font-size:14px; font-weight:700; letter-spacing:0.5px; text-transform:uppercase; margin:0 0 14px; }
.csfp-lead { font-size:16px; color:#cbd5e1; line-height:1.75; max-width:62ch; margin:0 0 28px; }
.csfp-actions { display:flex; gap:12px; flex-wrap:wrap; }
.csfp-btn { display:inline-flex; align-items:center; gap:8px; padding:11px 22px; border-radius:10px; font-size:14px; font-weight:700; text-decoration:none !important; transition:all 0.2s; cursor:pointer; border:none; }
.csfp-btn.primary { background:#00d1ff; color:#0a1628 !important; }
.csfp-btn.primary:hover { background:#24ddff; }
.csfp-btn.secondary { background:rgba(0,209,255,0.1); color:#00d1ff !important; border:1px solid rgba(0,209,255,0.35); }
.csfp-btn.secondary:hover { background:rgba(0,209,255,0.18); }
.csfp-btn.ghost { background:transparent; color:#cbd5e1 !important; border:1px solid rgba(148,163,184,0.3); }
.csfp-btn.ghost:hover { border-color:rgba(148,163,184,0.6); color:#f1f5f9 !important; }
.csfp-section { padding:40px 0; border-top:1px solid rgba(148,163,184,0.1); }
.csfp-section-title { font-family:Jost,sans-serif; font-size:26px; font-weight:800; color:#f8fafc; margin:0 0 24px; }
.csfp-cap-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }
@media(max-width:992px){ .csfp-cap-grid{grid-template-columns:repeat(2,1fr);} }
@media(max-width:576px){ .csfp-cap-grid{grid-template-columns:1fr;} }
.csfp-cap-card { background:rgba(255,255,255,0.05); border:1px solid rgba(148,163,184,0.2); border-radius:14px; padding:20px; }
.csfp-cap-icon { font-size:22px; margin-bottom:12px; }
.csfp-cap-card h4 { font-family:Jost,sans-serif; font-size:15px; font-weight:700; color:#f1f5f9; margin:0 0 8px; }
.csfp-cap-card p { font-size:13px; color:#94a3b8; line-height:1.65; margin:0; }
.csfp-usecases { background:rgba(255,255,255,0.04); border:1px solid rgba(148,163,184,0.15); border-radius:12px; padding:20px 24px; }
.csfp-uc-label { display:block; font-size:10.5px; font-weight:700; letter-spacing:1px; text-transform:uppercase; color:#64748b; margin-bottom:8px; }
.csfp-uc-text { font-size:14px; color:#94a3b8; margin:0; }
.csfp-pricing-strip {
  display:flex; align-items:center; justify-content:space-between; gap:24px; flex-wrap:wrap;
  background:linear-gradient(135deg,rgba(0,209,255,0.08),rgba(46,229,157,0.04));
  border:1px solid rgba(0,209,255,0.22); border-radius:16px; padding:24px 28px;
}
.csfp-pricing-strip h3 { font-family:Jost,sans-serif; font-size:20px; font-weight:800; color:#f8fafc; margin:0 0 6px; }
.csfp-pricing-strip p { font-size:13.5px; color:#94a3b8; margin:0; max-width:52ch; }
.csfp-strip-ctas { display:flex; gap:10px; flex-shrink:0; flex-wrap:wrap; }
"""

# ── 2. CloudSignals mega-menu HTML ────────────────────────────────────────────
CS_MENU_HTML = """            <li class="dropdown cs-product-menu"><a href="cspm-cloudsignals.html">CloudSignals+RiskOps</a>
                <div class="cs-product-megamenu">
                    <div class="cs-mega-hdr">
                        <div class="cs-mega-hdr-info">
                            <span class="cs-mega-status"><span class="cs-avail-dot"></span>Available Now</span>
                            <h3>CloudSignals+RiskOps&trade;</h3>
                            <p>AI-native cloud security posture, risk operations, and continuous compliance &mdash; in one platform.</p>
                        </div>
                        <a href="cloudsignals-pricing.html" class="cs-mega-pricing-cta">Compare plans &amp; pricing &rarr;</a>
                    </div>
                    <div class="cs-mega-body">
                        <div class="cs-mega-col">
                            <span class="cs-mega-col-label">Posture &amp; Discovery</span>
                            <a class="cs-mega-feat-card" href="cloudsignals-cspm.html"><i class="fas fa-cloud"></i><div><strong>Multi-Cloud CSPM</strong><span>Scan AWS, Azure, GCP, and OCI posture in real time.</span></div></a>
                            <a class="cs-mega-feat-card" href="cloudsignals-findings.html"><i class="fas fa-exclamation-triangle"></i><div><strong>Findings &amp; Risk Signals</strong><span>Prioritized risk signals with business-context scoring.</span></div></a>
                        </div>
                        <div class="cs-mega-col">
                            <span class="cs-mega-col-label">Risk &amp; Compliance</span>
                            <a class="cs-mega-feat-card" href="cloudsignals-risk-register.html"><i class="fas fa-clipboard-list"></i><div><strong>Risk Register &amp; RiskOps</strong><span>GRC-grade risk records, treatments, and portfolio exposure.</span></div></a>
                            <a class="cs-mega-feat-card" href="cloudsignals-compliance.html"><i class="fas fa-shield-alt"></i><div><strong>Continuous Compliance</strong><span>SOC 2, ISO 27001, PCI-DSS, CMMC, HIPAA.</span></div></a>
                            <a class="cs-mega-feat-card" href="cloudsignals-tprm.html"><i class="fas fa-handshake"></i><div><strong>Third-Party Risk (TPRM)</strong><span>Vendor assessments and ongoing monitoring.</span></div></a>
                        </div>
                        <div class="cs-mega-col">
                            <span class="cs-mega-col-label">Intelligence</span>
                            <a class="cs-mega-feat-card" href="cloudsignals-vision-ai.html"><i class="fas fa-brain"></i><div><strong>Vision AI &amp; Narratives</strong><span>GenAI risk summaries, AI chat, and model insights.</span></div></a>
                            <a class="cs-mega-feat-card" href="ai-inspector.html"><i class="fas fa-satellite-dish"></i><div><strong>AI Signals&trade; Integration</strong><span>LLM telemetry as security-native compliance signals.</span></div></a>
                        </div>
                    </div>
                    <div class="cs-mega-ftr">
                        <a href="cspm-cloudsignals.html" class="cs-mega-ftr-link">Product overview &rarr;</a>
                        <div class="cs-mega-ftr-ctas">
                            <a href="cloudsignals-pricing.html" class="cs-mega-btn-primary">Compare plans &amp; pricing</a>
                            <a href="request-demo.html" class="cs-mega-btn-ghost">Request a demo</a>
                        </div>
                    </div>
                </div>
            </li>
"""

BLOG_LINKS = """                    <li><a href="blog-portal.html">Blog</a></li>
                    <li><a href="why-aivric-exists.html">Why AiVRIC Exists</a></li>
                    <li><a href="blog-future-of-cloud-security.html">Future of Cloud Security</a></li>
                    <li><a href="blog-why-continuous-compliance-matters.html">Continuous Compliance</a></li>
"""

# ── 3. FEATURE PAGE DEFINITIONS ───────────────────────────────────────────────
FEATURE_PAGES = [
  {
    "file": "cloudsignals-cspm.html",
    "title": "Multi-Cloud CSPM | Cloud Security Posture Management | AiVRIC",
    "desc": "CloudSignals+RiskOps™ CSPM — scan AWS, Azure, GCP, and OCI for misconfigurations, exposed assets, and posture drift in real time.",
    "bread": "Multi-Cloud CSPM",
    "icon": "fas fa-cloud",
    "accent": "#00d1ff",
    "h1": "Cloud posture visibility you can act on.",
    "sub": "Multi-Cloud CSPM",
    "lead": "Scan every cloud account — AWS, Azure, GCP, OCI — for misconfigurations, exposed assets, and policy violations. Get a unified risk score with direct evidence links, continuously.",
    "usecases": "SOC 2 evidence &middot; ISO 27001 controls &middot; PCI-DSS monitoring &middot; CMMC readiness &middot; HIPAA configuration review",
    "caps": [
      ("fas fa-satellite-dish","#00d1ff","Real-Time Asset Discovery","Continuously enumerate cloud assets across accounts and regions. Delta tracking surfaces new or changed assets within minutes."),
      ("fas fa-search-plus","#2ee59d","Configuration Scanning","Check every resource against CIS Benchmarks, vendor best practices, and custom policies. 1,000+ check library out of the box."),
      ("fas fa-exclamation-circle","#ffd63a","Misconfiguration Detection","Pinpoint public buckets, open security groups, unencrypted volumes, and over-permissioned roles with remediation guidance."),
      ("fas fa-layer-group","#a78bfa","Multi-Cloud Coverage","Single console for AWS, Azure, GCP, and OCI. Unified finding schema means no translating between cloud-specific nomenclature."),
      ("fas fa-calendar-check","#00d1ff","Scheduled &amp; Continuous Scans","Run scans on configurable cadences or on-demand. New account onboarding triggers automatic baseline scans."),
      ("fas fa-bell","#2ee59d","Risk-Scored Alerts","Findings are scored by severity, blast radius, and exposure. Alerts route to SIEM, Slack, Jira, or PagerDuty with full context."),
    ],
  },
  {
    "file": "cloudsignals-findings.html",
    "title": "Findings & Risk Signals | Prioritized Risk Intelligence | AiVRIC",
    "desc": "CloudSignals+RiskOps™ Findings — prioritized risk signals with business context, deduplication, evidence capture, and SIEM export.",
    "bread": "Findings &amp; Risk Signals",
    "icon": "fas fa-exclamation-triangle",
    "accent": "#ffd63a",
    "h1": "Every finding scored. Every risk prioritized.",
    "sub": "Findings &amp; Risk Signals",
    "lead": "Raw scanner output becomes actionable intelligence. CloudSignals normalizes findings from every integrated scanner, scores them by business impact, and routes them to the right team.",
    "usecases": "Posture drift monitoring &middot; Compliance evidence &middot; Incident investigation &middot; Risk prioritization &middot; Executive reporting",
    "caps": [
      ("fas fa-balance-scale","#ffd63a","Business-Context Risk Scoring","Score findings by severity, asset criticality, and exposure. A critical finding on a dev account scores differently than on a prod payment system."),
      ("fas fa-compress-arrows-alt","#00d1ff","Cross-Scanner Deduplication","Merge findings from multiple integrations into canonical risk records. Stop triaging the same issue from six different sources."),
      ("fas fa-file-invoice","#2ee59d","Evidence Capture","Every finding retains its raw evidence artifact — screenshot, API response, config snapshot. Auditors get reproducible proof, not just a count."),
      ("fas fa-clipboard-check","#a78bfa","Triage &amp; Workflow","Accept, assign, escalate, or defer findings through a structured triage workflow. Full decision audit trail for compliance."),
      ("fas fa-history","#ffd63a","Finding Timeline","Track how a finding was introduced, modified, and resolved over time. Link back to the commit, deployment, or config change that caused it."),
      ("fas fa-share-alt","#00d1ff","SIEM &amp; Ticketing Export","Push findings to Splunk, Chronicle, Jira, ServiceNow, or any webhook. Structured JSON schema for clean downstream ingestion."),
    ],
  },
  {
    "file": "cloudsignals-risk-register.html",
    "title": "Risk Register & RiskOps | GRC Risk Management | AiVRIC",
    "desc": "CloudSignals+RiskOps™ Risk Register — GRC-grade risk records, impact and likelihood scoring, treatment plans, and portfolio exposure tracking.",
    "bread": "Risk Register &amp; RiskOps",
    "icon": "fas fa-clipboard-list",
    "accent": "#2ee59d",
    "h1": "Risk governance that keeps up with your cloud.",
    "sub": "Risk Register &amp; RiskOps",
    "lead": "Promote findings into governed risk records. Score impact and likelihood. Build treatment plans. Track residual exposure across your entire portfolio — all connected to the evidence that created them.",
    "usecases": "GRC programs &middot; CISO reporting &middot; Audit preparation &middot; FedRAMP POA&amp;M &middot; Board-level risk reporting",
    "caps": [
      ("fas fa-plus-circle","#2ee59d","Risk Record Creation","Promote any finding or group of findings into a formal risk record. Link back to source evidence automatically for auditor-verifiable traceability."),
      ("fas fa-sliders-h","#00d1ff","Impact &times; Likelihood Scoring","Score risks on a 5×5 matrix with customizable impact dimensions (financial, reputational, operational). Inherent vs. residual risk tracked separately."),
      ("fas fa-tasks","#ffd63a","Treatment Plans","Create mitigate, transfer, accept, or avoid treatment decisions. Assign owners, milestones, and due dates with automated follow-up."),
      ("fas fa-chart-pie","#a78bfa","Risk Portfolio View","Roll up all open risks into a portfolio dashboard. Filter by severity, owner, framework, or business unit. Export for board-level reporting."),
      ("fas fa-ban","#2ee59d","Security Exceptions","Document time-bound exceptions with business justification, approvals, and expiry controls. Keeps risks visible rather than silently ignored."),
      ("fas fa-file-export","#00d1ff","POA&amp;M &amp; Reporting","Generate Plan of Action &amp; Milestones (POA&amp;M) exports for CMMC and FedRAMP. Executive-ready risk dashboards in PDF or JSON."),
    ],
  },
  {
    "file": "cloudsignals-compliance.html",
    "title": "Continuous Compliance | SOC 2, ISO 27001, PCI-DSS, CMMC | AiVRIC",
    "desc": "CloudSignals+RiskOps™ Compliance — always-on framework mapping for SOC 2, ISO 27001, PCI-DSS v4.0, CMMC 2.0, HIPAA, NIST CSF, CIS, FedRAMP, and GDPR.",
    "bread": "Continuous Compliance",
    "icon": "fas fa-shield-alt",
    "accent": "#a78bfa",
    "h1": "Always-on compliance. Not point-in-time.",
    "sub": "Continuous Compliance",
    "lead": "Map every posture finding, risk record, and treatment to the frameworks your auditors care about. Evidence collects automatically. Audit packages export in one click.",
    "usecases": "SOC 2 Type II &middot; ISO 27001 certification &middot; PCI-DSS QSA prep &middot; CMMC Level 2 &middot; HIPAA risk analysis",
    "caps": [
      ("fas fa-sitemap","#a78bfa","Multi-Framework Mapping","SOC 2, ISO 27001, PCI-DSS v4.0, CMMC 2.0, HIPAA, NIST CSF, CIS Controls, FedRAMP, and GDPR — all mapped from a single evidence stream."),
      ("fas fa-check-double","#2ee59d","Automated Control Testing","Scheduled scans test control effectiveness continuously. Control status updates in real time as findings open and close — no manual refresh."),
      ("fas fa-archive","#00d1ff","Evidence Collection","Screenshots, API responses, config snapshots, and remediation logs captured automatically and linked to specific control requirements."),
      ("fas fa-search-minus","#ffd63a","Gap Analysis","See exactly which controls are failing, partially met, or untested. Gap heatmaps highlight the fastest path to audit readiness."),
      ("fas fa-file-pdf","#a78bfa","Audit-Ready Exports","One-click PDF and JSON evidence packages organized by framework section. Formatted for auditors, not engineers."),
      ("fas fa-tachometer-alt","#2ee59d","Compliance Dashboard","Live readiness score per framework. Track progress week-over-week. Share a read-only link with auditors or executives."),
    ],
  },
  {
    "file": "cloudsignals-tprm.html",
    "title": "Third-Party Risk (TPRM) | Vendor Risk Management | AiVRIC",
    "desc": "CloudSignals+RiskOps™ TPRM — vendor risk assessments, questionnaires, continuous monitoring, and risk scoring for your third-party ecosystem.",
    "bread": "Third-Party Risk (TPRM)",
    "icon": "fas fa-handshake",
    "accent": "#ffd63a",
    "h1": "Your vendors are part of your risk surface.",
    "sub": "Third-Party Risk Management",
    "lead": "Assess, score, and continuously monitor vendors across your supply chain. Build a vendor risk register that integrates with your posture data and compliance evidence — not a standalone spreadsheet.",
    "usecases": "Vendor due diligence &middot; SOC 2 third-party controls &middot; ISO 27001 supplier management &middot; CMMC supply chain &middot; HIPAA BAA tracking",
    "caps": [
      ("fas fa-building","#ffd63a","Vendor Profiles","Centralized vendor registry with risk tier classification, contact ownership, contract metadata, and integration status."),
      ("fas fa-clipboard-check","#00d1ff","Risk Assessments","Structured assessment workflows aligned to SIG, CAIQ, and custom questionnaire templates. Track completion and responses in one view."),
      ("fas fa-paper-plane","#2ee59d","Questionnaire Automation","Send, track, and follow up on vendor questionnaires. Responses are scored and fed into the vendor risk record automatically."),
      ("fas fa-eye","#a78bfa","Continuous Monitoring","Monitor vendor security posture signals from external feeds. Flag vendors when their risk profile changes between formal assessments."),
      ("fas fa-chart-bar","#ffd63a","Vendor Risk Scoring","Composite risk scores based on assessment responses, external signals, and your dependency tier. Prioritize follow-up by score."),
      ("fas fa-file-alt","#00d1ff","TPRM Reporting","Portfolio-level vendor risk dashboards and per-vendor evidence packages. Executive summaries and auditor-ready exports included."),
    ],
  },
  {
    "file": "cloudsignals-vision-ai.html",
    "title": "Vision AI & Narratives | GenAI Security Intelligence | AiVRIC",
    "desc": "CloudSignals+RiskOps™ Vision AI — GenAI risk narratives, AI chat, model insights, and LLM telemetry as security-native compliance signals.",
    "bread": "Vision AI &amp; Narratives",
    "icon": "fas fa-brain",
    "accent": "#a78bfa",
    "h1": "Security intelligence that speaks your language.",
    "sub": "Vision AI &amp; Narratives",
    "lead": "Ask your risk posture a question and get an answer. GenAI risk narratives, intelligent compliance summaries, and AI chat bring the power of language models to your CloudSignals data — with tenant-bound privacy controls.",
    "usecases": "CISO briefings &middot; Board-level risk summaries &middot; Compliance narrative generation &middot; AI governance evidence &middot; Executive dashboards",
    "caps": [
      ("fas fa-comment-dots","#a78bfa","Vision Chat","Ask natural-language questions about your cloud posture, risk register, and compliance status. Answers are grounded in your live CloudSignals data."),
      ("fas fa-pen-fancy","#00d1ff","GenAI Risk Narratives","AI-generated summaries of your highest-risk findings — formatted for technical teams, compliance managers, and executives. One click, three audience views."),
      ("fas fa-chart-line","#2ee59d","Model Insights Dashboard","Track tenant-scoped AI quality: 96 sessions, 67.7% success rate, 13.2Kms avg latency, 70.6 quality score — all surfaced as security-native telemetry."),
      ("fas fa-lock","#ffd63a","Tenant-Bound Privacy","Export boundary controls (Tenant Bound / Shared Project Per Tenant) ensure LLM telemetry never leaves your isolation tier. Standard, Strict, or Minimal privacy modes."),
      ("fas fa-bell","#a78bfa","Alert Signals","Prompt drift, quality degradation, and privacy tradeoff advisories surfaced automatically. No raw trace noise — only actionable signals."),
      ("fas fa-satellite-dish","#00d1ff","AI Signals&trade; Integration","Connect your AI Signals™ project to route LLM telemetry as security-native CloudSignals posture signals. Powered by the AI Signals observability platform."),
    ],
  },
]

def build_cap_cards(caps):
    html = ""
    for icon, color, title, body in caps:
        html += f"""              <div class="csfp-cap-card">
                <div class="csfp-cap-icon" style="color:{color}"><i class="{icon}"></i></div>
                <h4>{title}</h4>
                <p>{body}</p>
              </div>\n"""
    return html

def build_feature_page_content(pg):
    caps_html = build_cap_cards(pg["caps"])
    return f"""
        <div class="cs-product-page">
          <div class="csfp-page">
            <section class="csfp-hero">
              <div class="auto-container">
                <div class="csfp-hero-inner">
                  <div class="csfp-hero-copy">
                    <nav aria-label="breadcrumb" class="csfp-breadcrumb">
                      <a href="index.html">Home</a><span>/</span>
                      <a href="cspm-cloudsignals.html">CloudSignals+RiskOps</a><span>/</span>
                      <span>{pg["bread"]}</span>
                    </nav>
                    <div class="csfp-badge" style="border-color:{pg["accent"]}33;background:{pg["accent"]}11;">
                      <span class="csfp-avail-dot" style="background:{pg["accent"]}"></span>
                      <span style="color:{pg["accent"]}">Available in CloudSignals+RiskOps&trade;</span>
                    </div>
                    <h1 class="csfp-title">{pg["h1"]}</h1>
                    <p class="csfp-subtitle" style="color:{pg["accent"]}">{pg["sub"]}</p>
                    <p class="csfp-lead">{pg["lead"]}</p>
                    <div class="csfp-actions">
                      <a href="cloudsignals-pricing.html" class="csfp-btn primary"><i class="fas fa-bolt"></i> View plans &amp; pricing</a>
                      <a href="cspm-cloudsignals.html" class="csfp-btn secondary">Platform overview</a>
                      <a href="request-demo.html" class="csfp-btn ghost">Request a demo</a>
                    </div>
                  </div>
                  <div class="csfp-hero-icon-wrap" style="color:{pg["accent"]}"><i class="{pg["icon"]}"></i></div>
                </div>
              </div>
            </section>
            <section class="csfp-section">
              <div class="auto-container">
                <h2 class="csfp-section-title">Key capabilities</h2>
                <div class="csfp-cap-grid">
{caps_html}                </div>
              </div>
            </section>
            <section class="csfp-section">
              <div class="auto-container">
                <div class="csfp-usecases">
                  <span class="csfp-uc-label">Common use cases</span>
                  <p class="csfp-uc-text">{pg["usecases"]}</p>
                </div>
              </div>
            </section>
            <section class="csfp-section">
              <div class="auto-container">
                <div class="csfp-pricing-strip">
                  <div>
                    <h3>Included in CloudSignals+RiskOps&trade;</h3>
                    <p>This feature is available on all CloudSignals+RiskOps&trade; plans &mdash; Free, Growth, Premium, and Enterprise. Compare limits and access tiers.</p>
                  </div>
                  <div class="csfp-strip-ctas">
                    <a href="cloudsignals-pricing.html" class="csfp-btn primary"><i class="fas fa-bolt"></i> Compare plans</a>
                    <a href="cspm-cloudsignals.html" class="csfp-btn ghost">Platform overview</a>
                  </div>
                </div>
              </div>
            </section>
          </div>
        </div>"""

def main():
    # ── Append CSS ─────────────────────────────────────────────────────────────
    css_path = SITE / "assets" / "css" / "custom.css"
    with open(css_path, "a", encoding="utf-8") as f:
        f.write(MEGA_CSS)
    print("[OK] CSS appended to custom.css")

    # ── Read template ──────────────────────────────────────────────────────────
    template = TEMPLATE.read_text(encoding="utf-8")
    mobile_end = "        </div><!-- End Mobile Menu -->"
    ftr_start = "        </div><!-- /cs-product-page -->"

    hdr_end_idx = template.index(mobile_end) + len(mobile_end)
    ftr_idx = template.index(ftr_start)

    header_tmpl = template[:hdr_end_idx]
    footer_tmpl = template[ftr_idx:]

    # ── Create 6 feature pages ─────────────────────────────────────────────────
    for pg in FEATURE_PAGES:
        hdr = re.sub(r'<title>.*?</title>', f'<title>{pg["title"]}</title>', header_tmpl, flags=re.DOTALL)
        hdr = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{pg["desc"]}">', hdr)
        content = build_feature_page_content(pg)
        html = hdr + "\n" + content + "\n" + footer_tmpl
        out = SITE / pg["file"]
        out.write_text(html, encoding="utf-8")
        print(f"  Created: {pg['file']}")
    print("[OK] 6 feature pages created")

    # ── Nav update ─────────────────────────────────────────────────────────────
    html_files = [f for f in SITE.glob("*.html") if f.is_file()]
    print(f"\nUpdating nav in {len(html_files)} files...")

    # Platform menu close + Portfolio open — unique anchor for insertion
    PLATFORM_CLOSE_PORTFOLIO_OPEN = (
        '                <div class="dropdown-btn" role="button" tabindex="0"'
        ' aria-label="Toggle submenu" aria-controls="submenu-platform" aria-expanded="false">'
        '<span class="fas fa-angle-down"></span></div>\n'
        '            </li>\n'
        '            <li class="dropdown"><a href="#">Portfolio</a>'
    )
    PLATFORM_CLOSE_CS_PORTFOLIO = (
        '                <div class="dropdown-btn" role="button" tabindex="0"'
        ' aria-label="Toggle submenu" aria-controls="submenu-platform" aria-expanded="false">'
        '<span class="fas fa-angle-down"></span></div>\n'
        '            </li>\n'
        + CS_MENU_HTML
        + '            <li class="dropdown"><a href="#">Portfolio</a>'
    )

    updated = skipped = 0
    for f in html_files:
        raw = f.read_text(encoding="utf-8")
        if "cs-product-menu" in raw:
            skipped += 1
            continue
        orig = raw

        # a. Solutions → Portfolio
        raw = raw.replace('<a href="#">Solutions</a>', '<a href="#">Portfolio</a>')

        # b. Remove blogs-menu LI (greedy match from the LI open to just before Resources)
        raw = re.sub(
            r'\s+<li class="dropdown blogs-menu">.*?</li>'
            r'(\s+<li class="dropdown"><a href="https://aivric\.com/AiVRIC-UserGuide/index\.html">)',
            r'\1', raw, count=1, flags=re.DOTALL
        )

        # c. Add blog links into Resources <ul>
        raw = raw.replace(
            '<li><a href="why-aivric.html">Why AiVRIC</a></li>',
            '<li><a href="why-aivric.html">Why AiVRIC</a></li>\n' + BLOG_LINKS,
            1
        )

        # d. Insert CloudSignals menu between Platform and Portfolio
        if PLATFORM_CLOSE_PORTFOLIO_OPEN in raw:
            raw = raw.replace(PLATFORM_CLOSE_PORTFOLIO_OPEN, PLATFORM_CLOSE_CS_PORTFOLIO, 1)

        if raw != orig:
            f.write_text(raw, encoding="utf-8")
            updated += 1

    print(f"[OK] Nav: {updated} files updated, {skipped} already had new nav (skipped)")
    print("\n[OK] All done.")

if __name__ == "__main__":
    main()
