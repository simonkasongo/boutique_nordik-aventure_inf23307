// -------------------------------------------
// 1) Surbrillance dynamique de la navbar
// -------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  const currentPath = window.location.pathname;

  document.querySelectorAll(".navbar .nav-link").forEach((link) => {
    const href = link.getAttribute("href");

    if (href !== "/" && currentPath.startsWith(href)) {
      link.classList.add("active");
    } else if (currentPath === "/" && href === "/") {
      link.classList.add("active");
    }
  });
});

// -------------------------------------------
// 2) Animations d'apparition globale (fade-in)
// -------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  const items = document.querySelectorAll(".fade-in");

  items.forEach((el, i) => {
    setTimeout(() => el.classList.add("visible"), 150 * i);
  });
});

// -------------------------------------------
// 3) Effet "hover" amélioré sur toutes les cartes
// -------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".card, .card-dashboard");

  cards.forEach((card) => {
    card.addEventListener("mouseover", () => {
      card.style.transform = "scale(1.03)";
      card.style.transition = "0.2s ease";
    });

    card.addEventListener("mouseout", () => {
      card.style.transform = "scale(1)";
    });
  });
});

// -------------------------------------------
// 4) Menu utilisateur (username) dropdown
// -------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  const userMenu = document.querySelector("#userMenu");
  const dropdown = document.querySelector("#userDropdown");

  if (userMenu) {
    userMenu.addEventListener("click", () => {
      dropdown.classList.toggle("show");
    });

    // Fermer si clique ailleurs
    document.addEventListener("click", (event) => {
      if (
        !userMenu.contains(event.target) &&
        !dropdown.contains(event.target)
      ) {
        dropdown.classList.remove("show");
      }
    });
  }
});

// -------------------------------------------
// 5) Confettis (après avis client)
// -------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  const alertSuccess = document.querySelector(".alert-success");

  if (alertSuccess && window.location.pathname.includes("panier")) {
    setTimeout(() => {
      confetti({
        particleCount: 200,
        spread: 90,
        origin: { y: 0.6 },
      });
    }, 300);
  }
});

// -------------------------------------------
// 6) Animation bouton (click pulse)
// -------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll("button, .btn");

  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      btn.classList.add("btn-pulse");
      setTimeout(() => btn.classList.remove("btn-pulse"), 200);
    });
  });
});

// -------------------------------------------
// 7) Animation smooth scroll pour tous les liens
// -------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("a[href^='#']").forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();

      const section = document.querySelector(this.getAttribute("href"));
      if (section) {
        section.scrollIntoView({ behavior: "smooth" });
      }
    });
  });
});

// -------------------------------------------
// 8) Animation Slide-Up sur tous les titres h1/h2/h3
// -------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  const titles = document.querySelectorAll("h1, h2, h3");

  titles.forEach((title, index) => {
    setTimeout(() => {
      title.classList.add("animate-title");
    }, index * 150);
  });
});
// ================================
// Confettis après l'achat
// ================================
document.addEventListener("DOMContentLoaded", () => {
  if (window.location.search.includes("merci=1")) {
    lancerConfettis();
  }
});

function lancerConfettis() {
  for (let i = 0; i < 150; i++) {
    const confetti = document.createElement("div");
    confetti.classList.add("confetti");
    document.body.appendChild(confetti);

    confetti.style.left = Math.random() * 100 + "vw";
    confetti.style.animationDelay = Math.random() * 2 + "s";
  }
}
