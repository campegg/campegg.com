from django.db import models
from django.utils import timezone
from django.core.files.storage import default_storage
from django.template.defaultfilters import slugify
from django.contrib.sites.models import Site
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from mentions.models.mixins import MentionableMixin


from bs4 import BeautifulSoup
from datetime import datetime

import httpx
import utilities


def get_decimal_coordinates(lat_values, lat_ref, lon_values, lon_ref):
    latitude = lat_values[0] + lat_values[1] / 60.0 + lat_values[2] / 3600.0
    longitude = lon_values[0] + lon_values[1] / 60.0 + lon_values[2] / 3600.0

    if str(lat_ref) == "S":
        latitude = -latitude
    if str(lon_ref) == "W":
        longitude = -longitude

    return [latitude, longitude]


# Create your models here.


class Post(MentionableMixin, models.Model):
    draft = 0
    published = 1
    status_choices = [(draft, "Draft"), (published, "Published")]

    note = 0
    post = 1
    photo = 2
    type_choices = [(note, "Note"), (post, "Post"), (photo, "Photo")]

    id = models.AutoField(primary_key=True, unique=True, verbose_name="Post ID")
    create_date = models.DateTimeField(blank=True, null=True, verbose_name="Created")
    publish_date = models.DateTimeField(blank=True, null=True, verbose_name="Published")
    update_date = models.DateTimeField(blank=True, null=True, verbose_name="Updated")
    slug = models.CharField(max_length=32, null=False, verbose_name="Slug")
    post_type = models.IntegerField(
        choices=type_choices, default=note, verbose_name="Post type"
    )
    status = models.IntegerField(
        choices=status_choices, default=published, verbose_name="Post status"
    )
    send_to_fediverse = models.BooleanField(default=True, verbose_name="Federate post")
    send_to_archive = models.BooleanField(default=True, verbose_name="Archive post")
    rss_only = models.BooleanField(default=False, verbose_name="RSS only")
    title = models.CharField(
        max_length=500, blank=True, null=True, verbose_name="Title"
    )
    text = models.TextField(null=False, verbose_name="Text")
    html = models.TextField(blank=True, null=True, verbose_name="HTML")
    photo = models.ImageField(
        upload_to="photos/", blank=True, null=True, verbose_name="Photo"
    )
    photo_alt_text = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Alt text"
    )
    photo_meta = models.TextField(blank=True, null=True, verbose_name="EXIF data")
    ranking = models.FloatField(default=0.0, editable=False)

    def save(self, *args, **kwargs):
        # render the post's html and add/remove bridgy links if required
        bridgy_links = '\n</div><!-- bridgy links --><div class="ap-bridgy-link"><a class="u-bridgy-fed" href="https://fed.brid.gy/" hidden="from-humans"></a><!-- /bridgy links -->'
        self.html = self.html if self.html else utilities.render_html(self.text)
        if self.send_to_fediverse and bridgy_links not in self.html:
            self.html += bridgy_links
        else:
            self.html = self.html.replace(bridgy_links, "")

        # handle published vs draft posts and scheduled publishing
        savetime = timezone.now().replace(microsecond=0)
        if self.status:
            if self.pk:
                self.update_date = savetime
                if not self.publish_date:
                    self.publish_date = savetime
            else:
                self.create_date = savetime
                if not self.publish_date or self.publish_date <= savetime:
                    self.publish_date = savetime
        else:
            if self.pk:
                self.update_date = savetime
            else:
                self.create_date = savetime

        # create a slug if one doesn't exist
        if not self.slug:
            # if title exists, set the type to 'post' and use the first three words of the title for the slug
            if self.title:
                self.post_type = 1
                self.slug = slugify(" ".join(self.title.split()[:3]))

            # otherwise, let's set the appropriate post type and then generate a slug from what we have...
            else:
                self.post_type = 0

                soup = BeautifulSoup(self.html, "lxml")
                post_text = soup.get_text()

                # if no title but has text, use the first three words of the text
                if post_text:
                    self.slug = slugify(" ".join(post_text.split()[:3]))

                # if none of the above exist, create a time-based slug
                else:
                    time_format = "%H%M"
                    time_slug = datetime.strftime(self.publish_date, time_format)
                    self.slug = f"post-{time_slug}"

        # archive the post if required
        if self.send_to_archive:
            current_site = Site.objects.get_current()
            post_url = f"https://{current_site.domain}{self.get_absolute_url()}"
            archive_url = f"https://web.archive.org/save/{post_url}"
            headers = {
                "User-Agent": f"Mozilla/5.0 (Ubuntu; Linux x86_64; {current_site.domain})"
            }

            try:
                with httpx.Client(headers=headers, timeout=20.0) as client:
                    response = client.get(archive_url)
                if response.status_code == 200:
                    print(f"Successfully archived {post_url}")
                else:
                    print(
                        f"Failed to archive {post_url}. Status code: {response.status_code}, Response: {response.text}"
                    )
            except httpx.RequestError as e:
                print(f"An error occurred while requesting {e.request.url!r}.")

        super(Post, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.photo:
            if default_storage.exists(self.photo.name):
                default_storage.delete(self.photo.name)
        super(Post, self).delete(*args, **kwargs)

    def get_content_html(self) -> str:
        return self.html

    def get_absolute_url(self) -> str:
        return reverse(
            "post_detail",
            kwargs={
                "year": self.publish_date.year,
                "month": self.publish_date.strftime("%m"),
                "day": self.publish_date.strftime("%d"),
                "slug": self.slug,
            },
        )

    def __str__(self):
        if self.title:
            return self.title
        else:
            soup = BeautifulSoup(self.html, "lxml")
            full_text = soup.get_text().strip()
            if full_text:
                words = full_text.split()[:3]
                display_title = " ".join(words)
            else:
                image_tag = soup.find("img", alt=True)
                if image_tag:
                    alt_text = image_tag["alt"]
                    alt_words = alt_text.split()[:3]
                    display_title = " ".join(alt_words)
                else:
                    display_title = "[Untitled]"
            if display_title[-1] in [".", "!", "?", "…"]:
                pass
            elif display_title[-1] in [":", ";", ",", " "]:
                display_title = display_title[:-1] + "…"
            else:
                display_title += "…"
            return display_title

    class Meta:
        db_table = "cp_posts"
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-create_date"]
