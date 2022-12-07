from django import forms


class TranslationForm(forms.Form):

    sentence = forms.CharField(
        label='', widget=forms.Textarea(attrs={'cols': '70', 'rows': '20'}), required=True)
