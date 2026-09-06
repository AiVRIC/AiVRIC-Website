# Inside AiVRIC — explorable operations floor

A static web experience that lives at `aivric.com/experience/`: a cinematic render of the AiVRIC / 3HUE operations
floor that visitors can walk through. Click a room (Defense, Client Vision, Offense, AIRE, Executive Decisions,
Fabric) to fly into a close-up render, then browse that room's solutions with real screenshots and video.

The concept shows how the AiVRIC platform converges with human operators from disparate teams around one shared
goal: Defense and Offense findings flow into Client Vision, AIRE coordinates approved remediation, and every stream
ends at the executive table where 3HUE advisors turn findings into decisions.

- No build step, no framework, no vendored libraries. Plain HTML, CSS, and ES modules. Fully independent of the
  Bootstrap/jQuery stack used by the rest of the site, so it can be iterated in isolation.
- Relative paths only. Product screenshots and clips are shared with the main site (`../academy/screenshots/`,
  `../assets/images/`); only the scene renders, the intro film, and one compressed walkthrough clip live under
  `experience/media/`.
- All copy, media, hotspots, and streams live in one manifest: `content/experience.json`.
- `tools/reference/inside-aivric-infographic.png` is the original image-first concept this experience was built
  from (the numbered Defense / Offense / Client Vision / 3HUE Advisor layout).

## Run locally

From the repo root (not from `experience/`, since media and links reach up into `../`):

```bash
python -m http.server 8000
# then open http://localhost:8000/experience/?skipintro=1
```

## Folder layout

```
experience/
  index.html                 shell (stage, HUD, panel, lightbox, intro)
  css/experience.css         styles and brand tokens
  js/main.js                 boot + routing glue
  js/stage.js                master render pan/zoom, room crossfade, parallax
  js/hotspots.js             pins anchored to normalized master coordinates
  js/streams.js              animated SVG information streams
  js/router.js               hash routes  #/  #/room/<id>  #/station/<id>
  js/ui/hud.js               top bar, room buttons, breadcrumb, mobile room strip
  js/ui/panel.js             station tabs, copy, media gallery, CTAs
  js/ui/lightbox.js          fullscreen image / video viewer
  js/ui/intro.js             opening film overlay
  content/experience.json    THE manifest
  media/scene/master.jpg     master wide shot (2560×1440)
  media/scene/rooms/*.jpg    per-room close-ups (2048×1152)
  media/cloudsignals/        compressed walkthrough clip + poster (the 42 MB original is in ../assets/videos)
  media/film/                intro film + poster
  tools/hotspot-tool.html    click-to-get-coordinates helper (dev only)
  tools/reference/           original concept infographic
  tools/render-prompts/      prompts used to generate the scene renders
```

## Where it is wired into the site

- `index.html` top bar: an "Explore the floor" link next to Platform Guide / Academy / Trust Center.
- `index.html` "Platform in Action" section: a "Walk the operations floor" CTA in the `ve-cta-row`.
- Other pages share the same header markup; add the top-bar link there when the experience is ready for prime time.
- Deep links work anywhere in marketing or sales emails, for example
  `https://aivric.com/experience/#/station/rogueagent` opens straight into the Offense room with RogueAgent selected.
- `?skipintro=1` skips the opening film. The film is also skipped automatically after the first visit in a session.

GitHub Pages serves `.js` modules with the right MIME type. No server configuration is required.
A copy of the site favicon ships in the folder so the page is self-contained.

## Add or change content

Everything is in `content/experience.json`.

### Add a screenshot or video to a station

1. If the screenshot already exists in the main site, reference it in place (`../academy/screenshots/...` or
   `../assets/images/...`). Otherwise drop the file into `media/<station-id>/` (create the folder if needed).
   Keep images ≤ 1600 px wide and videos ≤ 5 MB, H.264 MP4 or WebM.
2. Add an entry to that station's `media` array:
   ```json
   { "type": "image", "src": "../academy/screenshots/exposure-map.png", "caption": "External exposure map" }
   { "type": "video", "src": "media/rogueagent/demo.mp4", "poster": "media/rogueagent/demo-poster.jpg", "caption": "Recon pipeline demo" }
   ```
   The first item is shown largest in the panel. Empty `media` arrays render a styled "Add screenshot or video" slot.

### Station fields

| Field | Meaning |
|---|---|
| `id` | URL slug, used in `#/station/<id>` deep links |
| `name` | tab label |
| `status` | `live` · `beta` · `alpha` · `roadmap` · `coming-soon` · `service` · `platform` (drives the badge) |
| `suite` | small muted line next to the badge |
| `headline`, `summary` | panel copy |
| `capabilities` | bullet list |
| `media` | gallery items (see above) |
| `links` | CTAs; `"primary": true` makes a filled button |

### Add a room

1. Add an object to `rooms` with `id`, `name`, `tagline`, `streamColor` (`blue` · `coral` · `gold`), `hotspot`, `zoomTo`, `zoom`, `render`, `focus`, `stations`.
2. `hotspot` is where the pin sits on the master image, normalized 0–1. `zoomTo` is where the camera centers when entering (defaults to the hotspot). `zoom` is the magnification (2–3 works well).
3. `render` is the close-up image shown after the zoom. Set it to `null` to simply zoom into the master (that is what Fabric does). `focus` is the point in the render (0–1) that should land at the visible center.
4. Open `tools/hotspot-tool.html` in a browser (served, not from `file://`) and click on the master to read coordinates. Shift-click to trace a stream path, then "Finish path" to get a `d` string for the `streams` array.

### Streams

`streams` are SVG paths in master-image pixels (2560×1440). `color` picks the palette, `room` links the stream to a room so it brightens on hover, `delay` offsets the dash animation so parallel streams don't move in lockstep.

## Regenerate scene renders

The renders were produced with OpenAI `gpt-image-2` using the prompts in `tools/render-prompts/`. The shared
style block is `tools/render-style-block.txt`; each room prompt appends its own SCENE paragraph. Regenerate a room
by re-running its prompt at 2048×1152 (master at 2560×1440) and replacing the file in `media/scene/`. Renders
must contain **no text or UI**; the interface is real HTML drawn on top.

If a new master is generated, re-check `hotspot`, `zoomTo`, and `streams` with the hotspot tool. Everything else
is independent of the images.

## Behaviour notes

- Transitions use only `transform` and `opacity` (GPU-composited). Parallax follows the pointer on desktop only.
- `prefers-reduced-motion` disables parallax, stream animation, and long transitions.
- Under 768 px the panel becomes a bottom sheet and a scrollable room strip replaces the HUD room buttons.
- Esc closes the lightbox first, then exits the room. Browser back/forward works because routes are hash-based.
- Media is lazy-loaded per station; the master image (≈540 KB) and film (≈3 MB) are the only up-front loads.

## Credits

Concept and first build: 3HUE. Scene renders: generated imagery, direction by 3HUE. Product screenshots: AiVRIC
CloudSignals+RiskOps. Fonts: Jost and Inter via Google Fonts (same as aivric.com).
