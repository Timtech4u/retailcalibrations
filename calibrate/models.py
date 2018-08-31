from django.db import models
from django.urls import reverse 
import datetime
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class Calibration(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    
    GENDER_CHOICES = (
        ('M', 'MALE'),
        ('F', 'FEMALE')
    )
    gender = models.CharField(max_length = 1, choices =GENDER_CHOICES)
    
    STATE_CHOICE = (
        ('ABIA', 'ABIA'),
        ('ADAMAWA', 'ADAMAWA'),
        ('AKWA IBOM', 'AKWA IBOM'),
        ('KANO', 'KANO')
    )
    state = models.CharField(max_length = 20, choices = STATE_CHOICE)

    phone = models.IntegerField(blank=True, null=True)
    email = models.EmailField(max_length=200)
    tyre_make = models.CharField(max_length=200)
    tyre_guage = models.IntegerField(blank=True, null=True)

    VALVE_POSITION_CHOICES = (
        ('OPEN', 'OPEN'),
        ('CLOSE', 'CLOSE'),
        ('NONE', 'NONE')
    )
    valve_position = models.CharField(max_length =20, choices = VALVE_POSITION_CHOICES)
    
    job_number = models.IntegerField(blank=True, null=True)

    TANK_POSITION_CHOICES = (
        ('BALLON', 'BALLON'),
        ('SPRING', 'SPRING')
    )
    tank_position = models.CharField(max_length=200, choices=TANK_POSITION_CHOICES)
    registration_number= models.CharField(max_length=200)
    transporter = models.CharField(max_length=200)
    chasis_number = models.CharField(max_length=200)
    date_issued = models.DateField(blank=True, null=True)
    date_expired = models.DateField(blank=True, null=True)
    certificate_number = models.IntegerField(default=0)
    capacity = models.IntegerField(default=0) 
    document = models.FileField(upload_to='documents', blank=True, null=True)
    
    def __str__(self):
       return self.first_name

    def get_absolute_url(self):
        return reverse('calibrate:calibration_edit', kwargs={'pk': self.pk})

    def status(self):
        today = datetime.date.today()
        difference = self.date_expired - today
        if difference.days <=0:
            status_code = "Expired"
        else:
            status_code = "Active"
        return status_code

class User(AbstractUser):
    is_regularAdmin = models.BooleanField(default=False)
    is_adminStaff = models.BooleanField(default=False)
    is_superAdmin = models.BooleanField(default = False)

    def user_type(self):
        if self.is_regularAdmin:
            return "Regular Staff"
        elif self.is_adminStaff:
            return "Admin Staff" 
        else:
            return "Super Admin"



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key =True)
    

    def __str__(self):
        return self.user.user_type
       
@receiver(post_save, sender=User)
def user_is_created(sender, instance, created, **kwargs):
    print(created)
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()