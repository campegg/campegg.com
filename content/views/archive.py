from django.views.generic import ListView
from django.db.models import Q
from django.utils import timezone
from bs4 import BeautifulSoup
import re

from content.models import Content


class Archive(ListView):
    context_object_name = "items"
    model = Content
    paginate_orphans = 2
    template_name = "content.html"

    def get_queryset(self):
        # Filter for items with content_type of 'note' or 'post' and adjust for 'publish_date' and 'content_rss_only'
        queryset = Content.objects.filter(
            Q(content_type="note") | Q(content_type="post") | Q(content_type="photo"),
            publish_date__lte=timezone.now(),
            content_rss_only=False,
        ).order_by("-publish_date")
        return queryset

    def get_archive_text(self, content):
        # Accessing the 'html' key directly from the 'content_meta' JSONField
        html_content = content.content_meta.get("html", "")
        soup = BeautifulSoup(html_content, "lxml")
        content_text = soup.get_text()

        if content_text:
            archive_text = " ".join(content_text.split()[:20])
            archive_text = re.sub(r"{{.*?}}", "", archive_text).strip()
            if archive_text and archive_text[-1] not in [".", "!", "?", "…"]:
                if archive_text[-1] in [":", ";", ",", " "]:
                    archive_text = archive_text[:-1]
                archive_text += "…"
            return archive_text
        else:
            image_tag = soup.find("img", alt=True)
            alt_text = image_tag["alt"] if image_tag else "Image post"
            return alt_text

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_count = len(context["items"])
        for post in context["items"]:
            post.archive_text = self.get_archive_text(post)

        context["page_meta"] = {
            "body_class": "archive",
            "title": f"Every one of the {post_count} posts I’ve posted",
            "desc": "All the things!",
        }

        return context


# The subclasses YearArchive, MonthArchive, DayArchive remain mostly the same,
# just ensure they inherit from the updated Archive class and work with Content model.
