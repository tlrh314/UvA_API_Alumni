from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import include, url
from django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views

from apiweb.context_processors import contactinfo
from .views import survey_contactinfo
from .views import survey_careerinfo_current, survey_careerinfo_first, survey_careerinfo_second, survey_careerinfo_third
from .views import survey_success


urlpatterns = [
    url(r"^(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="survey/survey_reset_password.html",
            extra_context = {
                "api_phonenumber_formatted": contactinfo(None)["api_phonenumber_formatted"],
                "secretary_email_address": contactinfo(None)["contactinfo"].secretary_email_address,
            },
            success_url=reverse_lazy("survey:contactinfo"),
            post_reset_login=True,
            post_reset_login_backend="django.contrib.auth.backends.ModelBackend",
        ), name="survey_url"),
    url(r"^contactinfo/$", survey_contactinfo, name="contactinfo"),
#    url(r"^careerinfo/$", survey_careerinfo, name="careerinfo"),
    url(r"^careerinfo_current/$", survey_careerinfo_current, name="careerinfo_current"),
    url(r"^careerinfo_first/$", survey_careerinfo_first, name="careerinfo_first"),
    url(r"^careerinfo_second/$", survey_careerinfo_second, name="careerinfo_second"),
    url(r"^careerinfo_third/$", survey_careerinfo_third, name="careerinfo_third"),



    url(r"^thanks/$", survey_success, name="survey_success")
]
