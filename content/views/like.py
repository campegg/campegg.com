from django.views.generic import DetailView, ListView
from django.db.models.functions import TruncDate


from content.models import Content


class Like(DetailView):
    context_object_name = "item"
    model = Content
    template_name = "content.html"
    slug_field = "content_path"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_meta"] = {
            "body_class": "like",
            "title": "Like",
        }
        return context


class LikeList(ListView):
    context_object_name = "items"
    model = Content
    template_name = "content.html"

    def get_queryset(self):
        queryset = super().get_queryset().filter(content_type="like")
        return queryset.annotate(date_only=TruncDate("create_date")).order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_meta"] = {
            "body_class": "like",
            "title": "Like",
        }
        return context
