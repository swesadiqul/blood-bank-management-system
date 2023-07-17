from django.shortcuts import render
from patient.forms import UserForm, PatientForm
from patient.models import * 
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from blood.forms import *
from blood.models import *
from donor.forms import DonorForm



def patient_signup(request):
    userForm = UserForm()
    patientForm = PatientForm()
    print(request.POST)
    if request.method=='POST':
        userForm = UserForm(request.POST)
        patientForm = PatientForm(request.POST, request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient.bloodgroup=patientForm.cleaned_data['bloodgroup']
            patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('login')
    
    context = {'userForm': userForm, 'patientForm': patientForm}
    return render(request,'patient/patientsignup.html', context)


def patient_dashboard(request):
    patient = Patient.objects.get(user_id = request.user.id)
    context = {
        'requestpending': BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Pending').count(),
        'requestapproved': BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Approved').count(),
        'requestmade': BloodRequest.objects.all().filter(request_by_patient=patient).count(),
        'requestrejected': BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Rejected').count(),

    }
   
    return render(request,'patient/patient_dashboard.html', context)


def make_request_view(request):
    request_form = BloodRequestForm()
    if request.method=='POST':
        request_form = BloodRequestForm(request.POST)
        if request_form.is_valid():
            blood_request = request_form.save(commit=False)
            blood_request.bloodgroup = request_form.cleaned_data['bloodgroup']
            patient= Patient.objects.get(user_id=request.user.id)
            blood_request.request_by_patient=patient
            blood_request.save()
            return HttpResponseRedirect('my-request')  
    return render(request,'patient/makerequest.html',{'request_form':request_form})


def my_request_view(request):
    patient = Patient.objects.get(user_id=request.user.id)
    blood_request = BloodRequest.objects.all().filter(request_by_patient=patient)
    return render(request,'patient/my_request.html', {'blood_request': blood_request})
