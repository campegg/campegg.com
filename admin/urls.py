# admin/urls.py

from django.urls import path
from django.contrib.auth import views
from django.views.generic import RedirectView
from django.contrib.auth.views import LogoutView


from admin.views import (
    AdminLogin,
    AdminDashboard,
    AdminPageCreate,
    AdminPageEdit,
    AdminPostCreate,
    AdminPostEdit,
    AdminReactionCreate,
    AdminReactionDelete,
)


urlpatterns = [
    # ---------- admin pages ----------#
    path(
        "admin/login/",
        views.LoginView.as_view(
            template_name="admin/login.html",
            extra_context={
                "page_meta": {"title": "Login", "body_class": "admin admin-login"}
            },
            next_page="/",
            authentication_form=AdminLogin,
        ),
        name="admin_login",
    ),
    path("admin/logout/", LogoutView.as_view(next_page="home"), name="admin_logout"),
    path("admin/page/", AdminPageCreate.as_view(), name="admin_page_new"),
    path("admin/page/edit/<int:pk>", AdminPageEdit.as_view(), name="admin_page_edit"),
    path("admin/post/", AdminPostCreate.as_view(), name="admin_post_new"),
    path("admin/post/edit/<int:pk>", AdminPostEdit.as_view(), name="admin_post_edit"),
    path("admin/reaction/", AdminReactionCreate.as_view(), name="admin_reaction_new"),
    path(
        "admin/reaction/delete/<int:pk>",
        AdminReactionDelete.as_view(),
        name="admin_reaction_delete",
    ),
    path("admin/", AdminDashboard.as_view(), name="admin_dashboard"),
    # ---------- redirects ----------#
    path("login/", RedirectView.as_view(pattern_name="admin_login", permanent=True)),
]
