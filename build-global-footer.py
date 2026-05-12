#!/usr/bin/env python3
"""Apply modern global footer to all HTML pages that contain <!-- main-footer -->."""
from pathlib import Path

SITE = Path(r"C:\Projects\AiVRIC-Website")

FOOTER_START_TAG = "<!-- main-footer"   # intentionally no closing --> to match variants
FOOTER_END_TAG   = "</footer>"

# ── INLINE CSS ─────────────────────────────────────────────────────────────────
GF_CSS = """<style id="gf-styles">
/* === GLOBAL FOOTER === */
.gf-footer{background:#050b17;position:relative;overflow:hidden;font-family:'Inter',sans-serif}
/* subtle dot-grid */
.gf-footer::before{content:'';position:absolute;inset:0;background-image:radial-gradient(rgba(0,209,255,.045) 1px,transparent 1px);background-size:28px 28px;pointer-events:none}
/* gradient glow top-line */
.gf-top-rule{height:1px;background:linear-gradient(90deg,transparent 0%,rgba(0,209,255,.55) 30%,rgba(46,229,157,.4) 70%,transparent 100%);position:relative;z-index:1}
/* body */
.gf-body{padding:72px 0 52px;position:relative;z-index:1}
.gf-grid{display:grid;grid-template-columns:1.45fr 1fr 1fr 1fr;gap:52px}
@media(max-width:991px){.gf-grid{grid-template-columns:1fr 1fr;gap:36px 40px}}
@media(max-width:599px){.gf-grid{grid-template-columns:1fr;gap:32px}}
/* brand col */
.gf-logo-link{display:inline-block;margin-bottom:14px}
.gf-logo{height:34px;width:auto;display:block}
.gf-tagline{font-size:13px;color:#4e637a;line-height:1.7;margin-bottom:22px;max-width:255px}
/* email subscribe */
.gf-subscribe-row{display:flex;gap:0;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);border-radius:8px;overflow:hidden;margin-bottom:7px;transition:border-color .2s}
.gf-subscribe-row:focus-within{border-color:rgba(0,209,255,.35)}
.gf-subscribe-row input{flex:1;background:transparent;border:none;outline:none;padding:10px 14px;font-size:13px;color:#e2e8f0;font-family:'Inter',sans-serif}
.gf-subscribe-row input::placeholder{color:#3d5268}
.gf-subscribe-row button{background:#00d1ff;border:none;padding:10px 15px;color:#030a12;cursor:pointer;font-size:13px;transition:background .2s;flex-shrink:0}
.gf-subscribe-row button:hover{background:#33daff}
.gf-subscribe-note{font-size:11px;color:#3d5268;margin:0 0 22px}
/* social */
.gf-social{display:flex;gap:8px}
.gf-social-link{width:33px;height:33px;border-radius:8px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);display:flex;align-items:center;justify-content:center;color:#4e637a;font-size:13px;text-decoration:none;transition:all .2s}
.gf-social-link:hover{background:rgba(0,209,255,.09);border-color:rgba(0,209,255,.28);color:#00d1ff}
/* nav columns */
.gf-col-title{font-size:10.5px;font-weight:800;letter-spacing:2px;text-transform:uppercase;color:#94a3b8;margin-bottom:16px;padding-bottom:11px;border-bottom:1px solid rgba(255,255,255,.06)}
.gf-links{list-style:none;padding:0;margin:0 0 22px;display:flex;flex-direction:column;gap:9px}
.gf-links li a{font-size:13.5px;color:#4e637a;text-decoration:none;transition:color .18s;display:inline-block}
.gf-links li a:hover{color:#cbd5e1}
/* contact block */
.gf-contact-block{display:flex;flex-direction:column;gap:9px;margin-top:4px}
.gf-contact-link{display:flex;align-items:center;gap:8px;font-size:13px;color:#4e637a;text-decoration:none;transition:color .18s}
.gf-contact-link i{color:#00d1ff;font-size:12px;width:14px;text-align:center;flex-shrink:0}
.gf-contact-link:hover{color:#cbd5e1}
/* bottom bar */
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
/* remove old footer pattern images */
.gf-footer .pattern-layer{display:none!important}
/* keep old .main-footer link colors from interfering */
.gf-footer .links-list,.gf-footer .footer-widget,.gf-footer .widget-section,.gf-footer .footer-bottom{display:none!important}
</style>"""

# ── FOOTER HTML ────────────────────────────────────────────────────────────────
GF_FOOTER = """        <!-- main-footer -->
        <footer class="main-footer gf-footer">

          <div class="gf-top-rule"></div>

          <div class="gf-body">
            <div class="auto-container">
              <div class="gf-grid">

                <!-- Brand -->
                <div class="gf-col">
                  <a href="index.html" class="gf-logo-link">
                    <img src="assets/images/logo/Aivric-logo-footer-1.avif" alt="AiVRIC" class="gf-logo">
                  </a>
                  <p class="gf-tagline">Autonomous Security, Compliance, and Risk Intelligence — hosted in your environment.</p>
                  <form class="gf-subscribe" action="contact.html" method="post">
                    <div class="gf-subscribe-row">
                      <input type="email" name="email" placeholder="Work email address" required>
                      <button type="submit" aria-label="Subscribe"><i class="fas fa-paper-plane"></i></button>
                    </div>
                    <p class="gf-subscribe-note">No spam &mdash; platform updates only.</p>
                  </form>
                  <div class="gf-social">
                    <a href="https://www.linkedin.com/company/aivric" class="gf-social-link" aria-label="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
                    <a href="https://x.com/aivric" class="gf-social-link" aria-label="X / Twitter"><i class="fab fa-twitter"></i></a>
                    <a href="https://www.facebook.com/61581937785235/" class="gf-social-link" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
                    <a href="https://www.instagram.com/aivrictechnologies/" class="gf-social-link" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
                  </div>
                </div>

                <!-- Platform -->
                <div class="gf-col">
                  <div class="gf-col-title">Platform</div>
                  <ul class="gf-links">
                    <li><a href="services.html">Platform Overview</a></li>
                    <li><a href="genai-chat.html">GenAI Chat</a></li>
                    <li><a href="shared-data-layer.html">Shared Data Layer</a></li>
                    <li><a href="agentic-design.html">Agentic Design</a></li>
                    <li><a href="efficient-compute.html">Efficient Compute</a></li>
                    <li><a href="data-localization.html">Data Localization</a></li>
                    <li><a href="ai-model-inspection.html">AI Model Inspection</a></li>
                  </ul>
                </div>

                <!-- Solutions -->
                <div class="gf-col">
                  <div class="gf-col-title">Solutions</div>
                  <ul class="gf-links">
                    <li><a href="cspm-cloudsignals.html">CloudSignals+RiskOps&trade;</a></li>
                    <li><a href="ai-inspector.html">AI Signals&trade;</a></li>
                    <li><a href="air-remediation.html">AIRE Agentic Mesh&trade;</a></li>
                    <li><a href="rogueagent.html">RogueAgent ASPM&trade;</a></li>
                    <li><a href="aivric-vision-professional.html">Vision AI Optics&trade;</a></li>
                    <li><a href="aivric-vision-enterprise.html">Vision Enterprise</a></li>
                    <li><a href="solutions-portal.html">All Products &rarr;</a></li>
                  </ul>
                </div>

                <!-- Company + Contact -->
                <div class="gf-col">
                  <div class="gf-col-title">Company</div>
                  <ul class="gf-links">
                    <li><a href="about.html">About Us</a></li>
                    <li><a href="why-aivric.html">Why AiVRIC</a></li>
                    <li><a href="pricing.html">Pricing</a></li>
                    <li><a href="blog-portal.html">Blog</a></li>
                    <li><a href="trust.html">Trust Center</a></li>
                    <li><a href="https://aivric.com/AiVRIC-UserGuide/index.html">Platform Guide</a></li>
                  </ul>
                  <div class="gf-contact-block">
                    <a href="mailto:info@aivric.com" class="gf-contact-link"><i class="fas fa-envelope"></i>info@aivric.com</a>
                    <a href="tel:+19543426637" class="gf-contact-link"><i class="fas fa-phone-alt"></i>+1 954 342 6637</a>
                  </div>
                </div>

              </div>
            </div>
          </div>

          <div class="gf-bottom">
            <div class="auto-container">
              <div class="gf-bottom-inner">
                <p class="gf-copy">&copy; 2025 <a href="index.html">AiVRIC Technologies</a>. All Rights Reserved.</p>
                <div class="gf-bottom-right">
                  <span class="gf-trust-pill"><span class="gf-trust-dot"></span>SOC&nbsp;2 Ready</span>
                  <nav class="gf-bottom-nav">
                    <a href="terms-of-use.html">Terms of Service</a>
                    <a href="privacy-policy.html">Privacy Policy</a>
                  </nav>
                </div>
              </div>
            </div>
          </div>

        </footer>"""


# ── UPDATE PAGES ──────────────────────────────────────────────────────────────

pages = sorted(SITE.glob("*.html"))
updated = skipped = 0

for page in pages:
    raw = page.read_text(encoding="utf-8", errors="replace")

    # Find footer start — try comment anchor first, fall back to opening tag variants
    fi = raw.find(FOOTER_START_TAG)
    if fi == -1:
        fi = raw.find('<footer class="main-footer">')
    if fi == -1:
        # footer tag with extra attributes (style="...", etc.)
        import re as _re
        m = _re.search(r'<footer\s+class="main-footer"', raw)
        fi = m.start() if m else -1
    if fi == -1:
        skipped += 1
        continue

    # Find the closing </footer> tag
    ei = raw.find(FOOTER_END_TAG, fi)
    if ei == -1:
        skipped += 1
        continue
    ei += len(FOOTER_END_TAG)

    # Inject CSS before </head> if not already present
    if 'id="gf-styles"' not in raw:
        raw = raw.replace("</head>", GF_CSS + "\n</head>", 1)
        # Recalculate positions after CSS injection
        fi = raw.find(FOOTER_START_TAG)
        ei = raw.find(FOOTER_END_TAG, fi) + len(FOOTER_END_TAG)

    # Replace footer
    output = raw[:fi] + GF_FOOTER + raw[ei:]
    page.write_text(output, encoding="utf-8")
    updated += 1

print(f"Updated: {updated}  |  Skipped (no footer anchor): {skipped}")
