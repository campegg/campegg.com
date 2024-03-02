from django.contrib import admin
from content.models import Content


# Register your models here.


class ContentAdmin(admin.ModelAdmin):
    def get_path(self, obj) -> str:
        year = obj.publish_date.strftime("%Y")
        month = obj.publish_date.strftime("%m")
        day = obj.publish_date.strftime("%d")

        slug = obj.content_path

        if obj.content_type in ["note", "post", "photo", "reply", "repost"]:
            return f"/{year}/{month}/{day}/{slug}.html"
        elif obj.content_type == "page":
            return f"/{slug}.html"
        elif obj.content_type == "like":
            return f"/likes/{slug}.html"
        elif obj.content_type == "activity":
            return f"/activities/{slug}.html"
        else:
            return "Path unknown 🤷🏻‍♂️"

    get_path.short_description = "Path"

    list_display = (
        "get_path",
        "publish_date",
    )

    readonly_fields = ("create_date",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "content_type",
                    "content_meta",
                    "content_path",
                )
            },
        ),
        (
            "Publishing",
            {
                "fields": (
                    "content_federate",
                    "allow_outgoing_webmentions",
                    "content_rss_only",
                )
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    "create_date",
                    "publish_date",
                    "update_date",
                )
            },
        ),
    )


admin.site.register(Content, ContentAdmin)
