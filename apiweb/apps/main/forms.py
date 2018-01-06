from django import forms

from dal import autocomplete

from ..research.models import Thesis
from ..alumni.templatetags.template_filters import display_thesis_type

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control required",
               "placeholder": "What is your name?"}))
    message = forms.CharField(required=True, widget=forms.Textarea(
        attrs={"class": "form-control required",
               "placeholder": "What would you like to tell us?"}))
    sender = forms.EmailField(required=False, widget=forms.EmailInput(
        attrs={"class": "form-control email",
               "placeholder": "email@adres.nl - so we know how to reach you"}))
    cc_myself = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={"class": "checkchoice"}))


class SelectThesisForm(forms.Form):
    def __init__(self, alumnus, *args, **kwargs):
        super(SelectThesisForm, self).__init__(*args, **kwargs)

        # Only show theses of the relevant Alumnus in the queryset
        self.fields["which_thesis"].queryset = Thesis.objects.filter(alumnus=alumnus)
        #Add the type to the choices, to make it more clear.
        self.fields["which_thesis"].label_from_instance = lambda obj: "%s: %s" % (display_thesis_type(obj.type), obj.title)

    which_thesis = forms.ModelChoiceField(
        label="Which thesis do you want to change?",
        required=False,
        queryset=None,  # note that we set the queryset in the init method above
        widget=forms.Select(attrs={"class": "form-control"})
    )


class ThesisForm(forms.ModelForm):
    class Meta:
        model = Thesis
        fields = ("type", "date_start", "date_start", "date_stop", "title", "date_of_defence",
                  "url", "pdf", "photo", "advisor")

        widgets = {
            "type": forms.Select(attrs={"class": "form-control"}),
            "date_start": forms.DateInput(attrs={"class": "form-control"}),
            "date_stop": forms.DateInput(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "date_of_defence": forms.DateInput(attrs={"class": "form-control"}),
            "url": forms.URLInput(attrs={"class": "form-control"}),
            "advisor": autocomplete.ModelSelect2Multiple(url="alumnus-autocomplete",
                attrs={"class": "form-control"})
            # use FileInput to remove the clear tickbox
            # "pdf": forms.ClearableFileInput(),
            # "photo": forms.ClearableFileInput(),
        }
