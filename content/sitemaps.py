# sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from datetime import datetime, timedelta


from content.models import Content


class ContentSitemap(Sitemap):
    def items(self):
        return (
            Content.objects.filter(
                content_rss_only=0,
                publish_date__lte=datetime.now().replace(microsecond=0),
            )
            .exclude(content_type="like")
            .order_by("-publish_date", "content_type")
        )

    def lastmod(self, obj):
        return obj.update_date if obj.update_date is not None else obj.publish_date

    def changefreq(self, obj):
        now = datetime.now()

        if obj.update_date is not None:
            delta = now - obj.update_date
        else:
            delta = now - obj.publish_date

        if delta <= timedelta(days=7):
            return "daily"
        elif timedelta(days=7) < delta <= timedelta(days=30):
            return "weekly"
        elif timedelta(days=30) < delta <= timedelta(days=365):
            return "monthly"
        else:
            return "yearly"

    def location(self, obj):
        view_name = {
            "note": "note",
            "photo": "photo",
            "post": "post",
            "reply": "reply",
            "repost": "repost",
            "page": "page",
            "activity": "activity",
        }.get(obj.content_type, "page")

        if obj.content_type in ["note", "photo", "post", "reply", "repost"]:
            return reverse(
                "dispatcher",
                args=[
                    obj.publish_date.year,
                    f"{obj.publish_date.month:02d}",
                    f"{obj.publish_date.day:02d}",
                    obj.content_path,
                ],
            )
        else:
            return reverse(view_name, kwargs={"slug": obj.content_path})

    def priority(self, obj):
        priority_map = {
            "note": 1.0,
            "photo": 0.75,
            "post": 0.75,
            "reply": 0.5,
            "repost": 0.5,
            "page": 0.75,
            "activity": 0.25,
        }
        return priority_map.get(obj.content_type, 0.5)


class StaticViewSitemap(Sitemap):
    def items(self):
        return ["home", "archive"]

    def location(self, obj):
        return reverse(obj)

    def lastmod(self, obj):
        latest_post = (
            Content.objects.filter(
                publish_date__lte=datetime.now().replace(microsecond=0),
                content_rss_only__exact=0,
            )
            .order_by("-publish_date")
            .first()
        )

        if latest_post:
            return latest_post.publish_date
        return None

    def changefreq(self, obj):
        return "daily"

    def priority(self, obj):
        return 1.0


# Define a dictionary to include all sitemaps
sitemaps = {
    "views": StaticViewSitemap(),
    "pages": ContentSitemap(),
}
