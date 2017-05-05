from __future__ import unicode_literals, absolute_import, division

from django.views.generic import ListView
from .models import Book, Proceeding, PhDThesis


class PhDView(ListView):
    template_name = 'library/phd-theses.html'
    queryset = PhDThesis.objects.order_by('-year')
    context_object_name = 'phdtheses'


class ProceedingsView(ListView):
    template_name = 'library/proceedings.html'
    queryset = Proceeding.objects.order_by('-year')
    context_object_name = 'proceedings'


class IndexView(ListView):
    template_name = 'library/index.html'
    queryset = Book.objects.order_by('label')
    context_object_name = 'books'

#    @method_decorator(login_required)
#    def dispatch(self, *args, **kwargs):
#        return super(IndexView, self).dispatch(*args, **kwargs)
