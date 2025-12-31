from django import forms
from .models import DemandeDevis, ContactMessage,News_letter
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .models import Service
import phonenumbers

class DemandeDevisForm(forms.ModelForm):
    # 1. On garde 'pays'
    pays = CountryField(blank_label='Pays').formfield(
        widget=forms.Select(attrs={
            'class': 'form-select shadow-sm',
            'style': 'max-width: none !important; border-radius: 8px 0 0 8px;'
        })
    )

    # 2. On supprime 'phone' et on définit proprement 'numero_telephone' ICI
    # C'est ce champ que ton modèle 'DemandeDevis' utilise probablement
    # numero_telephone = forms.CharField(
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control shadow-sm',
    #         'placeholder': '70112233',
    #         'style': 'border-radius: 0 8px 8px 0;'
    #     })
    # )
    numero_telephone  = PhoneNumberField(
        region=None, # On laisse None pour qu'il valide selon l'indicatif
        widget=forms.TextInput(attrs={
            'class': 'form-control shadow-sm',
            'placeholder': 'Numéro (ex: 70123456)',
            'style': 'border-radius: 0 8px 8px 0;'
        })
    )
    service_souhaite = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        empty_label="Sélectionnez un service",
        widget=forms.Select(attrs={'class': 'form-select shadow-sm'})
    )

    class Meta:
        model = DemandeDevis
        # Vérifie bien que le champ dans ton modèle s'appelle 'numero_telephone'
        fields = ['nom', 'email', 'pays', 'numero_telephone', 'service_souhaite', 'contenu']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'votre@email.com'}),
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'service_souhaite' in self.fields:
            self.fields['service_souhaite'].label_from_instance = lambda obj: obj.titre
   
    
class ContactMessageForm(forms.ModelForm):
    email = forms.EmailField(
        error_messages={
            'invalid': "L'adresse email est incorrecte.",
            'required': "L'adresse email est obligatoire."
        },
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'votre@email.com'})
    )

    # 1. On définit le champ pays explicitement
    pays = CountryField(blank_label='Pays').formfield(
        widget=forms.Select(attrs={
            'class': 'form-select',
            'style': ' border-radius: 8px 0 0 8px;'
        })
    )
    numero_telephone = PhoneNumberField(
        region=None, # On laisse None pour qu'il valide selon l'indicatif
        widget=forms.TextInput(attrs={
            'class': 'form-control shadow-sm',
            'placeholder': 'Numéro (ex: 70123456)',
            'style': 'border-radius: 0 8px 8px 0;'
        })
    )

    class Meta:
        model = ContactMessage
        # 2. IMPORTANT: Il FAUT ajouter 'pays' dans la liste des fields ici
        fields = ['nom', 'email', 'pays', 'numero_telephone', 'objet', 'contenu']
        
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}),
            'objet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Objet'}),
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            # 3. Simple TextInput pour éviter la validation automatique "PhoneNumber"
            'numero_telephone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '70112233',
                'style': 'border-radius: 0 8px 8px 0;'
            }),
        }
#............................................................................................
class NewsLetterForm(forms.ModelForm):
    email = forms.EmailField(
        label="Votre adresse email",
        error_messages={
            'invalid': "Veuillez entrer une adresse email valide (ex: contact@domaine.com).",
            'required': "L'email est nécessaire pour s'abonner.",
            'unique': "Cette adresse email est déjà inscrite à notre newsletter."
        },
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre email...',
            'id': 'newsletter-email'
        })
    )

    class Meta:
        model = News_letter
        # On ne demande que l'email, le slug et la date sont gérés automatiquement
        fields = ['email']

    def clean_email(self):
        """Vérifie si l'email existe déjà pour éviter les doublons proprement"""
        email = self.cleaned_data.get('email').lower() # On passe tout en minuscule
        if News_letter.objects.filter(email=email).exists():
            raise forms.ValidationError("Vous êtes déjà inscrit à notre newsletter !")
        return email
    
    
    def clean(self):
        cleaned_data = super().clean()
        pays_obj = cleaned_data.get('pays')
        phone_raw = cleaned_data.get('phone')

        if pays_obj and phone_raw:
            # On combine le code pays et le numéro
            # pays_obj.code est "BF", "FR", etc.
            # phonenumber_field fait la validation automatiquement ici
            pass 
        return cleaned_data