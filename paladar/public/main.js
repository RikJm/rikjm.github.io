async function loadMenu() {
    const dateEl = document.getElementById("menu-date");
    const primersEl = document.getElementById("primers-list");
    const segonsEl = document.getElementById("segons-list");
    const postresEl = document.getElementById("postres-list");
    const errorEl = document.getElementById("menu-error");
  
    try {
      const res = await fetch("/api/menu");
      if (!res.ok) throw new Error("Error carregant el menú");
  
      const menu = await res.json();
  
      // Simple date display – you can adapt to weekday names if you like
      dateEl.textContent = menu.date ? `Data: ${menu.date}` : "";
  
      const renderList = (el, items) => {
        el.innerHTML = "";
        (items || []).forEach((item) => {
          const li = document.createElement("li");
          li.textContent = item;
          el.appendChild(li);
        });
      };
  
      renderList(primersEl, menu.primers);
      renderList(segonsEl, menu.segons);
      renderList(postresEl, menu.postres);
  
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
  