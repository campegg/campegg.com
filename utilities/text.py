from bs4 import BeautifulSoup
from markdown import Markdown
import httpx
import json
import re


# ---------- markdown settings ----------#
md = Markdown(
    extensions=(
        "codehilite",
        "extra",
        "meta",
        "md_in_html",
        "sane_lists",
        "smarty",
        "toc",
    ),
    extension_configs={
        "codehilite": {
            "linenums": True,
            "linespans": "line",
            "lineseparator": "<br>",
        },
    },
    output_format="html5",
)


# ---------- widow/orphan control ----------#
def widont(text):
    widont_finder = re.compile(
        r"""((?:</?(?:a|em|span|strong|i|b)[^>]*>)|[^<>\s]) # must be proceeded by an approved inline opening or closing tag or a nontag/nonspace
            \s+                                             # the space to replace
            ([^<>\s]+                                       # must be followed by non-tag non-space characters
            \s*                                             # optional white space!
            (</(a|em|span|strong|i|b)>\s*)*                 # optional closing inline tags with optional white space after each
            ((</(p|h[1-6]|li|dt|dd)>)|$))                   # end with a closing p, h1-6, li or the end of the string
        """,
        re.VERBOSE,
    )
    output = widont_finder.sub(r"\1&nbsp;\2", text)
    return output


# ---------- process embeds ----------#
def process_embeds(source):
    regex = r"((<[a-zA-Z]>)?{{\s*)?(https?:\/\/(?:www\.|(?!www))?[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})(\s*}}(<\/[a-zA-Z]>)?)"
    embeds = re.findall(regex, source)

    if embeds:
        for match in embeds:
            raw = match[0] + match[1] + match[2] + match[3] + match[4]
            url = match[2]

            if "youtube.com/watch" in url or "youtu.be" in url:
                oembed_url = (
                    f"https://youtube.com/oembed?url={url}&format=json&maxwidth=576"
                )
                type = "video"
            elif "twitter.com" and "status" in url:
                oembed_url = f"https://publish.twitter.com/oembed?url={url}&align=center&maxwidth=576&dnt=true"
                type = "tweet"
            elif "vimeo.com" in url:
                oembed_url = f"https://vimeo.com/api/oembed.json?url={url}&maxwidth=576&transparent=false&responsive=true&dnt=true"
                type = "video"
            elif "apple.com" in url:
                oembed_url = None
                music_url = url.replace("music.apple", "embed.music.apple")
                custom_embed = f'<iframe allow="autoplay *; encrypted-media *; fullscreen *" frameborder="0" height="450" style="width:100%;max-width:660px;overflow:hidden;background:transparent;" sandbox="allow-forms allow-popups allow-same-origin allow-scripts allow-storage-access-by-user-activation allow-top-navigation-by-user-activation" src="{music_url}"></iframe>'
                type = "music"
            elif "ted.com" in url:
                oembed_url = f"https://www.ted.com/services/v1/oembed.json?url={url}"
                type = "video"
            else:
                oembed_url = None
                custom_embed = None

            if oembed_url:
                response = httpx.get(oembed_url)
                payload = json.loads(response.text)
                html = payload["html"]
                embed = f'<div class="embed {type}-embed">{html}</div>'
            elif custom_embed:
                embed = f'<div class="embed {type}-embed">{custom_embed}</div>'
            else:
                embed = f' <a href="{url}">{url}</a>'

            return source.replace(raw, embed)
    else:
        return source


# ---------- render html ----------#
def render_html(text):
    embeds = process_embeds(text)
    html = md.convert(embeds)
    output = widont(html)
    return output
