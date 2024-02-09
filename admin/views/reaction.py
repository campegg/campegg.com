from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


from content.models import Reaction


# Create your views here.


# ---------- new reaction ----------#
class AdminReactionCreate(LoginRequiredMixin, CreateView):
    login_url = "/admin/login"
    success_url = "/admin/reaction"
    model = Reaction
    template_name = "admin.html"
    fields = [
        "reaction_type",
        "react_to_url",
    ]

    def get_success_url(self):
        return reverse_lazy("admin_reaction_new")

    def get_context_data(self, **kwargs):
        context = super(AdminReactionCreate, self).get_context_data(**kwargs)
        context["reactions"] = Reaction.objects.all()
        context["page_meta"] = {
            "body_class": "admin admin-reaction",
            "title": "New reaction",
        }
        return context
