"""Static page generator for the Lakefront Home Hotel concept site.

Every page shares styles.css / script-main.js (and script-reviews.js on the
homepage only). Run: python3 build.py
"""
import hashlib
import html
import os
import re

BOOK = ("https://www.secure-booking-engine.com/accounts/2S8j5jeLZTQDF2DJYkD8OA/"
        "properties/nnvHaXiO3ObYitpHgYS-mA/booking-engine/web/source/4wsctBw6Oq6j-g9XuxeRzQ/")
WHATSAPP = "https://wa.me/919385620698"
STYLE_VERSION = hashlib.sha256(open("styles.css", "rb").read()).hexdigest()[:12]
MAIN_SCRIPT_VERSION = hashlib.sha256(open("script-main.js", "rb").read()).hexdigest()[:12]
REVIEWS_SCRIPT_VERSION = hashlib.sha256(open("script-reviews.js", "rb").read()).hexdigest()[:12]

ROOMS = [
    # slug, name, hero image, short blurb (homepage card copy, unchanged),
    # spec line, gallery images (from the newly sourced pool), long body
    dict(
        slug="room-family-multi-suite", name="Family Multi-Suite", img="rm_family",
        blurb="Thoughtfully designed for families &mdash; spacious suites combining modern amenities with the warmth of a home, and the balance of shared moments and personal space.",
        ideal="Families", bed="Multiple beds", gallery=["n_0817", "n_0925", "n_0838"],
        body="Set within the original 1937 bungalow, the Family Multi-Suite pairs the heritage woodwork of the house with enough room to actually spread out. It's built around the idea that a family holiday shouldn't mean everyone in one cramped box &mdash; there's space to gather together in the evening and room to close a door when someone wants quiet. Wardrobes, seating, and the original teak detailing throughout give it the same character as the rest of the house, just at family scale.",
    ),
    dict(
        slug="room-honeymoon-lakeview-suite", name="Honeymoon Lakeview Suite", img="rm_honeymoon",
        blurb="An intimate, beautifully decorated suite for couples celebrating their love, with a king-size bed and open views over the hills.",
        ideal="Couples", bed="King-size bed", gallery=["n_0906", "n_0958", "n_0919"],
        body="A dedicated retreat for couples, built around a king-size bed and generous windows that open onto the hills above Ooty Lake. The room is decorated with a lighter touch than the rest of the property &mdash; less heritage formality, more quiet comfort &mdash; and it's the room guests most often ask for by name when they mention it's a honeymoon or an anniversary.",
    ),
    dict(
        slug="room-deluxe-lakeview-rooms", name="Deluxe Lakeview Rooms", img="rm_deluxe",
        blurb="Lake-facing rooms with the bungalow's original woodwork and generous windows onto the water.",
        ideal="Couples or solo travellers", bed="Double bed", gallery=["n_0785", "n_0741", "n_0632"],
        body="These are the rooms that face the water. The bungalow's original wooden beams and window frames are still in place, and the lake-facing aspect means the morning mist off Ooty Lake is the first thing you see. Simple, well-kept, and the closest rooms to what the house actually looked like when it was still called Lourdesville Bungalow.",
    ),
    dict(
        slug="room-lakeview-premium-room", name="Lakeview Premium Room", img="rm_premium",
        blurb="Thoughtfully designed and well-appointed &mdash; a cosy retreat with modern amenities, and a delightful blend of comfort and convenience.",
        ideal="Couples or small families", bed="Double bed", gallery=["n_0663", "n_0674", "n_0817"],
        body="A step up in space and finish while staying true to the bungalow's character &mdash; period furniture alongside the modern essentials guests actually expect (television, filtered water, dependable Wi-Fi). Well-appointed without losing the cosy, lived-in feel that runs through the rest of the house.",
    ),
    dict(
        slug="room-the-economy-rooms", name="The Economy Rooms", img="rm_economy",
        blurb="Affordability without compromising comfort. Built for budget-conscious travellers: a cosy, practical stay with all the essentials.",
        ideal="Budget-conscious travellers", bed="Double bed", gallery=["n_0756", "n_0702", "n_0838"],
        body="Built for travellers who want a genuinely comfortable stay without paying for space they won't use. Every essential is here &mdash; a proper bed, hot water, television, Wi-Fi &mdash; inside the same heritage building as every other room, just at a price that keeps Ooty within reach.",
    ),
    dict(
        slug="room-lakeview-mini-suite", name="Lakeview Mini-Suite", img="rm_mini",
        blurb="A compact, stylish retreat for solo travellers and couples &mdash; every comfort you need, nothing you don't.",
        ideal="Solo travellers or couples", bed="Double bed", gallery=["n_0584", "n_0686", "n_0923"],
        body="A compact room that doesn't feel like a compromise. Everything a solo traveller or a couple actually needs is here, styled with the same dark-wood, heritage character as the rest of the property, just scaled down &mdash; and priced accordingly.",
    ),
]

AMENITIES = ["Camp fire", "Scenic view", "Wi-Fi access", "Room service",
             "Television", "Filtered water", "Parking available", "Driver accommodation"]

GALLERY_IMAGES = [
    ("hero", "Misty morning in the garden", "fg-a"),
    ("facade", "The heritage bungalow facade", ""),
    ("corridor", "The verandah corridor", ""),
    ("n_0617", "Curtained window, guest room", "fg-b"),
    ("n_0906", "Dark-wood suite interior", ""),
    ("n_0785", "Lake-facing room", ""),
    ("n_0663", "Guest room seating", ""),
    ("n_0702", "Bay window, guest room", "fg-a"),
    ("n_0838", "Room with garden view", ""),
    ("n_0925", "Family suite interior", ""),
    ("n_0584", "Exterior, garden side", ""),
    ("n_0919", "Suite entrance", "fg-b"),
    ("n_0674", "Guest room detail", ""),
    ("n_0958", "Dark-wood suite, wide view", ""),
    ("n_0756", "Economy room interior", ""),
    ("n_0883", "Garden and swing, daylight", ""),
    ("n_0923", "Mini-suite interior", ""),
    ("n_0632", "Misty tree line", ""),
    ("n_0741", "Guest room corner", ""),
    ("n_0817", "Family suite seating", ""),
]

POLICIES = [
    dict(slug="policy-booking", nav="Booking Policy", title="Booking Policy", src="booking-policy"),
    dict(slug="policy-cancellation", nav="Cancellation & Refund", title="Cancellation and Refund Policy", src="cancellation-policy"),
    dict(slug="policy-privacy", nav="Privacy Policy", title="Privacy Policy", src="privacypolicy"),
    dict(slug="policy-terms", nav="Terms & Conditions", title="Terms and Conditions", src="terms-and-condition"),
]

# These are the public URLs indexed by the WordPress site.  GitHub Pages does
# not provide server-side redirects, so each path gets a small, relative
# redirect document.  Relative targets work both at the GitHub project URL and
# later at the root of lakefronthomehotel.com.
LEGACY_PATHS = {
    "room-1": "room-family-multi-suite.html",
    "2024/02/privacypolicy": "policy-privacy.html",
    "2024/02/booking-policy": "policy-booking.html",
    "2024/02/cancellation-policy": "policy-cancellation.html",
    "2024/02/terms-and-condition": "policy-terms.html",
}


def esc(s):
    return html.escape(s, quote=True)


def nav_links(home):
    prefix = "" if home else "index.html"
    return (
        f'<a href="{prefix}#heritage">About</a>\n'
        f'      <a href="{prefix}#rooms">Rooms</a>\n'
        f'      <a href="{prefix}#trips">Day Trips</a>\n'
        f'      <a href="gallery.html">Gallery</a>\n'
        f'      <a href="{prefix}#contact">Contact</a>'
    )


def mnav_links(home):
    prefix = "" if home else "index.html"
    return (
        f'<a href="{prefix}#heritage">About</a>\n'
        f'  <a href="{prefix}#rooms">Rooms</a>\n'
        f'  <a href="{prefix}#trips">Day Trips</a>\n'
        f'  <a href="gallery.html">Gallery</a>\n'
        f'  <a href="{prefix}#contact">Contact</a>'
    )


def header(home):
    return f'''<header class="hdr">
  <img class="hdr__logo" src="assets/logo.png" alt="Lakefront Home Hotel">
  <nav class="nav">
    <span class="nav__links">
      {nav_links(home)}
    </span>
    <a class="btn btn--ghost" href="{BOOK}" target="_blank" rel="noopener">Book</a>
    <button class="burger" id="burger" aria-expanded="false" aria-controls="mnav" aria-label="Open menu">
      <span></span><span></span>
    </button>
  </nav>
</header>

<div class="mnav" id="mnav" hidden>
  <button class="mnav__close" id="mnavClose" aria-label="Close menu">&times;</button>
  {mnav_links(home)}
</div>'''


FOOTER = '''<footer class="wrap">
  <div class="ft">
    <div class="ft__brand">
      <img class="ft__logo" src="assets/logo.png" alt="Lakefront Home Hotel">
      <p class="lede" style="font-size:.92rem;max-width:34ch">Where luxury meets comfort, opposite the Boathouse on Ooty Lake.</p>
    </div>
    <div>
      <h4>Quick links</h4>
      <ul>
        <li><a href="policy-booking.html">Booking policy</a></li>
        <li><a href="policy-cancellation.html">Cancellation &amp; refund</a></li>
        <li><a href="policy-privacy.html">Privacy policy</a></li>
        <li><a href="policy-terms.html">Terms &amp; conditions</a></li>
      </ul>
    </div>
    <div>
      <h4>Get in touch</h4>
      <ul>
        <li><a href="tel:+919385620698"><svg class="ft__ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6.6 10.8c1.4 2.8 3.8 5.2 6.6 6.6l2.2-2.2c.3-.3.7-.4 1.1-.3 1.2.4 2.5.6 3.8.6.6 0 1 .4 1 1v3.4c0 .6-.4 1-1 1C10.9 21 3 13.1 3 3.7c0-.6.4-1 1-1H7.4c.6 0 1 .4 1 1 0 1.3.2 2.6.6 3.8.1.4 0 .8-.3 1.1L6.6 10.8z"/></svg>+91 93856 20698</a></li>
        <li><a href="mailto:lakefronthomehotel@gmail.com"><svg class="ft__ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="1.5"/><path d="M3.5 6.5L12 13l8.5-6.5"/></svg>lakefronthomehotel@gmail.com</a></li>
        <li><a href="https://wa.me/919385620698" target="_blank" rel="noopener"><svg class="ft__ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l2-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>WhatsApp</a></li>
        <li><a href="https://instagram.com/lakefronthomehotel" target="_blank" rel="noopener"><svg class="ft__ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r="1" fill="currentColor" stroke="none"/></svg>Instagram</a></li>
        <li><a href="https://youtube.com/@LakefrontHomeHotel" target="_blank" rel="noopener"><svg class="ft__ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="6" width="18" height="12" rx="4"/><path d="M10.5 9.5l5 2.5-5 2.5z" fill="currentColor" stroke="none"/></svg>YouTube</a></li>
      </ul>
    </div>
  </div>
  <div class="ft__end">
    <span>&copy; 2026 Lakefront Home Hotel. All rights reserved.</span>
  </div>
</footer>'''

WAFLOAT = f'''<a class="wa-float" href="{WHATSAPP}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l2-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>
</a>'''


def page(path, title, description, body, home=False, extra_scripts=""):
    out = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="index, follow">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:image" content="assets/hero.webp">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><text y='26' font-size='26'>&#127968;</text></svg>">
<link rel="stylesheet" href="styles.css?v={STYLE_VERSION}">
</head>
<body>
<div class="page">

{header(home)}

{body}

{FOOTER}

{WAFLOAT}

<script src="script-main.js?v={MAIN_SCRIPT_VERSION}"></script>
{extra_scripts}</div>
</body>
</html>
'''
    open(path, "w", encoding="utf-8").write(out)
    return len(out)


# ---------------------------------------------------------------- gallery --
def build_gallery():
    figs = "".join(
        f'<figure class="{cls}" data-lightbox data-full="assets/{img}.webp">'
        f'<img src="assets/{img}.webp" alt="{esc(alt)}" loading="lazy"></figure>'
        for img, alt, cls in GALLERY_IMAGES
    )
    body = f'''<section class="subhero">
  <img class="subhero__img" src="assets/n_0883.webp" alt="The garden at Lakefront Home Hotel">
  <div class="subhero__inner wrap">
    <p class="subhero__eyebrow">Gallery</p>
    <h1 class="subhero__title">Inside the bungalow</h1>
    <p class="subhero__sub">A closer look at the house, the rooms and the lakefront &mdash; 1937 heritage architecture, kept.</p>
  </div>
</section>

<section class="sec wrap">
  <div class="fullgrid rv">{figs}</div>
</section>

<section class="book">
  <div class="wrap book__in">
    <div class="book__txt">
      <p class="eyebrow">Reservations</p>
      <h2 class="h2">Ready to see it in person?</h2>
      <p class="lede">Rooms are held on the hotel's own booking engine.</p>
    </div>
    <div style="display:flex;gap:12px;flex-wrap:wrap">
      <a class="btn btn--solid" href="{BOOK}" target="_blank" rel="noopener">Check availability</a>
      <a class="btn btn--line" href="tel:+919385620698">+91 93856 20698</a>
    </div>
  </div>
</section>

<div class="lightbox" id="lightbox">
  <button class="lightbox__close" id="lightboxClose" aria-label="Close"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
  <button class="lightbox__prev" id="lightboxPrev" aria-label="Previous photo"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M15 6l-6 6 6 6"/></svg></button>
  <img src="" alt="">
  <button class="lightbox__next" id="lightboxNext" aria-label="Next photo"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg></button>
</div>'''
    page("gallery.html",
         "Gallery — Lakefront Home Hotel",
         "Photos of the 1937 heritage bungalow, guest rooms and lakefront gardens at Lakefront Home Hotel, Ooty.",
         body)


# ------------------------------------------------------------ room pages --
def build_rooms():
    card_html = {}
    for r in ROOMS:
        card_html[r["slug"]] = (
            f'<article class="card rv"><div class="card__fig">'
            f'<img src="assets/{r["img"]}.webp" alt="{esc(r["name"])}" loading="lazy"></div>'
            f'<div class="card__body"><h3 class="card__name">{r["name"]}</h3>'
            f'<p class="card__txt">{r["blurb"]}</p>'
            f'<a class="card__link" href="{r["slug"]}.html">See details &rarr;</a></div></article>'
        )

    for r in ROOMS:
        others = [x for x in ROOMS if x["slug"] != r["slug"]][:3]
        others_html = "".join(
            f'<article class="card rv"><div class="card__fig">'
            f'<img src="assets/{o["img"]}.webp" alt="{esc(o["name"])}" loading="lazy"></div>'
            f'<div class="card__body"><h3 class="card__name">{o["name"]}</h3>'
            f'<p class="card__txt">{o["blurb"]}</p>'
            f'<a class="card__link" href="{o["slug"]}.html">See details &rarr;</a></div></article>'
            for o in others
        )
        gallery_data = "".join(
            f'<li data-room-photo data-image="assets/{img}.webp" data-alt="{esc(r["name"])} &mdash; interior detail"></li>'
            for img in r["gallery"]
        )
        gallery_thumbs = "".join(
            f'<button class="roomgallery__thumb{" is-active" if i == 0 else ""}" type="button" data-room-photo-thumb="{i}" aria-label="Show photo {i + 1}" aria-pressed="{"true" if i == 0 else "false"}">'
            f'<img src="assets/{img}.webp" alt="" loading="lazy"></button>'
            for i, img in enumerate(r["gallery"])
        )
        gallery_html = f'''<div class="roomgallery rv" data-room-gallery>
  <figure class="roomgallery__main" data-lightbox data-full="assets/{r["gallery"][0]}.webp">
    <img src="assets/{r["gallery"][0]}.webp" alt="{esc(r["name"])} &mdash; interior detail" data-room-photo-image>
    <figcaption class="roomgallery__count"><span data-room-photo-current>01</span><i></i><span>0{len(r["gallery"])}</span></figcaption>
    <div class="roomgallery__controls">
      <button type="button" data-room-photo-prev aria-label="Previous photo"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg></button>
      <button type="button" data-room-photo-next aria-label="Next photo"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg></button>
    </div>
  </figure>
  <ol class="roomgallery__data" aria-hidden="true">{gallery_data}</ol>
  <div class="roomgallery__thumbs" role="group" aria-label="Room photos">{gallery_thumbs}</div>
</div>'''
        body = f'''<section class="subhero">
  <img class="subhero__img" src="assets/{r["img"]}.webp" alt="{esc(r["name"])}">
  <div class="subhero__inner wrap">
    <a class="subhero__back" href="index.html#rooms"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 18l-6-6 6-6"/></svg>Back to rooms</a>
    <p class="subhero__eyebrow">Rooms &amp; suites</p>
    <h1 class="subhero__title">{r["name"]}</h1>
  </div>
</section>

<section class="sec wrap" style="padding-bottom:0">
  <p class="lede" style="max-width:70ch">{r["body"]}</p>
  <div class="rd-specs rv">
    <div class="rd-spec"><span class="rd-spec__k">Ideal for</span><span class="rd-spec__v">{r["ideal"]}</span></div>
    <div class="rd-spec"><span class="rd-spec__k">Bed type</span><span class="rd-spec__v">{r["bed"]}</span></div>
    <div class="rd-spec"><span class="rd-spec__k">Check-in</span><span class="rd-spec__v">12:00 PM</span></div>
    <div class="rd-spec"><span class="rd-spec__k">Check-out</span><span class="rd-spec__v">11:00 AM</span></div>
  </div>
</section>

<section class="sec wrap">
  {gallery_html}
</section>

<section class="book">
  <div class="wrap book__in">
    <div class="book__txt">
      <p class="eyebrow">Reservations</p>
      <h2 class="h2">Book the {r["name"]}</h2>
      <p class="lede">Rooms are held on the hotel's own booking engine. Call or message us if you'd rather book by phone.</p>
    </div>
    <div style="display:flex;gap:12px;flex-wrap:wrap">
      <a class="btn btn--solid" href="{BOOK}" target="_blank" rel="noopener">Check availability</a>
      <a class="btn btn--line" href="tel:+919385620698">+91 93856 20698</a>
    </div>
  </div>
</section>

<section class="sec wrap room-other">
  <p class="eyebrow" style="margin-bottom:12px">Other rooms</p>
  <div class="rd-otherrooms">{others_html}</div>
</section>

<div class="lightbox" id="lightbox">
  <button class="lightbox__close" id="lightboxClose" aria-label="Close"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
  <button class="lightbox__prev" id="lightboxPrev" aria-label="Previous photo"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M15 6l-6 6 6 6"/></svg></button>
  <img src="" alt="">
  <button class="lightbox__next" id="lightboxNext" aria-label="Next photo"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg></button>
</div>'''
        page(f'{r["slug"]}.html',
             f'{r["name"]} — Lakefront Home Hotel',
             re.sub(r'&mdash;', '—', re.sub('<[^<]+?>', '', r["blurb"]))[:157],
             body)
    return card_html


# ---------------------------------------------------------- policy pages --
def parse_policy(raw_text):
    """Turn the extracted plain text into (heading, [paragraphs/bullets]) sections."""
    text = raw_text.strip()
    # split on "N. Heading:" markers where present
    parts = re.split(r'(\d+\.\s+[^:]+:)', text)
    sections = []
    if len(parts) > 1:
        intro = parts[0].strip()
        if intro:
            sections.append((None, [("p", intro)]))
        for i in range(1, len(parts), 2):
            heading = parts[i].rstrip(":").strip()
            heading = re.sub(r'^\d+\.\s*', '', heading)
            body = parts[i + 1].strip() if i + 1 < len(parts) else ""
            items = [x.strip(" -–") for x in re.split(r'\s*[–-]\s+(?=[A-Z])', body) if x.strip()]
            content = [("li", it) for it in items] if len(items) > 1 else [("p", body)]
            sections.append((heading, content))
    else:
        # terms-and-condition style: "Label : text" segments
        parts2 = re.split(r'([A-Z][A-Za-z /-]+ : )', text)
        if len(parts2) > 1:
            intro = parts2[0].strip()
            if intro:
                sections.append((None, [("p", intro)]))
            for i in range(1, len(parts2), 2):
                heading = parts2[i].rstrip(" :").strip()
                body = parts2[i + 1].strip() if i + 1 < len(parts2) else ""
                sections.append((heading, [("p", body)]))
        else:
            sections.append((None, [("p", text)]))
    return sections


def build_policies():
    for p in POLICIES:
        raw = open(f"/tmp/policies/{p['src']}.txt", encoding="utf-8").read()
        # strip the leading "<Title> - Lakefront Home" + repeated H1 that WP prepends
        raw = re.sub(r'^\s*.*?-\s*Lakefront Home\s*', '', raw, count=1).strip()
        raw = re.sub(r'^(Privacy Policy|Booking Policy|Cancellation and Refund Policy|Terms and Conditions)\s*', '', raw, count=1).strip()
        sections = parse_policy(raw)
        html_parts = []
        for heading, content in sections:
            if heading:
                html_parts.append(f'<h3>{esc(heading)}</h3>')
            lis = [c for t, c in content if t == "li"]
            if lis:
                html_parts.append("<ul>" + "".join(f"<li>{esc(li)}</li>" for li in lis) + "</ul>")
            else:
                for t, c in content:
                    if c:
                        html_parts.append(f"<p>{esc(c)}</p>")
        body_html = "\n    ".join(html_parts)

        body = f'''<section class="subhero" style="min-height:min(34svh,320px)">
  <img class="subhero__img" src="assets/corridor.webp" alt="Lakefront Home Hotel corridor">
  <div class="subhero__inner wrap">
    <p class="subhero__eyebrow">Policies</p>
    <h1 class="subhero__title">{esc(p["title"])}</h1>
  </div>
</section>

<section class="sec wrap">
  <div class="policy rv">
    {body_html}
  </div>
</section>'''
        page(f'{p["slug"]}.html',
             f'{p["title"]} — Lakefront Home Hotel',
             f'{p["title"]} for Lakefront Home Hotel, Ooty.',
             body)


# --------------------------------------------------------------- 404 page --
def build_404():
    body = '''<div class="darkband"></div>
<section class="wrap">
  <div class="notfound">
    <p class="notfound__code">404</p>
    <h1 class="notfound__title">This page has wandered off the property</h1>
    <p class="notfound__sub">The page you're looking for doesn't exist. Try the homepage, or check availability directly.</p>
    <div style="display:flex;gap:12px;flex-wrap:wrap;justify-content:center;margin-top:8px">
      <a class="btn btn--solid" href="index.html">Back to homepage</a>
      <a class="btn btn--line" href="''' + BOOK + '''" target="_blank" rel="noopener">Check availability</a>
    </div>
  </div>
</section>'''
    page("404.html", "Page not found — Lakefront Home Hotel",
         "This page could not be found.", body)


# -------------------------------------------------------- legacy URL paths --
def build_legacy_aliases():
    """Keep the old WordPress links usable on a static host.

    A real 301 belongs in the final hosting/DNS configuration.  Until then,
    this immediate, relative redirect is the portable option supported by
    GitHub Pages and by a future custom domain.
    """
    for legacy_path, target in LEGACY_PATHS.items():
        output_dir = legacy_path
        output_path = os.path.join(output_dir, "index.html")
        os.makedirs(output_dir, exist_ok=True)
        target_href = os.path.relpath(target, start=output_dir).replace(os.sep, "/")
        asset_href = os.path.relpath("assets/logo.png", start=output_dir).replace(os.sep, "/")
        style_href = os.path.relpath("styles.css", start=output_dir).replace(os.sep, "/") + f"?v={STYLE_VERSION}"
        title = "Lakefront Home Hotel"
        doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, follow">
<meta http-equiv="refresh" content="0; url={esc(target_href)}">
<title>{title}</title>
<link rel="stylesheet" href="{esc(style_href)}">
</head>
<body>
<main class="legacy-redirect">
  <img src="{esc(asset_href)}" alt="Lakefront Home Hotel">
  <p>Taking you to Lakefront Home Hotel.</p>
  <a class="btn btn--solid" href="{esc(target_href)}">Continue</a>
</main>
<script>window.location.replace({target_href!r});</script>
</body>
</html>
'''
        open(output_path, "w", encoding="utf-8").write(doc)


# ------------------------------------------------------- homepage rebuild --
def rebuild_homepage(room_cards):
    # Always rebuild from template-home.html, never from index.html itself —
    # index.html is a generated artifact, so reading it back in would make this
    # step non-idempotent (it already has the external <link>/<script src> and
    # local page links a second run would try, and fail, to re-derive).
    src = open("template-home.html", encoding="utf-8").read()

    src = re.sub(r'<style>.*?</style>', f'<link rel="stylesheet" href="styles.css?v={STYLE_VERSION}">', src, flags=re.S)

    scripts = re.findall(r'<script>.*?</script>', src, re.S)
    assert len(scripts) == 2, f"expected 2 inline script blocks in the template, found {len(scripts)}"
    src = src.replace(scripts[0], f'<script src="script-main.js?v={MAIN_SCRIPT_VERSION}"></script>')
    src = src.replace(scripts[1], f'<script src="script-reviews.js?v={REVIEWS_SCRIPT_VERSION}"></script>')

    old_grid = re.search(r'<div class="rgrid">.*?</div>\s*</section>', src, re.S)
    assert old_grid, "room grid not found"
    new_cards = "".join(room_cards[r["slug"]] for r in ROOMS)
    src = src[:old_grid.start()] + f'<div class="rgrid">{new_cards}</div>\n</section>' + src[old_grid.end():]

    src = src.replace('<a href="#gallery">Gallery</a>', '<a href="gallery.html">Gallery</a>')

    src = src.replace(
        'href="https://lakefronthomehotel.com/2024/02/booking-policy/" target="_blank" rel="noopener">Booking policy',
        'href="policy-booking.html">Booking policy')
    for label, slug in [("Cancellation &amp; refund", "policy-cancellation"),
                         ("Privacy policy", "policy-privacy"),
                         ("Terms &amp; conditions", "policy-terms")]:
        src = re.sub(
            r'href="https://lakefronthomehotel\.com/" target="_blank" rel="noopener">' + re.escape(label),
            f'href="{slug}.html">{label}', src, count=1)

    open("index.html", "w", encoding="utf-8").write(src)
    print(f"index.html rebuilt, {len(src)//1024} KB")


if __name__ == "__main__":
    cards = build_rooms()
    build_gallery()
    build_policies()
    build_404()
    build_legacy_aliases()
    rebuild_homepage(cards)
    print("build complete")
