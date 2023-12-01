from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name="dispatch")
class WebFinger(View):
    def get(self, request, *args, **kwargs):
        resource = request.GET.get("resource", None)

        if resource == "acct:cam@campegg.com":
            response_data = {
                "subject": "acct:cam@campegg.com",
                "links": [
                    {
                        "rel": "http://webfinger.net/rel/profile-page",
                        "type": "text/html",
                        "href": "https://campegg.com",
                    },
                    {
                        "rel": "self",
                        "type": "application/activity+json",
                        "href": "https://campegg.com",
                    },
                ],
            }
            return JsonResponse(response_data)

        return JsonResponse({"error": "Resource not found"}, status=404)
