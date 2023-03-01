from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class Entry(models.Model):
    nume = models.CharField(_("Nume"), max_length=255)
    prenume = models.CharField(_("Prenume"), max_length=255)
    facultate = models.CharField(_("Facultate/Departament"), max_length=255)
    specialitate = models.CharField(_("Specialitate"), max_length=255)
    functie = models.CharField(_("Functie"), max_length=255)
    email = models.CharField(_("Email"), max_length=255)
    password = models.CharField(_("Password"), max_length=255)
    note = models.CharField(_("Note"), max_length=255)
    status = models.BooleanField(_("Status"))


class Meta:
    def __str__(self):
        return self