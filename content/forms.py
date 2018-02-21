from django import forms
from django.conf import settings

class ContactForm(forms.Form):
    name = forms.CharField(label='Name', required=True)
    email = forms.EmailField(label='E-Mail', required=True)
    message = forms.CharField(label='Message', widget=forms.Textarea, required=True)
