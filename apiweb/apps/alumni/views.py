from __future__ import unicode_literals, absolute_import, division

from django.views.generic import TemplateView, DetailView, ListView


class IndexView(TemplateView):
    template_name = 'alumni/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        # categories = {}
        # categories['compacts'] = 'Neutron stars and black holes'
        # categories['cosmics'] = 'Cosmic explosions'
        # categories['astroparticles'] = 'Astroparticle physics'
        # categories['planets'] = 'Planet formation and exoplanets'
        # categories['stars'] = 'Stars, formation and evolution'
        # context['categories'] = categories
        return context
