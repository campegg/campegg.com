import httpx
import json


from mentions.models import Webmention


def get_mentions(content_id):
    print(f"Getting mentions for ID: {content_id}")
    mentions = (
        Webmention.objects.filter(object_id=content_id, approved=1)
        .select_related("hcard")
        .order_by("-created_at")
    )

    for mention in mentions:
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.head(mention.hcard.avatar)
                if response.status_code == 200:
                    mention.hcard.avatar = mention.hcard.avatar
                else:
                    mention.hcard.avatar = None
        except httpx.RequestError:
            mention.hcard.avatar = None

        hcard_meta = json.loads(mention.hcard.json)

        if hcard_meta and not mention.hcard.homepage:
            mention.hcard.homepage = hcard_meta.url if hcard_meta.url != "/" else None

        if "likes/" in mention.source_url or mention.post_type == "like":
            mention.action = "liked"
        elif mention.post_type == "bookmark":
            mention.action = "bookmarked"
        elif mention.post_type == "reply":
            mention.action = "replied to"
        elif mention.post_type == "repost":
            mention.action = "reposted"
        else:
            mention.action = "mentioned"

    return mentions
