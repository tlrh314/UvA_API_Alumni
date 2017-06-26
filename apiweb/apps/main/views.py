from __future__ import unicode_literals, absolute_import, division

from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, RedirectView
from django.contrib import messages
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required

from .models import ContactInfo
from .models import WelcomeMessage
from .models import PrivacyPolicy
from .forms import ContactForm
from ..interviews.models import Post
from ..alumni.models import Degree
from ..survey.models import JobAfterLeaving
from ..survey.forms import SurveyContactInfoForm, SurveyCareerInfoForm


def privacy_policy(request):
    pp = PrivacyPolicy.objects.all()
    if pp:
        policy = pp[0].policy
        last_updated = pp[0].last_updated
    else:
        policy = "Our privacy policy is still work in progress."
        last_updated = None
    return render(request, "main/privacy_policy.html",
        {"privacy_policy": policy, "privacy_policy_last_update": last_updated })


def index(request):
    welcome = WelcomeMessage.objects.all()
    if welcome:
        welcome = welcome[0].text
    else:
        welcome = "Welcome at the API Alumnus Website!"

    #Filtering all posts on whether they are published, and picking the latest
    latest_post = Post.objects.filter(is_published=True)
    if latest_post:
        latest_post = latest_post.latest("date_created")

    latest_thesis = Degree.objects.filter(type="phd")
    if latest_thesis:
        latest_thesis = latest_thesis.latest("date_of_defence")

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

    recipients = []
    contactinfo = ContactInfo.objects.all()
    if contactinfo:
        secretariat = contactinfo[0].secretary_email_address
        recipients.append(secretariat)
    else:
        # Hardcoded in case ContactInfo has no instances.
        secretariat = "secr-astro-science@uva.nl"
        recipients.append(secretariat)


    if request.method == "POST":
        form = form_class(data=request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            message = form.cleaned_data["message"]
            sender = form.cleaned_data["sender"]
            cc_myself = form.cleaned_data["cc_myself"]

            if cc_myself:
                recipients.append(sender)

            # Caution, this breaks if there is no site.
            site_name = Site.objects.all()[0].name
            msg = "{0}\n\n".format(message)
            msg += "-------------------------------------------------\n\n"
            msg += "From: {0}\n".format(name)
            msg += "Email Address: {0}\n\n".format(sender)
            msg += "This message was automatically send from https://{0}/contact".format(site_name)

            email = EmailMessage(
                subject="Message from {0}/contact".format(site_name),
                body=msg,
                # Caution, from_email must contain domain name!
                from_email="no-reply@api-alumni.nl",
                to=recipients,
                bcc=["timohalbesma@gmail.com", "davidhendriks93@gmail.com" ],
                # Caution, reply_to header is already set by Postfix!
                # reply_to=list(secretariat),
                # headers={'Message-ID': 'foo'},
            )
            email.send(fail_silently=False)
            return HttpResponseRedirect("/thanks/")
    else:
        form = ContactForm()

    return render(request, "main/contact.html", {"form": form})


def contact_success(request):
    return render(request, "main/thanks.html")


@login_required
def redirect_to_profile(request):
    messages.success(request, "Succesfully logged in!")
    return HttpResponseRedirect(reverse("alumni:alumnus-detail", kwargs={"slug": request.user.slug}))


@login_required
def site_contactinfo(request):
    if request.method == "POST":
        form = SurveyContactInfoForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            alumnus = form.save(commit=False)
            alumnus = request.user
            alumnus.save()
            messages.success(request, "Profile succesfully updated!")
            return HttpResponseRedirect(reverse("alumni:alumnus-detail", kwargs={"slug": request.user.slug}))
    else:
        form = SurveyContactInfoForm(instance=request.user)

    return render(request, "main/contactinfo_change_form.html", { "form": form,  })


@login_required
def site_careerinfo(request, which_position_value=0):
    try:
        prefill_instance = JobAfterLeaving.objects.all().filter(alumnus=request.user, which_position=which_position_value)[0]
    except IndexError:
        # This could occur if Alumnus did not yet supply the info
        prefill_instance = None

    if request.method == "POST":
        form = SurveyCareerInfoForm(data=request.POST, instance=prefill_instance)

        if form.is_valid():
            jobafterleaving = form.save(commit=False)
            jobafterleaving.alumnus = request.user
            jobafterleaving.which_position = which_position_value
            jobafterleaving.save()
            jobname = JobAfterLeaving.WHICH_POSITION_CHOICES[int(which_position_value)][1]
            if jobname == "Current":
                jobname += " Position"
            else:
                jobname += " Job after Leaving API"
            messages.success(request, "{0} succesfully updated!".format(jobname))
            return HttpResponseRedirect(reverse("alumni:alumnus-detail", kwargs={"slug": request.user.slug}))
    else:
        form = SurveyCareerInfoForm(instance=prefill_instance)

    return render(request, "main/careerinfo_change_form.html", {
        "form": form, "which_position_value": which_position_value,})


@login_required
def site_theses(request):
    if request.method == "POST":
        form = None
        # form = SurveyPrivacySettingsForm(data=request.POST)
        # if form.is_valid():
        if True:
            # form.save()
            messages.success(request, "Profile succesfully updated!")
            return HttpResponseRedirect(reverse("alumni:alumnus-detail", kwargs={"slug": request.user.slug}))
    else:
        # form = SurveyPrivacySettingsForm(instance=request.user)
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
