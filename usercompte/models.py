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
    def profile_completion_percentage(self):
        # Liste des champs que l'on veut voir remplis
        fields_to_check = [
            'first_name', 'last_name', 'gender', 'phone', 
            'birth_year', 'nationality', 'country', 'city', 'statut'
        ]
        total_fields = len(fields_to_check)
        filled_fields = 0
        
        for field in fields_to_check:
            value = getattr(self, field)
            if value: # Si le champ n'est pas None ou vide
                filled_fields += 1
        
        return int((filled_fields / total_fields) * 100)
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
from django.db import models
from django.conf import settings

class EtapeDossier(models.Model):
    # L'admin peut créer autant d'étapes qu'il veut
    titre = models.CharField(max_length=100, verbose_name="Nom de l'étape")
    ordre = models.PositiveIntegerField(default=0, help_text="Ordre d'affichage (1, 2, 3...)")
    description_aide = models.TextField(blank=True, verbose_name="Message d'aide pour l'étudiant")
    
    # Configuration UI scalable
    COLOR_CHOICES = [
        ('primary', 'Bleu (En cours)'),
        ('warning', 'Orange (En attente)'),
        ('success', 'Vert (Terminé)'),
        ('danger', 'Rouge (Bloqué)'),
        ('secondary', 'Gris (À venir)'),
    ]
    couleur_badge = models.CharField(max_length=20, choices=COLOR_CHOICES, default='secondary')

    class Meta:
        ordering = ['ordre']
        verbose_name = "Configuration : Étape de dossier"

    def __str__(self):
        return f"{self.ordre}. {self.titre}"

class SuiviDossier(models.Model):
    etudiant = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='suivi_dossier')
    etape_actuelle = models.ForeignKey(EtapeDossier, on_delete=models.SET_NULL, null=True, verbose_name="Étape actuelle")
    note_specifique = models.TextField(blank=True, verbose_name="Commentaire personnalisé pour cet étudiant")
    derniere_maj = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dossier de {self.etudiant.email}"

    @property
    def progression_pourcentage(self):
        # Calcul dynamique basé sur le nombre total d'étapes créées en admin
        total = EtapeDossier.objects.count()
        if total == 0 or not self.etape_actuelle:
            return 0
        return int((self.etape_actuelle.ordre / total) * 100)