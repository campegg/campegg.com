/* scripts.js -- main script library */

document.addEventListener("DOMContentLoaded", () => {

    // color theme switcher
    const themeToggle = document.getElementById("theme-toggle");
    const themeIcon = document.getElementById("theme-icon");
    let currentTheme = localStorage.getItem("theme") || "auto";

    localStorage.setItem("theme", currentTheme);

    const fetchSVG = async (theme) => {
        const response = await fetch(`/assets/img/${theme}.svg`);
        return response.text();
    };

    const applyTheme = async (theme) => {
        let newTheme = theme === "auto" ? (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light") : theme;
        document.querySelector('link[id="theme"]').href = `/assets/css/${newTheme}.css`;
        const iconTheme = theme; // 'auto', 'dark', or 'light'
        themeIcon.innerHTML = await fetchSVG(iconTheme);
    };

    themeToggle.addEventListener("click", async () => {
        currentTheme = currentTheme === "auto" ? "dark" : currentTheme === "dark" ? "light" : "auto";
        localStorage.setItem("theme", currentTheme);
        await applyTheme(currentTheme);
    });

    window.matchMedia("(prefers-color-scheme: dark)").addListener(() => {
        if (currentTheme === "auto") {
            applyTheme("auto");
        }
    });

    applyTheme(currentTheme);


    // set table cellpadding and cellspacing to 0
    const tables = document.querySelectorAll("table");
    tables.forEach(table => {
        table.setAttribute("cellspacing", "0");
        table.setAttribute("cellpadding", "0");
    });


    // add shadow to header on scroll
    const headerElement = document.querySelector("header");
    const handleScroll = () => {
        headerElement.classList.toggle("shadow", window.scrollY >= headerElement.offsetHeight);
    };
    window.addEventListener("scroll", handleScroll);
    handleScroll();
});
