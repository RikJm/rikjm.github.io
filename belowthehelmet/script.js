const mainLogo = document.getElementById("mainLogo");
const navLogo = document.getElementById("navLogo");
const navbar = document.getElementById("navbar");

const hamburger = document.getElementById("hamburger");
const mobileMenu = document.getElementById("mobileMenu");

hamburger.addEventListener("click", () => {
    mobileMenu.classList.toggle("active");
});


window.addEventListener("scroll", () => {
    if (window.scrollY > 100) {
        mainLogo.style.transform = "scale(0.4)";
        mainLogo.style.opacity = "0";

        navbar.style.top = "0";

        navLogo.style.opacity = "1";
        navLogo.style.transform = "scale(1)";
    } else {
        mainLogo.style.transform = "scale(1)";
        mainLogo.style.opacity = "1";

        navbar.style.top = "-120px";

        navLogo.style.opacity = "0";
        navLogo.style.transform = "scale(0.8)";
    }
});
