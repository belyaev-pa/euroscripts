from django import forms


class FileUpload(forms.Form):
    file = forms.FileField(widget=forms.FileInput)


class ResultUpload(forms.Form):
    company = forms.FileField(widget=forms.FileInput)
    stat = forms.FileField(widget=forms.FileInput)