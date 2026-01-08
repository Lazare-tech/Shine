from django import forms
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .models import Service,Consultation,DemandeDevis, ContactMessage,News_letter,SouscriptionSoutien,SouscriptionEtablissement,SouscriptionEtude,SouscriptionMobilite,SouscriptionLogement
from phonenumber_field.phonenumber import to_python
import phonenumbers
from django.core.validators import RegexValidator

class DemandeDevisForm(forms.ModelForm):
    email = forms.EmailField(
        error_messages={
            'invalid': "Veuillez entrer une adresse email valide (ex: contact@domaine.com).",
            'required': "L'email est obligatoire.",
        }),
    pays = CountryField(blank_label='Pays').formfield(
        widget=forms.Select(attrs={
            'class': 'form-select shadow-sm',
            'style': 'max-width: none !important; border-radius: 8px 0 0 8px;'
        })
    )

    # On utilise CharField pour garder le contrôle total sur l'erreur
    numero_telephone = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control shadow-sm',
            'placeholder': '70112233',
            'style': 'border-radius: 0 8px 8px 0;'
        }),
        error_messages={'required': "Le numéro de téléphone est obligatoire."}
    )

    service_souhaite = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        empty_label="Sélectionnez un service",
        widget=forms.Select(attrs={'class': 'form-select shadow-sm'}),
        error_messages={'required': "Veuillez sélectionner un service."}
    )

    class Meta:
        model = DemandeDevis
        fields = ['nom', 'email', 'pays', 'numero_telephone', 'service_souhaite', 'contenu']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'votre@email.com'}),
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        error_messages = {
            'nom': {'required': "Ce champ est requis."},
            'contenu': {'required': "Veuillez préciser votre demande."},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'service_souhaite' in self.fields:
            self.fields['service_souhaite'].label_from_instance = lambda obj: obj.titre
        
        # LOGIQUE DU CHAMP ROUGE : Si erreurs, on ajoute 'is-invalid'
        if self.errors:
            for field_name, field in self.fields.items():
                if field_name in self.errors:
                    classes = field.widget.attrs.get('class', '')
                    if 'is-invalid' not in classes:
                        field.widget.attrs['class'] = f"{classes} is-invalid"
    def clean_email(self):
        """Vérifie si l'email existe déjà pour éviter les doublons proprement"""
        email = self.cleaned_data.get('email').lower() # On passe tout en minuscule
        if DemandeDevis.objects.filter(email=email).exists():
            raise forms.ValidationError("Email invalid !")
        return email   
    
    
    def clean_numero_telephone(self):
        """ Validation du numéro en fonction du pays choisi """
        pays_code = self.data.get('pays')
        numero_brut = self.cleaned_data.get('numero_telephone')

        if not pays_code:
            raise forms.ValidationError("Sélectionnez d'abord un pays.")

        try:
            # Tente de convertir le numéro local en format international via le pays
            phone_obj = to_python(numero_brut, region=pays_code)
            
            if not phone_obj or not phone_obj.is_valid():
                raise forms.ValidationError("Numéro invalide pour ce pays.")
            
            return phone_obj # Retourne l'objet PhoneNumber valide pour le modèle
        except Exception:
            raise forms.ValidationError("Format de numéro incorrect.")
    
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
    email = forms.EmailField(
        label="Votre adresse email",
        error_messages={
            'invalid': "Veuillez entrer une adresse email valide (ex: contact@domaine.com).",
            'required': "L'email est obligatoire.",
            'unique': "Cette adresse email est déjà utilisée."
        }),
   
    numero_telephone = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control shadow-sm',
            'placeholder': 'Numéro (ex: 70123456)',
            'style': 'border-radius: 0 8px 8px 0;'
        }),
        error_messages={'required': "Le numéro de téléphone est obligatoire."}
    )
    class Meta:
        model = ContactMessage
        # 2. IMPORTANT: Il FAUT ajouter 'pays' dans la liste des fields ici
        fields = ['nom', 'email', 'pays', 'numero_telephone', 'objet', 'contenu']
        
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}),
            'objet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Objet'}),
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'email':forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Votre email'}),
            # 3. Simple TextInput pour éviter la validation automatique "PhoneNumber"
           
        }

        error_messages = {
            'nom': {
                'required': "Le nom est obligatoire.",
            },
            
            'pays': {
                'required': "Le pays est obligatoire.",
            },
            'numero_telephone': {
                'required': "Le numéro de téléphone est obligatoire.",
            },
            'objet': {
                'required': "L'objet est obligatoire.",
            },
            'contenu': {
                'required': "Le contenu est obligatoire.",
            },
        }
        
    def clean_email(self):
        """Vérifie si l'email existe déjà pour éviter les doublons proprement"""
        email = self.cleaned_data.get('email').lower() # On passe tout en minuscule
        if ContactMessage.objects.filter(email=email).exists():
            raise forms.ValidationError("Email déjà utilisé !")
        return email          
    def clean_numero_telephone(self):
        """
        Validation spécifique pour le numéro de téléphone en fonction du pays
        """
        # On récupère le pays directement depuis self.data car cleaned_data['pays'] 
        # peut ne pas encore être disponible si la validation de pays a échoué.
        pays_code = self.data.get('pays')
        numero_brut = self.cleaned_data.get('numero_telephone')

        if not pays_code:
            raise forms.ValidationError("Veuillez d'abord sélectionner un pays.")

        try:
            # Conversion en format international (ex: BF + 70123456 -> +22670123456)
            phone_number = to_python(numero_brut, region=pays_code)
            
            # Vérification de la validité réelle selon les règles du pays (longueur, préfixe)
            if not phone_number or not phone_number.is_valid():
                raise forms.ValidationError(f"Numéro invalide pour le pays sélectionné ({pays_code}).")
            
            return phone_number
        except Exception:
            raise forms.ValidationError("Format de numéro incorrect.")

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
##
class ConsultationForm(forms.ModelForm):
    pays = CountryField(blank_label='Pays').formfield(
        widget=forms.Select(attrs={
            'class': 'form-select',
            'style': 'border-radius: 8px 0 0 8px;'
        })
    )
    
    # numero_telephone = PhoneNumberField(
    #     region=None,
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control shadow-sm',
    #         'placeholder': 'Numéro (ex: 70123456)',
    #         'style': 'border-radius: 0 8px 8px 0;'
    #     })
    # )
    numero_telephone = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control shadow-sm',
            'placeholder': 'Numéro (ex: 70123456)',
            'style': 'border-radius: 0 8px 8px 0;'
        }),
        error_messages={'required': "Le numéro de téléphone est obligatoire."}
    )

    class Meta:
        model = Consultation
        fields = '__all__'
        error_messages = {
            'nom_complet': {
                'required': "Ce champ est requis.",
            },
            'email': {
                'required': "Veuillez entrer une adresse email.",
                'invalid': "L'adresse email n'est pas valide.",
            },
            'pays': {
                'required': "Veuillez sélectionner un pays.",
            },
            'numero_telephone': {
                'required': "Le numéro de téléphone est obligatoire.",
            },
            'destination': {
                'required': "Veuillez sélectionner une destination.",
            }
        }
        widgets = {
            'nom_complet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Jean Dupont'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'exemple@mail.com'}),
            'destination': forms.Select(attrs={'class': 'form-select'}),
        }
    def clean_numero_telephone(self):
        """
        Validation spécifique pour le numéro de téléphone en fonction du pays
        """
        # On récupère le pays directement depuis self.data car cleaned_data['pays'] 
        # peut ne pas encore être disponible si la validation de pays a échoué.
        pays_code = self.data.get('pays')
        numero_brut = self.cleaned_data.get('numero_telephone')

        if not pays_code:
            raise forms.ValidationError("Veuillez d'abord sélectionner un pays.")

        try:
            # Conversion en format international (ex: BF + 70123456 -> +22670123456)
            phone_number = to_python(numero_brut, region=pays_code)
            
            # Vérification de la validité réelle selon les règles du pays (longueur, préfixe)
            if not phone_number or not phone_number.is_valid():
                raise forms.ValidationError(f"Numéro invalide pour le pays sélectionné ({pays_code}).")
            
            return phone_number
        except Exception:
            raise forms.ValidationError("Format de numéro incorrect.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Gestion des classes is-invalid pour AJAX
        if self.errors:
            for field_name, field in self.fields.items():
                if field_name in self.errors:
                    existing_classes = field.widget.attrs.get('class', '')
                    field.widget.attrs['class'] = f"{existing_classes} is-invalid"
##
# Validateur pour forcer le texte uniquement
text_only = RegexValidator(r'^[a-zA-ZÀ-ÿ\s\-,\.\(\)]+$', "Ce champ ne doit contenir que des lettres.")

class SoutienForm(forms.ModelForm):
    class Meta:
        model = SouscriptionSoutien
        fields = ['niveau_etude', 'objectif_principal', 'matieres']
        labels = {
            'niveau_etude': "Niveau d'études actuel",
            'objectif_principal': "Objectif principal",
            'matieres': "Matières à renforcer",
        }
        widgets = {
            'niveau_etude': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Terminale D'}),
            'objectif_principal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Préparation Baccalauréat'}),
            'matieres': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ex: Mathématiques, PC...'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Indispensable pour ton script JS handleFieldValidation
        for field in self.fields.values():
            field.widget.attrs.update({'class': field.widget.attrs.get('class', '') + ' form-control'})

class EtudeInternationalForm(forms.ModelForm):
    class Meta:
        model = SouscriptionEtude
        fields = ['dernier_diplome', 'pays_destination', 'filiere_visee']
        labels = {
            'dernier_diplome': "Dernier diplôme obtenu",
            'pays_destination': "Pays de destination souhaité",
            'filiere_visee': "Filière ou domaine d'étude",
        }
        widgets = {
            'dernier_diplome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Licence 3'}),
            'pays_destination': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Canada'}),
            'filiere_visee': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Informatique'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Indispensable pour ton script JS handleFieldValidation
        for field in self.fields.values():
            field.widget.attrs.update({'class': field.widget.attrs.get('class', '') + ' form-control'})

class MobiliteForm(forms.ModelForm):
    class Meta:
        model = SouscriptionMobilite
        fields = ['type_visa', 'pays_destination', 'date_prevue']
        labels = {
            'type_visa': "Type de projet (Visa, Voyage...)",
            'pays_destination': "Pays de destination",
            'date_prevue': "Date de départ prévue",
        }
        widgets = {
            'type_visa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Visa Étudiant'}),
            'pays_destination': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: France'}),
            'date_prevue': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Indispensable pour ton script JS handleFieldValidation
        for field in self.fields.values():
            field.widget.attrs.update({'class': field.widget.attrs.get('class', '') + ' form-control'})

class EtablissementForm(forms.ModelForm):
    class Meta:
        model = SouscriptionEtablissement
        fields = ['nom_etablissement', 'nombre_eleves', 'problemes_identifies']
        labels = {
            'nom_etablissement': "Nom de l'établissement scolaire",
            'nombre_eleves': "Nombre d'élèves (environ)",
            'problemes_identifies': "Description des besoins",
        }
        widgets = {
            'nom_etablissement': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Groupe Scolaire Saint-Paul'}),
            'nombre_eleves': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Environ 500 élèves'}),
            'problemes_identifies': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Quels axes souhaitez-vous améliorer ?'}),
        }
        error_messages = {
            'nom_etablissement': {
                'required': "Ce champ est obligatoire.",
            },
            'nombre_eleves': {
                'required': "Ce champ est obligatoire.",
            },
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Indispensable pour ton script JS handleFieldValidation
        for field in self.fields.values():
            field.widget.attrs.update({'class': field.widget.attrs.get('class', '') + ' form-control'})

class LogementForm(forms.ModelForm):
    class Meta:
        model = SouscriptionLogement
        fields = ['ville_destination', 'date_arrivee_prevue', 'type_logement_recherche', 'budget_loyer_max', 'details_vol']
        widgets = {
            'ville_destination': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Paris, Lyon, Montréal...'}),
                        'date_arrivee_prevue': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),

            'type_logement_recherche': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Studio, Chambre CROUS, Colocation...'}),
            'budget_loyer_max': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 500€ - 700€'}),
            'details_vol': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'N° de vol, heure d\'arrivée ou précisions sur le logement...'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Indispensable pour ton script JS handleFieldValidation
        for field in self.fields.values():
            field.widget.attrs.update({'class': field.widget.attrs.get('class', '') + ' form-control'})
