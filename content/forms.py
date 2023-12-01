from django import forms


# Create your forms here.


class SearchForm(forms.Form):
    q = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Looking for something?"}),
    )
