# content/urls.py

from django.urls import path
from django.contrib.sitemaps.views import sitemap
from mentions.helpers import mentions_path


from content.models import Post
from content.views import (
    Home,
    Archive,
    ActivityIndex,
    ActivityDetail,
    Blogroll,
    BlogrollOPML,
    PostDetail,
    PageDetail,
    SearchView,
    YearArchive,
    MonthArchive,
    DayArchive,
)
from content.feeds import PostFeed, JsonFeed
from content.sitemaps import ArchiveSitemap, PageSitemap, PostSitemap, StaticViewSitemap

sitemaps = {
    "static": StaticViewSitemap,
    "pages": PageSitemap,
    "posts": PostSitemap,
    "archives": ArchiveSitemap,
}


urlpatterns = [
    # ---------- content pages ----------#
    path("", Home.as_view(), name="home"),
    path("page/<int:page>/", Home.as_view(), name="home_paginated"),
    path("archive.html", Archive.as_view(), name="archive"),
    path("<int:year>/", YearArchive.as_view(), name="archive_year"),
    path("<int:year>/<int:month>/", MonthArchive.as_view(), name="archive_month"),
    path("<int:year>/<int:month>/<int:day>/", DayArchive.as_view(), name="archive_day"),
    mentions_path(
        "<int:year>/<int:month>/<int:day>/<slug:slug>.html",
        PostDetail.as_view(),
        name="post_detail",
        model_class=Post,
        model_filter_map={
            "year": "publish_date__year",
            "month": "publish_date__month",
            "day": "publish_date__day",
            "slug": "slug",
        },
    ),
    path("activities/", ActivityIndex.as_view(), name="activity_index"),
    path(
        "activities/page/<int:page>/",
        ActivityIndex.as_view(),
        name="activity_index",
    ),
    path("activities/<int:id>.html", ActivityDetail.as_view(), name="activity_detail"),
    path("blogroll.html", Blogroll.as_view(), name="blogroll"),
    path("blogroll/subscriptions.opml", BlogrollOPML.as_view(), name="blogroll_opml"),
    path("search.html", SearchView.as_view(), name="search"),
    path("<path:path>.html", PageDetail.as_view(), name="page_detail"),
    path("feed.xml", PostFeed(), name="feed_atom"),
    path("feed.json", JsonFeed.as_view(), name="feed_json"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="sitemap",
    ),
]
