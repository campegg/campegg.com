/* scripts.js -- main script library */

document.addEventListener("DOMContentLoaded", () => {

    // color scheme switcher
    const isDaytime = () => { // maybe update this to more accurately detect sunrise/sunset at some point?
        const hour = new Date().getHours();
        return hour >= 7 && hour < 19;
    };
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
        let iconTheme = theme; // Separate variable for the icon theme

        if (theme === "auto") {
            newTheme = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
        } else if (theme === "time") {
            newTheme = isDaytime() ? "light" : "dark";
            // Keep iconTheme as 'time' to fetch the time icon
        }

        document.querySelector('link[id="theme"]').href = `/assets/css/${newTheme}.css`;
        const svgText = await fetchSVG(iconTheme); // Fetch the SVG for the iconTheme
        themeIcon.innerHTML = svgText;
    };

    themeToggle.addEventListener("click", async () => {
        if (currentTheme === "dark") {
            currentTheme = "light";
        } else if (currentTheme === "light") {
            currentTheme = "auto";
        } else if (currentTheme === "auto") {
            currentTheme = "time";
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

    let links = document.querySelectorAll("a");
    for (let i = 0; i < links.length; i++) {
        if (links[i].hostname !== window.location.hostname) {
            links[i].setAttribute("target", "_blank");
            let currentRel = links[i].getAttribute("rel");
            if (currentRel) {
                if (!currentRel.includes("noopener")) {
                    links[i].setAttribute("rel", currentRel + " noopener");
                }
            } else {
                links[i].setAttribute("rel", "noopener");
            }
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
