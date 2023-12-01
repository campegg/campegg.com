from django.contrib import admin
from content.models import Page


# Register your models here.


class PageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "full_path",
        "update_date",
    )

    exclude = (
        "html",
        "ranking",
    )

    readonly_fields = ("update_date", "full_path")

    fieldsets = (
        (
            "",
            {
                "fields": (
                    "title",
                    "text",
                    "description",
                )
            },
        ),
        (
            "Page Meta",
            {
                "fields": (
                    "parent",
                    "full_path",
                    "update_date",
                    "show_in_nav",
                )
            },
        ),
    )


admin.site.register(Page, PageAdmin)
