from django.views.generic import DetailView
from bs4 import BeautifulSoup


from content.models import Content


class Repost(DetailView):
    context_object_name = "item"
    model = Content
    template_name = "content.html"
    slug_field = "content_path"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.object.content_meta.get("json"):
            account = self.object.content_meta.get("json").get("account").get("acct")
        else:
            soup = BeautifulSoup(self.object.content_meta.get("html"), "lxml")
            for link in soup.find_all("a"):
                if link.text.startswith("@"):
                    account = link.text.strip()
                    break

        repost_title = f"Repost from {account}"

        context["page_meta"] = {
            "body_class": "repost",
            "title": repost_title,
        }
        return context
