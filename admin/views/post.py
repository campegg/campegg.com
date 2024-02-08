from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


from datetime import datetime


from content.models import Post


# Create your views here.


# ---------- posts admin ----------#
class AdminPostCreate(LoginRequiredMixin, CreateView):
    login_url = "/admin/login"
    model = Post
    template_name = "admin.html"
    fields = [
        "title",
        "text",
        "html",
        "publish_date",
        "status",
        "rss_only",
        "send_to_fediverse",
        "send_to_archive",
        "rss_only",
    ]

    def get_context_data(self, **kwargs):
        context = super(AdminPostCreate, self).get_context_data(**kwargs)
        context["page_meta"] = {
            "body_class": "admin admin-post",
            "title": "New post",
        }
        return context


class AdminPostEdit(LoginRequiredMixin, UpdateView):
    login_url = "/admin/login"
    model = Post
    template_name = "admin.html"
    fields = [
        "title",
        "text",
        "html",
        "publish_date",
        "status",
        "rss_only",
        "send_to_fediverse",
        "send_to_archive",
        "rss_only",
    ]

    def get_context_data(self, **kwargs):
        context = super(AdminPostEdit, self).get_context_data(**kwargs)

        post_day = self.object.publish_date.strftime("%A")
        post_month = self.object.publish_date.strftime("%B")
        post_date = str(self.object.publish_date.day)
        post_year = str(self.object.publish_date.year)
        post_hour = str(
            self.object.publish_date.hour % 12 or 12
        )  # Convert to 12-hour clock
        post_minute = self.object.publish_date.strftime("%M")
        post_ampm = self.object.publish_date.strftime("%p").lower()

        title_date = f"{post_hour}:{post_minute}{post_ampm} {post_day} {post_month} {post_date}, {post_year}"

        context["page_meta"] = {
            "body_class": "admin admin-post",
            "title": f"Editing ‘{self.object.title if self.object.title else title_date}’",
        }
        return context
