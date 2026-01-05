from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ContactMessage, DemandeDevis, News_letter,Service,PackService,Blog,AvisClient,Equipe,PaysDestination,StatutBourse,Bourse,FAQ,Consultation
from django.utils.html import format_html




# 1. On crée l'interface "en ligne" pour les FAQ
class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1  # Nombre de lignes vides affichées par défaut
    fields = ('question', 'reponse')



# On garde l'admin FAQ séparé au cas où
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'service')
    list_filter = ('service',)
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
    readonly_fields = ('nom', 'email', 'numero_telephone', 'service_souhaite', 'contenu', 'date_envoi')

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
# 1. On définit comment les packs s'affichent à l'intérieur du service
# On utilise 'StackedInline' pour que chaque pack prenne toute la largeur (comme un grand titre)
class PackServiceInline(admin.StackedInline):
    model = PackService
    extra = 1  # Permet d'avoir un formulaire vide pour ajouter un pack
    # On définit les champs à afficher
    fields = ('titre_pack', 'prix', 'liste_services_inclus', 'slug')
    readonly_fields = ('slug',)
    
    # On peut personnaliser le titre de chaque bloc de pack
    verbose_name = "Configuration du Pack"
    verbose_name_plural = "Packs associés à ce Service"

# 2. On configure l'admin du Service pour inclure les packs
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'slug','titre_blanc','titre_shine','text_hero','button_hero_fist','button_hero_second','get_image_preview')
    search_fields = ('titre',)
    
    # C'est ici que la magie opère : 
    # En ouvrant un Service, tu verras le titre du Service en haut, 
    # et tous ses packs listés juste en dessous.
    inlines = [PackServiceInline]
    inlines = [FAQInline]
    
    def get_image_preview(self, obj):
        if obj.image_service:
            from django.utils.html import format_html
            return format_html('<img src="{}" style="width: 50px; height: auto; border-radius: 5px;" />', obj.image_service.url)
        return "Pas d'image"
    
    get_image_preview.short_description = "Aperçu"
# 3. (Optionnel) Si tu veux quand même garder la liste globale des packs 
# mais avec un tri par service
@admin.register(PackService)
class PackServiceAdmin(admin.ModelAdmin):
    list_display = ('titre_pack', 'service', 'prix')
    list_filter = ('service',)
    ordering = ('service',)  # Regroupe les packs par service dans la liste
####
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    # Colonnes affichées dans la liste des articles
    list_display = ('titre', 'services_associes', 'date_publication', 'get_image_preview')
    
    # Filtres sur le côté droit
    list_filter = ('services_associes', 'date_publication')
    
    # Barre de recherche (titre et contenu)
    search_fields = ('titre', 'contenu')
    
    # Génération automatique du slug pendant la saisie du titre
    prepopulated_fields = {'slug': ('titre',)}
    
    # Organisation du formulaire d'édition
    fieldsets = (
        ("Informations principales", {
            'fields': ('titre', 'slug', 'services_associes')
        }),
        ("Contenu de l'article", {
            'fields': ('image', 'contenu')
        }),
    )

    # Fonction pour afficher un petit aperçu de l'image dans la liste
    def get_image_preview(self, obj):
        if obj.image:
            from django.utils.html import format_html
            return format_html('<img src="{}" style="width: 50px; height: auto; border-radius: 5px;" />', obj.image.url)
        return "Pas d'image"
    
    get_image_preview.short_description = "Aperçu"
####
@admin.register(AvisClient)
class AvisClientAdmin(admin.ModelAdmin):
    # On ajoute 'is_published' dans la liste
    list_display = ('get_photo_preview', 'nom_client', 'poste_client', 'is_published', 'get_avis_short')
    
    # On permet de modifier le statut directement depuis la liste sans ouvrir l'article
    list_editable = ('is_published',)
    
    # Filtre latéral pour voir les avis non validés
    list_filter = ('is_published', 'poste_client')
    
    search_fields = ('nom_client', 'avis')
    readonly_fields = ('slug',)
    
    # Action personnalisée pour valider en masse
    actions = ['make_published', 'make_unpublished']

    @admin.action(description="Valider les avis sélectionnés")
    def make_published(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description="Masquer les avis sélectionnés")
    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)

    # 1. Aperçu de la photo dans la liste
    def get_photo_preview(self, obj):
        if obj.photo_client:
            return format_html('<img src="{}" style="width: 45px; height: 45px; border-radius: 50%; object-fit: cover;" />', obj.photo_client.url)
        return format_html('<div style="width: 45px; height: 45px; border-radius: 50%; background: #ddd; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #666;">No pic</div>')
    get_photo_preview.short_description = "Photo"

    # 2. Aperçu court de l'avis pour ne pas encombrer la table
    def get_avis_short(self, obj):
        if len(obj.avis) > 80:
            return f"{obj.avis[:80]}..."
        return obj.avis
    get_avis_short.short_description = "Extrait de l'avis"
##########
@admin.register(Equipe)
class EquipeAdmin(admin.ModelAdmin):
    # Affichage en colonnes avec aperçu photo
    list_display = ('get_photo_preview', 'nom', 'poste', 'is_active')
    
    # Modification rapide du statut sans ouvrir la fiche
    list_editable = ('is_active',)
    
    # Filtres et recherche
    list_filter = ('is_active', 'poste')
    search_fields = ('nom', 'poste')
    
    # Le slug est géré par le modèle, on le protège
    readonly_fields = ('slug',)

    # Organisation du formulaire
    fieldsets = (
        ("Informations Personnelles", {
            'fields': ('nom', 'poste', 'photo')
        }),
        ("Paramètres d'affichage", {
            'fields': ('is_active', 'slug'),
            'description': "Cochez 'Membre actif' pour que le profil apparaisse sur le site."
        }),
    )

    # Fonction d'aperçu de la photo
    def get_photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width: 40px; height: 40px; border-radius: 5px; object-fit: cover;" />', obj.photo.url)
        return format_html('<span style="color: #999;">Pas de photo</span>')
    
    get_photo_preview.short_description = "Aperçu"
###
@admin.register(PaysDestination)
class PaysDestinationAdmin(admin.ModelAdmin):
    # Colonnes de la liste
    list_display = ('get_image_preview', 'nom', 'is_active', 'get_description_short')
    
    # Activation/Désactivation rapide
    list_editable = ('is_active',)
    
    # Recherche et Filtres
    search_fields = ('nom', 'description')
    list_filter = ('is_active',)
    
    # Slug en lecture seule
    readonly_fields = ('slug',)

    # Organisation du formulaire
    fieldsets = (
        ("Informations Générales", {
            'fields': ('nom', 'slug', 'is_active')
        }),
        ("Contenu Visuel & Texte", {
            'fields': ('image', 'description'),
            'description': "L'image doit être de haute qualité pour illustrer la destination."
        }),
    )

    # Aperçu de l'image de destination
    def get_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 80px; height: 50px; border-radius: 4px; object-fit: cover;" />', obj.image.url)
        return format_html('<span style="color: #999;">Pas d\'image</span>')
    get_image_preview.short_description = "Aperçu"

    # Extrait de la description
    def get_description_short(self, obj):
        if obj.description:
            return obj.description[:100] + "..."
        return "-"
    get_description_short.short_description = "Description"
##
@admin.register(StatutBourse)
class StatutBourseAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'get_color_badge')

    def get_color_badge(self, obj):
        return format_html(
            '<span class="badge bg-{}" style="padding: 5px 10px;">{}</span>',
            obj.couleur_classe,
            obj.libelle
        )
    get_color_badge.short_description = "Aperçu visuel"
##
@admin.register(Bourse)
class BourseAdmin(admin.ModelAdmin):
    list_display = ('titre', 'get_image_pays_preview', 'universite', 'statut', 'is_active')
    list_filter = ('statut', 'pays', 'is_active')
    search_fields = ('titre', 'universite')
    list_editable = ('statut', 'is_active')
    readonly_fields = ('slug',)
    
    fieldsets = (
        ("Informations Principales", {
            'fields': ('titre', 'slug', 'pays', 'universite', 'is_active')
        }),
        ("Détails financiers & Statut", {
            'fields': ('montant_info', 'badge_type', 'statut')
        }),
        ("Contenu détaillé", {
            'fields': ('description_detaillee',),
            'description': "Utilisez cet éditeur pour structurer les critères d'éligibilité, les documents requis, etc."
        }),
    )

    def get_image_pays_preview(self, obj):
        if obj.pays:
            return format_html('<img src="{}" style="width: 80px; height: 50px; border-radius: 4px; object-fit: cover;" />', obj.pays.url)
        return format_html('<span style="color: #999;">Pas d\'image</span>')
#
@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'email', 'pays', 'destination', 'date_demande')
    list_filter = ('destination', 'pays')
    search_fields = ('nom_complet', 'email')