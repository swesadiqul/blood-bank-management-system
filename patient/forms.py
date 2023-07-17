from django import forms
from django.contrib.auth.models import User
from patient.models import *


#create forms
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']


class PatientForm(forms.ModelForm):
    class Meta:
        model= Patient
        fields = ['age', 'bloodgroup', 'disease', 'address', 'doctorname', 'mobile', 'profile_pic']
