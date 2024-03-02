from django.views.generic import DetailView, ListView
import polyline


from content.models import Content


class Activities(ListView):
    template_name = "content.html"
    context_object_name = "items"
    paginate_by = 50

    def get_queryset(self):
        return Content.objects.filter(content_type="activity")

    def get_context_data(self, **kwargs):
        context = super(Activities, self).get_context_data(**kwargs)
        context["page_meta"] = {
            "body_class": "activity",
            "title": "Strava Activity Archive",
            "desc": "An archive of my old Strava activities, no longer actively updated",
        }
        return context


class Activity(DetailView):
    context_object_name = "item"
    model = Content
    template_name = "content.html"
    slug_field = "content_path"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        location = []
        if "map" in self.object.content_meta:
            for key, value in polyline.decode(
                self.object.content_meta["map"]["summary_polyline"]
            ):
                temp = [value, key]
                location.append(temp)
            context["location"] = location

        context["page_meta"] = {
            "body_class": "activity",
            "title": self.object.content_meta["name"]
            if self.object.content_meta.get("name")
            else "Strava Activity",
        }
        return context
