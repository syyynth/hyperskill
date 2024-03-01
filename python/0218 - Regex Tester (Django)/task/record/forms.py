from django import forms

from record.models import Record


class RegexForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['regex', 'text']
