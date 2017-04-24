from django import forms
from django.forms.widgets import Input
from django.utils.translation import ugettext_lazy as _
from .models import Person
from ..research.models import ResearchTopic


class EmailInput(Input):
    input_type = 'email'


class URLInput(Input):
    input_type = 'url'


class PersonForm(forms.ModelForm):
    email = forms.EmailField(label=_('email'), widget=EmailInput, required=False)
    homepage = forms.URLField(label=_('homepage'), widget=URLInput, required=False)
    research = forms.ModelMultipleChoiceField(
        queryset=ResearchTopic.objects.filter(category__gt=0), required=False)
    contact = forms.ModelMultipleChoiceField(
              queryset=ResearchTopic.objects.filter(category__gt=0), required=False)

    class Meta:
        model = Person
        fields = [ 'first_name', 'prefix', 'last_name', 'title', 'initials', 'gender',
                   'birth_date', 'address', 'zipcode', 'city', 'country', 'home_phone',
                   'mobile', 'mugshot', 'photo', 'position', 'office', 'work_phone',
                   'ads_name', 'email', 'homepage', 'research', 'contact', 'comments' ]
