# content/urls.py

from django.urls import path
from django.contrib.sitemaps.views import sitemap
from mentions.helpers import mentions_path

from content.models import Content
from content.views import (
    Activities,
    Activity,
    Archive,
    YearArchive,
    MonthArchive,
    DayArchive,
    Blogroll,
    BlogrollOPML,
    CoreContent,
    Home,
    Like,
    LikeList,
    Page,
    Reaction,
)
from content.feeds import ContentFeed
from content.sitemaps import sitemaps


urlpatterns = [
    # ---------- content pages ----------#
    path("", Home.as_view(), name="home"),
    path("archive.html", Archive.as_view(), name="archive"),
    path("<int:year>/", YearArchive.as_view(), name="archive_year"),
    path("<int:year>/<int:month>/", MonthArchive.as_view(), name="archive_month"),
    path(
        "<int:year>/<int:month>/<int:day>/",
        DayArchive.as_view(),
        name="archive_day",
    ),
    mentions_path(
        "<int:year>/<int:month>/<int:day>/<path:slug>.html",
        CoreContent.as_view(),
        name="content",
        model_class=Content,
        model_filter_map={
            "year": "publish_date__year",
            "month": "publish_date__month",
            "day": "publish_date__day",
            "slug": "content_path",
        },
    ),
    path("activities.html", Activities.as_view(), name="activities"),
    path("activities/<path:slug>.html", Activity.as_view(), name="activity"),
    path("likes.html", LikeList.as_view(), name="likelist"),
    path("likes/<path:slug>.html", Like.as_view(), name="like"),
    path("blogroll.html", Blogroll.as_view(), name="blogroll"),
    path("blogroll/subscriptions.opml", BlogrollOPML.as_view(), name="blogroll_opml"),
    path("reactions.html", Reaction.as_view(), name="reactions"),
    path("<path:slug>.html", Page.as_view(), name="page"),
    path("feed.xml", ContentFeed(), name="feed_atom"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
