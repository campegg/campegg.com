/* mentions.js -- handle post mentions/reactions */

document.addEventListener("DOMContentLoaded", () => {
    const postArticle = document.querySelector("article:last-of-type");

    async function getMentions() {
        const path = window.location.pathname;
        try {
            const response = await fetch(`/webmentions/get?url=${encodeURIComponent(path)}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            if (Array.isArray(data.mentions) && data.mentions.length > 0) {
                let reactionsDiv = document.getElementById("reaction-container");
                if (!reactionsDiv) {
                    reactionsDiv = document.createElement("div");
                    reactionsDiv.id = "reaction-container";
                    const heading = document.createElement("h3");
                    heading.textContent = "Reactions";
                    reactionsDiv.appendChild(heading);
                    reactionsDiv.appendChild(document.createElement("ul"));
                    postArticle.insertAdjacentElement("afterend", reactionsDiv);
                }

                const ul = reactionsDiv.querySelector("ul");
                ul.innerHTML = "";
                data.mentions.forEach(mention => {
                    const mentionTypes = {
                        "bookmark": "bookmarked",
                        "like": "liked",
                        "reply": "replied to",
                        "repost": "reposted"
                    };
                    let action = mentionTypes[mention.type] || "mentioned";
                    let includeActionLink = true;

                    if (mention.source_url.includes("likes/")) {
                        action = "liked";
                        includeActionLink = false; // do not include action link for bridgy/activitypub likes
                    }

                    const profileUrl = mention.hcard.homepage;
                    const avatarImg = mention.hcard.avatar || "/assets/img/no_avatar.png";
                    const name = mention.hcard.name;
                    const actionUrl = mention.source_url;

                    const liHtml = `
                        <li>
                            <a href="${profileUrl}">
                                <img src="${avatarImg}" class="mention_avatar" alt="${name}’s avatar" onerror="this.onerror=null;this.src='/assets/img/no_avatar.png';">
                                ${name}
                            </a>
                            ${includeActionLink ? ` <a href="${actionUrl}">${action}</a>` : ` ${action}`} this post
                        </li>
                    `;
                    ul.innerHTML += liHtml;
                });
            }
        } catch (error) {
            console.error("Error fetching reactions:", error);
        }
    }

    getMentions();
});
