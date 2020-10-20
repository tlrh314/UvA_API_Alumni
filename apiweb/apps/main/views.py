from datetime import datetime

from dal import autocomplete
from django.contrib import messages
from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import RedirectView, TemplateView

from ..alumni.models import Alumnus
from ..interviews.models import Post
from ..research.models import Thesis
from ..survey.forms import SurveyCareerInfoForm, SurveyContactInfoForm
from ..survey.models import JobAfterLeaving
from .forms import ContactForm, SelectThesisForm, ThesisForm
from .models import ContactInfo, PrivacyPolicy, WelcomeMessage


def privacy_policy(request):
    pp = PrivacyPolicy.objects.all()
    if pp:
        policy = pp[0].policy
        last_updated = pp[0].last_updated
    else:
        policy = "Our privacy policy is still work in progress."
        last_updated = None
    return render(
        request,
        "main/privacy_policy.html",
        {"privacy_policy": policy, "privacy_policy_last_update": last_updated},
    )


def index(request):
    welcome = WelcomeMessage.objects.all()
    if welcome:
        welcome = welcome[0].text
    else:
        welcome = "Welcome at the API Alumnus Website!"

    # Filtering all posts on whether they are published, and picking the latest
    latest_post = Post.objects.filter(is_published=True)
    if latest_post:
        latest_post = latest_post.latest("date_created")

    latest_thesis = Thesis.objects.filter(type="phd")
    if latest_thesis:
        latest_thesis = latest_thesis.latest("date_of_defence")

    return render(
        request,
        "main/index.html",
        {
            "welcome_text": welcome,
            "latest_post": latest_post,
            "latest_thesis": latest_thesis,
        },
    )


def page_not_found(request, exception=None, template_name=None):
    # TODO: passing contactinfo is given to all templates in context_processors.py.
    # The page_not_found method does not need to give contactinfo to template?
    contactinfo = ContactInfo.objects.all()
    if contactinfo:
        webmaster_email_address = contactinfo[0].webmaster_email_address
    else:
        # Hardcoded in case ContactInfo has no instances.
        webmaster_email_address = "secr-astro-science@uva.nl"
    return render(
        request,
        "404.html",
        {
            "webmaster_email_address": webmaster_email_address,
            "request_path": request.path,
            "exception": exception.__class__.__name__,
        },
    )


def handler500(request, *args, **argv):
    from django.conf import settings
    from sentry_sdk import last_event_id

    return render(
        request,
        "500.html",
        {"sentry_event_id": last_event_id(), "sentry_dsn": settings.SENTRY_DSN_API},
        status=500,
    )


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
            msg += "This message was automatically send from https://{0}/contact".format(
                site_name
            )

            email = EmailMessage(
                subject="Message from {0}/contact".format(site_name),
                body=msg,
                # Caution, from_email must contain domain name!
                from_email="no-reply@api-alumni.nl",
                to=recipients,
                bcc=["timohalbesma@gmail.com", "davidhendriks93@gmail.com"],
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
    return HttpResponseRedirect(
        reverse("alumni:alumnus-detail", kwargs={"slug": request.user.slug})
    )


@login_required
def site_contactinfo(request):
    if request.method == "POST":
        form = SurveyContactInfoForm(
            data=request.POST, instance=request.user, files=request.FILES
        )
        if form.is_valid():
            alumnus = form.save(commit=False)
            alumnus = request.user
            alumnus.save()

            # Add record to LogEntry
            content_type_pk = ContentType.objects.get_for_model(Alumnus).pk
            LogEntry.objects.log_action(
                request.user.pk,
                content_type_pk,
                alumnus.pk,
                str(alumnus),
                CHANGE,
                change_message="Information updated by the alumnus self via the website.",
            )

            messages.success(request, "Profile succesfully updated!")
            return HttpResponseRedirect(
                reverse("alumni:alumnus-detail", kwargs={"slug": request.user.slug})
            )
    else:
        form = SurveyContactInfoForm(instance=request.user)

    return render(request, "main/contactinfo_change_form.html", {"form": form})


@login_required
def site_thesis_select(request):
    if request.method == "POST":
        form = SelectThesisForm(
            data=request.POST, alumnus=request.user, files=request.FILES
        )
        if form.is_valid():
            thesis = form.cleaned_data["which_thesis"]
            if thesis:
                # Add record to LogEntry (only if the thesis exists, else it will raise an error)
                content_type_pk = ContentType.objects.get_for_model(Thesis).pk
                LogEntry.objects.log_action(
                    request.user.pk,
                    content_type_pk,
                    thesis.pk,
                    str(thesis),
                    CHANGE,
                    change_message="Thesis selected to be updated via the website.",
                )
                return HttpResponseRedirect(
                    reverse("site_thesis_update", kwargs={"slug": thesis.slug})
                )
            else:
                return HttpResponseRedirect(reverse("site_thesis_create"))
    else:
        form = SelectThesisForm(alumnus=request.user)

    return render(request, "main/thesis_select.html", {"form": form})


class AlumnusAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Alumnus.objects.none()

        qs = Alumnus.objects.all()
        if self.q:
            qs = qs.filter(
                Q(last_name__icontains=self.q) | Q(first_name__icontains=self.q)
            )

        return qs


@login_required
def site_thesis_update(request, slug):
    if request.method == "POST":
        form = ThesisForm(
            data=request.POST,
            instance=get_object_or_404(Thesis, slug=slug),
            files=request.FILES,
        )
        if form.is_valid():
            thesis = form.save()

            # Add record to LogEntry
            content_type_pk = ContentType.objects.get_for_model(Thesis).pk
            LogEntry.objects.log_action(
                request.user.pk,
                content_type_pk,
                thesis.pk,
                str(thesis),
                CHANGE,
                change_message="Thesis indeed updated via the website.",
            )

            messages.success(request, "Thesis succesfully updated!")
            return HttpResponseRedirect(
                reverse("research:thesis-detail", kwargs={"slug": thesis.slug})
            )
    else:
        form = ThesisForm(instance=get_object_or_404(Thesis, slug=slug))

    return render(request, "main/thesis_change.html", {"form": form})


@login_required
def site_thesis_create(request):
    if request.method == "POST":
        form = ThesisForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            thesis = form.save(commit=False)
            thesis.alumnus = request.user
            thesis.save()

            # Add record to LogEntry
            content_type_pk = ContentType.objects.get_for_model(Thesis).pk
            LogEntry.objects.log_action(
                request.user.pk,
                content_type_pk,
                thesis.pk,
                str(thesis),
                CHANGE,
                change_message="Thesis newly created via the website.",
            )

            messages.success(request, "Succesfully created new thesis!")
            return HttpResponseRedirect(
                reverse("research:thesis-detail", kwargs={"slug": thesis.slug})
            )
    else:
        form = ThesisForm()

    return render(request, "main/thesis_add.html", {"form": form})


@login_required
def site_careerinfo(request, which_position_value=0):
    try:
        prefill_instance = JobAfterLeaving.objects.all().filter(
            alumnus=request.user, which_position=which_position_value
        )[0]
    except IndexError:
        # This could occur if Alumnus did not yet supply the info
        prefill_instance = None

    if request.method == "POST":
        form = SurveyCareerInfoForm(data=request.POST, instance=prefill_instance)

        if form.is_valid():
            jobafterleaving = form.save(commit=False)
            jobafterleaving.alumnus = request.user
            jobafterleaving.which_position = which_position_value
            jobafterleaving.alumnus.survey_info_updated = datetime.now()
            jobafterleaving.alumnus.save()
            jobafterleaving.save()

            jobname = JobAfterLeaving.WHICH_POSITION_CHOICES[int(which_position_value)][
                1
            ]
            if jobname == "Current":
                jobname += " Position"
            else:
                jobname += " Job after Leaving API"

            # Add record to LogEntry
            content_type_pk = ContentType.objects.get_for_model(JobAfterLeaving).pk
            LogEntry.objects.log_action(
                request.user.pk,
                content_type_pk,
                jobafterleaving.pk,
                str(jobafterleaving),
                CHANGE,
                change_message="Job updated via the website.",
            )

            messages.success(request, "{0} succesfully updated!".format(jobname))
            return HttpResponseRedirect(
                reverse("alumni:alumnus-detail", kwargs={"slug": request.user.slug})
            )
    else:
        form = SurveyCareerInfoForm(instance=prefill_instance)

    return render(
        request,
        "main/careerinfo_change_form.html",
        {"form": form, "which_position_value": which_position_value},
    )


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

        url(r"^pizza/detail/(?P<slug>[-\w]+)/$",  # noqa W605
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
