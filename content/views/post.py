from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from bs4 import BeautifulSoup


from content.models import Post


# Create your views here.


class PostDetail(DetailView):
    context_object_name = "post"
    model = Post
    template_name = "content.html"

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

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)

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

        soup = BeautifulSoup(self.object.html, "lxml")
        full_text = soup.get_text().strip()
        if full_text:
            words = full_text.split()[:20]
            desc_text = " ".join(words)
            if desc_text[-1] in [".", "!", "?", "…"]:
                pass
            elif desc_text[-1] in [":", ";", ",", " "]:
                desc_text = desc_text[:-1] + "…"
            else:
                desc_text += "…"
        else:
            image_tag = soup.find("img", alt=True)
            if image_tag:
                desc_text = image_tag["alt"]
            else:
                desc_text = "No description available… you're on your own, buddy."

        context["page_meta"] = {
            "body_class": "post h-entry",
            "title": self.object.title if self.object.title else f"{ title_date }",
            "desc": desc_text,
        }
        return context
