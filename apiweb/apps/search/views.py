from __future__ import unicode_literals, absolute_import, division

from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from ...settings import GOOGLE_API_KEY
from ...settings import GOOGLE_CX_ID
from .forms import SearchForm
try:
    from urllib import urlencode
    from urllib2 import urlopen, URLError
except ImportError:
    from urllib.parse import urlencode
    from urllib.request import urlopen, URLError
import json


class SearchView(FormView):

    form_class = SearchForm
    template_name = 'search/index.html'
    success_url = reverse_lazy('search:index')

    def google_search(self, search_terms, start=1):
        GOOGLE_URL = "https://www.googleapis.com/customsearch/v1"
        params = urlencode({
            'key': GOOGLE_API_KEY,
            'cx': GOOGLE_CX_ID,
            'q': search_terms,
            'num': 10,              # items per page
            'start': start          # starting page
            })
        url = "{}?{}".format(GOOGLE_URL, params)
        try:
            search_response = urlopen(url)
            search_results = search_response.read()
        except URLError as exc:
            return None
        results = json.loads(search_results.decode('utf-8'))
        return results.get('items', [])

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(SearchView, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        search_terms = self.request.session.pop('search_terms', '')
        initial['search_terms'] = search_terms
        return initial

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)

        search_terms = self.request.session.pop('search_terms', '')
        context['results'] = self.request.session.pop('results', None)
        if context['results']:
            context['google_link'] = (
                "http://www.google.com/search?q={}+"
                "site:www.astro.uva.nl".format(search_terms))
        else:
            context['results_empty'] = True
        return context

    def form_valid(self, form):
        """
        This is what's called when the form is valid.
        """
        search_terms = form.cleaned_data['search_terms']
        results = self.google_search(search_terms)
        self.request.session['results'] = results
        self.request.session['search_terms'] = search_terms
        self.request.session.modified = True
        return HttpResponseRedirect(self.success_url)
