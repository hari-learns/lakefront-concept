(function(){
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* rotating word - the element that renders blank on the current live site.
     Only present on the homepage hero, so this must not assume it exists —
     every page shares this script via the header/footer partials. */
  var host = document.getElementById("cycler");
  if (host) {
    var words = ["Charm","Heritage","Nature","Luxury","Tranquility"];
    words.forEach(function(w,i){
      var s = document.createElement("span");
      s.className = "cyc" + (i === 0 ? " on" : "");
      s.textContent = w;
      host.appendChild(s);
    });
    if (!reduce && words.length > 1) {
      var idx = 0, items = host.querySelectorAll(".cyc");
      setInterval(function(){
        items[idx].classList.remove("on");
        idx = (idx + 1) % items.length;
        items[idx].classList.add("on");
      }, 2600);
    }
  }

  /* mobile menu — present on every page via the shared header partial */
  var burger = document.getElementById("burger"), mnav = document.getElementById("mnav");
  if (burger && mnav) {
    var setMenu = function (open) {
      mnav.hidden = !open;
      burger.setAttribute("aria-expanded", open ? "true" : "false");
      burger.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      document.documentElement.style.overflow = open ? "hidden" : "";
    };
    burger.addEventListener("click", function(){ setMenu(mnav.hidden); });
    var mnavClose = document.getElementById("mnavClose");
    if (mnavClose) mnavClose.addEventListener("click", function(){ setMenu(false); });
    mnav.addEventListener("click", function(e){ if(e.target.tagName === "A") setMenu(false); });
    document.addEventListener("keydown", function(e){ if(e.key === "Escape" && !mnav.hidden) setMenu(false); });
  }

  var rv = document.querySelectorAll(".rv");
  var trips = [].slice.call(document.querySelectorAll(".trip"));

  if (reduce || !("IntersectionObserver" in window)) {
    for (var i = 0; i < rv.length; i++) rv[i].classList.add("in");
    trips.forEach(function(t){ t.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    for (var j = 0; j < rv.length; j++) io.observe(rv[j]);

    if (trips.length) {
      var tio = new IntersectionObserver(function(es){
        es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add("in"); tio.unobserve(e.target); } });
      }, { rootMargin: "0px 0px -12% 0px", threshold: 0.15 });
      trips.forEach(function(t){ tio.observe(t); });
    }
  }

  /* sticky counter tracks which trip is centred — homepage day-trips only */
  var numEl = document.getElementById("tripNum"), nowEl = document.getElementById("tripNow"), active = -1;
  if (trips.length && numEl && nowEl && "IntersectionObserver" in window) {
    var track = new IntersectionObserver(function(es){
      es.forEach(function(e){
        if (!e.isIntersecting) return;
        var i = trips.indexOf(e.target);
        if (i === active) return;
        active = i;
        numEl.textContent = ("0" + (i + 1)).slice(-2);
        nowEl.style.opacity = "0";
        setTimeout(function(){
          nowEl.textContent = trips[i].getAttribute("data-short") || "";
          nowEl.style.opacity = "1";
        }, 180);
      });
    }, { rootMargin: "-42% 0px -42% 0px", threshold: 0 });
    trips.forEach(function(t){ track.observe(t); });
  }

  /* Safety net: nothing that starts at opacity:0 may ever stay stuck if the
     observer misses (bfcache restore, background tab, odd embedding). */
  function inView(el){
    var r = el.getBoundingClientRect();
    return r.top < window.innerHeight * 0.92 && r.bottom > -1;
  }
  function sweep(){
    for (var i = 0; i < rv.length; i++) if (inView(rv[i])) rv[i].classList.add("in");
    for (var j = 0; j < trips.length; j++) if (inView(trips[j])) trips[j].classList.add("in");
  }
  sweep();
  window.addEventListener("load", sweep);
  window.addEventListener("scroll", sweep, { passive: true });
  window.addEventListener("resize", sweep);

  /* room-detail photos — the page keeps its original three images, but gives
     each one a clean full frame and an explicit photo selector. */
  [].slice.call(document.querySelectorAll("[data-room-gallery]")).forEach(function(gallery){
    var photos = [].slice.call(gallery.querySelectorAll("[data-room-photo]"));
    var thumbs = [].slice.call(gallery.querySelectorAll("[data-room-photo-thumb]"));
    var image = gallery.querySelector("[data-room-photo-image]");
    var figure = gallery.querySelector("[data-lightbox]");
    var current = gallery.querySelector("[data-room-photo-current]");
    var index = 0;
    function showPhoto(next) {
      index = (next + photos.length) % photos.length;
      var photo = photos[index];
      image.src = photo.getAttribute("data-image");
      image.alt = photo.getAttribute("data-alt");
      figure.setAttribute("data-full", photo.getAttribute("data-image"));
      image.style.animation = "none"; void image.offsetWidth; image.style.animation = "";
      current.textContent = ("0" + (index + 1)).slice(-2);
      thumbs.forEach(function(thumb, i){ var active = i === index; thumb.classList.toggle("is-active", active); thumb.setAttribute("aria-pressed", active ? "true" : "false"); });
    }
    gallery.querySelector("[data-room-photo-prev]").addEventListener("click", function(e){ e.stopPropagation(); showPhoto(index - 1); });
    gallery.querySelector("[data-room-photo-next]").addEventListener("click", function(e){ e.stopPropagation(); showPhoto(index + 1); });
    thumbs.forEach(function(thumb, i){ thumb.addEventListener("click", function(){ showPhoto(i); }); });
  });

  /* enquiry form — the static site has no WordPress server behind it.  Keep
     the exact guest fields, then open the hotel's existing WhatsApp channel
     with a complete, editable enquiry rather than silently dropping it. */
  var enquiry = document.querySelector("[data-enquiry-form]");
  if (enquiry) {
    var enquiryStatus = enquiry.querySelector("[data-enquiry-status]");
    enquiry.addEventListener("submit", function(e){
      e.preventDefault();
      if (!enquiry.checkValidity()) { enquiry.reportValidity(); return; }
      var data = new FormData(enquiry);
      var message = "Hello Lakefront Home Hotel, I would like to enquire about a stay.\n\n"
        + "Name: " + data.get("name") + "\n"
        + "Email: " + data.get("email") + "\n"
        + "Subject: " + data.get("subject") + "\n"
        + "Message: " + data.get("message");
      var destination = "https://wa.me/919385620698?text=" + encodeURIComponent(message);
      window.open(destination, "_blank", "noopener");
      if (enquiryStatus) enquiryStatus.textContent = "WhatsApp opened with your enquiry ready to send.";
    });
  }

  /* lightbox — gallery page and room-detail photo grids */
  var lb = document.getElementById("lightbox");
  if (lb) {
    var lbImg = lb.querySelector("img");
    var figs = [].slice.call(document.querySelectorAll("[data-lightbox]"));
    var pos = 0;
    function openAt(i){
      pos = i;
      lbImg.src = figs[pos].getAttribute("data-full") || figs[pos].querySelector("img").src;
      lbImg.alt = figs[pos].querySelector("img").alt || "";
      lb.classList.add("is-open");
      document.documentElement.style.overflow = "hidden";
    }
    function closeLb(){
      lb.classList.remove("is-open");
      document.documentElement.style.overflow = "";
    }
    function step(d){ openAt((pos + d + figs.length) % figs.length); }
    figs.forEach(function(f, i){ f.addEventListener("click", function(){ openAt(i); }); });
    var lbClose = document.getElementById("lightboxClose");
    var lbPrev = document.getElementById("lightboxPrev");
    var lbNext = document.getElementById("lightboxNext");
    if (lbClose) lbClose.addEventListener("click", closeLb);
    if (lbPrev) lbPrev.addEventListener("click", function(){ step(-1); });
    if (lbNext) lbNext.addEventListener("click", function(){ step(1); });
    lb.addEventListener("click", function(e){ if (e.target === lb) closeLb(); });
    document.addEventListener("keydown", function(e){
      if (!lb.classList.contains("is-open")) return;
      if (e.key === "Escape") closeLb();
      else if (e.key === "ArrowLeft") step(-1);
      else if (e.key === "ArrowRight") step(1);
    });
  }
})();
