from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, Select

from .models import Answers, Respondents


class SignUpForm(UserCreationForm):
    class Meta:
        model = Respondents
        fields = ["username"]


class EvaluationForm(ModelForm):
    url = forms.fields.CharField(
        label="url",
        required=False,
        initial="",
        widget=forms.widgets.HiddenInput,
    )

    class Meta:
        model = Answers
        fields = ["naturalness", "intelligibility"]
        widgets = {
            "naturalness": Select,
            "intelligibility": Select,
        }
