from __future__ import unicode_literals, absolute_import, division

from django.views.generic import TemplateView, DetailView, ListView
from .models import ResearchTopic
from .models import Thesis


class LinksView(TemplateView):
    template_name = 'research/links.html'


class GrbSoftwareView(TemplateView):
    template_name = 'research/grb-software.html'

    def get_context_data(self, **kwargs):
        context = super(GrbSoftwareView, self).get_context_data(**kwargs)
        context['category'] = "cosmics"
        context['object_list'] = ResearchTopic.objects.all().filter(
            category='2')
        return context


class IndexView(TemplateView):
    template_name = 'research/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        categories = {}
        categories['compacts'] = 'Neutron stars and black holes'
        categories['cosmics'] = 'Cosmic explosions'
        categories['astroparticles'] = 'Astroparticle physics'
        categories['planets'] = 'Planet formation and exoplanets'
        categories['stars'] = 'Stars, formation and evolution'
        context['categories'] = categories
        return context


class CategoryView(ListView):
    cattypes = {'compacts': 1, 'cosmics': 2, 'astroparticles': 3,
                'planets': 4, 'stars': 5}

    def get_template_names(self):
        # must return a list
        names = ['research/' + self.category_type + '.html']
        return names

    def get_queryset(self):
        queryset = ResearchTopic.objects.all().filter(
            category=self.cattypes[self.category_type])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['category'] = self.category_type
        context['cattitle'] = ResearchTopic.CATEGORY[
            self.cattypes[self.category_type]-1][1]
        return context

    def dispatch(self, request, *args, **kwargs):
        self.category_type = kwargs.get('category_type', None)
        return super(CategoryView, self).dispatch(request, *args, **kwargs)


class TopicView(DetailView):
    cattypes = {'compacts': 1, 'cosmics': 2, 'astroparticles': 3,
                'planets': 4, 'stars': 5}
    template_name = 'research/researchtopic_detail.html'

    def get_queryset(self):
        queryset = ResearchTopic.objects.all().filter(
            category=self.cattypes[self.category_type])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(TopicView, self).get_context_data(**kwargs)
        context['category'] = self.category_type
        context['object_list'] = self.get_queryset()
        context['cattitle'] = ResearchTopic.CATEGORY[
            self.cattypes[self.category_type]-1][1]
        return context

    def dispatch(self, request, *args, **kwargs):
        self.category_type = kwargs.get('category_type', None)
        return super(TopicView, self).dispatch(request, *args, **kwargs)

#
#class SoftwareView(TemplateView):
#    cattypes = {'compacts': 1, 'cosmics': 2, 'astroparticles': 3,
#                'planets': 4, 'stars': 5}
#
#    def get_template_names(self):
#        # must return a list
#        names  = ['research/' + self.category_type + '-software.html']
#        return names
#
#    def get_context_data(self, **kwargs):
#        context = super(SoftwareView, self).get_context_data(**kwargs)
#        context['category'] = self.category_type
#        context['cattitle'] = ResearchTopic.CATEGORY[
#            self.cattypes[self.category_type]-1][1]
#        return context
#
#    def dispatch(self, request, *args, **kwargs):
#        self.category_type = kwargs.get('category_type', None)
#        return super(SoftwareView, self).dispatch(request, *args, **kwargs)
#

class ThesisView(ListView):
    template_name = 'research/thesis_list.html'

    def get_queryset(self):
        self.thesis_type = self.kwargs.get('thesis_type', None)
        queryset = Thesis.objects.all().filter(
            type=self.thesis_type).order_by('-date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ThesisView, self).get_context_data(**kwargs)

        my_title = 'Theses at the Anton Pannekoek Institute'
        if self.thesis_type == "phd":
            my_title = 'Phd theses at the Anton Pannekoek Institute'
        if self.thesis_type == "msc":
            my_title = 'Master theses at the Anton Pannekoek Institute'
        if self.thesis_type == "bsc":
            my_title = 'Bachelor theses at the Anton Pannekoek Institute'

        context['thesis_type'] = self.thesis_type
        context['thesis_title'] = my_title
        return context
