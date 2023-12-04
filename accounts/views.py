from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Profile

# Create your views here.

def doctors_list(request):
    
    doctors = User.objects.all()
    
    context = {
        'doctors': doctors
    }
    
    return render(request, 'accounts/doctors_list.html', context)

def doctor_detail(request, slug):
    
    doctor_detail = Profile.objects.get(slug=slug)
    
    context = {
        'doctor_detail': doctor_detail
    }
    
    return render(request, 'accounts/doctor_detail.html', context)