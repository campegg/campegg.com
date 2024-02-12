/* mentions.js -- handle post mentions/reactions */

document.addEventListener("DOMContentLoaded", () => {
    async function getMentions() {
        try {
            const path = window.location.pathname;
            const response = await fetch(`/webmentions/get?url=${encodeURIComponent(path)}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            const mentions = data.mentions;

            if (Array.isArray(mentions) && mentions.length > 0) {
                const reactionsDiv = document.createElement("div");
                reactionsDiv.id = "reaction-container";

                const heading = document.createElement("h3");
                heading.textContent = "Reactions";
                reactionsDiv.appendChild(heading);

                const ul = document.createElement("ul");
                mentions.forEach(mention => {
                    const li = document.createElement("li");
                    const profileLink = document.createElement("a");
                    profileLink.href = mention.hcard.homepage;
                    const img = document.createElement("img");
                    img.src = mention.hcard.avatar || "/assets/img/no_avatar.png";
                    img.className = "mention_avatar";
                    img.alt = `${mention.hcard.name}’s avatar`;
                    img.onerror = () => {
                        img.src = "/assets/img/no_avatar.png";
                    };
                    profileLink.appendChild(img);
                    profileLink.innerHTML += ` ${mention.hcard.name}`;

                    li.appendChild(profileLink);

                    const mentionTypes = {
                        "bookmark": "bookmarked",
                        "like": "liked",
                        "reply": "replied to",
                        "repost": "reposted"
                    };
                    let action = mentionTypes[mention.type] || "mentioned";
                    if (mention.source_url.includes("likes/")) {
                        action = "liked";
                    }

                    const actionLink = document.createElement("a");
                    actionLink.href = mention.source_url;
                    actionLink.textContent = action;
                    li.appendChild(document.createTextNode(" "));
                    li.appendChild(actionLink);
                    li.appendChild(document.createTextNode(" this post"));
                    ul.appendChild(li);
                });
                reactionsDiv.appendChild(ul);

                const postArticle = document.querySelector("article:last-of-type");
                postArticle.insertAdjacentElement("afterend", reactionsDiv);
            }
        } catch (error) {
            console.error("Error fetching reactions:", error);
        }
    }
    getMentions();
});
