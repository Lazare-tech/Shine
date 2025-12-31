from django.contrib import admin
from .models import User, StatutUtilisateur, MentorProfile,ProfilUtilisateur,EtapeDossier,SuiviDossier
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
    list_display = ('email', 'first_name', 'last_name', 'profil','phone', 'statut', 'city', 'is_staff')
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
    

@admin.register(EtapeDossier)
class EtapeDossierAdmin(admin.ModelAdmin):
    list_display = ('ordre', 'titre', 'couleur_badge', 'description_aide')
    
    # On rend l'ordre et la couleur éditables directement dans la liste
    list_editable = ('ordre', 'couleur_badge') 
    
    # IMPORTANT : Puisque 'ordre' est éditable, on force le lien 
    # de modification sur le champ 'titre'
    list_display_links = ('titre',) 
    
    ordering = ('ordre',)

@admin.register(SuiviDossier)
class SuiviDossierAdmin(admin.ModelAdmin):
    list_display = ('get_etudiant_email', 'get_etudiant_nom', 'etape_actuelle', 'progression', 'derniere_maj')
    list_filter = ('etape_actuelle', 'derniere_maj')
    search_fields = ('etudiant__email', 'etudiant__last_name', 'etudiant__first_name')
    autocomplete_fields = ['etudiant'] # Pratique si vous avez des milliers d'étudiants

    # Affichage du pourcentage de progression dans la liste
    def progression(self, obj):
        return f"{obj.progression_pourcentage}%"
    progression.short_description = "Avancement"

    # Accès aux infos de l'utilisateur lié
    def get_etudiant_email(self, obj):
        return obj.etudiant.email
    get_etudiant_email.short_description = "Email"

    def get_etudiant_nom(self, obj):
        return f"{obj.etudiant.first_name} {obj.etudiant.last_name}"
    get_etudiant_nom.short_description = "Nom Complet"