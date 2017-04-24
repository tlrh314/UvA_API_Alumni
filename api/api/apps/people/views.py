from django.views.generic import DetailView, ListView
from .models import Person
import re


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
    queryset = Person.objects.all().filter(show_person=True).filter(
               position__in=[Person.POSITION['DIRECTOR'],
                             Person.POSITION['STAFF'],
                             Person.POSITION['NOVA']]).order_by(
                            'position', 'last_name')
    context_object_name = 'person'

    def get_context_data(self, **kwargs):
        context = super(StaffListView, self).get_context_data(**kwargs)
        title_list = 'Staff at the Anton Pannekoek Institute'
        context['who'] = title_list
        return context


class StudentListView(ListView):
    template_name = 'people/person_list.html'
    queryset = Person.objects.all().filter(show_person=True).filter(
               position__in=[Person.POSITION['MASTER'],
                             Person.POSITION['BACHELOR']]).order_by(
                            'last_name')
    context_object_name = 'person'

    def get_context_data(self, **kwargs):
        context = super(StudentListView, self).get_context_data(**kwargs)
       #title_list = 'Master/Bachelor students at the Anton Pannekoek Institute'
        title_list = 'Master students at the Anton Pannekoek Institute'
        context['who'] = title_list
        return context


class PositionListView(ListView):
    template_name = 'people/person_list.html'
    context_object_name = 'person'

    def get_queryset(self):
        queryset = Person.objects.all().filter(show_person=True).filter(
                   position=Person.POSITION[self.position.upper()]).order_by(
                           'last_name')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        title_list = 'Unknowns at the Anton Pannekoek Institute'
        if self.position == "adjunct":
            title_list = 'Adjunct Staff at the Anton Pannekoek Institute'
        if self.position == "postdoc":
            title_list = 'Postdocs at the Anton Pannekoek Institute'
        if self.position == "phd":
            title_list = 'Phd Students at the Anton Pannekoek Institute'
        if self.position == "emeritus":
            title_list = 'Emeriti at the Anton Pannekoek Institute'
        if self.position == "guest":
            title_list = 'Visitors at the Anton Pannekoek Institute'
        if self.position == "developer":
            title_list = 'Software Developers at the Anton Pannekoek Institute'
        context['who'] = title_list
        return context

    def dispatch(self, request, *args, **kwargs):
        self.position = kwargs.get('position_type', None)
        return super(PositionListView, self).dispatch(request, *args, **kwargs)


class PersonDetailView(DetailView):
    template_name = 'people/person_detail.html'
    queryset = Person.objects.all().filter(show_person=True)
    context_object_name = 'person'



