# admin/urls.py
from django.urls import path


from siteadmin.views import PostCreate, PostEdit


urlpatterns = [
    # ---------- admin pages ----------#
    path("new", PostCreate.as_view(), name="admin_create"),
    path(
        "edit/<int:year>/<int:month>/<int:day>/<slug:slug>.html",
        PostEdit.as_view(),
        name="admin_edit",
    ),
]
