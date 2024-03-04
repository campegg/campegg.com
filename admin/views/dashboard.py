from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


from content.models import Content


class AdminDashboard(LoginRequiredMixin, TemplateView):
    template_name = "admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post_types = ["note", "post"]
        posts = Content.objects.filter(content_type__in=post_types).order_by(
            "-publish_date"
        )[:10]
        pages = Content.objects.filter(content_type="page").order_by("-publish_date")

        # Update context
        context["posts"] = posts
        context["pages"] = pages
        context["page_meta"] = {
            "body_class": "admin admin-dashboard",
            "title": "Admin dashboard",
        }

        return context
