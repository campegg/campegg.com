from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import is_aware, make_aware
import pytz


from content.models import Content


class AdminDashboard(LoginRequiredMixin, TemplateView):
    template_name = "admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        items = Content.objects.all().order_by("-publish_date")

        post_types = ["note", "post", "photo"]
        posts = [item for item in items if item.content_type in post_types]

        pages = [item for item in items if item.content_type == "page"]

        map_types = ["note", "post", "photo", "reply", "repost", "activity"]
        map_items = [item for item in items if item.content_type in map_types]

        date_list = []
        for map_item in map_items:
            date = map_item.publish_date
            if not is_aware(date):
                date = make_aware(date, pytz.UTC)
            formatted_date = date.isoformat()
            date_list.append(formatted_date)

        context["posts"] = posts[:10]
        context["pages"] = pages
        context["date_list"] = date_list
        context["page_meta"] = {
            "body_class": "admin admin-dashboard",
            "title": "Admin dashboard",
        }
        return context
