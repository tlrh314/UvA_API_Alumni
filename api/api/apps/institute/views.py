from django.views.generic import TemplateView
from ..people.models import Person
from .map import tooltips


class InstituteView(TemplateView):
    template_name = 'institute/index.html'

class ContactView(TemplateView):
    template_name = 'institute/contact.html'

class MapView(TemplateView):
    template_name = 'institute/map.html'

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)

        context['tooltips'] = tooltips()
        context['persons'] = Person.objects.filter(show_person=True).filter(
                             office__isnull=False).order_by('last_name')
        return context

    def render_to_response(self, context, **kwargs):
        return super(MapView,self).render_to_response(context,
                             content_type='application/xhtml+xml', **kwargs)

