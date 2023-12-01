from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


from content.models import Post


# Create your views here.


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "admin.html"
    fields = [
        "photo",
        "photo_alt_text",
        "publish_date",
        "rss_only",
        "send_to_archive",
        "send_to_fediverse",
        "status",
        "title",
        "text",
    ]
    success_url = reverse_lazy("home")

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

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.photo = self.request.FILES.get("photo", None)
        print(self.request.FILES)  # Debugging line
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(PostCreate, self).get_form_kwargs()
        kwargs["prefix"] = "post_form"
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_form"] = context.get("form")
        context["page_meta"] = {
            "body_class": "admin admin-new",
            "title": "New Post",
        }
        return context
