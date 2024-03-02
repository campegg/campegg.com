# content/urls.py

from django.urls import path


from content.views import (
    Activities,
    Activity,
    Archive,
    Blogroll,
    BlogrollOPML,
    Dispatcher,
    Home,
    Like,
    Page,
    Reaction,
)
from content.feeds import ContentFeed


urlpatterns = [
    # ---------- content pages ----------#
    path("", Home.as_view(), name="home"),
    path(
        "<int:year>/<int:month>/<int:day>/<path:slug>.html",
        Dispatcher.as_view(),
        name="dispatcher",
    ),
    path("activities.html", Activities.as_view(), name="activities"),
    path("activities/<path:slug>.html", Activity.as_view(), name="activity"),
    path("likes/<path:slug>.html", Like.as_view(), name="like"),
    path("archive.html", Archive.as_view(), name="archive"),
    path("blogroll.html", Blogroll.as_view(), name="blogroll"),
    path("blogroll/subscriptions.opml", BlogrollOPML.as_view(), name="blogroll_opml"),
    path("reactions.html", Reaction.as_view(), name="reactions"),
    path("<path:slug>.html", Page.as_view(), name="page"),
    path("feed.xml", ContentFeed(), name="feed_atom"),
]
