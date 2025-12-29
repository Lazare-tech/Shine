from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class StatutUtilisateur(models.Model):
    statut_name = models.CharField(max_length=100, verbose_name="Nom du statut")

    class Meta:
        verbose_name = "Statut Utilisateur"
        verbose_name_plural = "Statuts Utilisateurs"

    def __str__(self):
        return self.statut_name
##
class User(AbstractUser):
    USERNAME_FIELD = 'email'  # Définit l'email comme identifiant principal
    REQUIRED_FIELDS = []
    # Données Personnelles Communes
    email = models.EmailField(unique=True) # L'email doit être unique
    gender = models.CharField(max_length=20,verbose_name="Genre")
    phone = models.CharField(max_length=20, verbose_name="Numéro de téléphone")
    birth_year=models.DateField(verbose_name="Année de naissance",blank=True,null=True)
    nationality = models.CharField(max_length=100,verbose_name="Nationalité")
    statut = models.ForeignKey(
        StatutUtilisateur, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="utilisateurs",
        verbose_name="Statut actuel"
    )
    # Localisation Commune
    country = models.CharField(max_length=100,verbose_name="Pays")
    city = models.CharField(max_length=100,verbose_name="Ville")
    street_number = models.CharField(max_length=10, blank=True,null=True,verbose_name="Numéro de rue")
    street_name = models.CharField(max_length=255, blank=True,null=True,verbose_name="Nom de la rue")

   

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"] # On copie l'email dans l'username technique
        if commit:
            user.save()
        return user

##
class MentorProfile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='mentor_profile' # Très important pour le hasattr
    )
    
    # Champs particuliers mentor
    job_title = models.CharField(max_length=255,verbose_name="Intitulé du poste")
    activity_field = models.CharField(max_length=255,verbose_name="Domaine d'activité")
    bank_rib = models.CharField(max_length=34, blank=True,verbose_name="RIB Bancaire")
    mission_type = models.CharField(max_length=100,verbose_name="Type de mission")
    motivation = models.TextField(verbose_name="Motivation")

    def __str__(self):
        return f"Expertise de {self.user.last_name}"
##