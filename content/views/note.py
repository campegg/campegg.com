from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from utilities.mentions import get_mentions


from content.models import Content


class Note(DetailView):
    context_object_name = "item"
    model = Content
    template_name = "content.html"
    slug_field = "content_path"
    slug_url_kwarg = "slug"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        day = self.kwargs.get("day")
        slug = self.kwargs.get("slug")

        obj = get_object_or_404(
            queryset,
            content_path=slug,
            publish_date__year=year,
            publish_date__month=month,
            publish_date__day=day,
        )

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mentions"] = get_mentions(self.object.id)
        context["page_meta"] = {
            "body_class": "note",
            "title": self.object.publish_date.strftime("%B %-d %Y, %-I:%M%p")
            .replace("AM", "am")
            .replace("PM", "pm"),
        }
        return context
