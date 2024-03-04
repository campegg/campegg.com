from django.views.generic import DetailView
from utilities.mentions import get_mentions


from content.mixins import DateSlugObjectMixin
from content.models import Content


class Post(DateSlugObjectMixin, DetailView):
    context_object_name = "item"
    model = Content
    template_name = "content.html"
    slug_field = "content_path"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mentions"] = get_mentions(self.object.id)
        context["page_meta"] = {
            "body_class": "post",
            "title": "Post",
        }
        return context
