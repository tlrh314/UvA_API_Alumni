from __future__ import unicode_literals, absolute_import, division

from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, RedirectView
from django.http import Http404
from .models import Sticky
from ...settings import NEWS_LANGUAGES
from ..news.models import Press, Event, Colloquium, Pizza
from ..jobs.models import Job
import datetime
import operator


# Mainviews in api_urls.py

class MainView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)

        context['stickies'] = Sticky.objects.filter(
            visible=True).order_by('priority')

        EVENT_TYPES = dict(event='Event', colloquium='Colloquium',
                           pizza='Lunch talk')

        # show the five most recent jobs in the side bar
        context['jobs'] = Job.objects.current()[0:5]

        # Get the three most recent news items, up to 3 months in the past
        context['press'] = Press.objects.current(days=-180).order_by(
            '-date').filter(language__in=NEWS_LANGUAGES)[0:3]
        events = {}
        # Get the first upcoming events within 6 months

        events['event'] = Event.objects.current(days=180)[0:5]
        # Get the first upcoming colloquia and pizza lunch talks;

        # don't obtain talks more than 6 months in the future

        events['colloquium'] = Colloquium.objects.current(days=180)[0:5]
        events['pizza'] = Pizza.objects.current(days=180)[0:5]
        # sort by date

        context['events'] = []
        for key in ('event', 'colloquium', 'pizza'):
            for event in events[key]:
                event.type = EVENT_TYPES[key]
                context['events'].append(event)
        context['events'].sort(key=operator.methodcaller('date_time'))
        context['events'] = context['events'][0:3]
        return context


class SitemapView(TemplateView):
    template_name = 'main/sitemap.html'

class AboutView(TemplateView):
    template_name = 'main/about.html'

class TwentyFourSevenView(TemplateView):
    template_name = 'main/247.html'


# Redirect views

class HomeView(RedirectView):
    permanent = True

    def get_redirect_url(self, **kwargs):
        return reverse('home-page')


class ScatterView(RedirectView):
    permanent = True
    url = "http://www.iaa.es/scattering/%(arguments)s"


class LowercaseView(RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        return self.request.path.lower()


class DetailRedirectView(RedirectView):
    """Redirection view for items that used to have a unique slug.

    Items that were identified by their unique slug, are now
    identified by their (database) id; the slug is no longer unique.

    To redirect old links, the (first) item that matches a slug is
    fetched from the database, and the corresponding absolute url
    created using the the id and slug, to which the user is then
    redirected.

    The model is the essential class-based attribute, and can most
    easily be given through as_view() in the url configuration, for
    example:

        url(r'^pizza/detail/(?P<slug>[-\w]+)/$',
            view=RedirectView.as_view(model=Pizza),
            name='pizza-redirect'),

    """

    model = None
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        item = self.model.objects.filter(slug=kwargs['slug']).first()
        if not item:
            try:
                item = self.model.objects.filter(pk=kwargs['slug']).first()
            except ValueError as exc:
                if str(exc).startswith("invalid literal for int()"):
                    raise Http404
                raise
        if item:
            return item.get_absolute_url()
        else:
            raise Http404
