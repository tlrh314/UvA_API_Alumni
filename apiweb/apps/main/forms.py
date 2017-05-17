from django import forms

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
