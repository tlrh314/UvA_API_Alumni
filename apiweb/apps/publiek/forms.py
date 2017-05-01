from __future__ import unicode_literals, absolute_import, division

from django import forms
from django.core.mail import send_mail
from django.forms.widgets import Input
from django.utils.translation import ugettext_lazy as _
from .models import Starnight, StarnightApplicant


class EmailInput(Input):

    input_type = 'email'


class ApplicationForm(forms.ModelForm):

    date = forms.ModelChoiceField(label=_('Datum'),
                                  queryset=Starnight.objects.filter(
                                      is_registrable=True), empty_label=None)

    email = forms.EmailField(label=_('Email'), widget=EmailInput, required=True)

    def send_email_applicant(self):

        sender = "E.Hanko@uva.nl"
        subject = "Aanmelding voor API sterrenkijkavond"

        date = self.cleaned_data['date']

        recipients = [self.cleaned_data['email']]

        number = self.cleaned_data['number']

        newsletter = self.cleaned_data['newsletter']
        if newsletter == 0: choice = 'niet'
        if newsletter == 1: choice = 'wel'

        message = """\
Goedendag,

U heeft zich aangemeld voor de komende API-sterrenkijkavond ({date}).
U heeft aangegeven dat {visitors} bezoekers deze avond zullen bijwonen.
Vanaf heden ontvangt u {choice} de nieuwsbrief, waarmee u op de hoogte
blijft van de laatste ontwikkelingen omtrent de API-sterrenkijkavonden.

Tot ziens!

Met vriendelijke groet,
Esther Hanko MA
Anton Pannekoek Instituut voor Sterrenkunde
E-mail: E.Hanko@uva.nl
Telnr: +31 (0)20-5258316
        """.format(date=date, visitors=number, choice=choice)

        send_mail(subject, message, sender, recipients, fail_silently=False)


    def send_email_organiser(self):

        sender = "webadmin.api@gmail.com"
        subject = "Nieuwe aanmelding voor de API sterrenkijkavond"

        recipients = ['E.Hanko@uva.nl']
###     recipients = ['martin@science.uva.nl']

        date = self.cleaned_data['date']

        naam = self.cleaned_data['name']
        adres = self.cleaned_data['address']
        postcode = self.cleaned_data['zipcode']
        plaats = self.cleaned_data['city']
        email = self.cleaned_data['email']
        number = self.cleaned_data['number']

        newsletter = self.cleaned_data['newsletter']
        if newsletter == 0: choice = 'Nee'
        if newsletter == 1: choice = 'Ja'

        message = """\
Goedendag,

Er is een nieuwe aanmelding binnen voor de komende \
API-sterrenkijkavond ({date}).
Dit zijn de gegevens:

Naam:     {name}
Adres:    {address}
Postcode: {zipcode}
Plaats:   {city}
E-mail:   {email}

Aantal mensen dat komt: {number}

Wil nieuwsbrief ontvangen: {choice}

Met vriendelijke groet,
Het Apiweb Team
        """.format(date=date, name=naam, address=adres, zipcode=postcode,
                   city=plaats, email=email, number=number, choice=choice)

        send_mail(subject, message, sender, recipients, fail_silently=False)
#
# Just for backup
#
        recipients = ['m.h.m.heemskerk@uva.nl']
        send_mail(subject, message, sender, recipients, fail_silently=False)


    class Meta:
        model = StarnightApplicant
        widgets = {'activity': forms.RadioSelect()}
        fields = ['date', 'name', 'address', 'zipcode', 'city', 'email',
                  'newsletter', 'number']
