from __future__ import unicode_literals, absolute_import, division

from django.views.generic import TemplateView, CreateView
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Sum
from ..news.models import Press, Event
from .models import Starnight, Activity, StarnightApplicant
from .forms import ApplicationForm


class EducatieView(TemplateView):
    template_name = 'publiek/educatie.html'

class LinksView(TemplateView):
    template_name = 'publiek/links.html'

class StudieView(TemplateView):
    template_name = 'publiek/studie.html'



class OnderzoekView(TemplateView):
    template_name = 'publiek/onderzoek/index.html'

class PlanetsView(TemplateView):
    template_name = 'publiek/onderzoek/planets.html'

class StarsView(TemplateView):
    template_name = 'publiek/onderzoek/stars.html'

class LiveView(TemplateView):
    template_name = 'publiek/onderzoek/live.html'

class ExplosionsView(TemplateView):
    template_name = 'publiek/onderzoek/explosions.html'

class AccretionView(TemplateView):
    template_name = 'publiek/onderzoek/accretion.html'

class CompactsView(TemplateView):
    template_name = 'publiek/onderzoek/compacts.html'

class ExtremeView(TemplateView):
    template_name = 'publiek/onderzoek/extreme.html'


class PubliekView(TemplateView):
    template_name = 'publiek/index.html'

    def get_context_data(self, **kwargs):
        context = super(PubliekView, self).get_context_data(**kwargs)

        context['press'] = Press.objects.current(days=-180).order_by(
            '-date').filter(language='nl')
        context['events'] = Event.objects.current(days=180).filter(
            language='nl')
        return context


class StarnightsView(TemplateView):
    template_name = 'publiek/starnights/index.html'


class ApplicationFormView(CreateView):
    form_class = ApplicationForm
    template_name = 'publiek/starnights/applicationform.html'
    success_url = reverse_lazy('publiek:thanks')

    def form_valid(self, form):
        form.send_email_applicant()
        form.send_email_organiser()
        return super(ApplicationFormView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ApplicationFormView, self).get_context_data(**kwargs)

        register_open = False
        register_full = False

        nights = Starnight.objects.filter(is_registrable=True)
        if nights.exists():
            register_open = True
            nr_people = 0
            for night in nights:
                stardate = night.date
                star_dict = StarnightApplicant.objects.filter(
                    date__date=stardate).aggregate(Sum('number'))
                if star_dict['number__sum'] is not None:
                    nr_people = star_dict['number__sum']
                if nr_people >= night.max_people: register_full = True
                break

        if register_open and not register_full:
            people1 = {}
            people2 = {}
            people3 = {}
            nr_spots = 0
            nr_activities = 0
            for activity in Activity.objects.all():
                if activity.nr % 10 == 0:
                    if activity.is_in_block1: people1[activity.nr] = ""
                    if activity.is_in_block2: people2[activity.nr] = ""
                    if activity.is_in_block3: people3[activity.nr] = ""
                elif activity.nr > 0:

                    if activity.is_in_block1:
                        nr_people = 0
                        nr_activities += 1
                        star_dict = StarnightApplicant.objects.filter(
                            date__date=stardate).filter(
                                slot1__nr=activity.nr).aggregate(Sum('number'))
                        if star_dict['number__sum'] is not None:
                            nr_people = star_dict['number__sum']
                        if activity.max_people - nr_people == 1:
                            people1[activity.nr] = " 1 seat available"
                            nr_spots += 1
                        elif activity.max_people - nr_people < 1:
                            people1[activity.nr] = " Full "
                        else:
                            people1[activity.nr] = str(activity.max_people -
                                                       nr_people) + \
                                " seats available"
                            nr_spots += activity.max_people - nr_people

                    if activity.is_in_block2:
                        nr_people = 0
                        nr_activities += 1
                        star_dict = StarnightApplicant.objects.filter(
                            date__date=stardate).filter(
                                slot2__nr=activity.nr).aggregate(Sum('number'))
                        if star_dict['number__sum'] is not None:
                            nr_people = star_dict['number__sum']
                        if activity.max_people - nr_people == 1:
                            people2[activity.nr] = " 1 seat available"
                            nr_spots += 1
                        elif activity.max_people - nr_people < 1:
                            people2[activity.nr] = " Full "
                        else:
                            people2[activity.nr] = str(activity.max_people -
                                                       nr_people) + \
                                " seats available"
                            nr_spots += activity.max_people - nr_people

                    if activity.is_in_block3:
                        nr_people = 0
                        nr_activities += 1
                        star_dict = StarnightApplicant.objects.filter(
                            date__date=stardate).filter(
                                slot3__nr=activity.nr).aggregate(Sum('number'))
                        if star_dict['number__sum'] is not None:
                            nr_people = star_dict['number__sum']
                        if activity.max_people - nr_people == 1:
                            people3[activity.nr] = " 1 seat available"
                            nr_spots += 1
                        elif activity.max_people - nr_people < 1:
                            people3[activity.nr] = " Full "
                        else:
                            people3[activity.nr] = str(activity.max_people -
                                                       nr_people) + \
                                " seats available"
                            nr_spots += activity.max_people - nr_people

            if nr_spots < 1 and nr_activities > 0: register_full = True

            context['people1'] = sorted(people1.items())
            context['people2'] = sorted(people2.items())
            context['people3'] = sorted(people3.items())

        context['register_on'] = register_open
        context['register_full'] = register_full

        return context


class ThanksView(TemplateView):
    template_name = 'publiek/starnights/thanks.html'
