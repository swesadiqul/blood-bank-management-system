from django import forms
from blood.models import *


class BloodForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['bloodgroup', 'unit']

class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['patient_name', 'patient_age', 'reason', 'bloodgroup', 'unit']
