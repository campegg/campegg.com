from django.views.generic import DetailView
from content.models import Content


class Page(DetailView):
    model = Content
    template_name = "content.html"
    context_object_name = "item"
    slug_field = "content_path"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Content.objects.filter(content_type="page")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_meta = {
            "body_class": "page",
            "title": self.object.content_meta.get("title", ""),
            "desc": self.object.content_meta.get("description", ""),
        }
        context["page_meta"] = page_meta
        return context
