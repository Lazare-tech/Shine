from django.db import models
from django.utils.text import slugify
from django.core.validators import EmailValidator
from phonenumber_field.modelfields import PhoneNumberField


class News_letter(models.Model):
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    email = models.EmailField(validators=[EmailValidator(message="Email invalide")])
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Date d\inscription de l\'utilisateur ')
    
    class Meta:
        verbose_name = 'News letter'
        verbose_name_plural = 'News letter'
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        slug = slugify(self.email)
        unique_slug = slug
        num = 1
        while News_letter.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{num}'
            num += 1
        return unique_slug
    
    def __str__(self):
        return self.email
##
class ContactMessage(models.Model):
    nom = models.CharField(verbose_name="Nom et prénom", max_length=255)
    objet = models.CharField(verbose_name="Objet du message", max_length=255)
    numero_telephone = PhoneNumberField(
        verbose_name="Numéro de téléphone",
        region=None # Permet de détecter automatiquement le pays si l'indicatif est mis
    )
    email = models.EmailField(validators=[EmailValidator(message="Email invalide")],verbose_name="Email de l'utilisateur")

    contenu = models.TextField(verbose_name="Message")
    date_envoi = models.DateTimeField(verbose_name="Date d'envoi", auto_now=True)
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        slug = slugify(self.email)
        unique_slug = slug
        num = 1
        while ContactMessage.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{num}'
            num += 1
        return unique_slug

    def __str__(self):
        return self.email
    
    ##
class DemandeDevis(models.Model):
        nom = models.CharField(verbose_name="Nom et prénom", max_length=255)
        numero_telephone = PhoneNumberField(
        verbose_name="Numéro de téléphone",
        region=None # Permet de détecter automatiquement le pays si l'indicatif est mis
    )
        email = models.EmailField(validators=[EmailValidator(message="Email invalide")],verbose_name="Email de l'utilisateur")

        contenu = models.TextField(verbose_name="Message")
        service_souhaite = models.TextField(verbose_name="Services souhaités")

        date_envoi = models.DateTimeField(verbose_name="Date d'envoi", auto_now=True)
        slug = models.SlugField(unique=True, max_length=255, blank=True)

        class Meta:
            verbose_name = 'Service demandé'
            verbose_name_plural = 'Services demandés'

        def __str__(self):
            return self.email
##
class Service(models.Model):
    titre = models.CharField(verbose_name="Titre du service", max_length=255)
    description = models.TextField(verbose_name="Description du service",blank=True,null=True)
    titre_blanc= models.CharField(verbose_name="Titre blanc du service", max_length=255,blank=True,null=True)
    titre_shine= models.CharField(verbose_name="Titre shine du service", max_length=255,blank=True,null=True)
    text_hero= models.TextField(verbose_name="Texte de l'image principale",blank=True,null=True)
    button_hero_fist= models.CharField(verbose_name="Texte du premier bouton de l'image principale", max_length=255,blank=True,null=True)
    button_hero_second= models.CharField(verbose_name="Texte du second bouton de l'image principale", max_length=255,blank=True,null=True)
    image_service= models.ImageField(upload_to='services/images/', verbose_name="Image du service",blank=True,null=True)
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    # --- Champs de Style ---
    # Couleur de fond (ex: #122046 ou #F7F9FE)
    bg_color = models.CharField(max_length=20, default="#F7F9FE")
    # Couleur du texte du titre (ex: #FFFFFF ou #122046)
    title_color = models.CharField(max_length=20, default="#122046")
    # Couleur du texte de description
    text_color = models.CharField(max_length=20, default="#6c757d")
    # Pour savoir s'il faut afficher le cercle décoratif doré
    show_decor = models.BooleanField(default=False)
    # Type de bouton (warning, primary, etc.)
    btn_class = models.CharField(max_length=50, default="btn-responsive-primaryl")
    
    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        slug = slugify(self.titre)
        unique_slug = slug
        num = 1
        while Service.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{num}'
            num += 1
        return unique_slug

    def __str__(self):
        return self.titre
##
class PackService(models.Model):
    # Changé 'pack' en 'service' pour plus de clarté
    service = models.ForeignKey(
        'Service', 
        on_delete=models.CASCADE, 
        related_name='packs', 
        verbose_name="Service associé au pack"
    )
    
    prix = models.DecimalField(verbose_name="Prix du pack", max_digits=10, decimal_places=2)
    titre_pack=models.CharField(verbose_name="Titre du pack", max_length=255,blank=True,null=True)
    # Changé en TextField pour permettre les retours à la ligne (liste à puces)
  
    liste_services_inclus = models.TextField(
        verbose_name="Services inclus",
        help_text="Écrivez chaque service inclus du pack sur une nouvelle ligne."
    )
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    class Meta:
        verbose_name = 'Pack de service'
        verbose_name_plural = 'Packs de services'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        # On se base sur le titre du service associé puisqu'il n'y a plus de titre de pack
        base_slug = slugify(self.service.titre)
        unique_slug = base_slug
        num = 1
        # Boucle pour garantir l'unicité du slug
        while PackService.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{base_slug}-{num}'
            num += 1
        return unique_slug

    def __str__(self):
        # Affiche le nom du service et le prix dans l'admin
        return f"Pack {self.service.titre} - {self.prix} €"
    ####
class Blog(models.Model):
    titre = models.CharField(verbose_name="Titre du blog", max_length=255)
    contenu = models.TextField(verbose_name="Contenu du blog")
    image = models.ImageField(upload_to='blogs/images/', verbose_name="Image du blog", blank=True, null=True)
    
    # auto_now_add pour fixer la date à la création, auto_now pour la mise à jour
    date_publication = models.DateTimeField(verbose_name="Date de publication", auto_now_add=True)
    
    # Ajout du on_delete (obligatoire) et null=True si un blog n'est pas forcément lié à un service
    services_associes = models.ForeignKey('Service', on_delete=models.SET_NULL, verbose_name="Services associés", blank=True, null=True)
    
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    def save(self, *args, **kwargs):
        # Génération automatique du slug si vide
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Article de Blog"
        verbose_name_plural = "Articles de Blog"
        ordering = ['-date_publication']

    def __str__(self):
        return self.titre
##
class PaysDestination(models.Model):
    nom = models.CharField(verbose_name="Nom du pays", max_length=255)
    description = models.TextField(verbose_name="Description du pays", blank=True, null=True)
    image = models.ImageField(upload_to='pays_destinations/images/', verbose_name="Image du pays", blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    class Meta:
        verbose_name = 'Pays de destination'
        verbose_name_plural = 'Pays de destination'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        slug = slugify(self.nom)
        unique_slug = slug
        num = 1
        while PaysDestination.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{num}'
            num += 1
        return unique_slug

    def __str__(self):
        return self.nom
    ##
class Equipe(models.Model):
        nom = models.CharField(verbose_name="Nom du membre", max_length=255)
        poste = models.CharField(verbose_name="Poste du membre", max_length=255)
        photo = models.ImageField(upload_to='equipe/photos/', verbose_name="Photo du membre", blank=True, null=True)
        slug = models.SlugField(unique=True, max_length=255, blank=True)

        class Meta:
            verbose_name = 'Membre de l\'équipe'
            verbose_name_plural = 'Membres de l\'équipe'

        def save(self, *args, **kwargs):
            if not self.slug:
                self.slug = self.generate_unique_slug()
            super().save(*args, **kwargs)

        def generate_unique_slug(self):
            slug = slugify(self.nom)
            unique_slug = slug
            num = 1
            while Equipe.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{slug}-{num}'
                num += 1
            return unique_slug

        def __str__(self):
            return self.nom
##
class EntrepriseContact(models.Model):
    nom_entreprise = models.CharField(verbose_name="Nom de l'entreprise", max_length=255)
    adresse = models.CharField(verbose_name="Adresse de l'entreprise", max_length=255)
    location = models.CharField(verbose_name="Localisation", max_length=255)

    numero_telephone = models.CharField(verbose_name="Numéro de téléphone de l'entreprise", max_length=255)
    email = models.EmailField(verbose_name="Email de l'entreprise")
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    class Meta:
        verbose_name = 'Contact de l\'entreprise'
        verbose_name_plural = 'Contacts des entreprises'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        slug = slugify(self.nom_entreprise)
        unique_slug = slug
        num = 1
        while EntrepriseContact.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{num}'
            num += 1
        return unique_slug

    def __str__(self):
        return self.nom_entreprise  
##
