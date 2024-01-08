from .models import Feedback
from django import forms
from accounts.models import CustomUser
from . import models

class FeedbackForm(forms.Form):
    email = forms.EmailField()
    # rate = forms.IntegerField()
    feedback = forms.CharField()