from django.forms import modelform_factory
from content.models import Post


def post_form(request):
    PostForm = modelform_factory(
        Post,
        fields=[
            "publish_date",
            "rss_only",
            "send_to_archive",
            "send_to_fediverse",
            "status",
            "title",
            "text",
        ],
    )
    form = PostForm(prefix="post_form")
    return {"post_form": form}
