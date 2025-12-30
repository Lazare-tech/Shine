from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
#
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse email est obligatoire")
        email = self.normalize_email(email)
        # On force l'username à être l'email
        extra_fields.setdefault('username', email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # Important pour éviter l'erreur que tu as reçue
        extra_fields.setdefault('username', email)

        return self.create_user(email, password, **extra_fields)

class StatutUtilisateur(models.Model):
    statut_name = models.CharField(max_length=100, verbose_name="Nom du statut")

    class Meta:
        verbose_name = "Statut Utilisateur"
        verbose_name_plural = "Statuts Utilisateurs"

    def __str__(self):
        return self.statut_name
    
class ProfilUtilisateur(models.Model):
    profil_name=models.CharField(max_length=100,verbose_name="Nom du profil utilisateur")
    
    class Meta:
        verbose_name="Profil Utilisateur"
        verbose_name_plural="Profils Utilisateurs"

    def __str__(self):
            return self.profil_name
##
class User(AbstractUser):
    USERNAME_FIELD = 'email'  # Définit l'email comme identifiant principal
    REQUIRED_FIELDS = []
    objects = UserManager() # On lie le nouveau manager ici
    # Données Personnelles Communes
    email = models.EmailField(unique=True) # L'email doit être unique
    gender = models.CharField(max_length=20,verbose_name="Genre")
    phone = models.CharField(max_length=20, verbose_name="Numéro de téléphone")
    birth_year=models.DateField(verbose_name="Année de naissance",blank=True,null=True)
    nationality = models.CharField(max_length=100,verbose_name="Nationalité")
    code_postal=models.CharField(max_length=20,verbose_name="Code Postal",blank=True,null=True)
    statut = models.ForeignKey(
        StatutUtilisateur, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="utilisateurs",
        verbose_name="Statut actuel"
    )
    profil=models.ForeignKey(
        ProfilUtilisateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="utilisateurs",
        verbose_name="Profil utilisateur"
    )
    # Localisation Commune
    country = models.CharField(max_length=100,verbose_name="Pays")
    city = models.CharField(max_length=100,verbose_name="Ville")
    street_number = models.CharField(max_length=10, blank=True,null=True,verbose_name="Numéro de rue")
    street_name = models.CharField(max_length=255, blank=True,null=True,verbose_name="Nom de la rue")

   

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
    job_title = models.CharField(max_length=255,verbose_name="Intitulé du poste")
    activity_field = models.CharField(max_length=255,verbose_name="Domaine d'activité")
    bank_rib = models.CharField(max_length=34, blank=True,verbose_name="RIB Bancaire")
    mission_type = models.CharField(max_length=100,verbose_name="Type de mission")
    motivation = models.TextField(verbose_name="Motivation")

    def __str__(self):
        return f"Expertise de {self.user.last_name}"
##