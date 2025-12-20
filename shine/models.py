from django.db import models
from django.utils.text import slugify
from django.core.validators import EmailValidator, RegexValidator

# Create your models here.
phone_validator = RegexValidator(
    regex=r'^\+\d{9,15}$',
    message="Le numéro doit inclure l'indicatif international (ex: +226...)"
)
##
class News_letter(models.Model):
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    email = models.EmailField(verbose_name="Email de l'utilisateur",unique=True)
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
    numero_telephone = models.CharField(validators=[phone_validator], max_length=20,verbose_name="Numéro de téléphone")
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
        numero_telephone = models.CharField(validators=[phone_validator], max_length=20,verbose_name="Numéro de téléphone")

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
    image= models.ImageField(upload_to='services/images/', verbose_name="Image du service",blank=True,null=True)
    slug = models.SlugField(unique=True, max_length=255, blank=True)

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
    titre = models.CharField(verbose_name="Titre du pack", max_length=255)
    prix = models.DecimalField(verbose_name="Prix du pack", max_digits=10, decimal_places=2)
    liste_services_inclus = models.CharField(verbose_name="Liste des services inclus dans le pack", max_length=255)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    pack=models.ForeignKey(Service, on_delete=models.CASCADE, related_name='packs', verbose_name="Service associé au pack")
    

    class Meta:
        verbose_name = 'Pack de service'
        verbose_name_plural = 'Packs de services'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        slug = slugify(self.titre)
        unique_slug = slug
        num = 1
        while PackService.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{num}'
            num += 1
        return unique_slug

    def __str__(self):
        return self.titre
    ####
class Blog(models.Model):
        titre = models.CharField(verbose_name="Titre du blog", max_length=255)
        contenu = models.TextField(verbose_name="Contenu du blog")
        image = models.ImageField(upload_to='blogs/images/', verbose_name="Image du blog", blank=True, null=True)
        date_publication = models.DateTimeField(verbose_name="Date de publication", auto_now=True)
        slug = models.SlugField(unique=True, max_length=255, blank=True)

        class Meta:
            verbose_name = 'Blog'
            verbose_name_plural = 'Blogs'

        def save(self, *args, **kwargs):
            if not self.slug:
                self.slug = self.generate_unique_slug()
            super().save(*args, **kwargs)

        def generate_unique_slug(self):
            slug = slugify(self.titre)
            unique_slug = slug
            num = 1
            while Blog.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{slug}-{num}'
                num += 1
            return unique_slug

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
