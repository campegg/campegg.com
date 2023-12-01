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
        const countArea = document.getElementById("id_post_form-text");
        const countDisplay = document.getElementById("admin-text-chars");
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

        if (chars > 549) {
            countArea.setAttribute("rows", "20");
        } else {
            countArea.setAttribute("rows", "10");
        }
    };

    const adminTextChars = document.getElementById("admin-text-chars");
    const postCreateText = document.getElementById("id_post_form-text");

    if (adminTextChars) {
        updateChars();
        postCreateText.addEventListener("keyup", () => updateChars());
    }


    // handle the photo upload field
    const photoField = document.getElementById("id_post_form-photo");

    if (photoField) {
        const fileDisplay = document.getElementById("custom-upload-display");

        // Update the display text when a new photo is selected
        photoField.addEventListener("change", () => {
            const photoFile = photoField.files[photoField.files.length - 1];
            fileDisplay.textContent = photoFile.name;
            console.log(`Change: ${fileDisplay.textContent}`);
        });
    }


    // enforce checkbox rules
    const sendToFediverseCheckbox = document.getElementById("id_post_form-send_to_fediverse");
    const sendToArchiveCheckbox = document.getElementById("id_post_form-send_to_archive");
    const rssOnlyCheckbox = document.getElementById("id_post_form-rss_only");

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
