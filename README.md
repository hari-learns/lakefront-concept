# Lakefront Home Hotel — website concept

Static design proposal. Not the live site. Plain HTML/CSS/JS — no framework,
no build tool, no npm install. Deployed via GitHub Pages.

## Structure

```
index.html                    Homepage
room-*.html                   6 room detail pages
gallery.html                  Full photo gallery + lightbox
policy-*.html                 Booking / cancellation / privacy / terms
404.html                      Not-found page

styles.css                    Shared stylesheet — every page links this
script-main.js                Shared behaviour: mobile menu, scroll reveals,
                               day-trips sticky counter, lightbox
script-reviews.js             Homepage-only: the reviews marquee

assets/                       Processed, web-ready images (.webp) + logo +
                               the promo video (lakefront-promo.mp4)
fonts/                        Playfair Display + Archivo, self-hosted woff2

build_src/img/                Raw source photography (originals, ~66MB)
assets.py                     Resizes build_src/img/ → assets/*.webp
build.py                      Generates every HTML page from shared
                               partials + the data in build.py itself
template-home.html            The homepage's structural shell — build.py
                               reads this, swaps in external CSS/JS links
                               and current room/gallery/policy hrefs, and
                               writes the result to index.html
```

`template-home.html` is a real, checked-in file — not a scratch snapshot.
Never hand-edit `index.html` directly; edits go in `template-home.html`,
and `python3 build.py` regenerates `index.html` from it every time.

## Editing content

Room copy, gallery photo selection, and policy text all live as data inside
**`build.py`** (the `ROOMS`, `GALLERY_IMAGES`, `POLICIES` lists near the top).
Edit there, then rebuild:

```bash
python3 build.py
```

This regenerates every HTML page. It's idempotent — safe to run repeatedly.

To change the homepage's own structure (not just room/gallery/policy
content — e.g. editing the hero, the amenities grid, the day-trips
section), edit **`template-home.html`** directly, then run `python3
build.py` to regenerate `index.html` from it.

Policy text is pulled verbatim from the live WordPress site (not invented —
see `parse_policy()` in `build.py`). If the real policies change, re-fetch
and re-run rather than hand-editing the generated HTML.

## Adding new photos

1. Drop the new source JPEGs into `build_src/img/`.
2. Add an entry to `SPEC` in `assets.py` (source filename, target width,
   crop aspect, quality).
3. Run:
   ```bash
   python3 assets.py   # regenerates assets/*.webp
   python3 build.py    # regenerates any page referencing the new image
   ```

Room-detail companion photos and the gallery page pull from the `n_0XXX`
sourced-but-unassigned pool — reassign these in `build.py`'s `ROOMS` /
`GALLERY_IMAGES` data as better/more specific photos become available.

## Local preview

```bash
python3 -m http.server 4321
```
Then open `http://localhost:4321/`.

## Deploy

Push to `main` on GitHub — Pages rebuilds automatically.
Live at: https://hari-learns.github.io/lakefront-concept/
