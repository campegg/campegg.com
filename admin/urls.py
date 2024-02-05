# admin/urls.py

from django.urls import path
from django.contrib.auth import views
from django.views.generic import RedirectView


from admin.views import (
    AdminLogin,
    AdminDashboard,
    AdminPostCreate,
)


urlpatterns = [
    # ---------- admin pages ----------#
    path(
        "admin/login/",
        views.LoginView.as_view(
            template_name="admin.html",
            extra_context={
                "page_meta": {"title": "Login", "body_class": "admin admin-login"}
            },
            next_page="/",
            authentication_form=AdminLogin,
        ),
        name="admin_login",
    ),
    path("admin/post/", AdminPostCreate.as_view(), name="admin_post_new"),
    path("admin/", AdminDashboard.as_view(), name="admin_dashboard"),
    # ---------- redirects ----------#
    path("login/", RedirectView.as_view(pattern_name="admin_login", permanent=True)),
]
