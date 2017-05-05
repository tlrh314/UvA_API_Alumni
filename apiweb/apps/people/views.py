from __future__ import unicode_literals, absolute_import, division

from itertools import chain
from django.views.generic import DetailView, ListView
from django.db.models import Q
from django.views.generic import RedirectView
from django.http import Http404
from .models import Person, Position


class PersonListView(ListView):
    template_name = 'people/person_list.html'
    queryset = Person.objects.all().filter(show_person=True)
    context_object_name = 'person'

    def get_context_data(self, **kwargs):
        context = super(PersonListView, self).get_context_data(**kwargs)
        title_list = 'People at the Anton Pannekoek Institute'
        context['who'] = title_list
        return context


class StaffListView(ListView):
    template_name = 'people/person_list.html'
    # We append (and keep that order) director(s) and (faculty) staff
    directors = Person.objects.filter(show_person=True).filter(
        position__name__iexact='director').order_by('last_name')
    staff = Person.objects.filter(show_person=True).filter(
        position__name__iexact='faculty staff').order_by('last_name')
    context_object_name = 'person'

    def get_queryset(self):
        return list(chain(self.directors, self.staff))

    def get_context_data(self, **kwargs):
        context = super(StaffListView, self).get_context_data(**kwargs)
        context['who'] = 'Staff at the Anton Pannekoek Institute'
        return context


class StudentListView(ListView):
    template_name = 'people/person_list.html'
    # We don't bother with order for master and bachelor students
    queryset = Person.objects.all().filter(show_person=True).filter(
        Q(position__name__iexact='master student') |
        Q(position__name__iexact='bachelor student')).order_by(
                          'last_name')
    context_object_name = 'person'

    def get_context_data(self, **kwargs):
        context = super(StudentListView, self).get_context_data(**kwargs)
        title_list = 'Master students at the Anton Pannekoek Institute'
        context['who'] = title_list
        return context


class PositionListView(ListView):
    template_name = 'people/person_list.html'
    context_object_name = 'person'

    def get_queryset(self):
        queryset = Person.objects.all().filter(show_person=True).filter(
            position__name__iexact=self.position).order_by(
                'last_name')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        title_list = 'Unknowns at the Anton Pannekoek Institute'
        try:
            position = Position.objects.get(name__iexact=self.position)
            plural = position.name + "s"
            if position.plural:
                plural = position.plural
        except Position.DoesNotExist:
            plural = "Unknowns"
        title_list = "{} at the Anton Pannekoek Institute".format(plural)
        context['who'] = title_list
        return context

    def dispatch(self, request, *args, **kwargs):
        self.position = kwargs.get('position', None)
        return super(PositionListView, self).dispatch(request, *args, **kwargs)


class PersonDetailView(DetailView):
    template_name = 'people/person_detail.html'
    queryset = Person.objects.all().filter(show_person=True)
    context_object_name = 'person'


class PositionRedirectView(RedirectView):
    """We redirect old links, but some position type names have changed::

        adjunct = adjunct faculty
        phd = phd student
        developer = software developer

    """
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        typ = kwargs['position']
        if typ == 'adjunct':
            typ = 'adjunct faculty'
        if typ == 'phd':
            typ = 'phd student'
        if typ == 'developer':
            typ = 'software developer'

        item = Position.objects.filter(name__iexact=typ).first()
        if item:
            return item.get_absolute_url()
        else:
            raise Http404
