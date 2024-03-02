from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


from content.models import Content


# Create your views here.


# ---------- edit content ----------#
class AdminEdit(LoginRequiredMixin, UpdateView):
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.kwargs.get("content_type") == "page":
            context["pages"] = Content.objects.filter(content_type__exact="page")

        context["page_meta"] = {
            "body_class": f'admin admin-edit admin-{self.kwargs.get("content_type", "default")}',
            "title": f'Edit {self.kwargs.get("content_type", "default")}',
        }
        context["content_type"] = self.kwargs.get("content_type", "default")
        return context

    def get_object(self, queryset=None):
        content_id = self.kwargs.get("content_id")
        return self.model.objects.get(id=content_id)
