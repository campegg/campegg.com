from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


class AdminDashboard(LoginRequiredMixin, TemplateView):
    template_name = "admin.html"

    def get_context_data(self, **kwargs):
        context = super(AdminDashboard, self).get_context_data(**kwargs)
        context["page_meta"] = {
            "body_class": "admin",
            "title": "Dashboard",
        }
        return context
