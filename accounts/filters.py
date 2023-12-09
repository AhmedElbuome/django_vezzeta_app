import django_filters
from .models import Profile
class DoctorsFilter(django_filters.FilterSet):
    class Meta:
        model = Profile  # Replace with your actual model
        fields = ['name', 'price', 'working_hours', 'gender', 'specialist_doctor', 'waiting_hours', 'address']