from django.views.generic import ListView
from django.views.generic.dates import YearArchiveView, MonthArchiveView, DayArchiveView
from django.db.models import Q
from django.utils import timezone
from django.utils.dateformat import DateFormat
from bs4 import BeautifulSoup
from datetime import datetime
from num2words import num2words
import re


from content.models import Content


class BaseArchiveView:
    model = Content
    date_field = "publish_date"
    context_object_name = "items"
    make_object_list = True
    allow_future = False
    template_name = "content.html"

    def get_queryset(self):
        return Content.objects.filter(
            Q(content_type="note")
            | Q(content_type="post")
            | Q(content_type="photo")
            | Q(content_type="reply")
            | Q(content_type="repost"),
            publish_date__lte=timezone.now(),
            content_rss_only=False,
        ).order_by("-publish_date")

    def get_archive_text(self, object):
        if object.content_type == "repost" and object.content_meta.get("json"):
            html_content = object.content_meta.get("json").get("content", "")
        else:
            html_content = object.content_meta.get("html", "")

        soup = BeautifulSoup(html_content, "lxml")
        content_text = soup.get_text()

        if content_text:
            archive_text = " ".join(content_text.split()[:20])
            archive_text = re.sub(r"{{.*?}}", "", archive_text).strip()
            if archive_text and archive_text[-1] not in [".", "!", "?", "…"]:
                if archive_text[-1] in [":", ";", ",", " "]:
                    archive_text = archive_text[:-1]
                archive_text += "…"
            return archive_text
        else:
            image_tag = soup.find("img", alt=True)
            alt_text = image_tag["alt"] if image_tag else "Image post"
            return alt_text

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = context.get("items", [])

        for item in items:
            item.archive_text = self.get_archive_text(item)

        context.update(
            {
                "post_count": len(items),
                "post_words": num2words(len(items)),
            }
        )

        return context


class Archive(BaseArchiveView, ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post_words = context["post_words"]

        context["page_meta"] = {
            "body_class": "archive",
            "title": f"Every one of the {post_words} posts I’ve ever&nbsp;posted",
            "desc": "All the things!",
        }

        return context


class YearArchive(BaseArchiveView, YearArchiveView):
    make_object_list = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post_count = context["post_count"]
        post_words = context["post_words"]

        year = self.get_year()
        current_year = datetime.now().year

        in_progress = " (so far)" if int(year) == current_year else ""

        context["page_meta"] = {
            "body_class": "archive",
            "title": f"{'All' if post_count > 1 else 'The'} {post_words} {'posts' if post_count != 1 else 'post'} I{'’ve' if in_progress else ''} posted in {year}{in_progress}",
            "desc": "All the things!",
        }

        return context


class MonthArchive(BaseArchiveView, MonthArchiveView):
    month_format = "%m"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post_count = context["post_count"]
        post_words = context["post_words"]

        year = self.get_year()
        current_year = datetime.now().year
        month = self.get_month()
        current_month = datetime.now().month
        date = datetime(year=int(year), month=int(month), day=1)
        month_name = DateFormat(date).format("F")

        in_progress = (
            " (so far)"
            if int(year) == current_year and int(month) == current_month
            else ""
        )

        context["page_meta"] = {
            "body_class": "archive",
            "title": f"{'All' if post_count > 1 else 'The'} {post_words} {'posts' if post_count != 1 else 'post'} I{'’ve' if in_progress else ''} posted in {month_name}, {year}{in_progress}",
            "desc": "All the things!",
        }

        return context


class DayArchive(BaseArchiveView, DayArchiveView):
    month_format = "%m"
    day_format = "%d"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post_count = context["post_count"]
        post_words = context["post_words"]

        year = self.get_year()
        current_year = datetime.now().year
        month = self.get_month()
        current_month = datetime.now().month
        day = self.get_day()
        current_day = datetime.now().day
        date = DateFormat(
            datetime(year=int(year), month=int(month), day=int(day))
        ).format("F j, Y")

        in_progress = (
            " (so far)"
            if int(year) == current_year
            and int(month) == current_month
            and int(day) == current_day
            else ""
        )

        context["page_meta"] = {
            "body_class": "archive",
            "title": f"{'All' if post_count > 1 else 'The'} {post_words} {'posts' if post_count != 1 else 'post'} I{'’ve' if in_progress else ''} posted on {date}{in_progress}",
            "desc": "All the things!",
        }

        return context
