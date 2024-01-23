from django.contrib import admin
from .models import *
from django.utils.html import format_html
# Register your models here.

class BloodUsers(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'address','email','district','gender','age')

# Check if LogoPredictionAdmin is not already registered before registering
if not admin.site.is_registered(BloodUsers):
    admin.site.register(User, BloodUsers)

class BloodRequst(admin.ModelAdmin):
    list_display = ('donor', 'patient_name', 'reasen','blood_type','unit','doctor')

# Check if LogoPredictionAdmin is not already registered before registering
if not admin.site.is_registered(BloodRequst):
    admin.site.register(BloodRequest, BloodRequst)
