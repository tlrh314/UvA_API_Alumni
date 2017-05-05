from __future__ import unicode_literals, absolute_import, division

from django.views.generic import TemplateView, DetailView, ListView
from .models import BachelorProject, MasterProject, CourseTopic


class BachelorProjectView(DetailView):
    template_name = 'education/projects/bachelor/projects_detail.html'
    model = BachelorProject


class MasterProjectView(DetailView):
    template_name = 'education/projects/master/projects_detail.html'
    model = MasterProject


class ProjectsBachelorView(ListView):
    template_name = 'education/projects/bachelor/projects_list.html'
    queryset = BachelorProject.objects.current(year=[2, 3])

    def get_context_data(self, **kwargs):
        context = super(ProjectsBachelorView, self).get_context_data(**kwargs)

        context['second_year_count'] = BachelorProject.objects.current(
            year=2).count
        context['third_year_count'] = BachelorProject.objects.current(
            year=3).count

        return context


class ProjectsMasterView(ListView):
    template_name = 'education/projects/master/projects_list.html'
    queryset = MasterProject.objects.current()


class CourseView(DetailView):
    template_name = 'education/course/topic_detail.html'
    model = CourseTopic


class ProjectsView(TemplateView):
    template_name = 'education/projects/index.html'


class BachelorView(TemplateView):
    template_name = 'education/bachelor.html'

    def get_context_data(self, **kwargs):
        context = super(BachelorView, self).get_context_data(**kwargs)

        context['classes'] = {}
        for year in (1, 2, 3):
            context['classes'][year] = CourseTopic.objects.filter(
                semester__in=[year*2-1, year*2]).order_by('semester')
        return context


class MasterView(TemplateView):
    template_name = 'education/master.html'


class IndexView(TemplateView):
    template_name = 'education/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        context['classes'] = {}
        for year in (1, 2, 3):
            context['classes'][year] = CourseTopic.objects.filter(
                semester__in=[year*2-1, year*2])
        return context
