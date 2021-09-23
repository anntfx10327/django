from .models import *
from django import forms

class ActionForm(forms.ModelForm):
    class Meta:
        model = Action
        fields = "__all__"


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["price"]