#!/usr/bin/env python3
"""
Build CloudSignals feature product pages.
Fixes the csfp- / csp- class mismatch and redesigns all 7 feature pages
with a consistent, dark-system layout using the csp-* design system.
"""
from pathlib import Path

SITE = Path(r"C:\Projects\AiVRIC-Website")
TEMPLATE = SITE / "cloudsignals-findings.html"

# ── Extract shared blocks from existing template ─────────────────────────────
raw_t = TEMPLATE.read_text(encoding="utf-8", errors="replace")

# Body opening through mobile menu close
NAV_BLOCK = raw_t[raw_t.find("<!-- page wrapper -->") : raw_t.find("<!-- End Mobile Menu -->") + len("<!-- End Mobile Menu -->")]

# Global footer block
FOOTER_BLOCK = raw_t[raw_t.find("<!-- main-footer -->") : raw_t.find("<!-- main-footer end -->") + len("<!-- main-footer end -->")]

# ── Shared CSS ───────────────────────────────────────────────────────────────
FEATURE_CSS = """\
<style id="cs-feat-styles">
:root{
  --cf-cyan:#00d1ff;--cf-green:#2ee59d;--cf-gold:#ffd63a;--cf-purple:#a78bfa;--cf-amber:#fb923c;
  --cf-text:#f8fafc;--cf-body:#e5e7eb;--cf-muted:#cbd5e1;--cf-faint:#94a3b8;--cf-accent:#7dd3fc;
  --cf-s1:rgba(255,255,255,.06);--cf-s2:rgba(255,255,255,.10);
  --cf-line:rgba(148,163,184,.28);--cf-shadow:0 14px 40px rgba(0,0,0,.28);--cf-r:16px;
}
body.cf-page{
  font-family:Inter,system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
  background:radial-gradient(1200px 900px at 70% -20%,rgba(0,209,255,.18),transparent 55%),
    radial-gradient(900px 700px at 10% 10%,rgba(46,113,229,.12),transparent 60%),
    linear-gradient(180deg,#070b14 0%,#060a12 35%,#050814 100%);
  color:var(--cf-body);
}
/* hero */
.cf-hero{padding:100px 0 56px;position:relative;}
@media(max-width:992px){.cf-hero{padding:80px 0 40px;}}
.cf-hero-grid{display:grid;grid-template-columns:1.3fr 0.7fr;gap:36px;align-items:start;}
@media(max-width:992px){.cf-hero-grid{grid-template-columns:1fr;}}
.cf-breadcrumb{display:flex;align-items:center;gap:8px;font-size:13px;color:var(--cf-faint);margin-bottom:20px;}
.cf-breadcrumb a{color:var(--cf-faint);text-decoration:none;}
.cf-breadcrumb a:hover{color:var(--cf-accent);}
.cf-badge{
  display:inline-flex;align-items:center;gap:8px;padding:7px 14px;border-radius:999px;
  background:rgba(0,209,255,.10);border:1px solid rgba(0,209,255,.30);
  color:var(--cf-text);font-size:12.5px;font-weight:600;letter-spacing:.3px;margin-bottom:18px;
}
.cf-dot{width:8px;height:8px;border-radius:50%;background:var(--cf-green);box-shadow:0 0 6px rgba(46,229,157,.7);flex-shrink:0;}
.cf-title{
  font-family:Jost,Inter,sans-serif;font-size:48px;font-weight:800;
  line-height:1.06;letter-spacing:-1px;color:var(--cf-text);margin:0 0 8px;
}
@media(max-width:768px){.cf-title{font-size:34px;}}
.cf-sub{font-size:18px;font-weight:700;margin:0 0 14px;}
.cf-lead{font-size:16px;line-height:1.75;color:var(--cf-muted);max-width:62ch;margin:0 0 26px;}
.cf-actions{display:flex;gap:12px;flex-wrap:wrap;}
.cf-btn{
  display:inline-flex;align-items:center;gap:8px;padding:11px 22px;border-radius:999px;
  font-weight:700;font-size:14px;text-decoration:none;cursor:pointer;transition:all .22s;border:1px solid transparent;
}
.cf-btn.primary{background:#00d1ff;color:#fff!important;border-color:rgba(0,209,255,.6);box-shadow:0 10px 22px rgba(0,209,255,.2);}
.cf-btn.primary:hover{background:#24ddff;transform:translateY(-1px);}
.cf-btn.secondary{background:rgba(0,209,255,.10);color:var(--cf-text)!important;border-color:rgba(0,209,255,.55);}
.cf-btn.secondary:hover{background:#00d1ff;color:#fff!important;transform:translateY(-1px);}
.cf-btn.ghost{background:transparent;color:var(--cf-text)!important;border-color:rgba(255,255,255,.20);}
.cf-btn.ghost:hover{background:rgba(255,255,255,.07);transform:translateY(-1px);}
/* aside */
.cf-aside{display:flex;flex-direction:column;gap:14px;padding-top:8px;}
.cf-aside-card{border-radius:var(--cf-r);padding:20px;background:var(--cf-s1);border:1px solid var(--cf-line);box-shadow:var(--cf-shadow);}
.cf-aside-card h4{font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:1px;color:var(--cf-faint);margin:0 0 12px;}
.cf-ql{list-style:none;padding:0;margin:0;display:grid;gap:8px;}
.cf-ql li{display:flex;gap:9px;align-items:flex-start;font-size:13px;color:var(--cf-muted);line-height:1.45;}
.cf-ql li i{color:var(--cf-green);flex-shrink:0;margin-top:2px;font-size:11px;}
.cf-aside-link{
  display:flex;align-items:center;justify-content:space-between;
  padding:12px 16px;border-radius:12px;
  background:rgba(0,209,255,.07);border:1px solid rgba(0,209,255,.22);
  text-decoration:none;transition:background .2s;
}
.cf-aside-link:hover{background:rgba(0,209,255,.12);}
.cf-aside-link span{font-size:13.5px;font-weight:600;color:var(--cf-text);}
.cf-aside-link i{color:var(--cf-cyan);font-size:12px;}
/* sections */
.cf-section{padding:52px 0 0;}
.cf-eyebrow{display:block;font-size:12px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--cf-cyan);margin-bottom:8px;}
.cf-sec-title{font-family:Jost,Inter,sans-serif;font-size:32px;font-weight:800;color:var(--cf-text);margin:0 0 10px;letter-spacing:-.4px;line-height:1.15;}
.cf-sec-sub{font-size:15px;line-height:1.75;color:var(--cf-muted);max-width:80ch;margin:0 0 28px;}
/* caps grid */
.cf-cap-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;}
@media(max-width:992px){.cf-cap-grid{grid-template-columns:repeat(2,1fr);}}
@media(max-width:576px){.cf-cap-grid{grid-template-columns:1fr;}}
.cf-cap{
  border-radius:var(--cf-r);background:var(--cf-s1);border:1px solid var(--cf-line);
  padding:22px;box-shadow:var(--cf-shadow);transition:border-color .2s,box-shadow .2s;
}
.cf-cap:hover{border-color:rgba(0,209,255,.28);box-shadow:0 18px 44px rgba(0,0,0,.28);}
.cf-cap-icon{
  width:42px;height:42px;border-radius:12px;
  display:flex;align-items:center;justify-content:center;
  font-size:17px;margin-bottom:14px;flex-shrink:0;
}
.cf-cap-icon.cyan{background:rgba(0,209,255,.13);border:1px solid rgba(0,209,255,.28);color:var(--cf-cyan);}
.cf-cap-icon.green{background:rgba(46,229,157,.13);border:1px solid rgba(46,229,157,.28);color:var(--cf-green);}
.cf-cap-icon.gold{background:rgba(255,214,58,.13);border:1px solid rgba(255,214,58,.28);color:var(--cf-gold);}
.cf-cap-icon.purple{background:rgba(167,139,250,.13);border:1px solid rgba(167,139,250,.28);color:var(--cf-purple);}
.cf-cap-icon.amber{background:rgba(251,146,60,.13);border:1px solid rgba(251,146,60,.28);color:var(--cf-amber);}
.cf-cap h4{font-size:15px;font-weight:700;color:var(--cf-text);margin:0 0 7px;}
.cf-cap p{font-size:13.5px;color:var(--cf-muted);line-height:1.65;margin:0;}
/* steps */
.cf-steps-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:8px;}
@media(max-width:768px){.cf-steps-grid{grid-template-columns:1fr;}}
.cf-step{border-radius:var(--cf-r);background:var(--cf-s1);border:1px solid var(--cf-line);padding:24px;box-shadow:var(--cf-shadow);}
.cf-step-num{
  width:36px;height:36px;border-radius:10px;
  font-family:Jost,Inter,sans-serif;font-size:18px;font-weight:800;
  display:flex;align-items:center;justify-content:center;
  background:rgba(0,209,255,.12);border:1px solid rgba(0,209,255,.25);
  color:var(--cf-cyan);margin-bottom:14px;
}
.cf-step h4{font-size:16px;font-weight:700;color:var(--cf-text);margin:0 0 8px;}
.cf-step p{font-size:13.5px;color:var(--cf-muted);line-height:1.65;margin:0;}
/* use case pills */
.cf-uc-row{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px;}
.cf-uc-pill{
  display:inline-flex;align-items:center;gap:7px;padding:8px 14px;border-radius:12px;
  background:var(--cf-s1);border:1px solid var(--cf-line);
  color:var(--cf-muted);font-size:13px;font-weight:600;
  transition:border-color .2s,color .2s;
}
.cf-uc-pill i{color:var(--cf-cyan);font-size:10px;}
/* plan strip */
.cf-plan-strip{
  margin:52px 0 0;border-radius:var(--cf-r);
  background:linear-gradient(90deg,rgba(0,89,255,.10),rgba(0,209,255,.05));
  border:1px solid rgba(0,89,255,.20);padding:26px 28px;
  display:flex;align-items:center;justify-content:space-between;gap:20px;flex-wrap:wrap;
}
.cf-plan-strip h3{font-family:Jost,Inter,sans-serif;font-size:20px;font-weight:700;color:var(--cf-text);margin:0 0 6px;}
.cf-plan-strip p{font-size:14px;color:var(--cf-muted);margin:0;line-height:1.6;}
.cf-plan-ctas{display:flex;gap:12px;flex-wrap:wrap;}
/* divider */
.cf-divider{height:1px;background:linear-gradient(90deg,transparent,var(--cf-line),transparent);margin:52px 0 0;}
/* bottom cta */
.cf-bottom-cta{
  margin:52px 0 72px;border-radius:var(--cf-r);
  background:linear-gradient(135deg,rgba(0,209,255,.09),rgba(46,229,157,.05));
  border:1px solid rgba(0,209,255,.25);box-shadow:0 24px 60px rgba(0,209,255,.08);
  padding:44px;text-align:center;
}
.cf-bottom-cta h2{font-family:Jost,Inter,sans-serif;font-size:36px;font-weight:800;color:var(--cf-text);margin:0 0 12px;letter-spacing:-.5px;}
@media(max-width:768px){.cf-bottom-cta h2{font-size:26px;}}
.cf-bottom-cta p{font-size:16px;color:var(--cf-muted);line-height:1.7;max-width:60ch;margin:0 auto 24px;}
.cf-cta-actions{display:flex;gap:14px;flex-wrap:wrap;justify-content:center;}
</style>"""

GF_CSS = """\
<style id="gf-styles">
/* === GLOBAL FOOTER === */
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

# ── Page data ────────────────────────────────────────────────────────────────
PAGES = [
  {
    'file': 'cloudsignals-cspm.html',
    'title': 'Multi-Cloud CSPM | Cloud Security Posture Management | AiVRIC',
    'desc': 'CloudSignals+RiskOps™ CSPM — continuously scan AWS, Azure, GCP, and OCI for misconfigurations, exposed assets, and posture drift in real time.',
    'hero_title': 'Know your cloud posture.\nFix it faster.',
    'hero_sub': 'Multi-Cloud CSPM',
    'hero_sub_color': '#00d1ff',
    'lead': 'CloudSignals continuously scans AWS, Azure, GCP, and OCI for misconfigurations, exposed assets, and posture drift — scoring every finding by business impact before it reaches your queue.',
    'icon': 'fa-cloud',
    'ql': ['Agent-free scanning across all accounts','1,000+ built-in security checks','Real-time asset inventory','Configuration drift detection','Business-context finding scores','Framework compliance mapping'],
    'caps': [
      ('fa-sync-alt','cyan','Continuous Multi-Cloud Scanning','Monitor AWS, Azure, GCP, and OCI 24/7 with agent-free scanning across every account and subscription in your organization.'),
      ('fa-tasks','green','1,000+ Security Checks','Built-in checks across CIS Benchmarks, NIST, AWS Foundational Security, Azure Security Benchmark, and custom rule sets.'),
      ('fa-layer-group','purple','Real-Time Asset Inventory','Auto-discover every resource across your cloud accounts and maintain a live map of your attack surface and resource relationships.'),
      ('fa-code-branch','gold','Configuration Drift Detection','Detect when a resource drifts from its approved baseline and alert your team before the drift becomes a vulnerability.'),
      ('fa-sort-amount-down','cyan','Business-Context Scoring','Findings scored by severity, asset criticality, and environment sensitivity — not just CVSS — so your team focuses on what actually matters.'),
      ('fa-check-double','green','Framework Compliance Mapping','Every finding maps automatically to its relevant control in SOC 2, PCI-DSS, ISO 27001, CMMC, HIPAA, and CIS Benchmarks.'),
    ],
    'steps': [
      ('01','Connect your cloud accounts','Link AWS, Azure, GCP, or OCI with read-only IAM roles in minutes. No agent installation or network changes required.'),
      ('02','Run a posture scan','CloudSignals queries your cloud APIs, runs all active check policies, and builds your asset inventory — typically completing in under 10 minutes.'),
      ('03','Review scored findings','Findings surface in your dashboard scored by risk, grouped by resource type, and mapped to your compliance frameworks.'),
    ],
    'use_cases': ['Cloud security posture','Compliance evidence','Attack surface reduction','Pre-audit readiness','Executive reporting','DevSecOps guardrails'],
    'plan_title': 'Included in all CloudSignals+RiskOps™ plans',
    'plan_body': 'CSPM scanning is available on every plan — Free through Enterprise. Cloud account counts and resource limits scale with your tier.',
    'cta_title': 'Start scanning your cloud in 15 minutes.',
    'cta_body': 'Connect your first cloud account for free. No credit card required.',
  },
  {
    'file': 'cloudsignals-findings.html',
    'title': 'Findings & Risk Signals | Prioritized Risk Intelligence | AiVRIC',
    'desc': 'CloudSignals+RiskOps™ Findings — prioritized risk signals with business context, deduplication, evidence capture, and SIEM export.',
    'hero_title': 'Every finding scored.\nEvery risk prioritized.',
    'hero_sub': 'Findings & Risk Signals',
    'hero_sub_color': '#ffd63a',
    'lead': 'Raw scanner output becomes actionable intelligence. CloudSignals normalizes findings from every integrated scanner, scores them by business impact, and routes them to the right team.',
    'icon': 'fa-exclamation-triangle',
    'ql': ['Business-context risk scoring','Cross-scanner deduplication','Raw evidence artifact capture','Structured triage & workflow','Full finding timeline','SIEM & ticketing export'],
    'caps': [
      ('fa-balance-scale','gold','Business-Context Risk Scoring','Score findings by severity, asset criticality, and exposure. A critical finding on a dev account scores differently than on a prod payment system.'),
      ('fa-compress-arrows-alt','cyan','Cross-Scanner Deduplication','Merge findings from multiple integrations into canonical risk records. Stop triaging the same issue from six different sources.'),
      ('fa-file-invoice','green','Evidence Capture','Every finding retains its raw evidence artifact — screenshot, API response, config snapshot. Auditors get reproducible proof, not just a count.'),
      ('fa-clipboard-check','purple','Triage & Workflow','Accept, assign, escalate, or defer findings through a structured triage workflow. Full decision audit trail for compliance.'),
      ('fa-history','gold','Finding Timeline','Track how a finding was introduced, modified, and resolved over time. Link back to the commit, deployment, or config change that caused it.'),
      ('fa-share-alt','cyan','SIEM & Ticketing Export','Push findings to Splunk, Chronicle, Jira, ServiceNow, or any webhook. Structured JSON schema for clean downstream ingestion.'),
    ],
    'steps': [
      ('01','Findings normalize automatically','Every scanner integration feeds into a canonical finding schema — deduplicated, scored, and enriched with asset context on arrival.'),
      ('02','Triage with context','Open any finding to see its business-context score, evidence artifact, affected asset, and the compliance controls it impacts.'),
      ('03','Route and track to closure','Assign findings to owners, set SLAs, and push to your ticketing system. Track every decision in the audit trail.'),
    ],
    'use_cases': ['Posture drift monitoring','Compliance evidence','Incident investigation','Risk prioritization','Executive reporting','Audit preparation'],
    'plan_title': 'Included in CloudSignals+RiskOps™',
    'plan_body': 'Findings & Risk Signals is available on all plans — Free, Growth, Premium, and Enterprise. Finding retention and daily scan limits scale with your tier.',
    'cta_title': 'Turn scanner noise into risk intelligence.',
    'cta_body': 'Start free and connect your first cloud account in 15 minutes. No credit card required.',
  },
  {
    'file': 'cloudsignals-risk-register.html',
    'title': 'Risk Register & RiskOps | GRC-Grade Risk Management | AiVRIC',
    'desc': 'CloudSignals+RiskOps™ Risk Register — track risk treatments, assign owners, document acceptances, and maintain a full audit trail in one platform.',
    'hero_title': 'Every risk tracked.\nEvery treatment documented.',
    'hero_sub': 'Risk Register & RiskOps',
    'hero_sub_color': '#2ee59d',
    'lead': 'The RiskOps module transforms your CloudSignals findings into a GRC-grade risk register. Track treatments, assign owners, document acceptances, and maintain a full audit trail — no spreadsheet needed.',
    'icon': 'fa-clipboard-list',
    'ql': ['GRC-grade risk records','Accept / mitigate / transfer / avoid workflows','Portfolio risk aggregation','Issues and POA&M tracking','Owner notifications & reviews','Audit-ready export'],
    'caps': [
      ('fa-file-alt','green','GRC-Grade Risk Records','Elevate any finding to a formal risk record with severity classification, treatment status, owner, and linked evidence.'),
      ('fa-project-diagram','cyan','Treatment Workflows','Document risk acceptance, mitigation, transfer, or avoidance with required approvals, supporting evidence, and expiry dates.'),
      ('fa-chart-pie','purple','Portfolio Risk View','Aggregate risk across all environments and see your overall risk posture at the portfolio level — by owner, framework, or environment.'),
      ('fa-tasks','gold','Issues & POA&M Tracking','Create issues and Plans of Action & Milestones linked directly to your risk records and findings with milestone tracking.'),
      ('fa-bell','green','Owner Notifications','Assign risks to owners with automated reminders when reviews are due, treatments are expiring, or new findings affect an open risk.'),
      ('fa-file-export','cyan','Audit-Ready Export','Export your full risk register to PDF or CSV for auditors, board reporting, or executive reviews — formatted for common audit frameworks.'),
    ],
    'steps': [
      ('01','Elevate findings to risks','Convert any finding or group of findings into a formal risk record with one click — inheriting severity, evidence, and asset context automatically.'),
      ('02','Document your treatment','Select accept, mitigate, transfer, or avoid. Add evidence, assign an owner, and set a target resolution or review date.'),
      ('03','Review at portfolio level','Monitor your aggregate risk posture across all environments and frameworks in a single dashboard with trend lines and owner accountability.'),
    ],
    'use_cases': ['GRC programs','Audit preparation','Board risk reporting','Compliance evidence','Internal security assessments','Third-party audits'],
    'plan_title': 'Available on Growth, Premium, and Enterprise plans',
    'plan_body': 'Risk Register & RiskOps is included from the Growth tier. Portfolio-level views and bulk export are available on Premium and Enterprise.',
    'cta_title': 'Replace your risk spreadsheet today.',
    'cta_body': 'Start with a free account and upgrade to Growth when you\'re ready to operationalize risk management.',
  },
  {
    'file': 'cloudsignals-compliance.html',
    'title': 'Continuous Compliance | SOC 2, PCI-DSS, ISO 27001 | AiVRIC',
    'desc': 'CloudSignals+RiskOps™ Continuous Compliance — map cloud posture to SOC 2, PCI-DSS, ISO 27001, CMMC, and HIPAA controls in real time with automated evidence.',
    'hero_title': 'Always audit-ready.\nNever scrambling.',
    'hero_sub': 'Continuous Compliance',
    'hero_sub_color': '#00d1ff',
    'lead': 'CloudSignals maps your cloud posture directly to SOC 2, PCI-DSS, ISO 27001, CMMC, and HIPAA controls — in real time. Every passing check generates reproducible evidence auditors can cite directly.',
    'icon': 'fa-shield-alt',
    'ql': ['Continuous control monitoring','SOC 2, PCI-DSS, ISO 27001, CMMC, HIPAA','Automated evidence collection','Real-time gap analysis','Audit-ready compliance reports','Control ownership tracking'],
    'caps': [
      ('fa-infinity','cyan','Continuous Control Monitoring','Every scan run maps findings to their relevant compliance controls automatically. Control status updates in real time as your environment changes.'),
      ('fa-globe','green','Broad Framework Coverage','SOC 2 Type II, PCI-DSS v4, ISO 27001:2022, CMMC Level 2, HIPAA, FedRAMP Moderate, and custom frameworks built for your industry.'),
      ('fa-paperclip','purple','Automated Evidence Collection','Every passing check generates a reproducible evidence artifact — API response, config snapshot, or resource state — that auditors can cite directly.'),
      ('fa-search','gold','Real-Time Gap Analysis','See which controls are passing, which are failing, and which have no coverage at a glance. Filter by framework, account, or owner.'),
      ('fa-file-pdf','cyan','Audit-Ready Reports','Generate compliance posture reports by framework, time period, or scope with one click. Export for external auditors or board presentations.'),
      ('fa-user-check','green','Control Ownership','Assign controls to owners inside the platform and track their review, sign-off, and exception approvals across the compliance lifecycle.'),
    ],
    'steps': [
      ('01','Select your frameworks','Choose from SOC 2, PCI-DSS, ISO 27001, CMMC, HIPAA, or all of them. CloudSignals maps your existing checks to each framework\'s requirements automatically.'),
      ('02','Scan and map findings','CloudSignals scans your environment and maps each check result to the relevant control requirements across your selected frameworks.'),
      ('03','Monitor, remediate, and report','See your compliance posture live, triage gaps with owners, and export evidence packages when auditors ask — in minutes, not weeks.'),
    ],
    'use_cases': ['SOC 2 audit preparation','PCI-DSS continuous validation','ISO 27001 gap analysis','CMMC Level 2 readiness','HIPAA compliance monitoring','Auditor evidence packages'],
    'plan_title': 'Compliance frameworks on every paid plan',
    'plan_body': 'Core compliance mapping is available on Growth and above. Framework breadth, report generation, and custom frameworks scale with Premium and Enterprise.',
    'cta_title': 'Get audit-ready without the scramble.',
    'cta_body': 'Start with a free scan of your cloud environment and see your compliance posture in minutes.',
  },
  {
    'file': 'cloudsignals-tprm.html',
    'title': 'Third-Party Risk (TPRM) | Vendor Risk Management | AiVRIC',
    'desc': 'CloudSignals+RiskOps™ TPRM — assess, monitor, and document the security posture of every vendor your organization relies on, with built-in compliance workflows.',
    'hero_title': 'Know the risk every\nvendor brings.',
    'hero_sub': 'Third-Party Risk Management',
    'hero_sub_color': '#fb923c',
    'lead': 'Vendor risk doesn\'t end at the contract. TPRM lets you assess, monitor, and document the security posture of every third party your organization relies on — with workflows built for compliance.',
    'icon': 'fa-handshake',
    'ql': ['Vendor risk assessments','Inherent risk classification','Continuous vendor monitoring','Document & artifact repository','Remediation request workflows','SOC 2 CC9.2 & ISO A.15 ready'],
    'caps': [
      ('fa-envelope-open-text','amber','Vendor Risk Assessments','Send standardized security questionnaires to vendors and track completion status, responses, and escalations in a single dashboard.'),
      ('fa-sort-numeric-up','cyan','Inherent Risk Scoring','Automatically classify vendors by data access level, service criticality, and regulatory exposure before launching a formal assessment.'),
      ('fa-eye','green','Continuous Monitoring','Re-assess vendor risk on a configurable schedule and get alerted when a vendor\'s posture, certification, or contract status changes.'),
      ('fa-folder-open','purple','Document Repository','Store contracts, SOC 2 reports, penetration test results, and vendor-provided artifacts in context — linked to the vendor record.'),
      ('fa-wrench','amber','Remediation Requests','Send structured remediation findings to vendors and track their closure with approval workflows and evidence requirements.'),
      ('fa-clipboard-check','cyan','Compliance-Ready Reports','Export TPRM activity logs formatted for SOC 2 CC9.2, ISO 27001 A.15, and CMMC SC.L2 third-party requirements.'),
    ],
    'steps': [
      ('01','Onboard your vendors','Add vendor records with business context — data access level, service criticality, and regulatory scope — to drive automatic risk classification.'),
      ('02','Assess and monitor','Send questionnaires, collect evidence, and set re-assessment schedules. CloudSignals tracks every response and escalation in one place.'),
      ('03','Report for compliance','Export TPRM summaries and evidence packages formatted for your compliance requirements when auditors or board reviews require them.'),
    ],
    'use_cases': ['SOC 2 CC9.2 vendor reviews','ISO 27001 supplier assessments','CMMC third-party requirements','Board vendor risk reporting','Vendor onboarding risk gates','Continuous vendor monitoring'],
    'plan_title': 'Available on Premium and Enterprise plans',
    'plan_body': 'TPRM is included on Premium and Enterprise. Vendor count limits and questionnaire customization scale with your tier.',
    'cta_title': 'Get visibility into your vendor ecosystem.',
    'cta_body': 'Talk to our team to set up TPRM for your vendor portfolio and compliance requirements.',
  },
  {
    'file': 'cloudsignals-vision-ai.html',
    'title': 'Vision AI & Narratives | AI-Powered Risk Analysis | AiVRIC',
    'desc': 'CloudSignals+RiskOps™ Vision AI — generate plain-language risk narratives, executive summaries, and remediation guidance from your live posture data.',
    'hero_title': 'AI that explains your risk,\nnot just reports it.',
    'hero_sub': 'Vision AI & Narratives',
    'hero_sub_color': '#a78bfa',
    'lead': 'CloudSignals Vision AI generates plain-language risk narratives, executive summaries, and remediation guidance from your live posture data — powered by AI models running in your environment.',
    'icon': 'fa-brain',
    'ql': ['Plain-language risk narratives','Executive & board summaries','Step-by-step remediation guidance','Natural language risk chat','Trend analysis & insights','Audit control narratives'],
    'caps': [
      ('fa-align-left','purple','Risk Narratives','Generate plain-language explanations of your highest-priority findings, written for non-technical stakeholders and audit reviewers.'),
      ('fa-chart-bar','gold','Executive Summaries','Produce board-ready risk summaries that translate technical posture data into business language — on demand or on a schedule.'),
      ('fa-magic','cyan','Remediation Guidance','Get step-by-step remediation instructions tailored to your specific cloud environment, generated by AI from the raw finding evidence.'),
      ('fa-comments','green','AI Chat Interface','Ask natural language questions about your posture, findings, and compliance status in real time. Get answers in plain English, not query language.'),
      ('fa-chart-line','purple','Trend Analysis','AI-generated insights on how your risk posture is improving or degrading over time — by control, environment, owner, or framework.'),
      ('fa-file-contract','gold','Evidence Narratives','Auto-generate the control narrative text auditors need from your evidence artifacts — reducing audit prep time from weeks to hours.'),
    ],
    'steps': [
      ('01','Connect your posture data','Vision AI draws directly from your live CloudSignals findings, risk register, and compliance posture — no data exports or manual uploads required.'),
      ('02','Generate narratives on demand','Select any finding, risk, or compliance scope and generate a plain-language narrative, remediation plan, or executive summary in seconds.'),
      ('03','Chat, refine, and export','Ask follow-up questions through the AI chat interface, refine the output, and export for reports, board decks, or audit packages.'),
    ],
    'use_cases': ['Executive risk reporting','Board presentations','Audit control narratives','Remediation guidance','Posture trend analysis','Compliance gap explanations'],
    'plan_title': 'Available on Premium and Enterprise plans',
    'plan_body': 'Vision AI & Narratives is included on Premium and Enterprise. AI generation limits and model selection options vary by tier.',
    'cta_title': 'Let AI translate your risk for every audience.',
    'cta_body': 'Upgrade to Premium to unlock Vision AI and start generating risk narratives from your live posture data.',
  },
]

# ── Build helpers ─────────────────────────────────────────────────────────────
def cap_html(icon, color, title, body):
    return f"""              <div class="cf-cap">
                <div class="cf-cap-icon {color}"><i class="fas {icon}"></i></div>
                <h4>{title}</h4>
                <p>{body}</p>
              </div>"""

def step_html(num, title, body):
    return f"""              <div class="cf-step">
                <div class="cf-step-num">{num}</div>
                <h4>{title}</h4>
                <p>{body}</p>
              </div>"""

def pill_html(text):
    return f'              <span class="cf-uc-pill"><i class="fas fa-circle"></i>{text}</span>'

def build_page(p):
    caps_html   = "\n".join(cap_html(*c)  for c in p['caps'])
    steps_block = "\n".join(step_html(*s) for s in p['steps'])
    pills_block = "\n".join(pill_html(u)  for u in p['use_cases'])
    ql_items    = "\n".join(f'                  <li><i class="fas fa-check"></i>{q}</li>' for q in p['ql'])
    title_html  = p['hero_title'].replace('\n', '<br>')

    HEAD = f"""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
<title>{p['title']}</title>
<meta name="description" content="{p['desc']}">
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
{FEATURE_CSS}
{GF_CSS}
</head>"""

    BODY_OPEN = NAV_BLOCK.replace('class="portal-page"', 'class="cf-page"')

    CONTENT = f"""
        <div class="cf-outer">

          <!-- ── HERO ──────────────────────────────────────────────────── -->
          <section class="cf-hero">
            <div class="auto-container">
              <div class="cf-hero-grid">

                <div>
                  <nav class="cf-breadcrumb">
                    <a href="index.html">Home</a><span>/</span>
                    <a href="cspm-cloudsignals.html">CloudSignals+RiskOps</a><span>/</span>
                    <span>{p['hero_sub']}</span>
                  </nav>
                  <div class="cf-badge">
                    <span class="cf-dot"></span>
                    Available in CloudSignals+RiskOps&trade;
                  </div>
                  <h1 class="cf-title">{title_html}</h1>
                  <p class="cf-sub" style="color:{p['hero_sub_color']}">{p['hero_sub']}</p>
                  <p class="cf-lead">{p['lead']}</p>
                  <div class="cf-actions">
                    <a href="cloudsignals-pricing.html" class="cf-btn primary"><i class="fas fa-bolt"></i> View plans &amp; pricing</a>
                    <a href="cspm-cloudsignals.html" class="cf-btn secondary">Platform overview</a>
                    <a href="request-demo.html" class="cf-btn ghost">Request a demo</a>
                  </div>
                </div>

                <div class="cf-aside">
                  <div class="cf-aside-card">
                    <h4>What you get</h4>
                    <ul class="cf-ql">
{ql_items}
                    </ul>
                  </div>
                  <a href="cloudsignals-pricing.html" class="cf-aside-link">
                    <span>Compare plans &amp; pricing</span>
                    <i class="fas fa-arrow-right"></i>
                  </a>
                </div>

              </div>
            </div>
          </section>

          <!-- ── CAPABILITIES ───────────────────────────────────────────── -->
          <section class="cf-section">
            <div class="auto-container">
              <span class="cf-eyebrow">Key capabilities</span>
              <h2 class="cf-sec-title">Built for security teams that move fast.</h2>
              <div class="cf-cap-grid">
{caps_html}
              </div>
            </div>
          </section>

          <!-- ── HOW IT WORKS ───────────────────────────────────────────── -->
          <section class="cf-section">
            <div class="auto-container">
              <span class="cf-eyebrow">How it works</span>
              <h2 class="cf-sec-title">Simple to start. Powerful at scale.</h2>
              <div class="cf-steps-grid">
{steps_block}
              </div>
            </div>
          </section>

          <!-- ── USE CASES ─────────────────────────────────────────────── -->
          <section class="cf-section">
            <div class="auto-container">
              <span class="cf-eyebrow">Common use cases</span>
              <div class="cf-uc-row">
{pills_block}
              </div>
            </div>
          </section>

          <div class="cf-divider"></div>

          <!-- ── PLAN STRIP ─────────────────────────────────────────────── -->
          <div class="cf-section">
            <div class="auto-container">
              <div class="cf-plan-strip">
                <div>
                  <h3>{p['plan_title']}</h3>
                  <p>{p['plan_body']}</p>
                </div>
                <div class="cf-plan-ctas">
                  <a href="cloudsignals-pricing.html" class="cf-btn primary"><i class="fas fa-bolt"></i> Compare plans</a>
                  <a href="cspm-cloudsignals.html" class="cf-btn ghost">Platform overview</a>
                </div>
              </div>
            </div>
          </div>

          <!-- ── BOTTOM CTA ─────────────────────────────────────────────── -->
          <div class="cf-section">
            <div class="auto-container">
              <div class="cf-bottom-cta">
                <h2>{p['cta_title']}</h2>
                <p>{p['cta_body']}</p>
                <div class="cf-cta-actions">
                  <a href="https://gcp-defense.aivric.com/sign-up?plan=pkg-cloudsignals-free&source=aivric_website" class="cf-btn primary" data-cloudsignals-free data-package-id="pkg-cloudsignals-free"><i class="fas fa-rocket"></i> Start free &mdash; no credit card</a>
                  <a href="request-demo.html" class="cf-btn ghost">Request a demo</a>
                </div>
              </div>
            </div>
          </div>

        </div><!-- /cf-outer -->"""

    TAIL = f"""
        {FOOTER_BLOCK}

        <!--Scroll to top-->
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
    <script src="assets/js/stripe-checkout.js"></script>
</body>
</html>"""

    return HEAD + "\n" + BODY_OPEN + CONTENT + TAIL


# ── Write pages ───────────────────────────────────────────────────────────────
built = 0
for page_data in PAGES:
    html = build_page(page_data)
    out = SITE / page_data['file']
    out.write_text(html, encoding="utf-8")
    print(f"  Built: {page_data['file']}  ({len(html.splitlines())} lines)")
    built += 1

print(f"\nDone. {built} pages built.")
