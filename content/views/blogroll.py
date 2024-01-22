from django.conf import settings
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.template.loader import get_template


from datetime import datetime
from pathlib import Path


import json


subs_json = settings.BASE_DIR / "data" / "blogroll" / "subscriptions.json"
tags_json = settings.BASE_DIR / "data" / "blogroll" / "taggings.json"


def get_feeds():
    subs = sorted(
        json.loads(str(Path(subs_json).read_text())),
        key=lambda i: i["title"].lower(),
    )

    tags = sorted(
        json.loads(str(Path(tags_json).read_text())),
        key=lambda i: i["name"].lower(),
    )

    for sub in subs:
        for tag in tags:
            if tag["feed_id"] == sub["feed_id"]:
                sub["category"] = tag["name"]

    display_subs = [sub for sub in subs if sub.get("category") in ["Blogs", "General"]]

    return sorted(display_subs, key=lambda i: i["category"])


# Create your views here.


class Blogroll(TemplateView):
    template_name = "content.html"

    def get_context_data(self, **kwargs):
        context = super(Blogroll, self).get_context_data(**kwargs)
        context["feeds"] = get_feeds()
        context["page_meta"] = {
            "body_class": "blogroll",
            "title": "Blogroll",
            "desc": "The RSS feeds from where I steal most of the stuff to which I link",
        }
        return context


class BlogrollOPML(TemplateView):
    def get_times(self):
        created = datetime.fromtimestamp(int(Path(subs_json).stat().st_ctime))
        modified = datetime.fromtimestamp(int(Path(subs_json).stat().st_mtime))
        times = {}
        times["created"] = str(created.isoformat("T")) + "-04:00"
        times["modified"] = str(modified.isoformat("T")) + "-04:00"
        return times

    def get_context_data(self, **kwargs):
        context = super(BlogrollOPML, self).get_context_data(**kwargs)
        context["feeds"] = get_feeds()
        context["times"] = self.get_times()
        return context

    def get(self, request):
        response = HttpResponse(
            content_type="text/x-opml",
            headers={
                "Content-Disposition": 'attachment; filename="subscriptions.opml"'
            },
        )

        template = get_template("content/blogroll.opml")
        data = self.get_context_data()

        response.write(template.render(data))

        return response
