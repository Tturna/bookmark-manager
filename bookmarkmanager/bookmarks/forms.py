from django import forms


class BookmarkForm(forms.Form):
    name = forms.CharField(max_length=100)
    url = forms.URLField(max_length=200)
