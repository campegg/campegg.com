from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


from content.models import Content


# Create your views here.


# ---------- delete content ----------#
class AdminDelete(LoginRequiredMixin, DeleteView):
    login_url = "/admin/login"
    success_url = reverse_lazy("admin_dashboard")
    model = Content
    template_name = "admin.html"

    def get_context_data(self, **kwargs):
        context = super(AdminDelete, self).get_context_data(**kwargs)
        context["page_meta"] = {
            "body_class": "admin admin-post",
            "title": "Delete post",
        }
        return context
