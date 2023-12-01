from django.views.generic import ListView
from django.db.models import Q
from datetime import datetime
from calendar import month_name
from bs4 import BeautifulSoup
import re


from content.models import Post


# Create your views here.


class Archive(ListView):
    context_object_name = "posts"
    model = Post
    paginate_orphans = 2
    template_name = "content.html"

    def get_queryset(self):
        queryset = (
            Post.objects.all()
            .filter(
                publish_date__lte=datetime.now().replace(microsecond=0),
                status__exact=1,
                rss_only__exact=0,
            )
            .order_by("-publish_date")
        )

        return queryset

    def get_archive_text(self, post):
        soup = BeautifulSoup(post.html, "lxml")
        post_text = soup.get_text()

        if post_text:
            archive_text = " ".join(post_text.split()[:20])
            archive_text = re.sub(r"{{.*?}}", "", archive_text).strip()
            if archive_text[-1] not in [".", "!", "?", "…"]:
                if archive_text[-1] in [":", ";", ",", " "]:
                    archive_text = archive_text[:-1]
                archive_text += "…"
            return archive_text
        else:
            image_tag = soup.find("img", alt=True)
            alt_text = image_tag["alt"] if image_tag else "Image post"
            return alt_text

    def get_context_data(self, **kwargs):
        context = super(Archive, self).get_context_data(**kwargs)
        post_count = len(context["posts"])
        for post in context["posts"]:
            post.archive_text = self.get_archive_text(post)

        context["page_meta"] = {
            "body_class": "archive",
            "title": f"Every one of the {post_count} posts I’ve posted",
            "desc": "All the things!",
        }

        return context


class YearArchive(Archive):
    def get_queryset(self):
        year = self.kwargs["year"]
        return super().get_queryset().filter(Q(publish_date__year=year))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs["year"]
        post_count = len(context["posts"])
        current_year = datetime.now().year
        current_text = " (…so far)" if year == current_year else ""

        context["page_meta"] = {
            "body_class": "archive",
            "title": f"The only post from {year}{current_text}"
            if post_count == 1
            else f"All {post_count} posts from {year}{current_text}",
            "desc": f"All the posts from {year}",
        }

        return context


class MonthArchive(Archive):
    def get_queryset(self):
        year = self.kwargs["year"]
        month = self.kwargs["month"]
        return (
            super()
            .get_queryset()
            .filter(Q(publish_date__year=year) & Q(publish_date__month=month))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs["year"]
        month = self.kwargs["month"]
        month_name_str = month_name[month]
        post_count = len(context["posts"])
        current_year, current_month = datetime.now().year, datetime.now().month
        current_text = (
            " (…so far)" if year == current_year and month == current_month else ""
        )

        context["page_meta"] = {
            "body_class": "archive",
            "title": f"The only post from {month_name_str}, {year}{current_text}"
            if post_count == 1
            else f"All {post_count} posts from {month_name_str}, {year}{current_text}",
            "desc": f"All the posts from {month_name_str}, {year}",
        }

        return context


class DayArchive(Archive):
    def get_queryset(self):
        year = self.kwargs["year"]
        month = self.kwargs["month"]
        day = self.kwargs["day"]
        return (
            super()
            .get_queryset()
            .filter(
                Q(publish_date__year=year)
                & Q(publish_date__month=month)
                & Q(publish_date__day=day)
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs["year"]
        month = self.kwargs["month"]
        day = self.kwargs["day"]
        month_name_str = month_name[month]
        post_count = len(context["posts"])

        day_date = datetime(year, month, day)
        day_name = day_date.strftime("%A")

        current_year, current_month, current_day = (
            datetime.now().year,
            datetime.now().month,
            datetime.now().day,
        )
        current_text = (
            " (…so far)"
            if year == current_year and month == current_month and day == current_day
            else ""
        )

        context["page_meta"] = {
            "body_class": "archive",
            "title": f"The only post from {day_name} {month_name_str} {day}, {year}{current_text}"
            if post_count == 1
            else f"All {post_count} posts from {day_name} {month_name_str} {day}, {year}{current_text}",
            "desc": f"All the posts from {day_name} {month_name_str} {day}, {year}",
        }

        return context
