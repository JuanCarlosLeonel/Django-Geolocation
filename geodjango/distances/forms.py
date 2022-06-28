from dataclasses import fields
from django import forms
from . models import Medicao

class DistanceModelForm(forms.ModelForm):
    class Meta:
        model = Medicao
        fields = ('destino',)