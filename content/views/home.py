from django.http import JsonResponse
from django.views.generic import ListView
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
        queryset = (
            Post.objects.all()
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
