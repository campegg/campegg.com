from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from datetime import datetime, timedelta


from content.models import Post, Page


class PostSitemap(Sitemap):
    def items(self):
        return Post.objects.filter(
            publish_date__lte=datetime.now().replace(microsecond=0),
            status__exact=1,
            rss_only__exact=0,
        ).order_by("-publish_date")

    def location(self, obj):
        return reverse(
            "post_detail",
            args=[
                obj.publish_date.year,
                obj.publish_date.strftime("%m"),
                obj.publish_date.strftime("%d"),
                obj.slug,
            ],
        )

    def lastmod(self, obj):
        return obj.update_date if obj.update_date is not None else obj.publish_date

    def changefreq(self, obj):
        now = datetime.now()
        delta = now - obj.publish_date

        if delta <= timedelta(days=7):
            return "daily"
        elif timedelta(days=7) < delta <= timedelta(days=30):
            return "weekly"
        elif timedelta(days=30) < delta <= timedelta(days=365):
            return "monthly"
        else:
            return "yearly"

    def priority(self, obj):
        return 0.75


class PageSitemap(Sitemap):
    def items(self):
        return Page.objects.all()

    def location(self, obj):
        return reverse("page_detail", kwargs={"path": obj.full_path})

    def lastmod(self, obj):
        return obj.update_date if obj.update_date is not None else obj.publish_date

    def changefreq(self, obj):
        return "weekly"

    def priority(self, obj):
        return 0.5


class StaticViewSitemap(Sitemap):
    def items(self):
        return ["home", "archive"]

    def location(self, obj):
        return reverse(obj)

    def lastmod(self, obj):
        latest_post = (
            Post.objects.filter(
                publish_date__lte=datetime.now().replace(microsecond=0),
                status__exact=1,
                rss_only__exact=0,
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


class ArchiveSitemap(Sitemap):
    def items(self):
        dates = (
            Post.objects.filter(
                publish_date__lte=datetime.now().replace(microsecond=0),
                status__exact=1,
                rss_only__exact=0,
            )
            .dates("publish_date", "day")
            .order_by("-publish_date")
        )

        archive_data = []
        seen_years = set()
        seen_months = set()
        seen_days = set()

        for date in dates:
            year = date.year
            month = date.month
            day = date.day

            # yearly archive
            if year not in seen_years:
                archive_data.append({"type": "year", "year": year})
                seen_years.add(year)

            # monthly archive
            month_key = f"{year}-{month}"
            if month_key not in seen_months:
                archive_data.append({"type": "month", "year": year, "month": month})
                seen_months.add(month_key)

            # daily archive
            day_key = f"{year}-{month}-{day}"
            if day_key not in seen_days:
                archive_data.append(
                    {"type": "day", "year": year, "month": month, "day": day}
                )
                seen_days.add(day_key)

        return archive_data

    def location(self, obj):
        if obj["type"] == "year":
            return reverse("archive_year", kwargs={"year": obj["year"]})
        elif obj["type"] == "month":
            return reverse(
                "archive_month",
                kwargs={"year": obj["year"], "month": f"{obj['month']:02}"},
            )
        elif obj["type"] == "day":
            return reverse(
                "archive_day",
                kwargs={
                    "year": obj["year"],
                    "month": f"{obj['month']:02}",
                    "day": f"{obj['day']:02}",
                },
            )

    def changefreq(self, obj):
        current_year = datetime.now().year
        current_month = datetime.now().month

        archive_year = obj.get("year", None)
        archive_month = obj.get("month", None)

        if current_year == archive_year:
            if archive_month is not None:
                if current_month == archive_month:
                    return "daily"
                elif current_month > archive_month:
                    return "monthly"
            else:
                return "daily"
        else:
            return "yearly"

    def priority(self, obj):
        return 0.25
