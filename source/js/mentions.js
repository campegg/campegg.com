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
                heading.title = "When someone responds to one of my posts and sends a webmention, it will be displayed here.";
                mentionsDiv.appendChild(heading);

                const ul = document.createElement("ul");
                mentions.forEach(mention => {
                    const li = document.createElement("li");
                    const a = document.createElement("a");
                    const img = document.createElement("img");

                    a.href = mention.source_url;
                    img.src = mention.hcard.avatar;
                    img.className = "mention_avatar";
                    img.alt = mention.hcard.name + "'s avatar";

                    a.appendChild(img);
                    a.appendChild(document.createTextNode(" " + mention.hcard.name));

                    if (mention.source_url.includes('likes/')) {
                        li.appendChild(a);
                        li.appendChild(document.createTextNode(" liked this post"));
                    } else {
                        li.appendChild(a);
                        li.appendChild(document.createTextNode(" mentioned this post"));
                    }

                    ul.appendChild(li);
                    mentionsDiv.appendChild(ul);

                    const postArticle = document.querySelector('article:last-of-type');
                    postArticle.insertAdjacentElement('afterend', mentionsDiv);
                });
            }
        } catch (error) {
            console.error("Error fetching mentions:", error);
        }
    }
    getMentions();
});
