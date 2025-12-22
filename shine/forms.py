from django import forms
from .models import DemandeDevis, ContactMessage,News_letter
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField

class DemandeDevisForm(forms.ModelForm):
    # (Tes autres champs restent identiques...)
    # ...
    class Meta:
        model = DemandeDevis
        fields = ['nom', 'numero_telephone', 'email', 'service_souhaite', 'contenu']
        # ... widgets ...

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
            'style': 'max-width: 120px; border-radius: 8px 0 0 8px;'
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