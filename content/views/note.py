from django.views.generic import DetailView
import httpx
import json


from content.models import Content
from mentions.models import Webmention


class Note(DetailView):
    context_object_name = "item"
    model = Content
    template_name = "content.html"
    slug_field = "content_path"
    slug_url_kwarg = "slug"

    def get_mentions(self, *args, **kwargs):
        print(f"ID: {self.object.id}")
        mentions = (
            Webmention.objects.filter(object_id=self.object.id, approved=1)
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
                mention.hcard.homepage = (
                    hcard_meta.url if hcard_meta.url != "/" else None
                )

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mentions"] = self.get_mentions()
        context["page_meta"] = {
            "body_class": "note",
            "title": self.object.publish_date.strftime("%B %-d %Y, %-I:%M%p")
            .replace("AM", "am")
            .replace("PM", "pm"),
        }
        return context
