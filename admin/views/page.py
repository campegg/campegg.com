from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


from content.models import Page


# Create your views here.


# ---------- new page ----------#
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


# ---------- edit page ----------#
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


# ---------- delete page ----------#
class AdminPageDelete(LoginRequiredMixin, DeleteView):
    login_url = "/admin/login"
    success_url = reverse_lazy("admin_dashboard")
    model = Page
    template_name = "admin.html"

    def get_context_data(self, **kwargs):
        context = super(AdminPageDelete, self).get_context_data(**kwargs)
        context["page_meta"] = {
            "body_class": "admin admin-Page",
            "title": "Delete page",
        }
        return context
