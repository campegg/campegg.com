from django.views.generic import ListView, TemplateView
from django.conf import settings
from django.http import Http404

from pathlib import Path
from datetime import datetime
import json
import polyline


# Create your views here.


class ActivityIndex(ListView):
    template_name = "content.html"
    context_object_name = "activities"
    paginate_by = 50

    def get_queryset(self):
        activities = []
        activities_dir = Path(settings.BASE_DIR) / "data" / "activities"

        for file_path in activities_dir.glob("*.json"):
            with open(file_path, "r") as file:
                data = json.load(file)
                start_date_local = datetime.strptime(
                    data.get("start_date_local", ""), "%Y-%m-%dT%H:%M:%SZ"
                )
                activity = {
                    "name": data.get("name"),
                    "distance": data.get("distance"),
                    "moving_time": data.get("moving_time"),
                    "type": data.get("type"),
                    "id": data.get("id"),
                    "start_date_local": start_date_local,
                }
                activities.append(activity)

        activities.sort(key=lambda x: x["start_date_local"], reverse=True)
        return activities

    def get_context_data(self, **kwargs):
        context = super(ActivityIndex, self).get_context_data(**kwargs)
        context["page_meta"] = {
            "body_class": "activity",
            "title": "Strava Activity Archive",
            "desc": "An archive of my old Strava activities, no longer actively updated",
        }
        return context


class ActivityDetail(TemplateView):
    template_name = "content.html"

    def get_context_data(self, **kwargs):
        context = super(ActivityDetail, self).get_context_data(**kwargs)
        activity_id = self.kwargs.get("id")
        file_path = (
            Path(settings.BASE_DIR) / "data" / "activities" / f"{activity_id}.json"
        )

        if not file_path.exists():
            raise Http404("Activity not found")

        with open(file_path, "r") as file:
            activity = json.load(file)

            location = []
            if "map" in activity:
                for key, value in polyline.decode(activity["map"]["summary_polyline"]):
                    temp = [value, key]
                    location.append(temp)
                context["location"] = location

            if "start_date" in activity:
                activity["start_date"] = datetime.strptime(
                    activity["start_date"], "%Y-%m-%dT%H:%M:%SZ"
                )
            if "start_date_local" in activity:
                activity["start_date_local"] = datetime.strptime(
                    activity["start_date_local"], "%Y-%m-%dT%H:%M:%SZ"
                )

            context["activity"] = activity

        title = activity.get("name", "Activity")
        description = activity.get("description", "An archived Strava activity")

        context["page_meta"] = {
            "body_class": "activity",
            "title": title,
            "desc": description,
        }

        return context
