from pathlib import Path

SITE = Path(r"C:\Projects\AiVRIC-Website")
FREE_URL = "https://gcp-defense.aivric.com/sign-up?plan=pkg-cloudsignals-free&source=aivric_website"
CALENDLY = "https://calendly.com/aivric-sales/aivric-walkthrough-demo"

OLD_ONE = f'href="{CALENDLY}" class="theme-btn-one">Request a Demo</a>'
NEW_ONE = f'href="{FREE_URL}" class="theme-btn-one">Launch for Free</a>'

OLD_TWO = f'href="{CALENDLY}" class="theme-btn-two">Request a Demo</a>'
NEW_TWO = f'href="{FREE_URL}" class="theme-btn-two">Launch for Free</a>'

files_changed = replaced_count = 0

for f in sorted(SITE.glob("*.html")):
    raw = f.read_text(encoding="utf-8", errors="replace")
    updated = raw.replace(OLD_ONE, NEW_ONE).replace(OLD_TWO, NEW_TWO)
    if updated != raw:
        count = raw.count(OLD_ONE) + raw.count(OLD_TWO)
        replaced_count += count
        files_changed += 1
        f.write_text(updated, encoding="utf-8")

print(f"Files changed: {files_changed}  |  Buttons updated: {replaced_count}")
