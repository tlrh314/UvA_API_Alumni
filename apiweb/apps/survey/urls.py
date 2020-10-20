from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from apiweb.context_processors import contactinfo

from .views import (
    survey_careerinfo_current,
    survey_careerinfo_first,
    survey_careerinfo_second,
    survey_careerinfo_third,
    survey_contactinfo,
    survey_success,
)

app_name = "survey"
urlpatterns = [
    path(
        "<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="survey/survey_reset_password.html",
            extra_context={
                "api_phonenumber_formatted": contactinfo(None)[
                    "api_phonenumber_formatted"
                ],
                "secretary_email_address": contactinfo(None)[
                    "contactinfo"
                ].secretary_email_address,
            },
            success_url=reverse_lazy("survey:contactinfo"),
            post_reset_login=True,
            post_reset_login_backend="django.contrib.auth.backends.ModelBackend",
        ),
        name="survey_url",
    ),
    path("contactinfo/", survey_contactinfo, name="contactinfo"),
    #    path(r"careerinfo/", survey_careerinfo, name="careerinfo"),
    path("careerinfo_current/", survey_careerinfo_current, name="careerinfo_current"),
    path("careerinfo_first/", survey_careerinfo_first, name="careerinfo_first"),
    path("careerinfo_second/", survey_careerinfo_second, name="careerinfo_second"),
    path("careerinfo_third/", survey_careerinfo_third, name="careerinfo_third"),
    path("thanks/", survey_success, name="survey_success"),
]
