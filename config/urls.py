"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # ---------- main patterns ----------#
    path("django/", admin.site.urls),
    path("webmentions/", include("mentions.urls")),
    path("", include("admin.urls")),
    path("", include("content.urls")),
    # ---------- simple redirects ----------#
    path("about/", RedirectView.as_view(url="/about.html")),
    path("about/changelog/", RedirectView.as_view(url="/about/changelog.html")),
    path("feed/json/", RedirectView.as_view(pattern_name="feed_json", permanent=True)),
    path("feed/", RedirectView.as_view(pattern_name="feed_atom", permanent=True)),
    path("sitemap/", RedirectView.as_view(url="/sitemap.xml")),
    path(
        "github/",
        RedirectView.as_view(url="https://github.com/campegg", permanent=True),
    ),
    path(
        "linkedin/",
        RedirectView.as_view(url="https://linkedin.com/in/campegg", permanent=True),
    ),
    path(
        "mastodon/",
        RedirectView.as_view(url="https://indieweb.social/@campegg", permanent=True),
    ),
    path(
        "strava/",
        RedirectView.as_view(
            url="https://www.strava.com/athletes/273720", permanent=True
        ),
    ),
    path(
        "twitter/",
        RedirectView.as_view(url="/2023/07/31/its-done-i.html", permanent=True),
    ),
    # ---------- wildcard redirects ----------#
    re_path(r"^activitypub/.*$", RedirectView.as_view(pattern_name="home")),
    re_path(r"^bookmarks/.*$", RedirectView.as_view(pattern_name="home")),
    re_path(r"^books/.*$", RedirectView.as_view(pattern_name="home")),
    re_path(
        r"^feeds/.*$", RedirectView.as_view(pattern_name="feed_atom", permanent=True)
    ),
    re_path(r"^notes/.*$", RedirectView.as_view(pattern_name="home")),
    re_path(r"^photos/.*$", RedirectView.as_view(pattern_name="home")),
    re_path(r"^posts/.*$", RedirectView.as_view(pattern_name="home")),
    re_path(r"^reading/.*$", RedirectView.as_view(pattern_name="home")),
    re_path(r"^retired/.*$", RedirectView.as_view(pattern_name="home")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
