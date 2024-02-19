from django import forms

from .models import Student


class SearchForm(forms.Form):
    q = forms.CharField()


class EnrollForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'surname', 'age', 'course']
