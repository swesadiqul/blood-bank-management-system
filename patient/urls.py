from django.urls import path
from django.contrib.auth.views import LoginView
from . import views


#urlpatterns list
urlpatterns = [
    path('patientlogin', LoginView.as_view(template_name='patient/patientlogin.html'), name='patientlogin'),
    path('patient-signup', views.patient_signup, name='patient_signup'),
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('make-request', views.make_request_view, name='make-request'),
    path('my-request', views.my_request_view, name='my-request'),
]