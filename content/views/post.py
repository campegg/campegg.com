from django.views.generic import DetailView


from content.models import Content


class Post(DetailView):
    context_object_name = "item"
    model = Content
    template_name = "content.html"
    slug_field = "content_path"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_meta"] = {
            "body_class": "post",
            "title": "Post",
        }
        return context
