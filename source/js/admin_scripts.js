/* admin-scripts.js -- admin script library */


// debounce function to limit the rate at which a function is executed
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func.apply(this, args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}


document.addEventListener("DOMContentLoaded", () => {
    // set up marked.js for markdown processing
    marked.use(
        {
            breaks: true,
            pedantic: false,
            gfm: true,
        },
        markedSmartypants.markedSmartypants({ config: "3" }),
    );

    // set up constants for forms
    const postForm = document.getElementById("post-entry");
    const pageForm = document.getElementById("page-entry");
    const reactionForm = document.getElementById("reaction-entry");

    // set up contentMeta JSON object
    const contentMeta = document.getElementById("id_content_meta");
    let contentMetaValue = JSON.parse(contentMeta ? contentMeta.value : "{}");

    const updateContentMeta = function(key, value) {
        if (value) {
            contentMetaValue[key] = value;
        } else {
            delete contentMetaValue[key];
        }
        contentMeta.value = JSON.stringify(contentMetaValue);
    };

    // update markdown preview
    const markdownPreview = document.getElementById("preview-markdown");
    const previewDisplay = document.getElementById("preview-display");

    const updatePreview = function() {
        if (markdownPreview && previewDisplay) {
            const markdownText = markdownPreview.value.replace(/\n{3,}/g, "\n\n");
            const html = marked.parse(markdownText).trim();

            updateContentMeta("markdown", markdownText ? markdownText : null);
            updateContentMeta("html", html ? html : null);

            previewDisplay.innerHTML = html;
        }
    }

    if (markdownPreview) {
        markdownPreview.addEventListener("keyup", debounce(updatePreview, 100));
        updatePreview;
    }

    // process post form
    if (postForm) {
        const titleField = document.getElementById("preview-title");
        const contentTypeSelect = document.getElementById("id_content_type");
        contentTypeSelect.value = "note"

        if (titleField) {
            titleField.addEventListener("keyup", debounce(() => {
                contentTypeSelect.value = titleField.value.trim().length > 0 ? "post" : "note";

                const title = titleField.value;
                updateContentMeta("title", title ? title : null);

                let previewTitle = previewDisplay.querySelector("h2");

                if (title) {
                    if (previewTitle) {
                        previewTitle.textContent = title;
                    } else {
                        let newTitle = document.createElement("h2");
                        newTitle.textContent = title;
                        previewDisplay.insertAdjacentElement("afterbegin", newTitle);
                    }
                } else {
                    // If title is empty and an <h2> exists, remove it
                    if (previewTitle) {
                        previewTitle.remove();
                    }
                }
            }, 100));
        }

        // handle syndication checkboxes
        const contentFederate = document.getElementById("id_content_federate");
        const contentRssOnly = document.getElementById("id_content_rss_only");
        const contentWebmentions = document.getElementById("id_allow_outgoing_webmentions");

        const handleSyndication = function(event) {
            if (event.target === contentRssOnly && contentRssOnly.checked) {
                contentFederate.checked = false;
                contentWebmentions.checked = false;
            } else if ((event.target === contentFederate && contentFederate.checked) ||
                       (event.target === contentWebmentions && contentWebmentions.checked)) {
                contentRssOnly.checked = false;
            }
        }

        if (contentFederate && contentRssOnly && contentWebmentions) {
            contentFederate.addEventListener("change", handleSyndication);
            contentRssOnly.addEventListener("change", handleSyndication);
            contentWebmentions.addEventListener("change", handleSyndication);
        }

        updatePreview();
    }

    // process page form
    if (pageForm) {
        const descField = document.getElementById("preview-description");
        const titleField = document.getElementById("preview-title");
        const parentField = document.getElementById("id_parent_type");
        const pathField = document.getElementById("id_content_path");

        const updateContentPath = function() {
            const slug = titleField.value.trim().toLowerCase().replace(/[\s\W-]+/g, "-");
            const parentValue = parentField.value;

            let contentPath = parentValue ? parentValue + "/" + slug : slug

            pathField.value = contentPath;
        }

        if (descField) {
            descField.addEventListener("keyup", debounce(() => {
                updateContentMeta("description", descField.value.trim() ? descField.value.trim() : null);
            }, 100));
        }

        if (titleField) {
            titleField.addEventListener("keyup", debounce(() => {
                const title = titleField.value.trim();
                updateContentMeta("title", title ? title : null);
                updateContentPath();
            }, 100));
        }

        if (parentField) {
            parentField.addEventListener("change", updateContentPath);
        }

        updatePreview();

        const selectParent = function() {
            let contentPath = document.getElementById("id_content_path").value;
            contentPath = contentPath.substring(0, contentPath.lastIndexOf("/"));

            const parentType = document.getElementById("id_parent_type").options;

            for (const option of parentType) {
                if (option.value === contentPath) {
                    option.selected = true;
                    break;
                }
            }
        };

        selectParent();
    }

    // process reaction form
    if (reactionForm) {
        const reactionUrlField = document.getElementById("id_reaction_url");
        const contentTypeSelect = document.getElementById("id_content_type");
        const reactionContainer = document.getElementById("reaction-container");
        const reactionReactTo = document.getElementById("reaction-react-to");
        const reactionMarkdown = document.getElementById("reaction-markdown");

        // handle paste into reactionUrlField
        reactionUrlField.addEventListener("paste", (event) => {
            const pastedText = (event.clipboardData || window.clipboardData).getData("text");
            let match = pastedText.match(/^https:\/\/([^/]+)\/@(\w+)\/(\d+)$/);
            let originalDomain, name, id;

            if (match) {
                [, originalDomain, name, id] = match;
            } else {
                match = pastedText.match(/^https:\/\/([^/]+)\/@(\w+)@([^/]+)\/(\d+)$/);
                if (match) {
                    [, originalDomain, , id] = match;
                }
            }

            if (match) {
                fetch(`https://${originalDomain}/api/v1/statuses/${id}`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error("Network response was not ok");
                        }
                        return response.json();
                    })
                    .then(data => {
                        updateContentMeta("json", data);
                        updateContentMeta("url", data["url"]);
                        reactionReactTo.classList.remove("hide");
                        reactionReactTo.innerHTML = data["content"];
                    })
                    .catch(() => {
                        alert("Error fetching status");
                    });
            } else {
                alert("Unrecognized URL format");
            }
        });

        // handle clearing the reaction url
        reactionUrlField.addEventListener("input", (event) => {
            if (reactionUrlField.value === "") {
                reactionReactTo.classList.add("hide");
                reactionReactTo.innerHTML = "";
                reactionMarkdown.value = "";
                updateContentMeta("json", "");
                updateContentMeta("url", "");
                updateContentMeta("markdown", "");
                updateContentMeta("html", "");
            }
        });

        // handle change on contentTypeSelect
        const updateReplyText = function() {
            const markdown = reactionMarkdown.value;
            const html = marked.parse(markdown);
            updateContentMeta("markdown", markdown);
            updateContentMeta("html", html);
        };

        contentTypeSelect.addEventListener("change", () => {
            const contentType = contentTypeSelect.value;
            reactionMarkdown.removeEventListener("keyup", updateReplyText);

            switch (contentType) {
                case "like":
                case "repost":
                    reactionContainer.classList.add("hide");
                    reactionMarkdown.value = "";
                    updateContentMeta("markdown", "");
                    updateContentMeta("html", "");
                    break;
                case "reply":
                    reactionContainer.classList.remove("hide");
                    if (contentMetaValue.json && contentMetaValue.json.account) {
                        const { acct, url } = contentMetaValue.json.account;
                        if (!reactionMarkdown.value.startsWith(`<span class="hide"><a href="${url}">@${acct}</a><a class="u-in-reply-to" href="${reactionUrlField.value}"></a></span>`)) {
                            reactionMarkdown.value = `<span class="hide"><a href="${url}">@${acct}</a><a class="u-in-reply-to" href="${reactionUrlField.value}"></a></span>` + reactionMarkdown.value;
                        }
                    }
                    updateReplyText();
                    reactionMarkdown.addEventListener("keyup", updateReplyText);
                    break;
                default:
                    break;
            }
        });
    }
});
