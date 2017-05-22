from __future__ import unicode_literals, absolute_import, division

from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, RedirectView
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import ContactInfo
from .models import WelcomeMessage
from .forms import ContactForm
from ..interviews.models import Post
from ..alumni.models import Degree
from ..survey.forms import SurveyContactInfoForm


def privacy_policy(request):
    return render(request, "main/privacy_policy.html", {})


def index(request):
    welcome = WelcomeMessage.objects.all()
    if welcome:
        welcome = welcome[0].text
    else:
        welcome = "Welcome at the API Alumnus Website!"

    #Filtering all posts on whether they are published, and picking the latest
    latest_post = Post.objects.filter(is_published=True).latest("date_created")
    latest_thesis = Degree.objects.filter(type="phd").latest("date_of_defence")

    return render(request, "main/index.html", {"welcome_text": welcome, "latest_post": latest_post, "latest_thesis": latest_thesis})


def page_not_found(request):
    # TODO: passing contactinfo is given to all templates in context_processors.py.
    # The page_not_found method does not need to give contactinfo to template?
    contactinfo = ContactInfo.objects.all()
    if contactinfo:
        webmaster_email_address = contactinfo[0].webmaster_email_address
    else:
        # Hardcoded in case ContactInfo has no instances.
        webmaster_email_address = "secr-astro-science@uva.nl"
    return render(request, "404.html", {"webmaster_email_address": webmaster_email_address})


def contact(request):
    form_class = ContactForm

    contactinfo = ContactInfo.objects.all()
    if contactinfo:
        sent_to = contactinfo[0].secretary_email_address
    else:
        # Hardcoded in case ContactInfo has no instances.
        sent_to = "secr-astro-science@uva.nl"

    if request.method == "POST":
        form = form_class(data=request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            message = form.cleaned_data["message"]
            sender = form.cleaned_data["sender"]
            cc_myself = form.cleaned_data["cc_myself"]

            recipients = ["timohalbesma@gmail.com"]  #  TODO: use sent_to
            if cc_myself:
                recipients.append(sender)

            msg = "This message sent trough API Alumnus Website\n\n"
            msg += "From: {0}\n".format(name)
            msg += "Email Address: {0}\n".format(sender)
            msg += "-------------------------------------------------\n\n"
            msg += "{0}\n\n".format(message)

            send_mail("Message sent trough API Alumnus Website", msg, sent_to, recipients)
            return HttpResponseRedirect("/thanks/")
    else:
        form = ContactForm()

    return render(request, "main/contact.html", {"form": form})


def contact_success(request):
    return render(request, "main/thanks.html")


@login_required
def site_contactinfo(request):
    if request.method == "POST":
        form = SurveyContactInfoForm(data=request.POST)
        if form.is_valid():
            # TODO: storing stuff in Alumnus lives in the save method of the form
            form.save()
            messages.success(request, "Profile succesfully updated!")
            return HttpResponseRedirect(reverse("alumni:alumnus-detail", kwargs={"slug": request.user.alumnus.slug}))
    else:
        form = SurveyContactInfoForm(instance=request.user.alumnus)

    return render(request, "main/contactinfo_change_form.html", { "form": form,  })


@login_required
def site_privacysettings(request):
    if request.method == "POST":
        form = None
        # form = SurveyPrivacySettingsForm(data=request.POST)
        # if form.is_valid():
        if True:
            # form.save()
            messages.success(request, "Profile succesfully updated!")
            return HttpResponseRedirect(reverse("alumni:alumnus-detail", kwargs={"slug": request.user.alumnus.slug}))
    else:
        # form = SurveyContactInfoForm(instance=request.user.alumnus)
        form = None
        pass

    return render(request, "main/privacysettings_change_form.html", { "form": form,  })


# TODO: clean up code below
class MainView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        return context

class SitemapView(TemplateView):
    template_name = "main/sitemap.html"

class AboutView(TemplateView):
    template_name = "main/about.html"

class TwentyFourSevenView(TemplateView):
    template_name = "main/247.html"


# Redirect views

class HomeView(RedirectView):
    permanent = True

    def get_redirect_url(self, **kwargs):
        return reverse("home-page")


class ScatterView(RedirectView):
    permanent = True
    url = "http://www.iaa.es/scattering/%(arguments)s"


class LowercaseView(RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        return self.request.path.lower()


class DetailRedirectView(RedirectView):
    """Redirection view for items that used to have a unique slug.

    Items that were identified by their unique slug, are now
    identified by their (database) id; the slug is no longer unique.

    To redirect old links, the (first) item that matches a slug is
    fetched from the database, and the corresponding absolute url
    created using the the id and slug, to which the user is then
    redirected.

    The model is the essential class-based attribute, and can most
    easily be given through as_view() in the url configuration, for
    example:

        url(r"^pizza/detail/(?P<slug>[-\w]+)/$",
            view=RedirectView.as_view(model=Pizza),
            name="pizza-redirect"),

    """

    model = None
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        item = self.model.objects.filter(slug=kwargs["slug"]).first()
        if not item:
            try:
                item = self.model.objects.filter(pk=kwargs["slug"]).first()
            except ValueError as exc:
                if str(exc).startswith("invalid literal for int()"):
                    raise Http404
                raise
        if item:
            return item.get_absolute_url()
        else:
            raise Http404
