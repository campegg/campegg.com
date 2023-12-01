from django.db import models
from django.utils import timezone
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import default_storage
from django.template.defaultfilters import slugify
from django.contrib.sites.models import Site
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from mentions.models.mixins import MentionableMixin


from bs4 import BeautifulSoup
from datetime import datetime
from fractions import Fraction
from io import BytesIO
from PIL import Image
import exifread
import httpx
import json
import os
import tempfile
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

    def create_slug(self):
        # only if the slug doesn't exist
        if not self.slug:
            # if title exists, set the type to 'post' and use the first three words of the title for the slug
            if self.title:
                self.post_type = 1
                title_slug = " ".join(self.title.split()[:3])
                return slugify(title_slug)

            # otherwise, let's set the appropriate post type and then generate a slug from what we have...
            else:
                if self.photo:
                    self.post_type = 2
                else:
                    self.post_type = 0

                soup = BeautifulSoup(self.html, "lxml")
                post_text = soup.get_text()
                image_tag = soup.find("img", alt=True)
                alt_text = image_tag["alt"] if image_tag else None

                # if no title but has text, use the first three words of the text
                if post_text:
                    slug_text = " ".join(post_text.split()[:3])
                    return slugify(slug_text)

                # if no text but an image with alt text, use the first three words of the alt text
                elif not post_text and alt_text:
                    alt_slug = " ".join(alt_text.split()[:3])
                    return slugify(alt_slug)

                # if photo_alt_text exists, use it for the slug
                elif self.photo_alt_text:
                    photo_alt_slug = " ".join(self.photo_alt_text.split()[:3])
                    return slugify(photo_alt_slug)

                # if no title, text, image with alt text, or photo alt text, create a time-based slug
                else:
                    time_format = "%H%M"
                    time_slug = datetime.strftime(self.publish_date, time_format)
                    return f"post-{time_slug}"
        else:
            return self.slug

    def handle_publishing(self):
        # get the current time without microseconds
        savetime = timezone.now().replace(microsecond=0)

        # set create_date for new posts
        if self.pk is None:
            self.create_date = savetime

        # handle scheduled posts
        if self.publish_date is not None and self.publish_date > savetime:
            self.status = 1
            return

        # handle new posts that are published immediately
        if self.pk is None and self.status == 1:
            self.publish_date = savetime
            return

        # handle updates to existing posts
        if self.pk is not None:
            if self.status == 1:
                # update publish_date for newly published posts, update_date for others
                self.publish_date = self.publish_date if self.publish_date else savetime
                self.update_date = savetime
            else:
                # reset publish_date and update_date for unpublished posts
                self.publish_date = None
                self.update_date = None

    def archive_post(self):
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

    def handle_photo_upload(self):
        if self.photo:
            # Step 1: Save the uploaded photo to a temp file
            with tempfile.NamedTemporaryFile(delete=False) as temp:
                for chunk in self.photo.chunks():
                    temp.write(chunk)
                temp_path = temp.name  # Save the path to the temp file

            # Step 2: Extract the EXIF data and populate the img_data dict using exifread
            with open(temp_path, "rb") as f:
                tags = exifread.process_file(f, details=False)

            img_data = {}
            # Populate img_data with EXIF information
            img_data["make"] = str(tags.get("Image Make", None))
            img_data["model"] = str(tags.get("Image Model", None))
            img_data["orientation"] = str(tags.get("Image Orientation", None))
            img_data["date"] = str(tags.get("Image DateTime", None))
            img_data["fstop"] = float(Fraction(str(tags.get("EXIF FNumber", None))))
            img_data["exp"] = str(tags.get("EXIF ExposureProgram", None))
            img_data["iso"] = str(tags.get("EXIF ISOSpeedRatings", None))
            img_data["focal"] = float(Fraction(str(tags.get("EXIF FocalLength", None))))

            # GPS Data
            gps_latitude = tags.get("GPS GPSLatitude")
            gps_latitude_ref = tags.get("GPS GPSLatitudeRef")
            gps_longitude = tags.get("GPS GPSLongitude")
            gps_longitude_ref = tags.get("GPS GPSLongitudeRef")

            print(f"GPS Lat: {gps_latitude}")
            print(f"GPS Lat Ref: {gps_latitude_ref}")
            print(f"GPS Lon: {gps_longitude}")
            print(f"GPS Lon Ref: {gps_longitude_ref}")

            if (
                gps_latitude
                and gps_latitude_ref
                and gps_longitude
                and gps_longitude_ref
            ):
                lat_value = [float(x.num) / float(x.den) for x in gps_latitude.values]
                lon_value = [float(x.num) / float(x.den) for x in gps_longitude.values]
                coordinates = get_decimal_coordinates(
                    lat_value, gps_latitude_ref, lon_value, gps_longitude_ref
                )
                img_data["lat"] = coordinates[0]
                img_data["lon"] = coordinates[1]
            else:
                img_data["lat"] = None
                img_data["lon"] = None

            print(f"Coords: {coordinates}")

            # Step 3: Resize, rename and save the temp file to the media directory using Pillow
            img = Image.open(temp_path)
            img.thumbnail((2048, 2048), Image.Resampling.LANCZOS)
            photo_filename = self.create_date.strftime("%Y%m%d%H%M%S")
            output = BytesIO()
            img.save(output, format="JPEG", quality=95)
            output.seek(0)
            self.photo = InMemoryUploadedFile(
                output,
                "ImageField",
                f"{photo_filename}.jpg",
                "image/jpeg",
                output.tell(),
                None,
            )

            # Step 4: Delete the temp file
            os.unlink(temp_path)

            # Save the img_data as JSON
            self.photo_meta = json.dumps(img_data)
        else:
            pass

    def save(self, *args, **kwargs):
        self.html = utilities.render_html(self.text)
        self.handle_publishing()
        if self.pk is None:
            self.handle_photo_upload()
        self.slug = self.create_slug()
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


@receiver(post_save, sender=Post)
def post_saved(sender, instance, **kwargs):
    if instance.status == 1 and instance.send_to_archive:
        instance.archive_post()
