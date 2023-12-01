# activitypub/urls.py


from activitypub.views import WebFinger


from django.urls import path


urlpatterns = [
    # ---------- activitypub ----------#
    path(".well-known/webfinger", WebFinger.as_view(), name="webfinger"),
]
