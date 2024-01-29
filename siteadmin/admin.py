from django.contrib import admin


from siteadmin.models import Reaction


# Register your models here.


# ---------- reactions ----------#
class ReactionAdmin(admin.ModelAdmin):
    list_display = (
        "reaction_type",
        "react_to_url",
        "create_date",
    )

    exclude = (
        "allow_outgoing_webmentions",
        "create_date",
    )

    fieldsets = (
        (
            "",
            {
                "fields": (
                    "reaction_type",
                    "react_to_url",
                )
            },
        ),
    )


admin.site.register(Reaction, ReactionAdmin)
