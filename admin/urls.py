# admin/urls.py

from django.urls import path
from django.contrib.auth import views
from django.views.generic import RedirectView
from django.contrib.auth.views import LogoutView


from admin.views import AdminLogin, AdminDashboard, AdminNew, AdminEdit, AdminDelete


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
    path("admin/", AdminDashboard.as_view(), name="admin_dashboard"),
    path("admin/new/<slug:content_type>/", AdminNew.as_view(), name="admin_new"),
    path(
        "admin/edit/<slug:content_type>/<int:content_id>/",
        AdminEdit.as_view(),
        name="admin_edit",
    ),
    path(
        "admin/delete/<slug:content_type>/<int:pk>/",
        AdminDelete.as_view(),
        name="admin_delete",
    ),
    # ---------- redirects ----------#
    path("login/", RedirectView.as_view(pattern_name="admin_login", permanent=True)),
]
