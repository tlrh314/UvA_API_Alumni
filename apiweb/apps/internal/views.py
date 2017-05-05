from __future__ import unicode_literals, absolute_import, division

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView, DetailView, ListView
from django.views.generic import FormView, CreateView, UpdateView
from ..people.models import Person
from ..people.forms import PersonForm


class SecureView(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SecureView, self).dispatch(*args, **kwargs)


class LogoView(TemplateView, SecureView):
    template_name = 'internal/logo.html'


class IndexView(TemplateView, SecureView):
    template_name = 'internal/index.html'


class ObservatoryView(TemplateView, SecureView):
    template_name = 'internal/observatory.html'


class AdressesView(ListView, SecureView):
    template_name = 'internal/addresses.html'
    queryset = Person.objects.all().filter(show_person=True)
    context_object_name = 'persons'


class ShowProfileView(DetailView):
    template_name = 'internal/show_profile.html'
    context_object_name = 'profile'

    def get_object(self):
        object = self.request.user.person
        return object

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            _ = request.user.person
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('internal:create-profile'))
        return super(ShowProfileView, self).dispatch(request, *args, **kwargs)


class ModifyProfileView(FormView):
    form_class = PersonForm
    context_object_name = 'profile'
    template_name = 'internal/modify_profile.html'
    success_url = reverse_lazy('internal:show-profile')


class CreateProfileView(ModifyProfileView, CreateView):

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateProfileView, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            _ = request.user.person
            return HttpResponseRedirect(reverse('internal:edit-profile'))
        except ObjectDoesNotExist:
            pass
        return super(CreateProfileView, self).dispatch(request, *args, **kwargs)


class EditProfileView(ModifyProfileView, UpdateView):

    def get_object(self):
        object = self.request.user.person
        return object

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            _ = request.user.person
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('internal:create-profile'))
        return super(EditProfileView, self).dispatch(request, *args, **kwargs)
