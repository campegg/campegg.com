from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from datetime import datetime, timedelta


from content.models import Content


class PostSitemap(Sitemap):
    pass


class PageSitemap(Sitemap):
    pass


class StaticViewSitemap(Sitemap):
    pass


class ArchiveSitemap(Sitemap):
    pass
