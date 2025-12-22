from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ContactMessage, DemandeDevis, News_letter,Service,PackService
from django.utils.html import format_html
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    # 1. Colonnes affichées dans la liste
    list_display = ('nom', 'email', 'numero_telephone', 'objet', 'date_envoi')
    
    # 2. Filtres latéraux pour une recherche rapide
    list_filter = ('date_envoi', 'email')
    
    # 3. Barre de recherche (recherche sur plusieurs champs)
    search_fields = ('nom', 'email', 'objet', 'contenu')
    
    # 4. Tri par défaut (le plus récent en premier)
    ordering = ('-date_envoi',)
    
    # 5. Champs en lecture seule (Senior Tip: On ne modifie pas un message reçu !)
    readonly_fields = ('nom', 'email', 'numero_telephone', 'objet', 'contenu', 'date_envoi', 'slug')
    
    # 6. Organisation des détails (Fieldsets)
    fieldsets = (
        ('Informations Expéditeur', {
            'fields': ('nom', 'email', 'numero_telephone')
        }),
        ('Contenu du Message', {
            'fields': ('objet', 'contenu')
        }),
        ('Métadonnées', {
            'fields': ('date_envoi', 'slug'),
            'classes': ('collapse',), # Masque cette section par défaut
        }),
    )

    # Empêcher l'ajout manuel d'un message depuis l'admin (Optionnel)
    def has_add_permission(self, request):
        return False
########

@admin.register(DemandeDevis)
class DemandeDevisAdmin(admin.ModelAdmin):
    # 1. On affiche le service souhaité en évidence
    list_display = ('nom', 'email', 'numero_telephone', 'service_souhaite', 'date_envoi')
    
    # 2. Filtrer par service est crucial pour trier les demandes par département
    list_filter = ('service_souhaite', 'date_envoi')
    
    # 3. Recherche étendue
    search_fields = ('nom', 'email', 'service_souhaite', 'contenu')
    
    # 4. Tri chronologique
    ordering = ('-date_envoi',)
    
    # 5. Protection des données (Lecture seule)
    readonly_fields = ('nom', 'email', 'numero_telephone', 'service_souhaite', 'contenu', 'date_envoi', 'slug')

    # 6. Organisation visuelle
    fieldsets = (
        ('Identité du Prospect', {
            'fields': ('nom', 'email', 'numero_telephone'),
            'description': 'Informations de contact du client potentiel.'
        }),
        ('Détails de la Demande', {
            'fields': ('service_souhaite', 'contenu'),
            'classes': ('wide',),
        }),
        ('Informations Système', {
            'fields': ('date_envoi', 'slug'),
            'classes': ('collapse',),
        }),
    )

    # Empêcher la création manuelle (un devis doit venir du site)
    def has_add_permission(self, request):
        return False

    # Option Senior : Colorer les lignes selon le service (Exemple)
    # Cela permet de repérer visuellement les types de demandes dans la liste
@admin.register(News_letter)
class NewsLetterAdmin(admin.ModelAdmin):
    # 1. Colonnes à afficher dans la liste
    list_display = ('email', 'created_at', 'slug')
    
    # 2. Barre de recherche pour retrouver un abonné
    search_fields = ('email',)
    
    # 3. Filtre par date d'inscription
    list_filter = ('created_at',)
    
    # 4. Tri par défaut (les plus récents en premier)
    ordering = ('-created_at',)
    
    # 5. Rendre le slug et la date en lecture seule (pour éviter les erreurs)
    readonly_fields = ('slug', 'created_at')
    
    # 6. Configuration de l'affichage détaillé
    fieldsets = (
        ('Informations de l\'abonné', {
            'fields': ('email', 'slug')
        }),
        ('Dates importantes', {
            'fields': ('created_at',),
        }),
    )

    # Optionnel : Empêcher la modification des emails (pour l'intégrité de la liste)
    def has_change_permission(self, request, obj=None):
        return False
#######
# 1. Gestion des packs directement dans la page du Service
class PackServiceInline(admin.TabularInline):
    model = PackService
    extra = 1  # Permet d'ajouter un pack rapidement
    # On retire 'titre' et 'prepopulated_fields' car le titre n'existe plus
    fields = ['liste_services_inclus', 'slug']
    readonly_fields = ['slug'] # Le slug est automatique, on le met en lecture seule

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'slug','prix', 'image_preview')
    search_fields = ('titre',)
    prepopulated_fields = {'slug': ('titre',)} # Le titre existe toujours ici
    inlines = [PackServiceInline]

    # Version moderne pour l'aperçu de l'image
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: auto; border-radius: 5px;" />', obj.image.url)
        return "Pas d'image"
    
    image_preview.short_description = 'Aperçu'

@admin.register(PackService)
class PackServiceAdmin(admin.ModelAdmin):
    # On affiche 'service' au lieu de 'pack' et on retire 'titre'
    list_display = ('service',  'slug')
    list_filter = ('service',) 
    search_fields = ('service__titre', 'liste_services_inclus')
    readonly_fields = ['slug'] # On ne peut pas pré-remplir un slug sans le champ titre