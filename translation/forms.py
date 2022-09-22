from django import forms


class TranslationForm(forms.Form):

    sentence = forms.CharField(
        label='', widget=forms.Textarea(), required=True)
