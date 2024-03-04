from django.views.generic import DetailView
from utilities.mentions import get_mentions


from content.models import Content


class Page(DetailView):
    model = Content
    template_name = "content.html"
    context_object_name = "item"
    slug_field = "content_path"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mentions"] = get_mentions(self.object.id)
        page_meta = {
            "body_class": "page",
            "title": self.object.content_meta.get("title", ""),
            "desc": self.object.content_meta.get("description", ""),
        }
        context["page_meta"] = page_meta
        return context
