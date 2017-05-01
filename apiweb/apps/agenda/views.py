from __future__ import unicode_literals, absolute_import, division

import time
import calendar
from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.http import Http404
from django.views.generic import TemplateView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from ..news.models import Press, Event, Colloquium, Pizza
from ..people.models import Person
from .models import Entry
from .forms import EntryForm


mnames = "January February March April May June July August September "\
         "October November December"
mnames = mnames.split()


def get_year(year):
    if year is not None:
        year = int(year)
    else:
        year = time.localtime()[0]
    return year

def get_month(month):
    if month is not None:
        month = int(month)
    else:
        month = time.localtime()[1]
    return month

def get_day(day):
    if day is not None:
        day = int(day)
    else:
        day = time.localtime()[2]
    return day

def get_change(change, year, month, day):
    # apply next / previous change
    if change == "next":
        mod = 1
    elif change == "prev":
        mod = -1
    else:
        mod = 0

    if day is None:
        now, mdelta = date(year, month, 15), timedelta(days=30)
        year, month = (now+mod*mdelta).timetuple()[:2]
        return (year, month, None)
    else:
        now, mdelta = date(year, month, day), timedelta(days=7)
        year, month, day = (now+mod*mdelta).timetuple()[:3]
        return (year, month, day)


class Item(object):
    """Sample item."""
    def __init__(self, type, attr, link, tooltip):
        self.type = type
        self.attr = attr
        self.link = link
        self.tooltip = tooltip


class IndexView(TemplateView):
    """Main listing, years and months; three years per page."""

    template_name = 'agenda/index.html'

    def get_lst(self):
        # create a list of months for each year,
        # indicating ones that contain entries and current
        lst = []
        nowy, nowm = time.localtime()[:2]
        for y in [self.year, self.year+1, self.year+2]:
            mlst = []
            for n, month in enumerate(mnames):
                # are there entry(s) for this month; current month?
                entry = current = False
                entries = Entry.objects.filter(date__year=y, date__month=n+1)
                entries = entries.filter(creator=self.request.user)

                if entries:
                    entry = True
                if y == nowy and n+1 == nowm:
                    current = True
                mlst.append(dict(n=n+1, name=month, entry=entry,
                                 current=current))
            lst.append((y, mlst))
        return lst

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        self.year = get_year(self.kwargs.get('year', None))

        context['year'] = self.year
        context['years'] = self.get_lst()
        context['user'] = self.request.user
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)


class MonthView(TemplateView):
    """Listing of days in month."""

    template_name = 'agenda/month.html'

    def get_lst(self):

        # init variables
        cal = calendar.Calendar()
        month_days = cal.itermonthdays(self.year, self.month)
        today = date.today()
        week = 0
        entries = []
        lst = [[]]

        # make month lists containing list of days for each week
        # each day tuple will contain list of entries and 'current' indicator
        for day in month_days:
            current = False   # current day?
            entries = []
            if day:
                month_day = date(self.year, self.month, day)

                sub_entries = Entry.objects.filter(
                    Q(date=month_day) | (Q(date__lt=month_day) &
                                         Q(date_end__gte=month_day)),
                    Q(creator=self.request.user))

                attribute = ""
                for sub_entry in sub_entries:
                    if sub_entry.is_public:
                        attribute = "red"
                    else:
                        attribute = "green"
                    item = Item(sub_entry.title, attribute,
                                sub_entry.get_absolute_url,
                                sub_entry.title)

                    entries.append(item)


                sub_entries = Entry.objects.filter(
                    Q(date=month_day) | (Q(date__lt=month_day) &
                                         Q(date_end__gte=month_day)),
                    Q(is_public=True)).exclude(creator=self.request.user)

                attribute = ""
                for sub_entry in sub_entries:
                    item = Item(sub_entry.title, attribute,
                                sub_entry.get_absolute_url,
                                sub_entry.title)
                    entries.append(item)


                sub_entries = Event.objects.filter(
                    Q(date=month_day) | (Q(date__lt=month_day) &
                                         Q(date_end__gte=month_day)),
                    Q(visible=True))


                attribute = ""
                for sub_entry in sub_entries:
                    item = Item(sub_entry.title, attribute,
                                sub_entry.get_absolute_url,
                                sub_entry.title)
                    entries.append(item)


                sub_entries = Pizza.objects.filter(date=month_day,
                                                   visible=True)

                attribute = ""
                for sub_entry in sub_entries:
                    item = Item("Lunch Talk", attribute,
                                sub_entry.get_absolute_url,
                                sub_entry.speaker + ': ' + sub_entry.title)
                    entries.append(item)


                sub_entries = Colloquium.objects.filter(date=month_day,
                                                        visible=True)

                attribute = ""
                for sub_entry in sub_entries:
                    item = Item("Colloquium", attribute,
                                sub_entry.get_absolute_url,
                                sub_entry.speaker + ': ' + sub_entry.title)
                    entries.append(item)


                sub_entries = Press.objects.filter(date=month_day,
                                                   visible=True)

                attribute = ""
                for sub_entry in sub_entries:
                    item = Item("Press Release", attribute,
                                sub_entry.get_absolute_url,
                                sub_entry.title)
                    entries.append(item)


                this_month, this_day = month_day.timetuple()[1:3]
                sub_entries = Person.objects.filter(
                    birth_date__month=this_month,
                    birth_date__day=this_day,
                    show_person=True)
                attribute = ""
                for sub_entry in sub_entries:
                    item = Item("Birthday", attribute,
                                sub_entry.get_absolute_url,
                                "Happy birthday" + " " + sub_entry.full_name)
                    entries.append(item)


                if month_day == today: current = True

            lst[week].append((day, entries, current))
            if len(lst[week]) == 7:
                lst.append([])
                week += 1
        return lst

    def get_context_data(self, **kwargs):
        context = super(MonthView, self).get_context_data(**kwargs)

        day = None
        month = get_month(self.kwargs.get('month', None))
        year = get_year(self.kwargs.get('year', None))

        change = self.kwargs.get('change', None)

        self.year, self.month, _ = get_change(change, year, month, day)

        context['year'] = self.year
        context['month'] = self.month
        context['mname'] = mnames[self.month-1]
        context['month_days'] = self.get_lst()
        context['user'] = self.request.user
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MonthView, self).dispatch(*args, **kwargs)


class WeekView(TemplateView):
    """Listing of days in week."""

    template_name = 'agenda/week.html'

    def get_lst(self):

        today = date.today()
        this_day = date(self.year, self.month, self.day)
        week_day = this_day.weekday()
        start_delta = timedelta(days=week_day)
        start_of_week = this_day - start_delta
        week_dates = [start_of_week + timedelta(days=i) for i in range(7)]

        # init variables
        lst = []
        entries = []

        # each day list will contain list of entries and 'current' indicator
        for week_day in week_dates:
            current = False   # current day?
            entries = []
            if week_day:

                sub_entries = Entry.objects.filter(
                    Q(date=week_day) | (Q(date__lt=week_day) &
                                        Q(date_end__gte=week_day)),
                    Q(creator=self.request.user))

                attribute = ""
                for sub_entry in sub_entries:
                    if sub_entry.is_public:
                        attribute = "red"
                    else:
                        attribute = "green"
                    item = Item(sub_entry.title, attribute,
                                sub_entry.get_absolute_url,
                                "Created by" + " " +
                                sub_entry.creator.get_full_name())
                    entries.append(item)


                sub_entries = Entry.objects.filter(
                    Q(date=week_day) | (Q(date__lt=week_day) &
                                        Q(date_end__gte=week_day)),
                    Q(is_public=True)).exclude(creator=self.request.user)

                attribute = ""
                for sub_entry in sub_entries:
                    item = Item(sub_entry.title, attribute,
                                sub_entry.get_absolute_url,
                                "Created by" + " " +
                                sub_entry.creator.get_full_name())
                    entries.append(item)


                sub_entries = Event.objects.filter(
                    Q(date=week_day) | (Q(date__lt=week_day) &
                                        Q(date_end__gte=week_day)),
                    Q(visible=True))

                attribute = ""
                for sub_entry in sub_entries:
                    if sub_entry.time:
                        item = Item(sub_entry.title, attribute,
                                    sub_entry.get_absolute_url,
                                    sub_entry.time.strftime(" %H:%M - ") +
                                    sub_entry.location)
                    else:
                        item = Item(sub_entry.title, attribute,
                                    sub_entry.get_absolute_url,
                                    sub_entry.location)
                    entries.append(item)


                sub_entries = Pizza.objects.filter(date=week_day, visible=True)

                attribute = ""
                for sub_entry in sub_entries:
                    if sub_entry.time:
                        item = Item("Lunch Talk - " + sub_entry.speaker +
                                    ': ' + sub_entry.title,
                                    attribute,
                                    sub_entry.get_absolute_url,
                                    sub_entry.time.strftime(" %H:%M - ") +
                                    sub_entry.location)
                    else:
                        item = Item("Lunch Talk - " + sub_entry.speaker +
                                    ': ' + sub_entry.title,
                                    attribute,
                                    sub_entry.get_absolute_url,
                                    sub_entry.location)
                    entries.append(item)


                sub_entries = Colloquium.objects.filter(date=week_day,
                                                        visible=True)

                attribute = ""
                for sub_entry in sub_entries:
                    if sub_entry.time:
                        item = Item("Colloquium - " + sub_entry.speaker +
                                    ': ' + sub_entry.title,
                                    attribute,
                                    sub_entry.get_absolute_url,
                                    sub_entry.time.strftime(" %H:%M - ") +
                                    sub_entry.location)
                    else:
                        item = Item("Colloquium - " + sub_entry.speaker +
                                    ': ' + sub_entry.title,
                                    attribute,
                                    sub_entry.get_absolute_url,
                                    sub_entry.location)
                    entries.append(item)


                sub_entries = Press.objects.filter(date=week_day, visible=True)

                attribute = ""
                for sub_entry in sub_entries:
                    item = Item("Press Release - " + sub_entry.title,
                                attribute, sub_entry.get_absolute_url, " ")
                    entries.append(item)


                this_month, this_day = week_day.timetuple()[1:3]
                sub_entries = Person.objects.filter(
                    birth_date__month=this_month,
                    birth_date__day=this_day,
                    show_person=True)
                attribute = ""
                for sub_entry in sub_entries:
                    item = Item("Happy birthday" + " " + sub_entry.full_name,
                                attribute, sub_entry.get_absolute_url,
                                #" ")
                                sub_entry.age)
                    entries.append(item)

                if week_day == today: current = True

                this_year, this_month, this_day = week_day.timetuple()[:3]

            lst.append((week_day, this_year, this_month, this_day, entries,
                        current))
        return lst


    def get_context_data(self, **kwargs):
        context = super(WeekView, self).get_context_data(**kwargs)

        day = get_day(self.kwargs.get('day', None))
        month = get_month(self.kwargs.get('month', None))
        year = get_year(self.kwargs.get('year', None))

        change = self.kwargs.get('change', None)

        self.year, self.month, self.day = get_change(change, year, month, day)

        context['year'] = self.year
        context['month'] = self.month
        context['day'] = self.day
        context['week_days'] = self.get_lst()
        context['user'] = self.request.user
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WeekView, self).dispatch(*args, **kwargs)


class EntryDetailView(DetailView):
    template_name = 'agenda/entry_detail.html'
    model = Entry

    def get_object(self):
        object = super(EntryDetailView, self).get_object()
        if not object.is_public and not object.creator == self.request.user:
            raise Http404
        return object

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EntryDetailView, self).dispatch(*args, **kwargs)


class EntryCreateView(CreateView):
    """Create a new entry."""

    form_class = EntryForm
    template_name = 'agenda/entry_create.html'

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(EntryCreateView, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        day = int(self.kwargs.get('day'))
        year = int(self.kwargs.get('year'))
        month = int(self.kwargs.get('month'))
        initial['date'] = date(year, month, day)
        return initial

    def get_context_data(self, *args, **kwargs):
        context = super(EntryCreateView, self).get_context_data(*args, **kwargs)
        context['day'] = self.kwargs.get('day', None)
        context['year'] = self.kwargs.get('year', None)
        context['month'] = self.kwargs.get('month', None)
        return context

    def get_success_url(self):
        return reverse("agenda:entry-detail",
                       kwargs={'pk': self.object.pk,
                               'slug': self.object.slug})

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(EntryCreateView, self).form_valid(form)

#   def form_valid(self, form):
#       self.object = form.save(commit=False)
#       self.object.creator = self.request.user
#       self.object.save()
#       return HttpResponseRedirect(self.get_success_url())

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EntryCreateView, self).dispatch(*args, **kwargs)


class EntryUpdateView(UpdateView):
    """Update an old entry."""

    model = Entry
    form_class = EntryForm
    template_name = 'agenda/entry_update.html'

    def get_object(self):
        object = super(EntryUpdateView, self).get_object()
        if object.creator != self.request.user:
            raise Http404
        return object

    def get_success_url(self):
        return reverse("agenda:entry-detail",
                       kwargs={'pk': self.object.pk,
                               'slug': self.object.slug})

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(EntryUpdateView, self).form_valid(form)

#   def form_valid(self, form):
#       self.object = form.save(commit=False)
#       self.object.creator = self.request.user
#       self.object.save()
#       return HttpResponseRedirect(self.get_success_url())

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EntryUpdateView, self).dispatch(*args, **kwargs)


class EntryDeleteView(DeleteView):
    """Delete entry for this slug."""

    # template_name_suffix = '_delete' or
    template_name = 'agenda/entry_delete.html'
    model = Entry

    def get_object(self):
        object = super(EntryDeleteView, self).get_object()
        if object.creator != self.request.user:
            raise Http404
        return object

    def get_success_url(self):
        return reverse("agenda:month", args=(self.object.date.year,
                                             self.object.date.month))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EntryDeleteView, self).dispatch(*args, **kwargs)
