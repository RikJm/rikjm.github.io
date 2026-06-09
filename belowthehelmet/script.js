const logo = document.getElementById("mainLogo");
const navbar = document.getElementById("navbar");

window.addEventListener("scroll", () => {
    if (window.scrollY > 100) {
        logo.style.transform = "scale(0.4)";
        logo.style.opacity = "0";
        navbar.style.top = "0";
    } else {
        logo.style.transform = "scale(1)";
        logo.style.opacity = "1";
        navbar.style.top = "-80px";
    }
});
