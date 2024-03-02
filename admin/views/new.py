from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


from content.models import Content


# Create your views here.


# ---------- new content ----------#
class AdminNew(LoginRequiredMixin, CreateView):
    login_url = "/admin/login"
    model = Content
    template_name = "admin.html"
    fields = [
        "content_type",
        "content_path",
        "content_meta",
        "content_federate",
        "content_rss_only",
        "publish_date",
        "allow_outgoing_webmentions",
    ]

    def get_success_url(self):
        content_type = self.kwargs.get("content_type")
        if content_type == "reaction":
            return "/admin/new/reaction/"
        else:
            return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.kwargs.get("content_type") == "page":
            context["pages"] = Content.objects.filter(content_type__exact="page")

        if self.kwargs.get("content_type") == "reaction":
            context["reactions"] = Content.objects.filter(
                Q(content_type__exact="like")
                | Q(content_type__exact="reply")
                | Q(content_type__exact="repost")
            )

        context["page_meta"] = {
            "body_class": f'admin admin-new admin-{self.kwargs.get("content_type", "default")}',
            "title": f'New {self.kwargs.get("content_type", "default")}',
        }
        context["content_type"] = self.kwargs.get("content_type", "default")
        return context
