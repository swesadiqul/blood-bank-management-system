from django.shortcuts import render
from patient.forms import UserForm
from donor.forms import DonorForm, DonationForm
from donor.models import *
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from blood.forms import *
from blood.models import *


def doner_signup(request):
    userForm = UserForm()
    donerForm = DonorForm()
    print(request.POST)
    if request.method=='POST':
        userForm = UserForm(request.POST)
        donerForm= DonorForm(request.POST, request.FILES)
        if userForm.is_valid() and donerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            donor=donerForm.save(commit=False)
            donor.user=user
            donor.bloodgroup=donerForm.cleaned_data['bloodgroup']
            donor.save()
            my_donor_group = Group.objects.get_or_create(name='DONOR')
            my_donor_group[0].user_set.add(user)
        return HttpResponseRedirect('login')
    
    context = {'userForm': userForm, 'donerForm': donerForm}
    return render(request, 'donor/donorsignup.html', context)


def donor_dashboard_view(request):
    donor= Donor.objects.get(user_id=request.user.id)
    dict={
        'requestpending': BloodRequest.objects.all().filter(request_by_donor=donor).filter(status='Pending').count(),
        'requestapproved': BloodRequest.objects.all().filter(request_by_donor=donor).filter(status='Approved').count(),
        'requestmade': BloodRequest.objects.all().filter(request_by_donor=donor).count(),
        'requestrejected': BloodRequest.objects.all().filter(request_by_donor=donor).filter(status='Rejected').count(),
    }
    return render(request,'donor/donor_dashboard.html',context=dict)


def donate_blood_view(request):
    donation_form = DonationForm()
    if request.method=='POST':
        donation_form = DonationForm(request.POST)
        if donation_form.is_valid():
            blood_donate=donation_form.save(commit=False)
            blood_donate.bloodgroup=donation_form.cleaned_data['bloodgroup']
            donor= models.Donor.objects.get(user_id=request.user.id)
            blood_donate.donor=donor
            blood_donate.save()
            return HttpResponseRedirect('donation-history')  
    return render(request,'donor/donate_blood.html',{'donation_form':donation_form})

def donation_history_view(request):
    donor = Donor.objects.get(user_id=request.user.id)
    donations = BloodDonate.objects.all().filter(donor=donor)
    return render(request,'donor/donation_history.html',{'donations':donations})

def make_request_view(request):
    request_form = BloodRequestForm()
    if request.method=='POST':
        request_form = BloodRequestForm(request.POST)
        if request_form.is_valid():
            blood_request=request_form.save(commit=False)
            blood_request.bloodgroup=request_form.cleaned_data['bloodgroup']
            donor= Donor.objects.get(user_id=request.user.id)
            blood_request.request_by_donor=donor
            blood_request.save()
            return HttpResponseRedirect('request-history')  
    return render(request,'donor/makerequest.html',{'request_form':request_form})

def request_history_view(request):
    donor= models.Donor.objects.get(user_id=request.user.id)
    blood_request = BloodRequest.objects.all().filter(request_by_donor=donor)
    return render(request,'donor/request_history.html',{'blood_request':blood_request})
