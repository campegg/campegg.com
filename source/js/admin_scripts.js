/* admin_scripts.js -- admin-specific script library */

document.addEventListener("DOMContentLoaded", () => {
    // make sure umami tracking is disabled for me
    localStorage.setItem("umami.disabled", "true");


    // strip Markdown syntax for character counting
    const stripMarkdown = (md) => {
        return md
            .replace(/!\[[^\]]*\]\([^)]*\)/g, '') // images
            .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1') // links (but keep the text!)
            .replace(/#+\s+/g, '') // headings
            .replace(/`{3}.*?`{3}/gs, '') // code blocks
            .replace(/`.*?`/g, '') // inline code
            .replace(/[*_]{1,3}/g, '') // bold, italic, and strikethrough
            .replace(/~~/g, '') // strikethrough
            .replace(/(>+ )/g, '') // blockquotes
            .replace(/(-|\*|\+|\d+\.) /g, ''); // list items
    };


    // count post characters
    const updateChars = () => {
        const countArea = document.getElementById("id_text");
        const countDisplay = document.getElementById("post-entry-text-chars");
        const rawText = countArea.value;
        const strippedText = stripMarkdown(rawText);
        const chars = strippedText.length;

        countDisplay.textContent = chars;

        if (chars <= 239) {
            countDisplay.className = "";
        } else if (chars >= 240 && chars < 460) {
            countDisplay.className = "warning";
        } else if (chars >= 460) {
            countDisplay.className = "error";
        }
    };

    const adminTextChars = document.getElementById("post-entry-text-chars");
    const postCreateText = document.getElementById("id_text");

    if (adminTextChars) {
        updateChars();
        postCreateText.addEventListener("keyup", () => updateChars());
    }

    // enforce checkbox rules
    const sendToFediverseCheckbox = document.getElementById("id_send_to_fediverse");
    const sendToArchiveCheckbox = document.getElementById("id_send_to_archive");
    const rssOnlyCheckbox = document.getElementById("id_rss_only");

    const updateCheckboxes = () => {
        if (rssOnlyCheckbox.checked) {
            sendToFediverseCheckbox.checked = false;
            sendToArchiveCheckbox.checked = false;
            sendToFediverseCheckbox.disabled = true;
            sendToArchiveCheckbox.disabled = true;
        } else {
            sendToFediverseCheckbox.disabled = false;
            sendToArchiveCheckbox.disabled = false;
        }
    };

    if (sendToFediverseCheckbox) {
        updateCheckboxes();

        rssOnlyCheckbox.addEventListener("change", updateCheckboxes);
        sendToFediverseCheckbox.addEventListener("change", updateCheckboxes);
        sendToArchiveCheckbox.addEventListener("change", updateCheckboxes);
    }
});
