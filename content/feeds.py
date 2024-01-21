from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.http import JsonResponse
from django.utils import timezone
from django.views import View
from datetime import datetime
from datetime import timedelta


from content.models import Post


class PostFeed(Feed):
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
        return (
            Post.objects.all()
            .filter(
                publish_date__lte=datetime.now() + timedelta(minutes=5),
                status__exact=1,
            )
            .order_by("-publish_date")
        )[:20]

    def item_title(self, item):
        return (
            item.title
            if item.title
            else f"{datetime.strftime(item.publish_date, '%B %-d %Y, %-I:%M %p')}"
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


class JsonFeed(View):
    def get(self, request, *args, **kwargs):
        base_url = request.build_absolute_uri("/")[:-1]

        # feed metadata
        feed_info = {
            "version": "https://jsonfeed.org/version/1",
            "title": "Cam Pegg",
            "home_page_url": base_url,
            "feed_url": f"{base_url}/feed.json",
            "description": "The most recent posts to campegg.com",
            "author": {"name": "Cam Pegg"},
            "icon": f"{base_url}/assets/img/favicon-256x256.png",
        }

        # fetch posts
        posts = (
            Post.objects.all()
            .filter(
                publish_date__lte=datetime.now() + timedelta(minutes=5),
                status__exact=1,
                send_to_fediverse__exact=1,
                rss_only__exact=0,
            )
            .order_by("-publish_date")
        )

        # construct feed items
        items = []
        for post in posts:
            publish_date_tz = timezone.make_aware(post.publish_date)
            update_date_tz = (
                timezone.make_aware(post.update_date) if post.update_date else None
            )
            item = {
                "id": post.id,
                "title": (post.title if post.title else ""),
                "url": base_url + post.get_absolute_url(),
                "content_html": post.html,
                "date_published": publish_date_tz.isoformat(),
                "date_modified": update_date_tz.isoformat() if update_date_tz else None,
            }
            items.append(item)

        # combine feed info and items
        feed = {**feed_info, "items": items}
        return JsonResponse(feed)
