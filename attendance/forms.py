from django import forms

class RegistrationForms(forms.Form):
    first_name = forms.CharField(max_length=80)
    last_name = forms.CharField(max_length=80)
    email = forms.EmailField(unique=True)
    uid = forms.CharField(max_length=20, unique=True)
    phone = forms.CharField(max_length=10)
    description = forms.CharField(max_length=200)
