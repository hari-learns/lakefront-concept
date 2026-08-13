/* ============================================================
   GUEST REVIEWS  —  verbatim from the Google Business profile.
   Text is unedited; only visually clamped to 5 lines per card,
   the same way Google's own UI truncates a long review.
   ============================================================ */
var REVIEWS = [
  { r:5, t:"We had an excellent stay with our family at Lakefront home hotel. The rooms were very clean, spacious, and well-maintained, making our stay comfortable and relaxing. The staff was extremely courteous, helpful, and always ready to assist with a smile. The breakfast was excellent, with a good variety of tasty and fresh options served every morning. The overall hospitality and service exceeded our expectations. The location is also convenient and adds to the pleasant experience. We truly enjoyed our stay and would highly recommend Ooty Lake Rooms to families looking for a comfortable and memorable stay in Ooty.", n:"Siva Krishna", d:"a month ago" },
  { r:5, t:"I had an absolutely wonderful stay at this hotel—truly exceeding expectations in every way. The breakfast spread was exceptional, offering a wide variety of fresh and delicious options that catered to all tastes. It was the perfect start to each day. The room service was prompt, efficient, and always delivered with great attention to detail. The rooms themselves were clean, comfortable, and well-maintained, creating a relaxing and pleasant environment. What truly stood out was the staff—their friendliness, professionalism, and willingness to go the extra mile made the experience even more memorable. A special mention to Rajesh at the reception, whose very good cooperation and helpful nature made our stay smooth and hassle-free. Overall, I would rate this hotel beyond 5 stars for its outstanding service, excellent amenities, and incredible hospitality. Highly recommended for anyone looking for a top-notch stay!", n:"Girish Gavhale", d:"4 months ago" },
  { r:5, t:"Highly recommended stay. Very close to almost all site seeing spots. Very friendly and supportive staffs. This place is just above the boating lake. And also a great place to click some good pics. Also I need to mention their kichdi, sambar and dosa for breakfast, very tasty.", n:"Sona M M", d:"Edited 5 months ago" },
  { r:5, t:"A very unique stay it was. The vintage looking rooms with wooden floors was very luxurious looking. And the best part is, your windows will directly open to the ooty lake and the ooty boat house... Which was amazing. Will love to come back to this place. Speical mention Mr. Rajesh, who has been very kind and helpful throughout our stay :)", n:"Kheyali Naskar", d:"3 months ago" },
  { r:5, t:"We had an absolutely wonderful stay at Lake Front Home! The location is beautiful and peaceful, with a stunning lake view that made our mornings and evenings very special. The property was clean, well-maintained, and very comfortable. The rooms were spacious and neatly arranged. All the basic amenities were available, and everything was perfectly organized. The atmosphere was calm and relaxing — perfect for a family stay or a getaway with friends. The host was very kind, responsive, and helpful throughout our stay. We truly felt welcomed and taken care of. Room heater is missing", n:"Abishek U", d:"5 months ago" },
  { r:5, t:"The British bungalow has been beautifully transformed into a heritage hotel. I stayed here with my family, and it was truly one of our best experiences. The service is exceptional, and the manager, Mr.Johnbosco, went above and beyond to make our stay even more comfortable. Highly recommended for a peaceful and relaxing stay \ud83d\udc4d", n:"Victor Paranthan", d:"3 months ago" }
];
var GOOGLE_URL = "https://www.google.com/travel/search?q=lakefront%20home%20hotel&g2lb=4965990%2C72471280%2C72560029%2C72573224%2C72647020%2C72686036%2C72803964%2C72882230%2C73064764%2C121529350%2C121608705%2C121738283%2C121762713&hl=en-IN&gl=in&cs=1&ssta=1&ts=CAEaRwopEicyJTB4M2JhOGJkMDA0ODMyNGZjZjoweDdiYTI4ODBiM2ZhMmE0OTASGhIUCgcI6g8QCBgEEgcI6g8QCBgFGAEyAhAA&qs=CAEyE0Nnb0lrTW1LX2JPQm90RjdFQUU4AkIJCZCkoj8LiKJ7QgkJkKSiPwuIons&ap=ugEHcmV2aWV3cw&ictx=111&ved=0CAAQ5JsGahcKEwigqLif14KWAxUAAAAAHQAAAAAQAw";

(function(){
  var track = document.getElementById("revTrack");
  if (!track || !REVIEWS.length) return;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var mobile = window.matchMedia("(max-width: 640px)").matches;

  var STAR = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2l2.9 6.3 6.9.8-5.1 4.7 1.4 6.8L12 17.3 5.9 20.6l1.4-6.8L2.2 9.1l6.9-.8z"/></svg>';
  function stars(n){ var o=""; for(var i=0;i<n;i++) o+=STAR; return '<span class="stars">'+o+'</span>'; }
  function esc(x){ return String(x).replace(/[&<>"]/g, function(c){
    return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]; }); }

  var GMARK = '<svg class="revcard__g" viewBox="0 0 48 48" aria-hidden="true">'
    + '<path fill="#4285F4" d="M45 24c0-1.6-.1-2.7-.4-3.9H24v7.1h12c-.2 1.8-1.5 4.6-4.4 6.4l6.7 5.2C42.2 35.1 45 30 45 24z"/>'
    + '<path fill="#34A853" d="M24 46c5.9 0 10.9-2 14.5-5.3l-6.9-5.4c-1.9 1.3-4.4 2.2-7.6 2.2-5.8 0-10.7-3.8-12.5-9.1l-7.1 5.5C8 41.2 15.4 46 24 46z"/>'
    + '<path fill="#FBBC05" d="M11.5 28.4c-.5-1.4-.7-2.9-.7-4.4s.3-3 .7-4.4l-7.1-5.5C2.9 17 2 20.4 2 24s.9 7 2.4 9.9z"/>'
    + '<path fill="#EA4335" d="M24 10.4c4.1 0 6.9 1.8 8.5 3.3l6.2-6C34.9 4.2 29.9 2 24 2 15.4 2 8 6.8 4.4 14.1l7.1 5.5c1.8-5.3 6.7-9.2 12.5-9.2z"/></svg>';

  function card(rv){
    return '<a class="revcard" href="' + GOOGLE_URL + '" target="_blank" rel="noopener">'
      + '<div class="revcard__top">' + stars(rv.r) + GMARK + '</div>'
      + '<p class="revcard__txt">' + esc(rv.t) + '</p>'
      + '<div class="revcard__by"><div class="revcard__av">' + esc(rv.n.trim().charAt(0)) + '</div>'
      + '<div><div class="revcard__nm">' + esc(rv.n) + '</div>'
      + '<div class="revcard__dt">' + esc(rv.d) + '</div></div></div></a>';
  }

  /* Two copies back to back + a keyframe that slides exactly -50% gives a
     seamless infinite loop: as the first copy scrolls off, the second is
     already in the same position, so the seam is invisible. */
  var once = REVIEWS.map(card).join("");
  track.innerHTML = (reduce || mobile) ? once : once + once;

  /* A readable, automatic one-at-a-time presentation for phones. It avoids
     the desktop marquee's masked transition crossing an entire phone width. */
  if (mobile) {
    var cards = track.querySelectorAll(".revcard");
    var current = 0;
    function showReview(index) {
      for (var j = 0; j < cards.length; j++) cards[j].classList.toggle("is-mobile-active", j === index);
    }
    showReview(current);
    if (!reduce && cards.length > 1) {
      window.setInterval(function(){ current = (current + 1) % cards.length; showReview(current); }, 5600);
    }
  }

  var sum = 0; for (var i = 0; i < REVIEWS.length; i++) sum += REVIEWS[i].r;
  var avg = sum / REVIEWS.length;
  document.getElementById("revAvg").textContent = avg.toFixed(1);
  document.getElementById("revStars").innerHTML = stars(Math.round(avg));
  document.getElementById("revCount").textContent = "From recent Google reviews";
})();
