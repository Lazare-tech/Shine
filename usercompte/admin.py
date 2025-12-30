from django.contrib import admin
from .models import User, StatutUtilisateur, MentorProfile,ProfilUtilisateur
from django.contrib.auth.admin import UserAdmin # <--- IMPORTANT : Ne pas oublier cet import
# Register your models here.
# 1. Gestion des Statuts
# 1. Inline pour le profil Mentor (DOIT ÊTRE DÉFINI EN PREMIER)
class MentorProfileInline(admin.StackedInline):
    model = MentorProfile
    can_delete = False
    verbose_name_plural = 'Détails spécifiques au Profil Mentor'
    fk_name = 'user'
    extra = 0 

# 2. Configuration de l'administration de l'Utilisateur
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (MentorProfileInline,)
    
    # Liste des colonnes dans la vue tableau
    list_display = ('email', 'first_name', 'last_name', 'profil', 'statut', 'city', 'is_staff')
    list_filter = ('profil', 'statut', 'is_staff', 'country')
    
    # On ajoute 'profil' dans la recherche (attention: c'est une FK, donc profil__profil_name)
    search_fields = ('email', 'first_name', 'last_name', 'city', 'profil__profil_name')
    ordering = ('-date_joined',)

    # 3. Organisation de TOUS les champs dans la fiche détaillée
    fieldsets = UserAdmin.fieldsets + (
        ('Informations Shine (Profil & Statut)', {
            'fields': (
                'profil', 
                'statut', 
            )
        }),
        ('Données Personnelles', {
            'fields': (
                'gender', 
                'phone', 
                'birth_year', 
                'nationality'
            )
        }),
        ('Localisation complète', {
            'fields': (
                'country', 
                'city', 
                'code_postal', # Ajouté ici
                'street_number', 
                'street_name'
            )
        }),
    )

# 4. Autres configurations Admin
@admin.register(StatutUtilisateur)
class StatutUtilisateurAdmin(admin.ModelAdmin):
    list_display = ('statut_name', 'get_user_count')
    
    def get_user_count(self, obj):
        return obj.utilisateurs.count()
    get_user_count.short_description = "Nombre d'utilisateurs"

@admin.register(ProfilUtilisateur)
class ProfilUtilisateurAdmin(admin.ModelAdmin):
    list_display = ('profil_name',)

@admin.register(MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_title', 'activity_field', 'mission_type')