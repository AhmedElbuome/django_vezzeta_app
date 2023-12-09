from django.contrib.auth.models import User
from .models import Profile, Card
from .forms import SignupForm, LoginForm, LogoutForm, UpdateProfileForm, UpdateUserForm, DoctorSearchForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from .forms import AdvancedPasswordResetForm
from django.contrib import messages
from django.urls import reverse
import random
from django.shortcuts import get_object_or_404
from .models import Appointment
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required
from .forms import AppointmentConfirmationForm
from .filters import DoctorsFilter


# Create your views here.

def doctors_list(request):
    
    doctors = User.objects.all()

    

    
    context = {
        'doctors': doctors,
    
    }
    
    return render(request, 'accounts/doctors_list.html', context)

def doctor_detail(request, slug):
    
    doctor_detail = Profile.objects.get(slug=slug)
    
    context = {
        'doctor_detail': doctor_detail
    }
    
    return render(request, 'accounts/doctor_detail.html', context)

@login_required()
def my_profile(request):
    
    return render(request, 'accounts/my_profile.html', {})

@login_required()
def update_profile(request):
    
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, request.FILES, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid and profile_form.is_valid :
            user_form.save()
            profile_form.save()
            return redirect('accounts:my_profile')  # Redirect to the profile page
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
        
    context = {
        'user_form': user_form,
        'profile_form':profile_form,
    }

    return render(request, 'accounts/update_profile.html', context)

def random_card(request):
    # Retrieve a random card not shown recently
    recent_cards = request.session.get('recent_cards', [])
    all_cards = Card.objects.exclude(id__in=recent_cards)
    
    if not all_cards.exists():
        # Reset the list of recent cards if all cards have been shown
        recent_cards = []

    random_card = random.choice(Card.objects.all())
    recent_cards.append(random_card.id)

    # Limit the list to the last 5 shown cards (adjust as needed)
    recent_cards = recent_cards[-5:]

    # Save the updated list of recent cards in the session
    request.session['recent_cards'] = recent_cards

    context = {
        'card': random_card,
        'recent_cards': Card.objects.filter(id__in=recent_cards),
    }

    return render(request, 'accounts/random_card.html', context)

# login page
def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user) # Use the renamed auth_login function
                if not remember_me:
                    # If 'Remember Me' is not checked, set session expiry to 0 (browser close)
                    request.session.set_expiry(0)
                return redirect('accounts:doctors_list')  # Redirect to the dashboard upon successful login
            else:
                messages.error(request, 'Invalid login credentials. Please try again.')

    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})

# signup page
def signup(request):
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            auth_login(request, user)
            return redirect('accounts:doctors_list')
        
    else:
        form = SignupForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'registration/signup.html', context)

def logout(request):
    auth_logout(request)
    messages.info(request, 'You have been successfully logged out.')
    return redirect('home')  # Replace 'home' with the appropriate URL name or path

class AdvancedPasswordResetView(PasswordResetView):
    form_class = AdvancedPasswordResetForm
    template_name = 'registration/password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Profile, pk=doctor_id)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            # Check appointment availability here if needed
            appointment = form.save(commit=False)
            appointment.doctor = doctor
            appointment.patient = request.user  # Assuming the user is logged in
            appointment.save()
            return redirect('accounts:appointment_confirmation', appointment_id=appointment.id)
    else:
        form = AppointmentForm()

    context = {'form': form, 'doctor': doctor}
    return render(request, 'accounts/book_appointment.html', context)

@login_required
def appointment_confirmation(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        form = AppointmentConfirmationForm(request.POST)
        if form.is_valid():
            # Perform any additional processing or validation if needed
            form.save()  # Save the form data (if necessary)
            return render(request, 'accounts/appointment_confirmation.html', {'appointment': appointment})
    else:
        form = AppointmentConfirmationForm()

    return render(request, 'accounts/appointment_confirmation.html', {'form': form, 'appointment': appointment})

def search_doctor(request):
    queryset = Profile.objects.all()  # Replace with your actual model
    filter = DoctorsFilter(request.GET, queryset=queryset)
    results = filter.qs

    context = {
        'filter': filter,
        'results': results,
    }

    return render(request, 'accounts/search.html', context)