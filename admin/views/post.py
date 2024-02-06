from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


from content.models import Post


# Create your views here.


# ---------- posts admin ----------#
class AdminPostCreate(LoginRequiredMixin, CreateView):
    login_url = "/admin/login"
    model = Post
    template_name = "admin.html"
    fields = [
        "title",
        "text",
        "html",
        "publish_date",
        "status",
        "rss_only",
        "send_to_fediverse",
        "send_to_archive",
        "rss_only",
        "allow_outgoing_webmentions",
    ]

    def get_context_data(self, **kwargs):
        context = super(AdminPostCreate, self).get_context_data(**kwargs)
        context["page_meta"] = {
            "body_class": "admin admin-post",
            "title": "New post",
        }
        return context
