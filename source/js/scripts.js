/* scripts.js -- main script library */

document.addEventListener("DOMContentLoaded", () => {

    // color scheme switcher
    const themeToggle = document.getElementById("theme-toggle");
    const themeIcon = document.getElementById("theme-icon");
    let currentTheme = localStorage.getItem("theme") || "auto";

    const fetchSVG = async (theme) => {
        const response = await fetch(`/assets/img/${theme}.svg`);
        const text = await response.text();
        return text;
    };

    const applyTheme = async (theme) => {
        let newTheme = theme;
        if (theme === "auto") {
            newTheme = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
        }
        document.querySelector('link[id="theme"]').href = `/assets/css/${newTheme}.css`;
        const svgText = await fetchSVG(theme);
        themeIcon.innerHTML = svgText;
    };

    themeToggle.addEventListener("click", async () => {
        if (currentTheme === "dark") {
            currentTheme = "light";
        } else if (currentTheme === "light") {
            currentTheme = "auto";
        } else {
            currentTheme = "dark";
        }
        localStorage.setItem("theme", currentTheme);
        await applyTheme(currentTheme);
    });

    const systemThemeListener = window.matchMedia("(prefers-color-scheme: dark)");
    systemThemeListener.addListener(() => {
        if (currentTheme === "auto") {
            applyTheme(currentTheme);
        }
    });

    applyTheme(currentTheme);
    localStorage.setItem("theme", currentTheme);


    // open external links in new tabs
    let links = document.querySelectorAll("a")
    for(let i = 0; i < links.length; i++) {
        if(links[i].hostname != window.location.hostname) {
            links[i].setAttribute("target", "_blank")
            links[i].setAttribute("rel", "noopener")
        }
    }


    // set table cell spacing and padding
    const tables = document.querySelectorAll("table");
    if (tables.length > 0) {
        tables.forEach((table) => {
        table.setAttribute("cellspacing", "0");
        table.setAttribute("cellpadding", "0");
        });
    }


    // add shadow to header on scroll
    const headerElement = document.querySelector("header");
    const handleScroll = () => {
        const scrollPosition = window.scrollY;
        const threshold = headerElement.offsetHeight;

        if (scrollPosition >= threshold) {
            headerElement.classList.add("shadow");
        } else {
            headerElement.classList.remove("shadow");
        }
    };
    window.addEventListener("scroll", handleScroll);
    handleScroll();
});
