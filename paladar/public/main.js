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
  
    setInterval(() => {
      // fade out
      heroImg.classList.add("fade-out");
  
      setTimeout(() => {
        // change image
        index = (index + 1) % images.length;
        heroImg.src = images[index];
  
        // fade in
        heroImg.classList.remove("fade-out");
      }, 800); // matches CSS transition
    }, 4500); // change every 4.5 seconds
  }
  
  document.addEventListener("DOMContentLoaded", () => {
    loadMenu();
    startHeroSlideshow();
  });
    
  document.addEventListener("DOMContentLoaded", loadMenu);
  