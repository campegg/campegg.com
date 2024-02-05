# admin/urls.py

from django.urls import path
from django.contrib.auth import views


from admin.views import (
    AdminLogin,
    AdminDashboard,
    AdminPost,
)


urlpatterns = [
    # ---------- admin pages ----------#
    path(
        "admin/login",
        views.LoginView.as_view(
            template_name="admin.html",
            extra_context={
                "page_meta": {"title": "Login", "body_class": "admin admin-login"}
            },
            next_page="/",
            authentication_form=AdminLogin,
        ),
        name="login",
    ),
    path("admin/post", AdminPost.as_view(), name="post"),
    path("admin/", AdminDashboard.as_view(), name="dashboard"),
]
