from django.views.generic import ListView
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, OuterRef, Subquery, IntegerField


from bs4 import BeautifulSoup
from datetime import datetime


from content.models import Post


# Create your views here.


class Home(ListView):
    context_object_name = "posts"
    model = Post
    paginate_by = 20
    paginate_orphans = 2
    template_name = "content.html"

    def get_queryset(self):
        post_content_type = ContentType.objects.get_for_model(Post)
        from mentions.models import Webmention

        mentions_count_subquery = Subquery(
            Webmention.objects.filter(
                content_type=post_content_type, object_id=OuterRef("id")
            )
            .order_by()
            .values("object_id")
            .annotate(cnt=Count("id"))
            .values("cnt")[:1],
            output_field=IntegerField(),  # Corrected usage
        )

        queryset = (
            Post.objects.all()
            .annotate(mention_count=mentions_count_subquery)
            .filter(
                publish_date__lte=datetime.now().replace(microsecond=0),
                status__exact=1,
                rss_only__exact=0,
            )
            .order_by("-publish_date")
        )

        # get the first paragraph only (or first two if the first is an image) for posts
        for post in queryset:
            if post.post_type == 1:
                soup = BeautifulSoup(post.html, "lxml")
                paragraphs = soup.find_all("p")
                post.first_paragraph = str(paragraphs[0])

        return queryset

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context["page_meta"] = {
            "body_class": "home h-feed",
            "desc": "Musings about stuff by someone old enough to know better than to put them on the internet",
        }
        return context

    def get_page(self):
        return self.kwargs.get("page", 1)
