from __future__ import unicode_literals, absolute_import, division

from django import forms
from django.core.mail import send_mail
from django.forms.widgets import Input
from django.utils.translation import ugettext_lazy as _
from django.db.models import Sum
from .models import Starnight, Activity, StarnightApplicant


class EmailInput(Input):

    input_type = 'email'


class ApplicationForm(forms.ModelForm):

    date = forms.ModelChoiceField(label=_('Datum'),
                                  queryset=Starnight.objects.filter(
                                      is_registrable=True), empty_label=None)

    email = forms.EmailField(label=_('Email'), widget=EmailInput, required=True)

    slot1 = forms.ModelChoiceField(label=_('Activiteit 19:00 - 19:45'),
                                   queryset=Activity.objects.filter(
                                       is_in_block1=True).order_by('nr'),
                                   widget=forms.RadioSelect, initial='0')

    slot2 = forms.ModelChoiceField(label=_('Activiteit 20:00 - 20:45'),
                                   queryset=Activity.objects.filter(
                                       is_in_block2=True).order_by('nr'),
                                   widget=forms.RadioSelect, initial='0')

    slot3 = forms.ModelChoiceField(label=_('Activiteit 21:00 - 21:45'),
                                   queryset=Activity.objects.filter(
                                       is_in_block3=True).order_by('nr'),
                                   widget=forms.RadioSelect, initial='0')


    def send_email_applicant(self):

        sender = "E.Hanko@uva.nl"
        subject = "Aanmelding voor API sterrenkijkavond"

        date = self.cleaned_data['date']

        recipients = [self.cleaned_data['email']]

        number = self.cleaned_data['number']

        newsletter = self.cleaned_data['newsletter']
        if newsletter == 0: choice = 'niet'
        if newsletter == 1: choice = 'wel'

        slot1 = self.cleaned_data['slot1']
        slot2 = self.cleaned_data['slot2']
        slot3 = self.cleaned_data['slot3']

        message = """\
Goedendag,

U heeft zich aangemeld voor de komende API-sterrenkijkavond ({date}).
U heeft aangegeven dat {visitors} bezoekers deze avond zullen bijwonen.
Vanaf heden ontvangt u {choice} de nieuwsbrief, waarmee u op de hoogte
blijft van de laatste ontwikkelingen omtrent de API-sterrenkijkavonden.

U heeft gekozen voor de volgende activiteiten:

Tussen 19:00 - 19:45 : {slot1}
Tussen 20:00 - 20:45 : {slot2}
Tussen 21:00 - 21:45 : {slot3}

Tot ziens!

Met vriendelijke groet,
Esther Hanko MA
Anton Pannekoek Instituut voor Sterrenkunde
E-mail: E.Hanko@uva.nl
Telnr: +31 (0)20-5258316
        """.format(date=date, visitors=number, choice=choice,
                   slot1=slot1, slot2=slot2, slot3=slot3)

        send_mail(subject, message, sender, recipients, fail_silently=False)


    def send_email_organiser(self):

        sender = "webadmin.api@gmail.com"
        subject = "Nieuwe aanmelding voor de API sterrenkijkavond"

        recipients = ['E.Hanko@uva.nl']
###        recipients = ['martin@science.uva.nl']

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

        slot1 = self.cleaned_data['slot1']
        slot2 = self.cleaned_data['slot2']
        slot3 = self.cleaned_data['slot3']

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

Gekozen activiteiten:

Tussen 19:00 - 19:45 : {slot1}
Tussen 20:00 - 20:45 : {slot2}
Tussen 21:00 - 21:45 : {slot3}

Met vriendelijke groet,
Het Apiweb Team
        """.format(date=date, name=naam, address=adres, zipcode=postcode,
                   city=plaats, email=email, number=number, choice=choice,
                   slot1=slot1, slot2=slot2, slot3=slot3)

        send_mail(subject, message, sender, recipients, fail_silently=False)
#
# Just for backup
#
        recipients = ['m.h.m.heemskerk@uva.nl']
        send_mail(subject, message, sender, recipients, fail_silently=False)


    def clean(self):

        cleaned_data = self.cleaned_data

        slot1 = str(cleaned_data.get("slot1"))
        slot2 = str(cleaned_data.get("slot2"))
        slot3 = str(cleaned_data.get("slot3"))

        if slot1 == slot2 and slot2 == slot3 and slot1 == "Geen":
            raise forms.ValidationError("U heeft geen activiteit gekozen!")

        if slot1 == slot2 and slot1 != "Geen":
            raise forms.ValidationError("U heeft eenzelfde activiteit gekozen!")

        if slot1 == slot3 and slot1 != "Geen":
            raise forms.ValidationError("U heeft eenzelfde activiteit gekozen!")

        if slot2 == slot3 and slot2 != "Geen":
            raise forms.ValidationError("U heeft eenzelfde activiteit gekozen!")

        msg = "Er zijn niet genoeg plaatsen"

        night = str(cleaned_data.get("date"))
        number = cleaned_data.get("number")

        data = str(cleaned_data.get("slot1"))
        if data != "Geen":
            activities = Activity.objects.filter(name=data)
            max_people = activities[0].max_people

            nr_people = 0
            star_dict = StarnightApplicant.objects.filter(
                date__date=night).filter(
                    slot1__name=data).aggregate(Sum('number'))
            if star_dict['number__sum'] is not None:
                nr_people = star_dict['number__sum']

            if max_people - nr_people - number < 0:
                self._errors["slot1"] = self.error_class([msg])
                del cleaned_data["slot1"]

        data = str(cleaned_data.get("slot2"))
        if data != "Geen":
            activities = Activity.objects.filter(name=data)
            max_people = activities[0].max_people

            nr_people = 0
            star_dict = StarnightApplicant.objects.filter(
                date__date=night).filter(
                    slot2__name=data).aggregate(Sum('number'))
            if star_dict['number__sum'] is not None:
                nr_people = star_dict['number__sum']

            if max_people - nr_people - number < 0:
                self._errors["slot2"] = self.error_class([msg])
                del cleaned_data["slot2"]

        data = str(cleaned_data.get("slot3"))
        if data != "Geen":
            activities = Activity.objects.filter(name=data)
            max_people = activities[0].max_people

            nr_people = 0
            star_dict = StarnightApplicant.objects.filter(
                date__date=night).filter(
                    slot3__name=data).aggregate(Sum('number'))
            if star_dict['number__sum'] is not None:
                nr_people = star_dict['number__sum']

            if max_people - nr_people - number < 0:
                self._errors["slot3"] = self.error_class([msg])
                del cleaned_data["slot3"]

        return cleaned_data


    class Meta:
        model = StarnightApplicant
        widgets = {'activity': forms.RadioSelect()}
        fields = ['date', 'name', 'address', 'zipcode', 'city', 'email',
                  'newsletter', 'number', 'slot1', 'slot2', 'slot3']
