from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


from content.models import Reaction


# Create your views here.


# ---------- new reaction ----------#
class AdminReactionCreate(LoginRequiredMixin, CreateView):
    login_url = "/admin/login"
    success_url = reverse_lazy("admin_reaction_new")
    model = Reaction
    template_name = "admin.html"
    fields = [
        "reaction_type",
        "react_to_url",
    ]

    def get_context_data(self, **kwargs):
        context = super(AdminReactionCreate, self).get_context_data(**kwargs)
        context["reactions"] = Reaction.objects.all()
        context["page_meta"] = {
            "body_class": "admin admin-reaction",
            "title": "New reaction",
        }
        return context


# ---------- delete reaction ----------#
class AdminReactionDelete(LoginRequiredMixin, DeleteView):
    login_url = "/admin/login"
    success_url = reverse_lazy("admin_reaction_new")
    model = Reaction
    template_name = "admin.html"

    def get_context_data(self, **kwargs):
        context = super(AdminReactionDelete, self).get_context_data(**kwargs)
        context["page_meta"] = {
            "body_class": "admin admin-reaction",
            "title": "Delete reaction",
        }
        return context
