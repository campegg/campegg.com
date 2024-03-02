from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.utils import timezone
from datetime import datetime
from datetime import timedelta


from content.models import Content


class ContentFeed(Feed):
    feed_type = Atom1Feed
    title = "Cam Pegg"
    link = "/"
    description = "The most recent posts to campegg.com"
    description_template = "feeds/feed_description.html"
    author_name = "Cam Pegg"

    def __call__(self, request, *args, **kwargs):
        response = super().__call__(request, *args, **kwargs)
        response["Content-Type"] = "application/atom+xml; charset=utf-8"
        return response

    def items(self):
        content_types = ["note", "post", "photo"]
        items = (
            Content.objects.filter(content_type__in=content_types)
            .filter(publish_date__lte=datetime.now() + timedelta(minutes=5))
            .order_by("-publish_date")
        )[:20]
        return items

    def item_title(self, item):
        return (
            item.content_meta.get("title")
            if item.content_meta.get("title")
            else datetime.strftime(item.publish_date, "%B %-d %Y, %-I:%M%p")
            .replace("AM", "am")
            .replace("PM", "pm")
        )

    def item_pubdate(self, item):
        return timezone.make_aware(item.publish_date)

    def item_updateddate(self, item):
        if item.update_date != item.publish_date:
            return timezone.make_aware(item.publish_date)
        else:
            return timezone.make_aware(item.update_date)

    def item_link(self, item):
        return item.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
