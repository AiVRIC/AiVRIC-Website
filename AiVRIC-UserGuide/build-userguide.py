#!/usr/bin/env python3
"""
AiVRIC Platform Guide — v3 rebuild
Generates/updates every page in AiVRIC-UserGuide/ with:
  - new dark-glass header
  - expanded sidebar nav covering all 40+ pages
  - refreshed search JS with full page index
  - preserved inner content on policy pages
  - full new homepage (index.html)
"""
from pathlib import Path
from html import escape

GUIDE = Path(__file__).parent

# ─── Page index (used in search + sidebar) ────────────────────────────────
PAGE_INDEX = [
    ("Platform Guide Home",          "index.html"),
    ("Getting Started",              "getting-started.html"),
    ("Platform Overview",            "platform-overview.html"),
    ("CloudSignals+RiskOps Overview","cloudsignals-riskops.html"),
    ("Connectors",                   "connectors.html"),
    ("Integrations",                 "integrations.html"),
    ("Security & Trust",             "security-trust.html"),
    ("AI Governance",                "ai-governance.html"),
    ("Compliance Overview",          "compliance.html"),
    ("FAQ & Support",                "faq.html"),
    ("Insider Early Access",         "insider-early-access.html"),
    ("Cloud Security",               "cloud-security.html"),
    ("Network Security",             "network-security.html"),
    ("Endpoint Security",            "endpoint-security.html"),
    ("Identity & Access Control",    "identification-authorization-control.html"),
    ("Data Classification",          "data-classification-handling.html"),
    ("Data Privacy",                 "data-privacy.html"),
    ("Incident Response",            "incident-response-operations.html"),
    ("Threat Management",            "threat-management.html"),
    ("Vulnerability & Patch Mgmt",   "vulnerability-patch-management.html"),
    ("Security Operations",          "security-operations.html"),
    ("Risk Assessment",              "risk-assessment.html"),
    ("Third-Party Management",       "third-party-management.html"),
    ("AI & Autonomous Technologies", "ai-autonomous-technologies.html"),
    ("Secure Engineering Architecture","secure-engineering-architecture.html"),
    ("Web Security",                 "web-security.html"),
    ("Asset Management",             "asset-management.html"),
    ("Cryptographic Operations",     "cryptographic-operations.html"),
    ("Information Assurance",        "information-assurance.html"),
    ("Acceptable Use Policy",        "acceptable-use-policy.html"),
    ("Business Continuity & DR",     "business-continuity-disaster-recovery.html"),
    ("Capacity & Performance Mgmt",  "capacity-performance-management.html"),
    ("Maintenance",                  "maintenance.html"),
    ("Security Awareness & Training","security-awareness-training.html"),
    ("Mobile Device Management",     "mobile-device-management.html"),
    ("Physical & Environmental Security","physical-environmental-security.html"),
    ("HR Security",                  "human-resources-security.html"),
    ("Project & Resource Management","project-resource-management.html"),
    ("Tech Dev & Acquisition",       "technology-development-acquisition.html"),
    ("Security & Privacy Governance","security-privacy-governance.html"),
]

# data-page attribute → file mapping
FILE_TO_PAGE = {url: title for title, url in PAGE_INDEX}

# ─── Shared HTML blocks ────────────────────────────────────────────────────
def head_block(title: str, desc: str, canonical: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
  <title>{escape(title)}</title>
  <link rel="canonical" href="{canonical}">
  <meta name="description" content="{escape(desc)}">
  <link rel="icon" href="../assets/images/Aivric-favicon-logo.ico" type="image/x-icon">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Jost:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link href="../assets/css/font-awesome-all.css" rel="stylesheet">
  <link href="../assets/css/bootstrap.css" rel="stylesheet">
  <link href="userguide.css?v=3" rel="stylesheet">
</head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-EG2Q8GD30V"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-EG2Q8GD30V');
</script>"""


HEADER_HTML = """  <header class="guide-header">
    <div class="bar">
      <a class="brand" href="index.html">
        <img src="../assets/images/logo/aivric.svg" alt="AiVRIC">
        <span class="brand-sep"></span>
        <span class="brand-sub">Platform Guide</span>
      </a>
      <div class="top-links">
        <a href="../index.html">AiVRIC.com</a>
        <a href="../trust.html">Trust Center</a>
        <a href="../support.html">Support</a>
        <a href="insider-early-access.html" class="ug-cta">Insider Access</a>
      </div>
      <div class="guide-search">
        <i class="fas fa-search" aria-hidden="true"></i>
        <input id="guide-search-input" type="search" placeholder="Search the Platform Guide…" aria-label="Search the AiVRIC Platform Guide">
        <span class="ug-kbd">⌘K</span>
        <div class="search-results" id="guide-search-results"></div>
      </div>
      <button class="nav-toggle" type="button" aria-label="Toggle navigation" onclick="document.getElementById('sidebar').classList.toggle('open')">Menu</button>
    </div>
  </header>"""


def sidebar_html(active_file: str) -> str:
    def link(title, url):
        cls = 'nav-link active' if url == active_file else 'nav-link'
        return f'        <a class="{cls}" href="{url}">{escape(title)}</a>'

    return f"""    <aside class="guide-sidebar" id="sidebar">
      <div class="nav-section">
        <p class="nav-label">Quick Start</p>
{link("Overview", "index.html")}
{link("Getting Started", "getting-started.html")}
{link("Platform Overview", "platform-overview.html")}
      </div>
      <div class="nav-section">
        <p class="nav-label">CloudSignals+RiskOps</p>
{link("Module Overview", "cloudsignals-riskops.html")}
{link("Connectors", "connectors.html")}
{link("Integrations", "integrations.html")}
      </div>
      <div class="nav-section">
        <p class="nav-label">Assurance</p>
{link("Security & Trust", "security-trust.html")}
{link("AI Governance", "ai-governance.html")}
{link("Compliance Overview", "compliance.html")}
{link("FAQ & Support", "faq.html")}
      </div>
      <div class="nav-section">
        <p class="nav-label">Security Policies</p>
{link("Cloud Security", "cloud-security.html")}
{link("Network Security", "network-security.html")}
{link("Endpoint Security", "endpoint-security.html")}
{link("Identity & Access Control", "identification-authorization-control.html")}
{link("Data Classification", "data-classification-handling.html")}
{link("Data Privacy", "data-privacy.html")}
{link("Incident Response", "incident-response-operations.html")}
{link("Threat Management", "threat-management.html")}
{link("Vuln & Patch Mgmt", "vulnerability-patch-management.html")}
{link("Security Operations", "security-operations.html")}
{link("Risk Assessment", "risk-assessment.html")}
{link("Third-Party Mgmt", "third-party-management.html")}
      </div>
      <div class="nav-section">
        <p class="nav-label">Platform Policies</p>
{link("AI & Autonomous Tech", "ai-autonomous-technologies.html")}
{link("Secure Engineering", "secure-engineering-architecture.html")}
{link("Web Security", "web-security.html")}
{link("Asset Management", "asset-management.html")}
{link("Cryptographic Ops", "cryptographic-operations.html")}
{link("Information Assurance", "information-assurance.html")}
{link("Acceptable Use", "acceptable-use-policy.html")}
      </div>
      <div class="nav-section">
        <p class="nav-label">Operations</p>
{link("Business Continuity & DR", "business-continuity-disaster-recovery.html")}
{link("Capacity Management", "capacity-performance-management.html")}
{link("Maintenance", "maintenance.html")}
{link("Security Awareness", "security-awareness-training.html")}
{link("Mobile Device Mgmt", "mobile-device-management.html")}
{link("Physical Security", "physical-environmental-security.html")}
{link("HR Security", "human-resources-security.html")}
{link("Project Management", "project-resource-management.html")}
{link("Tech Dev & Acquisition", "technology-development-acquisition.html")}
{link("Privacy & Governance", "security-privacy-governance.html")}
      </div>
      <div class="nav-section">
        <p class="nav-label">More</p>
{link("Insider Early Access", "insider-early-access.html")}
      </div>
    </aside>"""


SEARCH_JS = """  <script>
    (function(){
      var searchInput = document.getElementById('guide-search-input');
      var resultsBox  = document.getElementById('guide-search-results');
      var pageIndex = """ + str([{"title": t, "url": u} for t, u in PAGE_INDEX]).replace("'", '"') + """;
      var pageCache = {};

      function sanitize(t){ return t.replace(/[<>]/g, function(c){ return c==='<'?'&lt;':'&gt;'; }); }

      function getPageText(page){
        if(pageCache[page.url]) return Promise.resolve(pageCache[page.url]);
        return fetch(page.url).then(function(r){ return r.text(); }).then(function(html){
          var doc = new DOMParser().parseFromString(html, 'text/html');
          var main = doc.querySelector('.guide-content') || doc.body;
          var text = (main.textContent||'').replace(/\\s+/g,' ').trim();
          pageCache[page.url] = text;
          return text;
        }).catch(function(){ return ''; });
      }

      async function performSearch(raw){
        var query = raw.trim().toLowerCase();
        if(!resultsBox) return;
        if(query.length < 2){ resultsBox.innerHTML=''; resultsBox.classList.remove('open'); return; }
        var matches = [];
        for(var i=0; i<pageIndex.length; i++){
          var page = pageIndex[i];
          var text = await getPageText(page);
          var hay = text.toLowerCase();
          var idx = hay.indexOf(query);
          if(idx===-1) continue;
          var start = Math.max(0,idx-70);
          var end = Math.min(text.length,idx+140);
          var snippet = sanitize(text.slice(start,end));
          matches.push({title:page.title, url:page.url, snippet:snippet});
        }
        if(!matches.length){
          resultsBox.innerHTML='<div class="no-results">No matches found.</div>';
          resultsBox.classList.add('open'); return;
        }
        resultsBox.innerHTML = matches.slice(0,8).map(function(m){
          return '<a class="result" href="'+m.url+'"><strong>'+m.title+'</strong><span>'+m.snippet+'…</span></a>';
        }).join('');
        resultsBox.classList.add('open');
      }

      if(searchInput && resultsBox){
        searchInput.addEventListener('input', function(e){ performSearch(e.target.value); });
        searchInput.addEventListener('focus', function(){ if(resultsBox.innerHTML) resultsBox.classList.add('open'); });
      }
      document.addEventListener('click', function(e){
        if(!resultsBox) return;
        if(!resultsBox.contains(e.target) && searchInput && !searchInput.contains(e.target))
          resultsBox.classList.remove('open');
      });
    })();
  </script>"""


FOOTER_HTML = """  <footer class="guide-footer">
    <span>&copy; 2025 AiVRIC Technologies &mdash; <a href="../privacy-policy.html">Privacy</a> &middot; <a href="acceptable-use-policy.html">Acceptable Use</a></span>
    <span class="tag">Platform Guide v3</span>
  </footer>"""


# ─── Inner page template ───────────────────────────────────────────────────
def inner_page(title: str, desc: str, filename: str, canonical: str,
               content_html: str, toc_html: str = "") -> str:
    if not toc_html:
        toc_html = """    <aside class="guide-toc">
      <p class="toc-title">On this page</p>
      <div class="toc-links"></div>
    </aside>"""
    return f"""{head_block(title, desc, canonical)}
<body data-page="{filename.replace('.html','')}">
{HEADER_HTML}

  <div class="guide-shell">
{sidebar_html(filename)}

    <main class="guide-content" id="main-content">
{content_html}
    </main>

{toc_html}
  </div>

{FOOTER_HTML}
{SEARCH_JS}
  <script src="../assets/js/support-form.js"></script>
</body>
</html>"""


# ═══════════════════════════════════════════════════════════════════════════
# INDEX.HTML — Full new homepage
# ═══════════════════════════════════════════════════════════════════════════
INDEX_HTML = f"""{head_block(
    "AiVRIC Platform Guide",
    "The complete resource center for AiVRIC: onboarding, module documentation, security policies, governance, and support.",
    "https://aivric.com/AiVRIC-UserGuide/index.html"
)}
<body data-page="home">
{HEADER_HTML}

  <main class="handbook-main">

    <!-- Hero -->
    <div class="handbook-hero">
      <span class="badge">AiVRIC Platform Guide</span>
      <h1>Everything you need<br>to run AiVRIC.</h1>
      <p>Onboarding guides, connector references, compliance policies, and governance documentation — organized for security teams and platform administrators.</p>
      <div class="handbook-actions">
        <a class="tag" href="getting-started.html" style="background:rgba(0,209,255,.1);border-color:rgba(0,209,255,.3);color:#00d1ff;font-weight:700;">Start onboarding &rarr;</a>
        <a class="tag" href="platform-overview.html">Platform overview</a>
        <a class="tag" href="../trust.html">Trust Center</a>
        <a class="tag" href="faq.html">FAQ &amp; Support</a>
      </div>
    </div>

    <!-- Quick-start paths -->
    <p class="ug-section-label">Quick paths</p>
    <div class="ug-paths">
      <a class="ug-path-card" href="getting-started.html">
        <div class="ug-path-icon cyan"><i class="fas fa-rocket"></i></div>
        <div class="ug-path-label">New to AiVRIC?</div>
        <div class="ug-path-desc">Workspace setup, team invites, and your first connector — in under 30 minutes.</div>
        <div class="ug-path-arrow">Getting Started &rarr;</div>
      </a>
      <a class="ug-path-card" href="connectors.html">
        <div class="ug-path-icon green"><i class="fas fa-plug"></i></div>
        <div class="ug-path-label">Connect cloud accounts</div>
        <div class="ug-path-desc">AWS, Azure, GCP, Kubernetes, GitHub, Microsoft 365, and more.</div>
        <div class="ug-path-arrow">Connector guides &rarr;</div>
      </a>
      <a class="ug-path-card" href="cloudsignals-riskops.html">
        <div class="ug-path-icon amber"><i class="fas fa-shield-alt"></i></div>
        <div class="ug-path-label">Set up compliance</div>
        <div class="ug-path-desc">Map controls to SOC 2, ISO 27001, PCI DSS, HIPAA, and CMMC frameworks automatically.</div>
        <div class="ug-path-arrow">CloudSignals+RiskOps &rarr;</div>
      </a>
      <a class="ug-path-card" href="ai-governance.html">
        <div class="ug-path-icon purple"><i class="fas fa-brain"></i></div>
        <div class="ug-path-label">Govern AI workloads</div>
        <div class="ug-path-desc">Approval workflows, guardrails, lifecycle controls, and policy enforcement for AI models.</div>
        <div class="ug-path-arrow">AI Governance &rarr;</div>
      </a>
    </div>

    <!-- Core docs -->
    <p class="ug-section-label">Core documentation</p>
    <section class="handbook-grid" aria-label="Core documentation">
      <article class="handbook-card">
        <h3>&#x1F4CB; Getting Started</h3>
        <p>Set up workspaces, configure SSO, connect cloud providers, and invite your team.</p>
        <ul>
          <li><a href="getting-started.html">Onboarding checklist</a></li>
          <li><a href="connectors.html">Connectors setup guide</a></li>
          <li><a href="https://calendly.com/aivric-sales/aivric-walkthrough-demo">Book a guided setup</a></li>
        </ul>
      </article>
      <article class="handbook-card">
        <h3>&#x1F6E1;&#xFE0F; CloudSignals+RiskOps&trade;</h3>
        <p>Continuous cloud posture monitoring, compliance automation, and AI-driven remediation.</p>
        <ul>
          <li><a href="cloudsignals-riskops.html">Module overview</a></li>
          <li><a href="connectors.html">Connect cloud accounts</a></li>
          <li><a href="cloudsignals-riskops.html#compliance">Framework mapping</a></li>
          <li><a href="integrations.html">SIEM &amp; ticketing integrations</a></li>
        </ul>
      </article>
      <article class="handbook-card">
        <h3>&#x1F50C; Connectors &amp; Integrations</h3>
        <p>Step-by-step setup for every supported cloud provider, data source, and alerting destination.</p>
        <ul>
          <li><a href="connectors.html#aws">AWS</a></li>
          <li><a href="connectors.html#azure">Microsoft Azure</a></li>
          <li><a href="connectors.html#gcp">Google Cloud Platform</a></li>
          <li><a href="connectors.html#k8s">Kubernetes</a></li>
          <li><a href="connectors.html">All connectors &rarr;</a></li>
        </ul>
      </article>
      <article class="handbook-card">
        <h3>&#x1F510; Security &amp; Trust</h3>
        <p>Data handling, access controls, and compliance posture details.</p>
        <ul>
          <li><a href="security-trust.html">Platform Security &amp; Trust</a></li>
          <li><a href="../trust.html">AiVRIC Trust Center</a></li>
          <li><a href="ai-governance.html">AI Governance guide</a></li>
        </ul>
      </article>
      <article class="handbook-card">
        <h3>&#x2139;&#xFE0F; About AiVRIC</h3>
        <p>Company values, product philosophy, and platform vision.</p>
        <ul>
          <li><a href="../why-aivric.html">Why AiVRIC</a></li>
          <li><a href="../about.html">About us</a></li>
          <li><a href="../aivric-vision.html">Platform vision</a></li>
        </ul>
      </article>
      <article class="handbook-card">
        <h3>&#x2753; FAQ &amp; Support</h3>
        <p>Quick answers, support contacts, and working session booking.</p>
        <ul>
          <li><a href="faq.html">Frequently asked questions</a></li>
          <li><a href="mailto:support@aivric.com">support@aivric.com</a></li>
          <li><a href="https://calendly.com/aivric-sales/aivric-walkthrough-demo">Schedule a working session</a></li>
        </ul>
      </article>
    </section>

    <!-- Quick-launch tiles -->
    <p class="ug-section-label">Quick-launch</p>
    <section class="policy-section" aria-label="Quick launch tiles">
      <div class="policy-card">
        <h2>Platform guide sections</h2>
        <p>Quick access to core areas of the AiVRIC Platform Guide.</p>
        <div class="policy-link-grid">
          <a class="policy-pill" href="getting-started.html">
            <div class="pill-inner">
              <div class="pill-face pill-front"><span class="pill-acronym">START</span><span class="pill-title">Getting Started</span></div>
              <div class="pill-face pill-back"><span class="pill-acronym">START</span><span class="pill-desc">Onboarding steps, invites, and workspace setup.</span></div>
            </div>
          </a>
          <a class="policy-pill" href="platform-overview.html">
            <div class="pill-inner">
              <div class="pill-face pill-front"><span class="pill-acronym">PLATFORM</span><span class="pill-title">Platform Overview</span></div>
              <div class="pill-face pill-back"><span class="pill-acronym">PLATFORM</span><span class="pill-desc">Architecture, connectors, and guardrails tour.</span></div>
            </div>
          </a>
          <a class="policy-pill" href="security-trust.html">
            <div class="pill-inner">
              <div class="pill-face pill-front"><span class="pill-acronym">TRUST</span><span class="pill-title">Security &amp; Trust</span></div>
              <div class="pill-face pill-back"><span class="pill-acronym">TRUST</span><span class="pill-desc">Trust Center summaries and compliance posture.</span></div>
            </div>
          </a>
          <a class="policy-pill" href="ai-governance.html">
            <div class="pill-inner">
              <div class="pill-face pill-front"><span class="pill-acronym">AI GOV</span><span class="pill-title">AI Governance</span></div>
              <div class="pill-face pill-back"><span class="pill-acronym">AI GOV</span><span class="pill-desc">Approvals, controls, and lifecycle for AI workloads.</span></div>
            </div>
          </a>
          <a class="policy-pill" href="faq.html">
            <div class="pill-inner">
              <div class="pill-face pill-front"><span class="pill-acronym">FAQ</span><span class="pill-title">FAQ &amp; Support</span></div>
              <div class="pill-face pill-back"><span class="pill-acronym">FAQ</span><span class="pill-desc">Quick answers on setup, roles, and support.</span></div>
            </div>
          </a>
          <a class="policy-pill" href="cloudsignals-riskops.html">
            <div class="pill-inner">
              <div class="pill-face pill-front"><span class="pill-acronym">CS+RO</span><span class="pill-title">CloudSignals+RiskOps</span></div>
              <div class="pill-face pill-back"><span class="pill-acronym">CS+RO</span><span class="pill-desc">Continuous posture monitoring, compliance, and risk scoring.</span></div>
            </div>
          </a>
        </div>
      </div>
    </section>

    <!-- Policy library -->
    <p class="ug-section-label">Policy library</p>
    <div class="ug-policy-hub">
      <div class="ug-policy-group">
        <div class="ug-policy-group-title">Security policies</div>
        <div class="ug-policy-links">
          <a class="ug-policy-link" href="cloud-security.html">Cloud Security</a>
          <a class="ug-policy-link" href="network-security.html">Network Security</a>
          <a class="ug-policy-link" href="endpoint-security.html">Endpoint Security</a>
          <a class="ug-policy-link" href="identification-authorization-control.html">Identity &amp; Access</a>
          <a class="ug-policy-link" href="data-classification-handling.html">Data Classification</a>
          <a class="ug-policy-link" href="data-privacy.html">Data Privacy</a>
          <a class="ug-policy-link" href="incident-response-operations.html">Incident Response</a>
          <a class="ug-policy-link" href="threat-management.html">Threat Management</a>
          <a class="ug-policy-link" href="vulnerability-patch-management.html">Vuln &amp; Patch Mgmt</a>
          <a class="ug-policy-link" href="security-operations.html">Security Operations</a>
          <a class="ug-policy-link" href="risk-assessment.html">Risk Assessment</a>
          <a class="ug-policy-link" href="third-party-management.html">Third-Party Mgmt</a>
        </div>
      </div>
      <div class="ug-policy-group">
        <div class="ug-policy-group-title">Platform policies</div>
        <div class="ug-policy-links">
          <a class="ug-policy-link" href="ai-autonomous-technologies.html">AI &amp; Autonomous Tech</a>
          <a class="ug-policy-link" href="secure-engineering-architecture.html">Secure Engineering</a>
          <a class="ug-policy-link" href="web-security.html">Web Security</a>
          <a class="ug-policy-link" href="asset-management.html">Asset Management</a>
          <a class="ug-policy-link" href="cryptographic-operations.html">Cryptographic Ops</a>
          <a class="ug-policy-link" href="information-assurance.html">Information Assurance</a>
          <a class="ug-policy-link" href="acceptable-use-policy.html">Acceptable Use</a>
        </div>
      </div>
      <div class="ug-policy-group">
        <div class="ug-policy-group-title">Operations</div>
        <div class="ug-policy-links">
          <a class="ug-policy-link" href="business-continuity-disaster-recovery.html">Business Continuity &amp; DR</a>
          <a class="ug-policy-link" href="capacity-performance-management.html">Capacity Management</a>
          <a class="ug-policy-link" href="maintenance.html">Maintenance</a>
          <a class="ug-policy-link" href="security-awareness-training.html">Security Awareness</a>
          <a class="ug-policy-link" href="mobile-device-management.html">Mobile Device Mgmt</a>
          <a class="ug-policy-link" href="physical-environmental-security.html">Physical Security</a>
          <a class="ug-policy-link" href="human-resources-security.html">HR Security</a>
          <a class="ug-policy-link" href="project-resource-management.html">Project Mgmt</a>
          <a class="ug-policy-link" href="technology-development-acquisition.html">Tech Dev &amp; Acquisition</a>
          <a class="ug-policy-link" href="security-privacy-governance.html">Privacy &amp; Governance</a>
        </div>
      </div>
    </div>

    <!-- Support strip -->
    <p class="ug-section-label">Support</p>
    <div class="ug-support-strip">
      <div class="ug-support-item">
        <div class="ug-support-label">Email support</div>
        <div class="ug-support-value"><a href="mailto:support@aivric.com">support@aivric.com</a></div>
      </div>
      <div class="ug-support-item">
        <div class="ug-support-label">Phone</div>
        <div class="ug-support-value"><a href="tel:+19543426637">+1-954-342-6637</a> &mdash; Mon&ndash;Fri, 8am&ndash;6pm ET</div>
      </div>
      <div class="ug-support-item">
        <div class="ug-support-label">Live session</div>
        <div class="ug-support-value"><a href="https://calendly.com/aivric-sales/aivric-walkthrough-demo">Book a guided setup &rarr;</a></div>
      </div>
      <div class="ug-support-item">
        <div class="ug-support-label">Response SLA</div>
        <div class="ug-support-value">Standard: 1 business day &mdash; Urgent: same-day triage</div>
      </div>
    </div>

  </main>

{FOOTER_HTML}
{SEARCH_JS}
</body>
</html>"""


# ═══════════════════════════════════════════════════════════════════════════
# GETTING STARTED
# ═══════════════════════════════════════════════════════════════════════════
GETTING_STARTED_CONTENT = """      <span class="badge">Onboarding</span>
      <h1>Getting started</h1>
      <p>Launch AiVRIC quickly with a secure baseline. Follow the four-step flow below, then connect your first cloud account.</p>

      <div class="ug-steps">
        <div class="ug-step">
          <div class="ug-step-num">1</div>
          <div class="ug-step-body">
            <h3>Plan workspaces</h3>
            <p>Map environments to workspaces (e.g., prod, staging, R&amp;D). Align each with data sensitivity and named owners.</p>
            <ul>
              <li>Define owners in IAM groups before inviting users.</li>
              <li>Enable SSO and SCIM first to enforce directory-driven access.</li>
            </ul>
          </div>
        </div>
        <div class="ug-step">
          <div class="ug-step-num">2</div>
          <div class="ug-step-body">
            <h3>Secure access</h3>
            <p>Use SSO + MFA; grant least-privilege roles in cloud accounts. Configure break-glass with short-lived tokens.</p>
            <ul>
              <li>Map cloud roles to AiVRIC permission groups.</li>
              <li>Audit login attempts weekly; alert on anomalies.</li>
            </ul>
          </div>
        </div>
        <div class="ug-step">
          <div class="ug-step-num">3</div>
          <div class="ug-step-body">
            <h3>Connect systems</h3>
            <p>Connect cloud accounts, Kubernetes clusters, GitHub, and ticketing to start continuous control monitoring.</p>
            <ul>
              <li>Use deployment templates provided per connector.</li>
              <li>Verify data collection scope before enabling enforcement.</li>
            </ul>
          </div>
        </div>
        <div class="ug-step">
          <div class="ug-step-num">4</div>
          <div class="ug-step-body">
            <h3>Apply guardrails</h3>
            <p>Enable policy packs for compliance (SOC 2, ISO 27001) and AI safeguards (PII, secrets, jailbreaks).</p>
            <ul>
              <li>Run dry-runs first; review impact report before enforcing.</li>
              <li>Promote to enforce mode after stakeholder sign-off.</li>
            </ul>
          </div>
        </div>
      </div>

      <h2 id="connect">Connect your environment</h2>
      <p>All connectors are powered by <strong>CloudSignals+RiskOps&trade;</strong> — AiVRIC's continuous posture monitoring engine. Every connected provider is audited automatically on a 24-hour cycle.</p>
      <table class="table">
        <thead><tr><th>Provider</th><th>Purpose</th><th>Quick action</th></tr></thead>
        <tbody>
          <tr><td>AWS</td><td>Monitor IAM hygiene, network rules, and resource configurations for drift.</td><td>Deploy read-only IAM role via CloudFormation Quick Link.</td></tr>
          <tr><td>Microsoft Azure</td><td>Audit subscriptions for misconfigurations, identity posture, and policy compliance.</td><td>Create App Registration + Service Principal; enter Tenant ID, Client ID, Secret.</td></tr>
          <tr><td>Google Cloud Platform</td><td>Scan GCP projects for posture drift and framework control gaps.</td><td>Create read-only Service Account; paste JSON key into AiVRIC.</td></tr>
          <tr><td>Kubernetes</td><td>Secure cluster workloads, service account access, and runtime configurations.</td><td>Paste kubeconfig; apply read-only RBAC manifests.</td></tr>
          <tr><td>GitHub</td><td>Protect repos, branch protections, secrets exposure, and pipeline tokens.</td><td>Connect via PAT, OAuth App, or GitHub App.</td></tr>
          <tr><td>Microsoft 365</td><td>Monitor tenant controls for SOC 2, PCI DSS, and CMMC compliance.</td><td>Register Entra ID app; configure certificate authentication.</td></tr>
          <tr><td>MongoDB Atlas</td><td>Audit database cluster configurations and access controls.</td><td>Generate an Atlas API key pair and paste into AiVRIC.</td></tr>
          <tr><td>Alibaba Cloud</td><td>Monitor resource configurations and IAM posture for drift.</td><td>Use RAM Role Assumption or static credentials.</td></tr>
          <tr><td>Jira / ServiceNow</td><td>Send findings to owners and track remediation bidirectionally.</td><td>Connect via OAuth; map severity to ticket priority.</td></tr>
        </tbody>
      </table>
      <div class="callout primary">
        <strong>Full connector guides</strong> — step-by-step instructions and authentication details for every provider — are on the <a href="connectors.html">Connectors page</a>.
      </div>

      <h2 id="collaborate">Collaborate and ship</h2>
      <div class="list-grid">
        <ul>
          <li><strong>Approvals:</strong> Require dual approval for high-impact guardrails; log who approved and when.</li>
          <li><strong>Change windows:</strong> Align policy changes with your release calendar.</li>
          <li><strong>Notifications:</strong> Route critical findings to Slack/Teams with runbooks attached.</li>
        </ul>
        <ul>
          <li><strong>Observability:</strong> Forward audit logs to your SIEM; tag events by workspace.</li>
          <li><strong>Testing:</strong> Validate connectors in staging workspaces before production.</li>
          <li><strong>Ownership:</strong> Keep owners visible in tickets for fast escalation.</li>
        </ul>
      </div>

      <h2 id="resources">Resources</h2>
      <div class="guide-grid">
        <div class="guide-card">
          <h3>Connector setup guides</h3>
          <p>Step-by-step instructions for all eight supported cloud providers.</p>
          <a href="connectors.html">View all connectors</a>
        </div>
        <div class="guide-card">
          <h3>CloudSignals+RiskOps overview</h3>
          <p>Scan cadence, compliance mapping, alerts, SIEM integration, and reporting.</p>
          <a href="cloudsignals-riskops.html">Read the overview</a>
        </div>
        <div class="guide-card">
          <h3>Trust Center</h3>
          <p>SOC 2 readiness, penetration testing summaries, and data handling details.</p>
          <a href="../trust.html">Open Trust Center</a>
        </div>
        <div class="guide-card">
          <h3>Support</h3>
          <p>Live working sessions available. We'll walk through your setup with you.</p>
          <a href="../support.html">Contact support</a>
        </div>
      </div>"""

GETTING_STARTED_TOC = """    <aside class="guide-toc">
      <p class="toc-title">On this page</p>
      <div class="toc-links">
        <a href="#checklist">Four steps</a>
        <a href="#connect">Connect</a>
        <a href="#collaborate">Collaborate</a>
        <a href="#resources">Resources</a>
      </div>
    </aside>"""


# ═══════════════════════════════════════════════════════════════════════════
# PLATFORM OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════
PLATFORM_OVERVIEW_CONTENT = """      <span class="badge">Documentation</span>
      <h1>Platform overview</h1>
      <p>AiVRIC is an autonomous security, compliance, and risk intelligence platform that runs in your environment. This page covers the architecture, modules, guardrails, and operational model.</p>

      <h2 id="architecture">Architecture</h2>
      <p>AiVRIC is composed of four interconnected modules deployed as containerized services on your Kubernetes cluster. All processing stays in your environment — no data leaves your control plane.</p>
      <div class="guide-grid">
        <div class="guide-card">
          <h3>CloudSignals+RiskOps&trade;</h3>
          <p>Continuous cloud posture monitoring, compliance automation, and AI-driven risk remediation across AWS, Azure, GCP, Kubernetes, and more.</p>
        </div>
        <div class="guide-card">
          <h3>AI Signals&trade;</h3>
          <p>Real-time detection of AI model misuse, shadow AI, prompt injection, PII leakage, and model drift across your AI workloads.</p>
        </div>
        <div class="guide-card">
          <h3>AIRE Agentic Mesh&trade;</h3>
          <p>Autonomous remediation engine that closes security gaps, raises tickets, and applies approved fixes without human handoff.</p>
        </div>
        <div class="guide-card">
          <h3>RogueAgent ASPM&trade;</h3>
          <p>Application Security Posture Management for agentic and AI-driven applications — tracks permissions, dependencies, and runtime behavior.</p>
        </div>
        <div class="guide-card">
          <h3>Vision AI Optics&trade;</h3>
          <p>AI/ML-powered threat intelligence and behavioral analytics that surface anomalies before they become incidents.</p>
        </div>
        <div class="guide-card">
          <h3>Shared Data Layer</h3>
          <p>A unified data fabric that normalizes signals from every connected source into a single risk-aware context model.</p>
        </div>
      </div>

      <h2 id="connectors">Connectors</h2>
      <p>AiVRIC connects to your environment via read-only, least-privilege integrations. No agents required for cloud accounts.</p>
      <table class="table">
        <thead><tr><th>Category</th><th>Supported providers</th></tr></thead>
        <tbody>
          <tr><td>Cloud providers</td><td>AWS, Microsoft Azure, Google Cloud Platform, Alibaba Cloud</td></tr>
          <tr><td>Container &amp; Kubernetes</td><td>Amazon EKS, Azure AKS, Google GKE, self-managed clusters</td></tr>
          <tr><td>Source control</td><td>GitHub, GitLab (roadmap)</td></tr>
          <tr><td>SaaS productivity</td><td>Microsoft 365 / Entra ID</td></tr>
          <tr><td>Databases</td><td>MongoDB Atlas</td></tr>
          <tr><td>Ticketing &amp; alerting</td><td>Jira, ServiceNow, PagerDuty, Slack, Microsoft Teams</td></tr>
          <tr><td>SIEM</td><td>Splunk, Microsoft Sentinel, Elastic SIEM (via webhook)</td></tr>
        </tbody>
      </table>

      <h2 id="guardrails">Guardrails</h2>
      <p>Guardrails are policy-as-code rules that AiVRIC evaluates continuously. They can run in <strong>Detect</strong> (alert only), <strong>Prevent</strong> (block + alert), or <strong>Remediate</strong> (auto-fix + alert) mode.</p>
      <div class="callout primary">
        Always start in <strong>Detect</strong> mode and review impact for at least one scan cycle before promoting to Prevent or Remediate.
      </div>
      <div class="guide-grid">
        <div class="guide-card">
          <h3>Compliance packs</h3>
          <p>Pre-built control mappings for SOC 2 Type II, ISO 27001, PCI DSS, HIPAA, NIST CSF, CIS Benchmarks, CMMC, and more.</p>
        </div>
        <div class="guide-card">
          <h3>AI safeguards</h3>
          <p>Detect PII exfiltration, model hallucinations, prompt injection, unauthorized model access, and jailbreak attempts in real time.</p>
        </div>
        <div class="guide-card">
          <h3>Custom rules</h3>
          <p>Author guardrails in YAML or Python. AiVRIC evaluates them within the same scan cadence as built-in rules.</p>
        </div>
      </div>

      <h2 id="deployment">Deployment model</h2>
      <p>AiVRIC deploys into your Kubernetes cluster using Helm charts managed by ArgoCD. All images are pulled from your private container registry — no public internet egress required at runtime.</p>
      <div class="callout warn">
        AiVRIC requires cluster-admin permissions during initial Helm install only. Runtime permissions are scoped to the <code>aivric</code> namespace via RBAC.
      </div>

      <h2 id="data">Data handling</h2>
      <p>AiVRIC processes configuration metadata — not customer data. All findings, scan results, and audit logs are stored in your environment's PostgreSQL instance and are never transmitted to AiVRIC infrastructure.</p>
      <div class="guide-grid">
        <div class="guide-card">
          <h3>Data residency</h3>
          <p>100% in-environment. Your cloud, your cluster, your data store. AiVRIC never receives your findings or cloud configurations.</p>
        </div>
        <div class="guide-card">
          <h3>Encryption</h3>
          <p>TLS 1.3 in transit; AES-256 at rest via your cloud provider's KMS. Secrets stored in Azure Key Vault / AWS Secrets Manager.</p>
        </div>
        <div class="guide-card">
          <h3>Audit logging</h3>
          <p>Every platform action is logged with actor, timestamp, and outcome. Logs forward to your SIEM via configurable webhook.</p>
        </div>
      </div>"""

PLATFORM_OVERVIEW_TOC = """    <aside class="guide-toc">
      <p class="toc-title">On this page</p>
      <div class="toc-links">
        <a href="#architecture">Architecture</a>
        <a href="#connectors">Connectors</a>
        <a href="#guardrails">Guardrails</a>
        <a href="#deployment">Deployment</a>
        <a href="#data">Data handling</a>
      </div>
    </aside>"""


# ═══════════════════════════════════════════════════════════════════════════
# FAQ
# ═══════════════════════════════════════════════════════════════════════════
FAQ_CONTENT = """      <span class="badge">Support</span>
      <h1>FAQ &amp; Support</h1>
      <p>Frequently asked questions about setup, security, billing, and platform operations. Can't find what you need? <a href="mailto:support@aivric.com">Contact support</a>.</p>

      <h2 id="setup">Setup &amp; onboarding</h2>
      <div class="guide-card" style="margin-bottom:10px">
        <h3>How long does initial setup take?</h3>
        <p>Most teams complete workspace setup and connect their first cloud account in under 30 minutes using our guided onboarding flow. Full multi-cloud coverage typically takes 1–2 hours.</p>
      </div>
      <div class="guide-card" style="margin-bottom:10px">
        <h3>Do I need to install an agent?</h3>
        <p>No agents are required for cloud accounts (AWS, Azure, GCP, Alibaba Cloud). AiVRIC uses read-only API credentials. For Kubernetes, you apply a small read-only RBAC manifest — no sidecar required.</p>
      </div>
      <div class="guide-card" style="margin-bottom:10px">
        <h3>What permissions does AiVRIC require?</h3>
        <p>Read-only permissions across all cloud and SaaS integrations. AiVRIC never writes to your cloud environment during scans. Remediation actions are gated by explicit approvals. See the <a href="connectors.html">Connectors page</a> for per-provider permission scopes.</p>
      </div>

      <h2 id="security">Security &amp; compliance</h2>
      <div class="guide-card" style="margin-bottom:10px">
        <h3>Where is my data stored?</h3>
        <p>100% in your environment. AiVRIC deploys into your Kubernetes cluster. Findings, scan results, and audit logs stay in your PostgreSQL instance. Nothing is transmitted to AiVRIC's infrastructure.</p>
      </div>
      <div class="guide-card" style="margin-bottom:10px">
        <h3>Is AiVRIC SOC 2 compliant?</h3>
        <p>AiVRIC is SOC 2 Type II ready. Visit the <a href="../trust.html">Trust Center</a> for current compliance documentation, penetration test summaries, and data handling details.</p>
      </div>
      <div class="guide-card" style="margin-bottom:10px">
        <h3>What compliance frameworks are supported?</h3>
        <p>CloudSignals+RiskOps includes pre-built control mappings for SOC 2, ISO 27001, PCI DSS, HIPAA, NIST CSF, CIS Benchmarks, CMMC, and GDPR. Custom frameworks can be authored in YAML.</p>
      </div>

      <h2 id="billing">Billing &amp; plans</h2>
      <div class="guide-card" style="margin-bottom:10px">
        <h3>What plans are available?</h3>
        <p>AiVRIC is available in Starter, Professional, and Enterprise tiers. See <a href="../pricing.html">Pricing</a> or contact <a href="mailto:sales@aivric.com">sales@aivric.com</a> for enterprise pricing.</p>
      </div>
      <div class="guide-card" style="margin-bottom:10px">
        <h3>Can I trial AiVRIC before buying?</h3>
        <p>Yes. <a href="https://calendly.com/aivric-sales/aivric-walkthrough-demo">Book a guided walkthrough</a> to see the platform against a real cloud environment, or request a proof-of-concept deployment for your team.</p>
      </div>

      <h2 id="support">Contact support</h2>
      <div class="support-grid">
        <div class="policy-card">
          <h3>Contact &amp; hours</h3>
          <ul class="policy-list">
            <li>Email: <a href="mailto:support@aivric.com">support@aivric.com</a></li>
            <li>Phone: <a href="tel:+19543426637">+1-954-342-6637</a> (Mon–Fri, 8:00 am – 6:00 pm ET)</li>
            <li>Standard response target: within one business day</li>
            <li>Urgent (security/compliance risk): same-day triage</li>
            <li><a href="faq.html">FAQs</a> &middot; <a href="https://calendly.com/aivric-sales/aivric-walkthrough-demo">Schedule a working session</a></li>
          </ul>
        </div>
        <div class="policy-card">
          <h3>Submit a support request</h3>
          <form id="support-form" class="support-form" onsubmit="return false;">
            <div><label for="support-name">Full Name</label><input id="support-name" name="name" type="text" placeholder="Your name" required></div>
            <div><label for="support-email">Work Email</label><input id="support-email" name="email" type="email" placeholder="you@company.com" required></div>
            <div><label for="support-company">Organization</label><input id="support-company" name="company" type="text" placeholder="Company name"></div>
            <div><label for="support-plan">Plan</label>
              <select id="support-plan" name="plan">
                <option value="">Select your plan</option>
                <option value="defense-starter">AiVRIC Defense — Starter</option>
                <option value="defense-professional">AiVRIC Defense — Professional</option>
                <option value="defense-enterprise">AiVRIC Defense — Enterprise</option>
                <option value="aivric-plus">AiVRIC+ Services Platform</option>
                <option value="managed-grc">Managed GRC Services</option>
                <option value="other">Other / Evaluating</option>
              </select>
            </div>
            <div><label for="support-priority">Priority</label>
              <select id="support-priority" name="priority">
                <option value="normal">Normal</option>
                <option value="high">High — Production Impact</option>
                <option value="urgent">Urgent — Security or Compliance Risk</option>
              </select>
            </div>
            <div><label for="support-subject">Subject</label><input id="support-subject" name="subject" type="text" placeholder="Short summary of your request" required></div>
            <div><label for="support-message">Details</label><textarea id="support-message" name="message" placeholder="Describe the issue. Include environment, error messages, and recent changes." required></textarea></div>
            <div><small>By submitting, you consent to AiVRIC using this info to respond per our <a href="../privacy-policy.html">Privacy Policy</a>.</small></div>
            <div><button type="submit">Submit Support Request</button></div>
          </form>
        </div>
      </div>"""

FAQ_TOC = """    <aside class="guide-toc">
      <p class="toc-title">On this page</p>
      <div class="toc-links">
        <a href="#setup">Setup</a>
        <a href="#security">Security</a>
        <a href="#billing">Billing</a>
        <a href="#support">Contact</a>
      </div>
    </aside>"""


# ═══════════════════════════════════════════════════════════════════════════
# TEMPLATE FOR POLICY PAGES (extract + rewrap existing content)
# ═══════════════════════════════════════════════════════════════════════════
def extract_guide_content(raw: str) -> str:
    """Pull the inner HTML from <main class="guide-content">…</main>."""
    import re
    # Try to find content between <main class="guide-content"> and </main>
    m = re.search(r'<main[^>]*class="guide-content"[^>]*>(.*?)</main>',
                  raw, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1)
    # Fallback: content between opening guide-content div and closing
    m = re.search(r'<div[^>]*class="guide-content"[^>]*>(.*?)</div>\s*(?:<aside|</div>)',
                  raw, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1)
    return ""


def rewrap_policy_page(filename: str) -> bool:
    """Read existing policy page, extract content, write new shell around it."""
    path = GUIDE / filename
    if not path.exists():
        print(f"  SKIP (not found): {filename}")
        return False

    raw = path.read_text(encoding="utf-8", errors="replace")

    # Extract existing title from <title> tag
    import re
    title_m = re.search(r'<title>(.*?)</title>', raw, re.IGNORECASE)
    raw_title = title_m.group(1) if title_m else f"AiVRIC Platform Guide | {filename}"
    # Normalize title
    title = raw_title.replace("AiVRIC User Guide |", "AiVRIC Platform Guide |").strip()

    desc_m = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]*)"', raw, re.IGNORECASE)
    desc = desc_m.group(1) if desc_m else ""

    content = extract_guide_content(raw)
    if not content.strip():
        print(f"  WARN (no content extracted): {filename}")
        return False

    canonical = f"https://aivric.com/AiVRIC-UserGuide/{filename}"
    new_html = inner_page(title, desc, filename, canonical, content)
    path.write_text(new_html, encoding="utf-8")
    return True


# ─── Build all pages ───────────────────────────────────────────────────────
def main():
    # 1. Homepage
    (GUIDE / "index.html").write_text(INDEX_HTML, encoding="utf-8")
    print("Built: index.html")

    # 2. Getting started
    gs = inner_page(
        "AiVRIC Platform Guide | Getting Started",
        "Onboard to AiVRIC with setup steps, workspace design, connectors, and team collaboration guidance.",
        "getting-started.html",
        "https://aivric.com/AiVRIC-UserGuide/getting-started.html",
        GETTING_STARTED_CONTENT,
        GETTING_STARTED_TOC,
    )
    (GUIDE / "getting-started.html").write_text(gs, encoding="utf-8")
    print("Built: getting-started.html")

    # 3. Platform overview
    po = inner_page(
        "AiVRIC Platform Guide | Platform Overview",
        "Understand the AiVRIC platform architecture, modules, connectors, guardrails, and operational model.",
        "platform-overview.html",
        "https://aivric.com/AiVRIC-UserGuide/platform-overview.html",
        PLATFORM_OVERVIEW_CONTENT,
        PLATFORM_OVERVIEW_TOC,
    )
    (GUIDE / "platform-overview.html").write_text(po, encoding="utf-8")
    print("Built: platform-overview.html")

    # 4. FAQ
    faq = inner_page(
        "AiVRIC Platform Guide | FAQ & Support",
        "Frequently asked questions about AiVRIC: setup, security, operations, and support contacts.",
        "faq.html",
        "https://aivric.com/AiVRIC-UserGuide/faq.html",
        FAQ_CONTENT,
        FAQ_TOC,
    )
    (GUIDE / "faq.html").write_text(faq, encoding="utf-8")
    print("Built: faq.html")

    # 5. Rewrap all remaining policy / inner pages
    skip = {"index.html", "getting-started.html", "platform-overview.html",
            "faq.html", "userguide.css", "build-userguide.py"}

    rewrapped = 0
    for html_file in sorted(GUIDE.glob("*.html")):
        if html_file.name in skip:
            continue
        ok = rewrap_policy_page(html_file.name)
        if ok:
            rewrapped += 1
            print(f"  Rewrapped: {html_file.name}")

    print(f"\nDone — 4 full rebuilds + {rewrapped} rewrapped pages.")


if __name__ == "__main__":
    main()
