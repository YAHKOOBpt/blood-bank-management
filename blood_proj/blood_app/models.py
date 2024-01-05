from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

BLOOD_GROUPS = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
]

class User(AbstractUser):
    is_donor = models.BooleanField(default=False, verbose_name="Is Donor")
    is_patient = models.BooleanField(default=False, verbose_name="Is Patient")
    name = models.CharField(max_length=100,null=True, blank=True)
    mobile = models.CharField(max_length=15,null=True, blank=True)
    address = models.CharField(max_length=200,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    district = models.CharField(max_length=100,null=True, blank=True)
    gender = models.CharField(max_length=10,null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    blood_grou = models.CharField(max_length=3, choices=BLOOD_GROUPS, null=True, blank=True)  # Set a default value
    disease=  models.CharField(max_length=100,null=True, blank=True)
    doctor =  models.CharField(max_length=100,null=True, blank=True)
    photo = models.ImageField(upload_to='profile/')   
    status = models.BooleanField(default=False)
    unit= models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.username
    
    @property
    def imageURL(self):
        try:
            url = self.photo.url
        except:
            url = ''
        return  url

class BloodRequest(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blood', verbose_name="blood")
    patient_id = models.IntegerField(null=True, blank=True)
    reasen = models.CharField(max_length=100, null=True, blank=True)
    patient_name = models.CharField(max_length=100, null=True, blank=True)
    patient_age = models.PositiveIntegerField(null=True, blank=True)
    reason = models.CharField(max_length=100, null=True, blank=True)
    blood_type = models.CharField(max_length=3, choices=BLOOD_GROUPS, null=True, blank=True)
    unit = models.PositiveIntegerField(null=True, blank=True)
    doctor =  models.CharField(max_length=100,null=True, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.patient_name