from logging import PlaceHolder
from django import forms
from django.forms.widgets import Textarea


class SearchesForm(forms.Form):
    keywork = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'class':'search', 'placeholder': 'Search Encyclopedia'}))
    
class NewPageForm(forms.Form):
    title = forms.CharField(max_length=64, label="Title")
    dcument = forms.CharField(label="", widget=Textarea(attrs={"placeholder": 'Markdown'}))

# class EditPageForm(forms.Form):
#     title = forms.CharField(max_length=64, label="Title")
#     dcument = forms.CharField(label="", widget=Textarea(attrs={"placeholder": 'Markdown'}))