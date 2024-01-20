# admin/urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views


from siteadmin.views import AdminLogin, PostCreate, PostEdit


urlpatterns = [
    # ---------- admin pages ----------#
    path("logout/", LogoutView.as_view(next_page="/login"), name="admin_logout"),
    path(
        "login/",
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
    path("new", PostCreate.as_view(), name="admin_create"),
    path(
        "edit/<int:year>/<int:month>/<int:day>/<slug:slug>.html",
        PostEdit.as_view(),
        name="admin_edit",
    ),
]
