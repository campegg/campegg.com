from django.views.generic import DetailView
from django.shortcuts import get_object_or_404


from content.models import Page


# Create your views here.


class PageDetail(DetailView):
    context_object_name = "page"
    model = Page
    template_name = "content.html"

    def get_object(self, queryset=None):
        path = self.kwargs.get("path")
        return get_object_or_404(Page, full_path=path)

    def get_context_data(self, **kwargs):
        context = super(PageDetail, self).get_context_data(**kwargs)
        context["page_meta"] = {
            "body_class": "page",
            "title": self.object.title,
            "desc": self.object.description,
        }
        return context
