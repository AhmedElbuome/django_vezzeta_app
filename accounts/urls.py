from django.urls import path
from . import views
# from django.contrib.auth.views import PasswordResetConfirmView
# from .views import AdvancedPasswordResetView

app_name = 'accounts'

urlpatterns = [
    
    path('doctors/', views.doctors_list, name='doctors_list'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('search_doctor/', views.search_doctor, name='search_doctor'),
    path('random-card/', views.random_card, name='random_card'),
    path('appointment/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('appointment_confirmation/<int:appointment_id>/', views.appointment_confirmation, name='appointment_confirmation'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    # path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password_reset/', AdvancedPasswordResetView.as_view(), name='password_reset'),
    # path(
    #     'password-reset-confirm/<uidb64>/<token>/', 
    #     AdvancedPasswordResetView.as_view(),
    #     name='password_reset_confirm'
    # ),
    path('<slug:slug>/', views.doctor_detail, name='doctor_detail'),
]
