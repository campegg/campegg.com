from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.template.defaultfilters import slugify
from mentions.models.mixins import MentionableMixin
from bs4 import BeautifulSoup
from datetime import datetime
import pytz


# Create your models here.


class Content(MentionableMixin, models.Model):
    CONTENT_TYPES = (
        ("note", "Note"),
        ("post", "Post"),
        ("photo", "Photo"),
        ("page", "Page"),
        ("like", "Like"),
        ("reply", "Reply"),
        ("repost", "Repost"),
        ("activity", "Activity"),
    )

    id = models.AutoField(primary_key=True, unique=True, verbose_name="Content ID")
    content_type = models.CharField(
        max_length=50, choices=CONTENT_TYPES, verbose_name="Content type"
    )
    content_path = models.CharField(
        null=True, blank=True, max_length=512, verbose_name="Content path"
    )
    content_meta = models.JSONField(default=dict, verbose_name="Content meta")
    content_federate = models.BooleanField(default=True, verbose_name="Federate")
    content_rss_only = models.BooleanField(default=False, verbose_name="RSS only")
    create_date = models.DateTimeField(
        null=True, blank=True, verbose_name="Create date"
    )
    publish_date = models.DateTimeField(
        null=True, blank=True, verbose_name="Publish date"
    )
    update_date = models.DateTimeField(
        null=True, blank=True, verbose_name="Update date"
    )
    ranking = models.FloatField(default=0.0, editable=False, verbose_name="Search rank")

    def save(self, *args, **kwargs):
        # handle all the dates
        local_tz = pytz.timezone(settings.TIME_ZONE)
        savetime = timezone.now().astimezone(local_tz).replace(microsecond=0)
        if self.pk:
            self.update_date = savetime
            if not self.publish_date:
                self.publish_date = savetime
        else:
            self.create_date = savetime
            if not self.publish_date or self.publish_date <= savetime:
                self.publish_date = savetime

            if self.content_type == "page":
                self.update_date = savetime

        # build the slug
        if not self.content_path:
            if self.content_type in ["note", "post", "photo", "reply", "repost"]:
                # if title exists, use the first three words of the title for the slug
                title = self.content_meta.get("title", None)
                if title:
                    self.content_path = slugify(" ".join(title.split()[:3]))

                # otherwise, let's set the appropriate post type and then generate a slug from what we have...
                else:
                    if self.content_meta.get("html"):
                        soup = BeautifulSoup(self.content_meta["html"], "lxml")
                    else:
                        soup = BeautifulSoup(
                            self.content_meta["json"]["content"], "lxml"
                        )
                    post_text = soup.get_text()
                    image_alt = [img for img in soup.find_all("img") if img.get("alt")]

                    # if no title try to use the first three words of the text
                    if post_text:
                        self.content_path = slugify(" ".join(post_text.split()[:3]))

                    # if that doesn't exist, try using image alt text
                    elif image_alt:
                        alt_text = image_alt[0].get("alt")
                        self.content_path = slugify(" ".join(alt_text.split()[:3]))

                    # and if none of the above exist, create a time-based slug
                    else:
                        time_format = "%H%M"
                        time_slug = datetime.strftime(self.publish_date, time_format)
                        self.content_path = f"post-{time_slug}"
            elif self.content_type == "page":
                page_slug = slugify(self.content_meta["title"])
                self.content_path = {page_slug}
            elif self.content_type == "like":
                self.content_path = f'like-{self.content_meta["json"]["account"]["acct"]}-{self.content_meta["json"]["id"]}'
            elif self.content_type == "activity":
                self.content_path = f'{self.content_meta["id"]}'
            else:
                self.content_path = None

        super(Content, self).save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        year = self.publish_date.strftime("%Y")
        month = self.publish_date.strftime("%m")
        day = self.publish_date.strftime("%d")

        slug = self.content_path

        if self.content_type in ["note", "post", "photo", "reply", "repost"]:
            return f"/{year}/{month}/{day}/{slug}.html"
        elif self.content_type == "page":
            return f"/{slug}.html"
        elif self.content_type == "like":
            return f"/likes/{slug}.html"
        elif self.content_type == "activity":
            return f"/activities/{slug}.html"
        else:
            return reverse("home")

    def get_content_html(self) -> str:
        bridgy_link = '<div class="ap-bridgy-link"><a class="u-bridgy-fed" href="https://fed.brid.gy/" hidden="from-humans"></a></div>'

        if self.content_meta.get("json"):
            item_html = (
                f'<div class="e-content">{self.content_meta["json"]["content"]}</div>'
            )
        elif self.content_meta.get("html"):
            item_html = f'<div class="e-content">{self.content_meta.get("html")}</div>'
        else:
            item_html = None

        if self.content_federate:
            return item_html + bridgy_link
        else:
            return item_html

    def __str__(self):
        return f"{self.get_content_type_display()} - {self.id}"

    class Meta:
        db_table = "cp_content"
        verbose_name = "Item"
        verbose_name_plural = "Items"
        ordering = ["-create_date"]
