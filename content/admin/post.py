from django.contrib import admin
from bs4 import BeautifulSoup


from content.models import Post


# Register your models here.


class PostAdmin(admin.ModelAdmin):
    def display_title(self, obj):
        if obj.title:
            display_title = obj.title
        else:
            soup = BeautifulSoup(obj.html, "lxml")
            full_text = soup.get_text().strip()

            if full_text:
                words = full_text.split()[:3]
                display_title = " ".join(words)
            else:
                # Check for image alt text
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

    display_title.short_description = "Title"

    list_display = (
        "display_title",
        "post_type",
        "status",
        "create_date",
        "publish_date",
    )

    exclude = (
        "html",
        "ranking",
    )

    readonly_fields = (
        "update_date",
        "photo_meta",
    )

    fieldsets = (
        (
            "",
            {
                "fields": (
                    "post_type",
                    "title",
                    "text",
                )
            },
        ),
        (
            "Photo",
            {
                "fields": (
                    "photo",
                    "photo_alt_text",
                    "photo_meta",
                )
            },
        ),
        (
            "Post Meta",
            {
                "fields": (
                    "status",
                    "create_date",
                    "publish_date",
                    "update_date",
                    "send_to_fediverse",
                    "send_to_archive",
                    "allow_outgoing_webmentions",
                    "rss_only",
                )
            },
        ),
    )


admin.site.register(Post, PostAdmin)
