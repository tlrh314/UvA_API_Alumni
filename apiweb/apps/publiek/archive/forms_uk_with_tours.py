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

    UK_CHOICES = (
        ("", '-----'),
        (0, 'No'),
        (1, 'Yes'),
    )

    NR_CHOICES = (
        (1, ' 1'), (2, ' 2'), (3, ' 3'), (4, ' 4'), (5, ' 5'),
        (6, ' 6'), (7, ' 7'), (8, ' 8'), (9, ' 9'), (10, '10'),
    )


    name = forms.CharField(label=_('Name'))
    address = forms.CharField(label=_('Street and number'))
    zipcode = forms.CharField(label=_('Postal code'), max_length=40)
    city = forms.CharField(label=_('City'), max_length=40)

    newsletter = forms.IntegerField(label=_('Newsletter'),
                                    widget=forms.Select(choices=UK_CHOICES))
    number = forms.IntegerField(label=_('Number of people'),
                                widget=forms.Select(choices=NR_CHOICES))

    date = forms.ModelChoiceField(label=_('Date'),
                                  queryset=Starnight.objects.filter(
                                      is_registrable=True), empty_label=None)

    email = forms.EmailField(label=_('E-mail'), widget=EmailInput,
                             required=True)

    slot1 = forms.ModelChoiceField(label=_('Tour between'),
                                   queryset=Activity.objects.filter(
                                       is_in_block1=True).order_by('nr'),
                                   widget=forms.RadioSelect, initial='10')


    def send_email_applicant(self):

        sender = "E.Hanko@uva.nl@uva.nl"
        subject = "Subscribtion for the API stargazing night"

        date = self.cleaned_data['date']

        recipients = [self.cleaned_data['email']]

        number = self.cleaned_data['number']

        newsletter = self.cleaned_data['newsletter']
        if newsletter == 0: choice = 'not'
        if newsletter == 1: choice = ''

        slot1 = self.cleaned_data['slot1']

        message = """\
Good day,

You have subscribed to the next API stargazing night ({date}).
You have indicated that {visitors} people will come to this night.
From now on you will {choice} receive the newsletter, which informs
you of the latest developments concerning de API stargazing nights.

You have choosen for the following activity:

Tour between : {slot1}

See you later!

Best regards,
Esther Hanko MA
Anton Pannekoek Instutute for Astronomy
E-mail: E.Hanko@uva.nl
Phone: +31 (0)20-5258316
        """.format(date=date, visitors=number, choice=choice, slot1=slot1)

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

        slot1 = self.cleaned_data['slot1']

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

Gekozen activiteit:

Rondleiding tussen : {slot1}

Met vriendelijke groet,
Het Apiweb Team
        """.format(date=date, name=naam, address=adres, zipcode=postcode,
                   city=plaats, email=email, number=number, choice=choice,
                   slot1=slot1)

        send_mail(subject, message, sender, recipients, fail_silently=False)
#
# Just for backup
#
        recipients = ['m.h.m.heemskerk@uva.nl']
        send_mail(subject, message, sender, recipients, fail_silently=False)


    def clean(self):

        cleaned_data = self.cleaned_data

        slot1 = str(cleaned_data.get("slot1"))

        if slot1 == "None":
            raise forms.ValidationError("You did not choose any activity!")

        msg = "There are not enough seats available"

        night = str(cleaned_data.get("date"))
        number = cleaned_data.get("number")

        data = str(cleaned_data.get("slot1"))
        if data != "None":
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

        return cleaned_data


    class Meta:
        model = StarnightApplicant
        widgets = {'activity': forms.RadioSelect()}
        fields = ['date', 'name', 'address', 'zipcode', 'city', 'email',
                  'newsletter', 'number', 'slot1']
