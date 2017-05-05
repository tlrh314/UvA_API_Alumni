from __future__ import unicode_literals, absolute_import, division

from django.contrib.auth.decorators import login_required
from ...decorators import ipallowed_or_403
from django.utils.decorators import method_decorator
from django.template.defaultfilters import slugify
from django.views.generic import View, TemplateView, DetailView
from django.views.generic import FormView, UpdateView, DeleteView, RedirectView
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from datetime import datetime
from .models import WikiPage
from .forms import WikiPageForm, WikiPageCreateForm


class SecureView(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SecureView, self).dispatch(*args, **kwargs)


class IndexView(RedirectView, SecureView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        return reverse('wiki:view', kwargs={'name': 'main-wikipage'})


class WikiPageView(DetailView):
    template_name = 'wiki/view.html'
    context_object_name = 'page'

    def get_object(self):
        object = get_object_or_404(WikiPage.visible, name=self.name)
        # Record another visit of this view
        object.visits += 1
        object.save()
        return object

#    def get_context_data(self, **kwargs):
#        context = super(WikiPageView, self).get_context_data(**kwargs)
#        context['page'] = self.page
#        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        name = kwargs.get('name', None)
        self.name = slugify(name)
        return super(WikiPageView, self).dispatch(*args, **kwargs)


class WikiEditView(UpdateView):
    """Update an old entry."""

    form_class = WikiPageForm
    template_name = 'wiki/edit.html'
    context_object_name = 'page'

    def get_object(self):
        object = get_object_or_404(WikiPage.visible, name=self.name)
        if self.request.user.username != "khouri" and \
           self.name == "api-meerkamp":
            raise Http404()
        return object

    def get_success_url(self):
        return reverse('wiki:edit', kwargs={'name': self.name})

    def form_valid(self, form):
        form.instance.modification_author = self.request.user.person.full_name
        form.instance.modification_date = datetime.now()
        return super(WikiEditView, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        name = kwargs.get('name', None)
        self.name = slugify(name)
        return super(WikiEditView, self).dispatch(*args, **kwargs)


class WikiCreateView(FormView, SecureView):
    """Create an new entry."""

    form_class = WikiPageCreateForm
    template_name = 'wiki/create.html'

    def get_success_url(self):
        return reverse('wiki:edit', kwargs={'name': self.name})

    def form_valid(self, form):
        self.name = slugify(form.cleaned_data['name'])
        page, created = WikiPage.objects.get_or_create(name=self.name)
        page.is_category_page = form.cleaned_data['is_category_page']
        page.is_visible = True # in case page was previously deleted
        if created:
            page.creation_author = self.request.user.person.full_name
            page.modification_date = datetime.now()
        page.save()
        return HttpResponseRedirect(self.get_success_url())


class WikiDeleteView(DeleteView):
    """Delete an old entry."""

    form_class = WikiPageForm
    template_name = 'wiki/delete.html'
    context_object_name = 'page'

    def get_object(self):
        object = get_object_or_404(WikiPage.visible, name=self.name)
        if self.request.user != "khouri" and self.name == "api-meerkamp":
            raise Http404()
        return object

    def get_success_url(self):
        return reverse('wiki:view', kwargs={'name': 'main-wikipage'})

    def form_valid(self, form):
        page = self.object
        page.is_visible = False
        page.creation_author = self.request.user.person.full_name
        page.modification_date = datetime.now()
        page.save()
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        name = kwargs.get('name', None)
        self.name = slugify(name)
        return super(WikiDeleteView, self).dispatch(*args, **kwargs)


class AllView(TemplateView, SecureView):
    template_name = 'wiki/all.html'

    def get_context_data(self, **kwargs):
        context = super(AllView, self).get_context_data(**kwargs)
        context['category_pages'] = WikiPage.visible.filter(
            is_category_page=True).order_by('name')
        context['normal_pages'] = WikiPage.visible.filter(
            is_category_page=False).order_by('name')
        return context


class IPSecureView(View):

    @method_decorator(ipallowed_or_403)
    def dispatch(self, *args, **kwargs):
        return super(IPSecureView, self).dispatch(*args, **kwargs)


class Index2View(RedirectView, IPSecureView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        return reverse('wiki2:view2', kwargs={'name': 'main-wikipage'})


class WikiPage2View(DetailView):
    template_name = 'wiki/view2.html'
    context_object_name = 'page'

    def get_object(self):
        object = get_object_or_404(WikiPage.visible, name=self.name)
        return object

#    def get_context_data(self, **kwargs):
#        context = super(WikiPage2View, self).get_context_data(**kwargs)
#        context['page'] = self.page
#        return context

    @method_decorator(ipallowed_or_403)
    def dispatch(self, *args, **kwargs):
        name = kwargs.get('name', None)
        self.name = slugify(name)
        return super(WikiPage2View, self).dispatch(*args, **kwargs)


class All2View(TemplateView, IPSecureView):
    template_name = 'wiki/all2.html'

    def get_context_data(self, **kwargs):
        context = super(All2View, self).get_context_data(**kwargs)
        context['category_pages'] = WikiPage.visible.filter(
            is_category_page=True).order_by('name')
        context['normal_pages'] = WikiPage.visible.filter(
            is_category_page=False).order_by('name')
        return context
