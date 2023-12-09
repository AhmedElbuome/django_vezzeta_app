from django.contrib import admin
from .models import Profile, Card, Appointment

# Register your models here.

admin.site.register(Profile)
admin.site.register(Card)
admin.site.register(Appointment)