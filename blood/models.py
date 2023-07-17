from django.db import models
from patient.models import *
from donor.models import *



class Stock(models.Model):
    bloodgroup = models.CharField(max_length=10)
    unit = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.bloodgroup

class BloodRequest(models.Model):
    request_by_patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE)
    request_by_donor = models.ForeignKey(Donor, null=True, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=30)
    patient_age = models.PositiveIntegerField()
    reason = models.CharField(max_length=500)
    bloodgroup = models.CharField(max_length=10)
    unit = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, default="Pending")
    date = models.DateField(auto_now=True)


    def __str__(self):
        return self.bloodgroup

        