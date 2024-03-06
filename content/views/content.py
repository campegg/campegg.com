from django.views.generic import DetailView
from utilities.mentions import get_mentions
from bs4 import BeautifulSoup

from content.models import Content

title_map = {
    "note": lambda obj: obj.publish_date.strftime("%B %-d, %Y, %-I:%M%p")
    .replace("AM", "am")
    .replace("PM", "pm"),
    "post": lambda obj: obj.content_meta.get("title", ""),
    "photo": lambda obj: "Photo",  # placeholder (for now)
}


class CoreContent(DetailView):
    model = Content
    template_name = "content.html"
    slug_field = "content_path"
    slug_url_kwarg = "slug"
    context_object_name = "item"

    def get_queryset(self):
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        day = self.kwargs.get("day")
        slug = self.kwargs.get("slug")

        return (
            super()
            .get_queryset()
            .filter(
                content_path=slug,
                publish_date__year=year,
                publish_date__month=month,
                publish_date__day=day,
            )
        )

    def get_title(self):
        content_title = title_map.get(self.object.content_type)
        if content_title:
            return content_title(self.object)
        elif self.object.content_type in ["reply", "repost"]:
            account = self._get_account()
            prefix = (
                "Repost from" if self.object.content_type == "repost" else "Reply to"
            )
            return f"{prefix} @{account}" if account else "some rando on the internet"
        else:
            return "Unsupported content type :("

    def _get_account(self):
        if self.object.content_meta.get("json"):
            return self.object.content_meta.get("json").get("account").get("acct")
        soup = BeautifulSoup(self.object.content_meta.get("html"), "html.parser")
        account = next(
            (
                link.text.strip()
                for link in soup.find_all("a")
                if link.text.startswith("@")
            ),
            None,
        )
        return account

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mentions"] = get_mentions(self.object.id)
        context["page_meta"] = {
            "body_class": self.object.content_type,
            "title": self.get_title(),
        }
        return context
