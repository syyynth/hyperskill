from django import forms


class UploadForm(forms.Form):
    video = forms.FileField()
    title = forms.CharField(max_length=50, required=False)
    tags = forms.CharField(max_length=50, required=False)
