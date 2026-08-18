(function () {
  "use strict";

  /* ---------------- Mobile menu ---------------- */
  const burger = document.querySelector(".burger");
  const overlay = document.querySelector(".overlay");
  const menu = document.getElementById("mobile-menu");

  function openMenu() {
    if (!menu || !overlay || !burger) return;
    overlay.hidden = false;
    menu.hidden = false;
    burger.classList.add("open");
    burger.setAttribute("aria-expanded", "true");
    burger.setAttribute("aria-label", "Close menu");
    document.body.classList.add("menu-open");
  }

  function closeMenu() {
    if (!menu || !overlay || !burger) return;
    overlay.hidden = true;
    menu.hidden = true;
    burger.classList.remove("open");
    burger.setAttribute("aria-expanded", "false");
    burger.setAttribute("aria-label", "Open menu");
    document.body.classList.remove("menu-open");
  }

  function toggleMenu() {
    if (menu && menu.hidden) openMenu();
    else closeMenu();
  }

  if (burger) burger.addEventListener("click", toggleMenu);
  if (overlay) overlay.addEventListener("click", closeMenu);
  if (menu) {
    menu.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", closeMenu);
    });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeMenu();
  });
  window.addEventListener("resize", function () {
    if (window.innerWidth > 720) closeMenu();
  });

  /* ---------------- Count-up stats ---------------- */
  const values = Array.prototype.slice.call(
    document.querySelectorAll(".stat-value")
  );

  function easeOutCubic(t) {
    return 1 - Math.pow(1 - t, 3);
  }

  function format(num, decimals) {
    return num.toFixed(decimals);
  }

  function countUp(el, index) {
    const target = parseFloat(el.dataset.target);
    const decimals = parseInt(el.dataset.decimals, 10) || 0;
    const suffix = el.dataset.suffix || "";
    const duration = 1500 + index * 80;
    const startTime = performance.now();

    function tick(now) {
      const elapsed = now - startTime;
      const t = Math.min(elapsed / duration, 1);
      const value = target * easeOutCubic(t);
      el.textContent = format(value, decimals) + suffix;
      if (t < 1) {
        requestAnimationFrame(tick);
      } else {
        el.textContent = format(target, decimals) + suffix;
      }
    }
    requestAnimationFrame(tick);
  }

  const statsSection = document.querySelector(".stats");
  let counted = false;

  function runCounts() {
    if (counted) return;
    counted = true;
    values.forEach(function (el, i) {
      window.setTimeout(function () {
        countUp(el, i);
      }, 480 + i * 90);
    });
  }

  if (statsSection && "IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            runCounts();
            io.disconnect();
          }
        });
      },
      { threshold: 0.25 }
    );
    io.observe(statsSection);
  } else {
    runCounts();
  }
})();
