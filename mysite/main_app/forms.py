from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label="Your name", max_length=100)
    email = forms.CharField(
        label="Email", max_length=100, widget=forms.widgets.EmailInput
    )
    password = forms.CharField(label="Password", max_length=100)


class AnswerForm(forms.Form):
    naturalness = forms.fields.ChoiceField(
        label="naturalness",
        choices=(
            (1, "1: 非常に悪い"),
            (2, "2: 悪い"),
            (3, "3: 普通"),
            (4, "4: 良い"),
            (5, "5: 非常に良い"),
        ),
        required=True,
        
        initial="",
        widget=forms.widgets.RadioSelect,
    )
    intelligibility = forms.fields.ChoiceField(
        label="intelligibility",
        choices=(
            (1, "1: 非常に悪い"),
            (2, "2: 悪い"),
            (3, "3: 普通"),
            (4, "4: 良い"),
            (5, "5: 非常に良い"),
        ),
        required=True,
        initial="",
        widget=forms.widgets.RadioSelect,
    )
    url = forms.fields.CharField(
        label="url",
        required=False,
        initial="",
        widget=forms.widgets.HiddenInput,
    )
