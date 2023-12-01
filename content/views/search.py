from django.views.generic import TemplateView
from django.db.models import Q, Case, When, Value, FloatField, F, ExpressionWrapper
from django.db.models.functions import Length
from functools import cmp_to_key
from bs4 import BeautifulSoup


from content.models import Post, Page
from content.forms import SearchForm


# Create your views here.


def custom_sort(a, b):
    if a.final_ranking < b.final_ranking:
        return 1
    elif a.final_ranking > b.final_ranking:
        return -1
    else:
        a_date = getattr(a, "publish_date", None)
        b_date = getattr(b, "publish_date", None)
        if a_date and b_date:
            return 1 if b_date > a_date else -1
        elif a_date:
            return -1
        elif b_date:
            return 1
        else:
            return 0


def get_result_summary(text):
    soup = BeautifulSoup(text, "lxml")
    first_paragraph = soup.find("p")
    if first_paragraph:
        img = first_paragraph.find("img")
        if img:
            alt_text = img.get("alt", "<em>Image result</em>")
            return alt_text
        else:
            words = first_paragraph.get_text().split()[:20]
            summary = " ".join(words)
            last_char = summary[-1] if summary else ""
            if last_char in [".", "!", "?", "…"]:
                pass
            elif last_char in [":", ";", ",", " "]:
                summary = summary[:-1] + "…"
            else:
                summary += "…"
            return summary
    return "<em>No summary available</em>"


class SearchView(TemplateView):
    template_name = "content.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = SearchForm(self.request.GET or None)
        results = []

        if form.is_valid():
            query = form.cleaned_data.get("q")

            post_results = Post.objects.annotate(
                text_length=Length("text"),
                final_ranking=ExpressionWrapper(
                    F("text_length") * Value(0.5)
                    + Case(
                        When(title__icontains=query, then=Value(1.0)),
                        default=Value(0.0),
                    ),
                    output_field=FloatField(),
                ),
            ).filter(
                Q(title__icontains=query) | Q(text__icontains=query),
                status=Post.published,
                final_ranking__gt=0,
            )

            page_results = Page.objects.annotate(
                text_length=Length("text"),
                final_ranking=ExpressionWrapper(
                    F("text_length") * Value(0.5)
                    + Case(
                        When(title__icontains=query, then=Value(5000.0)),
                        default=Value(0.0),
                    ),
                    output_field=FloatField(),
                ),
            ).filter(
                Q(title__icontains=query) | Q(text__icontains=query),
                final_ranking__gt=0,
            )

            results = sorted(
                list(post_results) + list(page_results),
                key=cmp_to_key(custom_sort),
            )

            for result in results:
                result.result_summary = get_result_summary(result.html)

        context["results"] = results
        context["page_meta"] = {
            "body_class": "search",
            "title": "Search",
            "desc": "Are you lookin' at (for?) me?",
        }
        return context
