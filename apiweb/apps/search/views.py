from __future__ import unicode_literals, absolute_import, division

import json
import re
from functools import reduce

try:
    from urllib import urlencode
    from urllib2 import urlopen, URLError
except ImportError:
    from urllib.parse import urlencode
    from urllib.request import urlopen, URLError

from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from django.core.urlresolvers import reverse, reverse_lazy

from .forms import SearchForm
from ...settings import GOOGLE_API_KEY
from ...settings import GOOGLE_CX_ID
from ..alumni.models import Alumnus
from ..research.models import Thesis

def search(request):
    """  Searches through following fields:
            - Alumni first name
            - Alumni last name
            - Thesis title
            - Alumni date of defence
            - Alumni start date
            - Alumni stop date

            - Exact matches if input is given between quotes ' or "

    Return list of alumni with all thesis links """

    words = request.GET.get("terms", "")
    terms = []

    # If no keywords, return nothing
    if not words:
        return render(request, "search/search_results.html", {"alumni": [], "key_words": []})

    if len(words) <= 2:
        msg = "Please use at least 3 characters to search. "
        msg += "Tip: you can use exact match by placing ' or \" around words!"
        messages.error(request, msg)
        return render(request, "search/search_results.html", {"alumni": [], "key_words": []})

    if len(words.split()) > 10:
        msg = "Please limit your search to <10 words. "
        msg += "Tip: you can use exact match by placing ' or \" around words!"
        messages.error(request, msg)
        return render(request, "search/search_results.html", {"alumni": [], "key_words": []})

    # Check if must be exact match (i.e. if between quotation marks)
    words = words.replace("'", '"')
    if '"' in words:
        exact_match = re.findall('"([^"]*)"', words)

        for exact in exact_match:
            words.replace(exact, "")
            terms.append(exact)

    # Create final lists of search terms
    terms = terms + words.split()

    # Set maximum number of words
    if len(terms) > 42:
        return render(request, "search/search_results.html", {"alumni": [],
                                                              "key_words": []})
    #  Remove single characters
    terms = [term for term in terms if len(term) > 1]

    # Compute filters
    search_filter = Q()
    time_filter = Q()
    alumni = Alumnus.objects.all()

    for term in terms:

        # Check if year, if set time filters
        if (term.isdigit() and len(term) == 4):
            end_year = str(int(term) + 1)
            date_range=[term+"-01-01",end_year+"-01-01"]
            time_filter = (time_filter | Q(theses__date_of_defence__range=date_range)
                                       | Q(theses__date_stop__range=date_range)
                                       | Q(theses__date_start__range=date_range))

        else:
            search_filter = (search_filter | Q(last_name__icontains=term)|
                                             Q(first_name__icontains=term) |
                                             Q(theses__title__icontains=term))

    # Compute combined filter
    total_filter = time_filter & search_filter

    # Apply all filters
    results = alumni.filter(total_filter).distinct()

    if len(results) > 10:
        msg = "Search matched {0} items. Tip: you can use exact match by placing ' or \" around words!".format(len(results))
        messages.warning(request, msg)

    return render(request, "search/search_results.html", {"alumni": results, "key_words": terms})


class SearchView(FormView):

    form_class = SearchForm
    template_name = "search/index.html"
    success_url = reverse_lazy("search:index")

    def google_search(self, search_terms, start=1):
        GOOGLE_URL = "https://www.googleapis.com/customsearch/v1"
        params = urlencode({
            "key": GOOGLE_API_KEY,
            "cx": GOOGLE_CX_ID,
            "q": search_terms,
            "num": 10,              # items per page
            "start": start          # starting page
            })
        url = "{}?{}".format(GOOGLE_URL, params)
        try:
            search_response = urlopen(url)
            search_results = search_response.read()
        except URLError as exc:
            return None
        results = json.loads(search_results.decode("utf-8"))
        return results.get("items", [])

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(SearchView, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        search_terms = self.request.session.pop("search_terms", "")
        initial["search_terms"] = search_terms
        return initial

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)

        search_terms = self.request.session.pop("search_terms", "")
        context["results"] = self.request.session.pop("results", None)
        if context["results"]:
            context["google_link"] = (
                "http://www.google.com/search?q={}+"
                "site:www.astro.uva.nl".format(search_terms))
        else:
            context["results_empty"] = True
        return context

    def form_valid(self, form):
        """
        This is what's called when the form is valid.
        """
        search_terms = form.cleaned_data["search_terms"]
        results = self.google_search(search_terms)
        self.request.session["results"] = results
        self.request.session["search_terms"] = search_terms
        self.request.session.modified = True
        return HttpResponseRedirect(self.success_url)
