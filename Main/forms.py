import re

from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import request

from Main.models import Entry


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['nume', 'prenume', 'facultate', 'specialitate', 'functie', 'email', 'password', 'note',
                  'status']


class AuthentificationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class EmailForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    to = forms.EmailField(max_length=100)
    comments = forms.CharField(required=False, widget=forms.Textarea)
