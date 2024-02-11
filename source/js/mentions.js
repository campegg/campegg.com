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
                const mentionsDiv = document.createElement("div");
                mentionsDiv.id = "mentions";

                const heading = document.createElement("h3");
                heading.textContent = "Reactions";
                mentionsDiv.appendChild(heading);

                const ul = document.createElement("ul");
                mentions.forEach(mention => {
                    console.log(mention)
                    const li = document.createElement("li");
                    const a = document.createElement("a");
                    const img = document.createElement("img");

                    a.href = mention.source_url;
                    img.src = mention.hcard.avatar || "/assets/img/no_avatar.png";
                    img.className = "mention_avatar";
                    img.alt = mention.hcard.name + "'s avatar";

                    // Add an error handler for the image
                    img.onerror = () => {
                        img.src = "/assets/img/no_avatar.png";
                    };

                    a.appendChild(img);
                    a.appendChild(document.createTextNode(" " + mention.hcard.name));

                    li.appendChild(a);

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

                    li.appendChild(document.createTextNode(` ${action} this post`));

                    ul.appendChild(li);
                    mentionsDiv.appendChild(ul);

                    const postArticle = document.querySelector("article:last-of-type");
                    postArticle.insertAdjacentElement("afterend", mentionsDiv);
                });
            }
        } catch (error) {
            console.error("Error fetching reactions:", error);
        }
    }
    getMentions();
});
