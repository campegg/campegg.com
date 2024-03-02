from django.views.generic import ListView
from django.utils import timezone
from django.db.models import Count, OuterRef, Subquery, IntegerField

from content.models import Content
from mentions.models import Webmention


class Home(ListView):
    context_object_name = "contents"
    model = Content
    paginate_by = 20
    paginate_orphans = 2
    template_name = "content.html"

    def get_queryset(self):
        # Filter Content objects by the specified types
        content_types = ["note", "post", "photo", "reply", "repost"]
        contents_filtered = Content.objects.filter(content_type__in=content_types)

        mentions_count_subquery = Subquery(
            Webmention.objects.filter(object_id=OuterRef("id"), approved=True)
            .order_by()
            .values("object_id")
            .annotate(cnt=Count("id"))
            .values("cnt")[:1],
            output_field=IntegerField(),
        )

        queryset = (
            contents_filtered.annotate(mention_count=mentions_count_subquery)
            .filter(
                publish_date__lte=timezone.now(),
                content_rss_only=False,
            )
            .order_by("-publish_date")
        )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contents_with_template_path = []

        for item in context["contents"]:
            item.template_path = f"content/{item.content_type}.html"
            contents_with_template_path.append(item)
        context["contents"] = contents_with_template_path

        context["page_meta"] = {
            "body_class": "home h-feed",
            "desc": "Musings about stuff by someone old enough to know better than to put them on the internet",
        }
        return context
