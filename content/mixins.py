# content/mixins.py
from django.shortcuts import get_object_or_404


class DateSlugObjectMixin:
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
