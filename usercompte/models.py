from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Données Personnelles Communes
    gender = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    birth_year = models.IntegerField(null=True, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    
    # Localisation Commune
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    street_number = models.CharField(max_length=10, blank=True)
    street_name = models.CharField(max_length=255, blank=True)

   

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

##
class MentorProfile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='mentor_profile' # Très important pour le hasattr
    )
    
    # Champs particuliers mentor
    job_title = models.CharField(max_length=255)
    activity_field = models.CharField(max_length=255)
    bank_rib = models.CharField(max_length=34, blank=True)
    mission_type = models.CharField(max_length=100)
    motivation = models.TextField()

    def __str__(self):
        return f"Expertise de {self.user.last_name}"