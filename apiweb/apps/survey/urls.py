from django.conf.urls import include, url
from .views import survey
from .views import survey_success


urlpatterns = [
	url(r'^form',survey,name='form'),
	url(r'^thanks',survey_success,name='survey_success')
]