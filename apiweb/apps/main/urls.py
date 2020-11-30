from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from apiweb.context_processors import contactinfo

from .views import (
    AlumnusAutocomplete,
    index,
    page_not_found,
    privacy_policy,
    redirect_to_profile,
    site_careerinfo,
    site_contactinfo,
    site_thesis_create,
    site_thesis_select,
    site_thesis_update,
)

urlpatterns = [
    path("", index, name="index"),
    path("404.html", page_not_found, name="page_not_found"),
    path("privacy-policy/", privacy_policy, name="privacy_policy"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="main/login.html",
        ),
        name="site_login",
    ),
    path("redirect_to_profile/", redirect_to_profile, name="login_success"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="main/logged_out.html"),
        name="site_logout",
    ),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="main/password_change_form.html",
            success_url=reverse_lazy("site_password_change_done"),
        ),
        name="site_password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="main/password_change_done.html",
        ),
        name="site_password_change_done",
    ),
    path("update_contactinfo/", site_contactinfo, name="site_contactinfo"),
    path(
        "update_careerinfo/<which_position_value>/",
        site_careerinfo,
        name="site_careerinfo",
    ),
    path("select_thesis/", site_thesis_select, name="site_thesis_select"),
    path("update_thesis/<slug>", site_thesis_update, name="site_thesis_update"),
    path(
        "alumnus-autocomplete/",
        AlumnusAutocomplete.as_view(),
        name="alumnus-autocomplete",
    ),
    path("create_thesis/", site_thesis_create, name="site_thesis_create"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="main/password_reset_form.html",
            extra_context={
                "api_phonenumber_formatted": contactinfo(None)[
                    "api_phonenumber_formatted"
                ],
                "secretary_email_address": contactinfo(None)[
                    "contactinfo"
                ].secretary_email_address,
            },
            email_template_name="main/password_reset_email.html",
            extra_email_context={
                "api_phonenumber_formatted": contactinfo(None)[
                    "api_phonenumber_formatted"
                ],
                "secretary_email_address": contactinfo(None)[
                    "contactinfo"
                ].secretary_email_address,
            },
            success_url=reverse_lazy("site_password_reset_done"),
        ),
        name="site_password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="main/password_reset_done.html",
            extra_context={
                "api_phonenumber_formatted": contactinfo(None)[
                    "api_phonenumber_formatted"
                ],
                "secretary_email_address": contactinfo(None)[
                    "contactinfo"
                ].secretary_email_address,
            },
        ),
        name="site_password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="main/password_reset_confirm.html",
            success_url=reverse_lazy("site_password_reset_complete"),
        ),
        name="site_password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="main/password_reset_complete.html"
        ),
        name="site_password_reset_complete",
    ),
]
