from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import is_aware, make_aware
import pytz


from content.models import Post  # Adjust according to your project structure


class AdminDashboard(LoginRequiredMixin, TemplateView):
    template_name = "admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        posts = Post.objects.all().order_by("publish_date")
        date_list = []
        for post in posts:
            date = post.publish_date
            if not is_aware(date):
                date = make_aware(date, pytz.UTC)
            formatted_date = date.isoformat()
            date_list.append(formatted_date)

        context["date_list"] = date_list
        context["page_meta"] = {
            "body_class": "admin admin-dashboard",
            "title": "Admin dashboard",
        }
        return context
