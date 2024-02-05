from django.views.generic import ListView, DetailView
from django.db.models.functions import TruncDate
from django.shortcuts import get_object_or_404


from content.models import Reaction


# Create your views here.


class ReactionIndex(ListView):
    model = Reaction
    template_name = "admin.html"
    context_object_name = "reactions"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.annotate(date_only=TruncDate("create_date")).order_by("-id")

    def get_context_data(self, **kwargs):
        context = super(ReactionIndex, self).get_context_data(**kwargs)
        context["page_meta"] = {
            "body_class": "reaction",
            "title": "Things to which I have reacted",
            "desc": "Why are you even looking at this page?",
        }
        return context


class ReactionDetail(DetailView):
    model = Reaction
    template_name = "admin.html"
    context_object_name = "reaction"

    def get_object(self, queryset=None):
        id = self.kwargs.get("id")

        return get_object_or_404(
            Reaction,
            id=id,
        )

    def get_context_data(self, **kwargs):
        context = super(ReactionDetail, self).get_context_data(**kwargs)
        context["page_meta"] = {
            "body_class": "reaction",
            "title": f"{self.object.get_reaction_type_display()}: {self.object.react_to_url}",
            "desc": "Why are you even looking at this page?",
        }
        return context
