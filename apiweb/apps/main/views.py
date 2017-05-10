from __future__ import unicode_literals, absolute_import, division

from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, RedirectView

from .models import ContactInfo
from .forms import ContactForm


def index(request):
    return render(request, "main/index.html")


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
