from django.views.generic import ListView
from django.db.models.functions import TruncDate


from content.models import Content


# Create your views here.


class Reaction(ListView):
    model = Content
    template_name = "content.html"
    context_object_name = "items"

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .filter(content_type__in=["like", "reply", "repost"])
            .annotate(date_only=TruncDate("create_date"))
            .order_by("-id")
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(Reaction, self).get_context_data(**kwargs)
        context["page_meta"] = {
            "body_class": "reaction",
            "title": "Things to which I have reacted",
            "desc": "Why are you even looking at this page?",
        }
        return context
