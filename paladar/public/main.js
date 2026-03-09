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
  
  document.addEventListener("DOMContentLoaded", loadMenu);
  