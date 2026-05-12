#!/usr/bin/env python3
"""
Fix cloudsignals-pricing.html:
  1. Remove duplicate HTML (entire page was appended twice)
  2. Replace old bootstrap footer with the global footer
"""
from pathlib import Path

SITE = Path(r"C:\Projects\AiVRIC-Website")
f    = SITE / "cloudsignals-pricing.html"
raw  = f.read_text(encoding="utf-8", errors="replace")

# ── 1. Cut at old footer comment (first occurrence) ───────────────────────────
CUT_MARKER = "  <!-- FOOTER -->"
cut = raw.find(CUT_MARKER)
assert cut != -1, "Could not find footer cut marker"
clean = raw[:cut]

# ── 2. Extract modals from first copy ─────────────────────────────────────────
MODAL_START = "  <!-- Release notification modal"
modal_pos = raw.find(MODAL_START)
assert modal_pos != -1, "Could not find release modal"

SCROLL_TOP = "  <div class=\"scroll-to-top\">"
scroll_pos = raw.find(SCROLL_TOP)
assert scroll_pos != -1, "Could not find scroll-to-top"

BODY_END = "  <div class=\"scroll-to-top\">"
scripts_start = raw.find("</div>\n\n<!-- JS -->", scroll_pos)
assert scripts_start != -1, "Could not find scripts block"

modals_block = raw[modal_pos : scroll_pos]

scripts_block = raw[scripts_start : raw.find("</body>", scripts_start) + len("</body>")]

# ── 3. Build global footer HTML ───────────────────────────────────────────────
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

        </footer>
        <!-- main-footer end -->"""

# ── 4. Assemble clean file ────────────────────────────────────────────────────
output = clean + "\n\n" + GF_FOOTER + "\n\n" + modals_block + "\n" + scripts_block + "\n</html>"

f.write_text(output, encoding="utf-8")
print(f"Fixed: cloudsignals-pricing.html  ({len(output.splitlines())} lines)")
