from __future__ import unicode_literals, absolute_import, division

from django.http import Http404
from django.core.urlresolvers import NoReverseMatch
from django.views.generic import TemplateView, DetailView, ListView
from datetime import datetime
from ...settings import NEWS_LANGUAGES
from .models import Press, Event, Colloquium, Pizza


class IndexView(TemplateView):
    # The use of TemplateView as base may seem a bit odd,
    # since ListView may appear a better choice.
    # The context sent to the template, however, are not
    # a simple queryset, so we can't really use ListView
    # with a queryset. Therefore, the simpler view is
    # used and all the data is supplied in the context
    template_name = 'news/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        context['press'] = Press.objects.current(days=-180).order_by(
            '-date').filter(language__in=NEWS_LANGUAGES)[0:3]
        context['events'] = Event.objects.current(days=180).filter(
            language__in=NEWS_LANGUAGES)[0:3]
        context['pizza'] = Pizza.objects.current(days=180).order_by(
            'date', 'time')[0:3]
        context['colloquium'] = Colloquium.objects.current(days=180).order_by(
            'date', 'time')[0:3]
        return context


class DateOrderedListView(ListView):
    """A view that returns a paginated view of a list of objects,
    ordered by date, but in such a way that:
    - objects after the current date (upcoming events) are ordered
      ascending: from nearest to furthest in the future,
      followed by
    - objects before the current date (past events) are ordered
      descending: from nearest to furthest in the past
    """
    paginate_by = 10
    date_key = 'date'
    order_keys = ('date', 'time')
    order_keys_past = None
    limit_by_date_onoff = False

    # get_queryset needs to return an iterable, not a queryset per se.
    def get_queryset(self):
        now = datetime.now().date()
        queryset = self.model.objects.filter(visible=True)
        if self.limit_by_date_onoff:
            queryset = queryset.filter(
                date_on__lte=now).filter(date_off__gte=now)
        lookups = {'gte': {self.date_key + '__gte': now},
                   'lt': {self.date_key + '__lt': now}}
        if self.order_keys_past is None:
            # Invert the normal ordering keys
            order_keys_past = ["-{}".format(key) for key in self.order_keys]
        else:
            order_keys_past = self.order_keys_past
        q1 = list(queryset.filter(**lookups['gte']).order_by(*self.order_keys))
        q2 = list(queryset.filter(**lookups['lt']).order_by(*order_keys_past))
        return q1+q2


class ColloquiumDetailView(DetailView):
    template_name = 'news/colloquium_detail.html'
    model = Colloquium

class ColloquiumSummaryView(DateOrderedListView):
    paginate_by = 30
    template_name = 'news/colloquium_summary.html'
    model = Colloquium

class ColloquiumView(DateOrderedListView):
    template_name = 'news/colloquium_list.html'
    model = Colloquium

class EventDetailView(DetailView):
    template_name = 'news/event_detail.html'
    model = Event

    def get_object(self):
        try:
            return super(EventDetailView, self).get_object()
        except NoReverseMatch:
            print(self)
            #return reverse('news:events-redirect',
            #               *self.args, **self.kwargs)
            raise

class EventsView(DateOrderedListView):
    template_name = 'news/event_list.html'
    model = Event

class PressDetailView(DetailView):
    """Special detail view, so that special permissions can apply when
        under embargo"""
    template_name = 'news/press_detail.html'
    model = Press

    def get_object(self):
        object = super(PressDetailView, self).get_object()
        if not object.visible and not self.request.user.is_authenticated():
            raise Http404
        return object

class PressView(ListView):
    template_name = 'news/press_list.html'
    model = Press
    paginate_by = 10

    def get_queryset(self):
        now = datetime.now().date()
        queryset = self.model.objects.filter(visible=True).filter(
            date_on__lte=now).order_by('-date').filter(
                language__in=NEWS_LANGUAGES)
        return queryset

class PizzaDetailView(DetailView):
    template_name = 'news/pizza_detail.html'
    model = Pizza

class PizzaAboutView(TemplateView):
    template_name = 'news/pizza_about.html'

class PizzaView(DateOrderedListView):
    template_name = 'news/pizza_list.html'
    model = Pizza
