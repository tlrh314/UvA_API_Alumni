from django import forms


class SearchForm(forms.Form):
    search_terms = forms.CharField(
        label="Search", required=True, widget=forms.TextInput(attrs={"size": 60})
    )
