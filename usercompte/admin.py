from django.contrib import admin
from .models import User, StatutUtilisateur, MentorProfile
from django.contrib.auth.admin import UserAdmin # <--- IMPORTANT : Ne pas oublier cet import
# Register your models here.
# 1. Gestion des Statuts
@admin.register(StatutUtilisateur)
class StatutUtilisateurAdmin(admin.ModelAdmin):
    list_display = ('statut_name', 'get_user_count')
    search_fields = ('statut_name',)

    def get_user_count(self, obj):
        return obj.utilisateurs.count()
    get_user_count.short_description = "Nombre d'utilisateurs"

# 2. Inline pour le profil Mentor
# Cela permet d'afficher les champs Mentor directement dans la fiche User
class MentorProfileInline(admin.StackedInline):
    model = MentorProfile
    can_delete = False
    verbose_name_plural = 'Détails du Profil Mentor'
    fk_name = 'user'
    extra = 0 # N'affiche pas de formulaire vide par défaut

# 3. Personnalisation de l'UserAdmin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # On ajoute l'inline Mentor
    inlines = (MentorProfileInline,)
    
    # Colonnes affichées dans la liste des utilisateurs
    list_display = ('username', 'email', 'first_name', 'last_name', 'statut', 'city', 'is_staff')
    list_filter = ('statut', 'is_staff', 'is_superuser', 'country')
    
    # Organisation des champs dans la fiche détaillée
    fieldsets = UserAdmin.fieldsets + (
        ('Informations Shine', {
            'fields': (
                'statut', 
                'gender', 
                'phone', 
                'birth_year', 
                'nationality'
            )
        }),
        ('Localisation', {
            'fields': (
                'country', 
                'city', 
                'street_number', 
                'street_name'
            )
        }),
    )
    
    # Permet de chercher par nom, email ou ville
    search_fields = ('username', 'first_name', 'last_name', 'email', 'city')
    ordering = ('-date_joined',)

# Optionnel : Enregistrer MentorProfile séparément si tu veux aussi une vue liste dédiée
@admin.register(MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_title', 'activity_field', 'mission_type')
    list_filter = ('activity_field', 'mission_type')
    search_fields = ('user__last_name', 'job_title')