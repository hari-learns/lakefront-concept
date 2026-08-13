/* ============================================================
   LAKEFRONT — LAB REDESIGN
   No libraries. All scroll work reads window.scrollY inside a
   single rAF loop rather than hijacking scroll with a transformed
   wrapper — transform-based "smooth scroll" silently breaks
   position:sticky, and this page leans on sticky in two places.
   ============================================================ */
(function () {
  "use strict";

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var desktop = window.matchMedia("(min-width: 901px)");
  var finePointer = window.matchMedia("(hover: hover) and (pointer: fine)");

  var lerp = function (a, b, n) { return a + (b - a) * n; };
  var clamp = function (v, a, b) { return Math.min(Math.max(v, a), b); };

  /* ── preloader ───────────────────────────────────────────────────── */
  var pre = document.getElementById("pre");
  function dismissPre() { if (pre) pre.classList.add("done"); }
  window.addEventListener("load", function () { setTimeout(dismissPre, reduce ? 0 : 1250); });
  // failsafe: never let a stuck asset trap the page behind the curtain
  setTimeout(dismissPre, 4000);

  /* ── custom cursor ───────────────────────────────────────────────── */
  var cur = document.getElementById("cur");
  var curD = document.getElementById("curD");
  if (cur && curD && finePointer.matches && !reduce) {
    var mx = innerWidth / 2, my = innerHeight / 2, dx = mx, dy = my;
    document.addEventListener("mousemove", function (e) {
      mx = e.clientX; my = e.clientY;
      cur.style.transform = "translate(" + mx + "px," + my + "px)";
    }, { passive: true });
    (function ring() {
      dx = lerp(dx, mx, 0.16); dy = lerp(dy, my, 0.16);
      curD.style.transform = "translate(" + dx + "px," + dy + "px)";
      requestAnimationFrame(ring);
    })();
    document.querySelectorAll("[data-cursor], a, button").forEach(function (el) {
      el.addEventListener("mouseenter", function () { curD.classList.add("grow"); });
      el.addEventListener("mouseleave", function () { curD.classList.remove("grow"); });
    });
  } else if (cur && curD) {
    cur.style.display = curD.style.display = "none";
  }

  /* ── reveals ─────────────────────────────────────────────────────── */
  var revealEls = document.querySelectorAll(".r-mask, .r-up, .r-clip");
  if (reduce || !("IntersectionObserver" in window)) {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -10% 0px", threshold: 0.12 });
    revealEls.forEach(function (el) { io.observe(el); });
  }
  // safety net — nothing that starts hidden may stay stuck if the observer misses
  function sweepReveals() {
    revealEls.forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < innerHeight * 0.94 && r.bottom > -1) el.classList.add("in");
    });
  }
  sweepReveals();
  window.addEventListener("load", sweepReveals);

  /* ── count-up ────────────────────────────────────────────────────── */
  document.querySelectorAll("[data-count]").forEach(function (el) {
    var target = parseInt(el.getAttribute("data-count"), 10);
    var pad = el.hasAttribute("data-pad");
    if (el.hasAttribute("data-plain") || reduce) {
      el.textContent = pad ? ("0" + target).slice(-2) : target;
      return;
    }
    var run = false;
    var obs = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting || run) return;
        run = true;
        var t0 = performance.now(), dur = 1500;
        (function step(now) {
          var p = clamp((now - t0) / dur, 0, 1);
          var eased = 1 - Math.pow(1 - p, 3);
          var v = Math.round(target * eased);
          el.textContent = pad ? ("0" + v).slice(-2) : v;
          if (p < 1) requestAnimationFrame(step);
        })(performance.now());
        obs.disconnect();
      });
    }, { threshold: 0.5 });
    obs.observe(el);
  });

  /* ── amenities marquee (two copies = seamless -50% loop) ─────────── */
  var amenTrack = document.getElementById("amenTrack");
  if (amenTrack) {
    var items = ["Camp fire", "Scenic view", "Wi-Fi access", "Room service",
                 "Television", "Filtered water", "Parking available", "Driver accommodation"];
    var once = items.map(function (t) {
      return '<span class="amen__i">' + t + "</span>";
    }).join("");
    amenTrack.innerHTML = reduce ? once : once + once;
  }

  /* ── heritage: pinned image follows whichever block is centred ───── */
  var stack = document.getElementById("heritStack");
  var heritCap = document.getElementById("heritCap");
  var heritNo = document.getElementById("heritNo");
  var blocks = document.querySelectorAll(".herit__b");
  if (stack && blocks.length) {
    var shots = stack.querySelectorAll("img");
    var activeShot = 0;
    var setShot = function (i) {
      if (i === activeShot || !shots[i]) return;
      activeShot = i;
      shots.forEach(function (s, n) { s.classList.toggle("on", n === i); });
      if (heritCap) heritCap.textContent = shots[i].getAttribute("data-cap") || "";
      if (heritNo) heritNo.textContent = ("0" + (i + 1)).slice(-2) + " / " + ("0" + shots.length).slice(-2);
    };
    var hio = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var i = Array.prototype.indexOf.call(blocks, e.target);
        // 4 photos across 3 narrative blocks — last block holds the final two
        setShot(Math.min(i, shots.length - 1));
      });
    }, { rootMargin: "-45% 0px -45% 0px", threshold: 0 });
    blocks.forEach(function (b) { hio.observe(b); });
  }

  /* ── reviews cycler ──────────────────────────────────────────────── */
  var stage = document.getElementById("revStage");
  var revNav = document.getElementById("revNav");
  if (stage && revNav) {
    var quotes = stage.querySelectorAll(".rev__q");
    var qi = 0, qTimer = null;
    revNav.innerHTML = Array.prototype.map.call(quotes, function (_, i) {
      return '<button type="button" aria-label="Review ' + (i + 1) +
             '" aria-current="' + (i === 0) + '"></button>';
    }).join("");
    var dots = revNav.querySelectorAll("button");
    function showQuote(i) {
      qi = i;
      quotes.forEach(function (q, n) { q.classList.toggle("on", n === i); });
      dots.forEach(function (d, n) { d.setAttribute("aria-current", String(n === i)); });
    }
    function startQuotes() {
      if (reduce || qTimer) return;
      qTimer = setInterval(function () { showQuote((qi + 1) % quotes.length); }, 5200);
    }
    function stopQuotes() { clearInterval(qTimer); qTimer = null; }
    dots.forEach(function (d, i) {
      d.addEventListener("click", function () { stopQuotes(); showQuote(i); startQuotes(); });
    });
    stage.addEventListener("mouseenter", stopQuotes);
    stage.addEventListener("mouseleave", startQuotes);
    document.addEventListener("visibilitychange", function () {
      document.hidden ? stopQuotes() : startQuotes();
    });
    startQuotes();
  }

  /* ── horizontal rooms: vertical scroll drives X travel ───────────── */
  var hSection = document.querySelector(".hrooms");
  var hTrack = document.getElementById("hTrack");
  var hDistance = 0;

  function measureRooms() {
    if (!hSection || !hTrack) return;
    if (!desktop.matches) {           // touch: native horizontal scroll, no pinning
      hSection.style.height = "";
      hTrack.style.transform = "";
      hDistance = 0;
      return;
    }
    hDistance = Math.max(0, hTrack.scrollWidth - innerWidth);
    hSection.style.height = (hDistance + innerHeight) + "px";
  }

  /* ── single rAF loop for every scroll-linked effect ──────────────── */
  var nav = document.getElementById("nav");
  var heroImg = document.getElementById("heroImg");
  var maskWord = document.getElementById("maskWord");
  var ticking = false;

  function onFrame() {
    var y = window.scrollY || window.pageYOffset;

    if (nav) nav.classList.toggle("stuck", y > innerHeight * 0.6);

    // hero: settle the 1.12 scale back to 1 and drift down slightly
    if (heroImg && !reduce) {
      var hp = clamp(y / innerHeight, 0, 1);
      heroImg.style.transform = "scale(" + (1.12 - hp * 0.12) + ") translateY(" + (hp * 6) + "%)";
    }

    // rooms: translate the track across its measured distance
    if (hSection && hTrack && hDistance > 0 && desktop.matches) {
      var rect = hSection.getBoundingClientRect();
      var p = clamp(-rect.top / (rect.height - innerHeight), 0, 1);
      hTrack.style.transform = "translate3d(" + (-hDistance * p) + "px,0,0)";
    }

    // masked headline: shift the photo inside the letterforms
    if (maskWord && !reduce) {
      var mr = maskWord.getBoundingClientRect();
      if (mr.bottom > 0 && mr.top < innerHeight) {
        var mp = clamp(1 - (mr.top + mr.height) / (innerHeight + mr.height), 0, 1);
        maskWord.style.backgroundPosition = "center " + (30 + mp * 40) + "%";
      }
    }
  }

  function requestFrame() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      // finally: a throw inside onFrame must never latch `ticking` true, which
      // would silently kill every scroll-linked effect for the rest of the session
      try { onFrame(); } finally { ticking = false; }
    });
  }

  window.addEventListener("scroll", requestFrame, { passive: true });
  // rAF is paused while a tab is hidden; re-sync the moment it comes back
  document.addEventListener("visibilitychange", function () {
    if (!document.hidden) requestFrame();
  });
  window.addEventListener("resize", function () { measureRooms(); requestFrame(); sweepReveals(); });
  // crossing the 901px breakpoint must re-measure even if no resize event lands
  if (desktop.addEventListener) {
    desktop.addEventListener("change", function () { measureRooms(); requestFrame(); });
  }
  window.addEventListener("load", function () { measureRooms(); requestFrame(); });
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(function () { measureRooms(); requestFrame(); });
  }
  measureRooms();
  requestFrame();
})();
