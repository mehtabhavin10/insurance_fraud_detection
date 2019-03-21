from django import forms

class upload_file_form(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()