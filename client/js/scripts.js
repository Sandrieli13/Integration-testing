const navbar = document.getElementById("navbar");
const navbarToggle = navbar && navbar.querySelector(".navbar-toggle");

function openMobileNavbar() {
  if (!navbar || !navbarToggle) return;
  navbar.classList.add("opened");
  navbarToggle.setAttribute("aria-expanded", "true");
}

function closeMobileNavbar() {
  if (!navbar || !navbarToggle) return;
  navbar.classList.remove("opened");
  navbarToggle.setAttribute("aria-expanded", "false");
}

if (navbarToggle) {
  navbarToggle.addEventListener("click", () => {
    if (navbar.classList.contains("opened")) {
      closeMobileNavbar();
    } else {
      openMobileNavbar();
    }
  });
}

const navbarMenu = navbar && navbar.querySelector("#navbar-menu");
const navbarLinksContainer = navbar && navbar.querySelector(".navbar-links");

if (navbarLinksContainer) {
  navbarLinksContainer.addEventListener("click", (clickEvent) => {
    clickEvent.stopPropagation();
  });
}

if (navbarMenu) {
  navbarMenu.addEventListener("click", closeMobileNavbar);
}

/* Close mobile sheet when crossing to desktop (hamburger hidden there). */
(function () {
  var mq = window.matchMedia("(min-width: 1024px)");
  function onChange() {
    if (mq.matches) closeMobileNavbar();
  }
  if (typeof mq.addEventListener === "function") {
    mq.addEventListener("change", onChange);
  } else if (typeof mq.addListener === "function") {
    mq.addListener(onChange);
  }
})();

/* Desktop nav: one dropdown open at a time */
(function () {
  var deskMq = window.matchMedia("(min-width: 1024px)");
  var dds = navbar && navbar.querySelectorAll(".navbar-art-dd");
  if (!dds || !dds.length) return;
  dds.forEach(function (dd) {
    dd.addEventListener("toggle", function () {
      if (!deskMq.matches || !dd.open) return;
      dds.forEach(function (other) {
        if (other !== dd) other.removeAttribute("open");
      });
    });
  });
})();
 