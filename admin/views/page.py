from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


from content.models import Page


# Create your views here.


# ---------- new post ----------#
class AdminPageCreate(LoginRequiredMixin, CreateView):
    login_url = "/admin/login"
    model = Page
    template_name = "admin.html"
    fields = [
        "title",
        "description",
        "text",
        "html",
        "parent",
        "show_in_nav",
    ]

    def get_context_data(self, **kwargs):
        context = super(AdminPageCreate, self).get_context_data(**kwargs)
        context["page_meta"] = {
            "body_class": "admin admin-page",
            "title": "New page",
        }
        return context


# ---------- edit post ----------#
class AdminPageEdit(LoginRequiredMixin, UpdateView):
    login_url = "/admin/login"
    model = Page
    template_name = "admin.html"
    fields = [
        "title",
        "description",
        "text",
        "html",
        "parent",
        "show_in_nav",
    ]

    def get_context_data(self, **kwargs):
        context = super(AdminPageEdit, self).get_context_data(**kwargs)
        context["page_meta"] = {
            "body_class": "admin admin-page",
            "title": f"Editing ‘{self.object.title}’",
        }
        return context
