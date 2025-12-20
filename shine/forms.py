from django import forms
from .models import DemandeDevis,ContactMessage

#############################
class DemandeDevisForm(forms.ModelForm):
    
    # On définit les choix ici pour une meilleure maintenance
    SERVICE_CHOICES = [
        ('Etudes Internationales', 'Etudes Internationales'),
        ('Mobilité Générale (Hors Études)', 'Mobilité Générale (Hors Études)'),
        ('Accompagnement des Établissements Scolaires', 'Accompagnement des Établissements Scolaires'),
        ('Soutien Scolaire', 'Soutien Scolaire'),
        ('Logement & Accueil & Installation', 'Logement & Accueil & Installation'),
    ]

    service_souhaite = forms.ChoiceField(
        choices=SERVICE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Service souhaité"
    )

    email = forms.EmailField(
        error_messages={
            'invalid': "Oups ! Cette adresse email ne semble pas correcte (ex: nom@domaine.com).",
            'required': "L'adresse email est obligatoire pour que nous puissions vous répondre."
        },
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'votre@email.com'})
    )
    class Meta:
        model = DemandeDevis
        # On mappe les champs du modèle aux champs du formulaire
        fields = ['nom', 'numero_telephone', 'email', 'service_souhaite', 'contenu']
        
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Votre nom et prénom'
            }),
            'numero_telephone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Votre numéro de téléphone',
                'type': 'tel'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Votre adresse email'
            }),
            'contenu': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Décrivez votre projet en quelques mots...',
                'rows': 4
            }),
        }
####
class ContactMessageForm(forms.ModelForm):
    email = forms.EmailField(
        error_messages={
            'invalid': "Oups ! Cette adresse email ne semble pas correcte (ex: nom@domaine.com).",
            'required': "L'adresse email est obligatoire pour que nous puissions vous répondre."
        },
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'votre@email.com'})
    )
    class Meta:
        model = ContactMessage
        # On exclut le slug car il est généré automatiquement dans le save() du modèle
        fields = ['nom', 'email', 'numero_telephone', 'objet', 'contenu']
        
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre nom',
                'id': 'nom'
            }),
          
            
            'numero_telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ex:+226numéro',
                'id': 'telephone',
                'type': 'tel'
            }),
            'objet': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Objet de votre message',
                'id': 'objet'
            }),
            'contenu': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Votre message',
                'id': 'message',
                'rows': 4
            }),
        }