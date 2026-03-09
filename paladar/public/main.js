async function loadMenu() {
  const SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRexQ-IsFU_rrVUremrCiGgFouOkTNWOInz3kyCCnymrEYExfrBpqaDO0kepjeNsrdkz5dsU_U6oKWD/pub?output=csv";

  const dateEl = document.getElementById("menu-date");
  const primersEl = document.getElementById("primers-list");
  const segonsEl = document.getElementById("segons-list");
  const postresEl = document.getElementById("postres-list");
  const errorEl = document.getElementById("menu-error");

  try {
    const res = await fetch(SHEET_URL);
    if (!res.ok) throw new Error("Error loading Google Sheet");

    const csv = await res.text();

    // Parse CSV
    const [headerLine, dataLine] = csv.split("\n");
    const headers = headerLine.split(",");
    const values = dataLine.split(",");

    const menu = {};
    headers.forEach((h, i) => {
      menu[h.trim()] = values[i] ? values[i].trim() : "";
    });

    // Convert semicolon lists into arrays
    const parseList = (str) =>
      str ? str.split(";").map((s) => s.trim()).filter(Boolean) : [];

    // Menu text
    const primers = parseList(menu.primers);
    const segons = parseList(menu.segons);
    const postres = parseList(menu.postres);

    // One image for the menu
    window.menuImage = menu.image ? `img/${menu.image}` : null;

    // Render date
    dateEl.textContent = menu.date ? `Data: ${menu.date}` : "";

    // Render lists
    const renderList = (el, items) => {
      el.innerHTML = "";
      items.forEach((item) => {
        const li = document.createElement("li");
        li.textContent = item;
        el.appendChild(li);
      });
    };

    renderList(primersEl, primers);
    renderList(segonsEl, segons);
    renderList(postresEl, postres);

    errorEl.textContent = "";
  } catch (err) {
    console.error(err);
    errorEl.textContent = "No s’ha pogut carregar el menú del dia.";
  }
}

  function startHeroSlideshow() {
    const heroImg = document.querySelector(".hero-image");
  
    const images = [
      "img/hero-1.jpg",
      "img/hero-2.jpg",
      "img/hero-3.jpg"
    ];
  
    let index = 0;
    let intervalId;
  
    const start = () => {
      intervalId = setInterval(() => {
        heroImg.classList.add("fade-out");
  
        setTimeout(() => {
          index = (index + 1) % images.length;
          heroImg.src = images[index];
          heroImg.classList.remove("fade-out");
        }, 800);
      }, 4500);
    };
  
    const stop = () => clearInterval(intervalId);
  
    // Start slideshow
    start();
  
    // Pause on hover
    heroImg.addEventListener("mouseenter", stop);
    heroImg.addEventListener("mouseleave", start);
  }
  
  
  function startCardSlideshows() {
    const slideshows = [
      {
        selector: ".slideshow-primers",
        images: [
          "img/plats-primers-1.jpg",
          "img/plats-primers-2.jpg",
          "img/plats-primers-3.jpg"
        ]
      },
      {
        selector: ".slideshow-segons",
        images: [
          "img/plats-segons-1.jpg",
          "img/plats-segons-2.jpg",
          "img/plats-segons-3.jpg"
        ]
      },
      {
        selector: ".slideshow-postres",
        images: [
          "img/plats-postres-1.jpg",
          "img/plats-postres-2.jpg",
          "img/plats-postres-3.jpg"
        ]
      }
    ];
  
    slideshows.forEach(({ selector, images }) => {
      const imgEl = document.querySelector(selector);
      if (!imgEl) return;
  
      let index = 0;
      let intervalId;
  
      const start = () => {
        intervalId = setInterval(() => {
          imgEl.classList.add("fade-out");
  
          setTimeout(() => {
            index = (index + 1) % images.length;
            imgEl.src = images[index];
            imgEl.classList.remove("fade-out");
          }, 800);
        }, 5000);
      };
  
      const stop = () => clearInterval(intervalId);
  
      // Start slideshow
      start();
  
      // Pause on hover
      imgEl.addEventListener("mouseenter", stop);
      imgEl.addEventListener("mouseleave", start);
    });
  }
  
  

  document.addEventListener("DOMContentLoaded", () => {
    loadMenu();
    startHeroSlideshow();
    startCardSlideshows();
  });  
  