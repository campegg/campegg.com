from django.http import Http404
from django.views import View


from content.models import Content


class Dispatcher(View):
    def get(self, request, year, month, day, slug):
        try:
            content = Content.objects.get(
                publish_date__year=year,
                publish_date__month=month,
                publish_date__day=day,
                content_path=slug,
            )
        except Content.DoesNotExist:
            raise Http404("Content does not exist")

        if content.content_type == "note":
            from content.views.note import Note

            return Note.as_view()(request, year=year, month=month, day=day, slug=slug)
        elif content.content_type == "photo":
            from content.views.photo import Photo

            return Photo.as_view()(request, year=year, month=month, day=day, slug=slug)
        elif content.content_type == "post":
            from content.views.post import Post

            return Post.as_view()(request, year=year, month=month, day=day, slug=slug)
        elif content.content_type == "reply":
            from content.views.reply import Reply

            return Reply.as_view()(request, year=year, month=month, day=day, slug=slug)
        elif content.content_type == "repost":
            from content.views.repost import Repost

            return Repost.as_view()(request, year=year, month=month, day=day, slug=slug)
        else:
            raise Http404("Unsupported content type")
