from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy


from content.models import Post


# Create your views here.


class PostEdit(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "admin.html"
    fields = [
        "photo",
        "photo_alt_text",
        "publish_date",
        "rss_only",
        "send_to_archive",
        "send_to_fediverse",
        "slug",
        "status",
        "title",
        "text",
    ]

    def get_object(self, queryset=None):
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        day = self.kwargs.get("day")
        slug = self.kwargs.get("slug")

        return get_object_or_404(
            Post,
            publish_date__year=year,
            publish_date__month=month,
            publish_date__day=day,
            slug=slug,
        )

    def get_success_url(self):
        return reverse_lazy(
            "post_detail",
            kwargs={
                "year": self.object.publish_date.year,
                "month": self.object.publish_date.strftime("%m"),
                "day": self.object.publish_date.strftime("%d"),
                "slug": self.object.slug,
            },
        )

    def get_form_kwargs(self):
        kwargs = super(PostEdit, self).get_form_kwargs()
        kwargs["prefix"] = "post_form"
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_form"] = context.get("form")
        context["page_meta"] = {
            "body_class": "admin admin-edit",
            "title": "Edit Post",
        }
        return context
