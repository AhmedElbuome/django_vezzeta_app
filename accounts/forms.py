from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import Appointment, Profile

class SignupForm(UserCreationForm):
    
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    
class LogoutForm(forms.Form):
    confirm_logout = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Confirm Logout',
    )
    
class UpdateUserForm(forms.ModelForm):
    
    class Meta:
        
        model = User
        fields = ['first_name', 'last_name', 'email']
        
class UpdateProfileForm(forms.ModelForm):
    
    class Meta:
        
        model = Profile
        fields = '__all__'
        exclude = ('user', 'slug', 'id')
    
class AdvancedPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
    )
    
class AppointmentForm(forms.ModelForm):
    
    class Meta:
        model = Appointment
        fields = ['date', 'time', 'additional_notes']  # Add other fields as needed
        
class AppointmentConfirmationForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['additional_notes'] 
        

DOCTOR_IN = (
        ('الجلدية','الجلدية'),
        ('أسنان','أسنان'),
        ('نفسي','نفسي'),
        ('اطفال حديثي الولادة','اطفال حديثي الولادة'),
        ('نساء و توليد','نساء و توليد'),
        
    )        

LOCATION = (
    
    ('البحيرة','البحيرة'),
    ('المنصوره','المنصوره'),
    ('الدقي','الدقي'),
    (' الاسكندرية ','الاسكندرية'),

)

GENDER = (
    ('M', 'Male'),
    ('F', 'Female')
)

class DoctorSearchForm(forms.Form):
    name = forms.CharField(max_length=255, required=False)
    location = forms.ChoiceField(choices=[LOCATION])
    specialization = forms.ChoiceField(choices=[DOCTOR_IN])
    gender = forms.ChoiceField(choices=[GENDER])
