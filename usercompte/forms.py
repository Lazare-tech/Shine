from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, StatutUtilisateur,ProfilUtilisateur,MentorProfile
from django.contrib.auth.forms import AuthenticationForm
from django_countries.fields import CountryField
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
import phonenumbers


class RegistrationForm(UserCreationForm):
    statut = forms.ModelChoiceField(
        queryset=StatutUtilisateur.objects.all(),
        empty_label="Sélectionnez votre statut",
        widget=forms.Select(attrs={'class': 'form-select shadow-sm'})
    )
    profil_name=forms.ModelChoiceField(
        queryset=ProfilUtilisateur.objects.exclude(profil_name__icontains='Mentor'),
        empty_label="Sélectionnez votre profil",
        widget=forms.Select(attrs={'class': 'form-select shadow-sm'})
    )
    pays = CountryField(blank_label='Sélectionnez votre pays').formfield(
        widget=forms.Select(attrs={
            'class': 'form-select shadow-sm',
            'style': 'max-width: none !important; border-radius: 8px 0 0 8px;' # Correction affichage
        })
    )
    phone = PhoneNumberField(
        region=None, 
        widget=forms.TextInput(attrs={
            'class': 'form-control shadow-sm',
            'placeholder': '70112233',
            'style': 'border-radius: 0 8px 8px 0;'
        })
    )
    class Meta(UserCreationForm.Meta):
        model = User
        # L'username est retiré d'ici car on le remplit via l'email dans save()
        fields = (
             'email', 'first_name', 'last_name', 'gender', 
            'phone','birth_year', 'code_postal','nationality', 'country', 'city', 
            'street_number', 'street_name'
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control shadow-sm'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control shadow-sm'}),
            'email': forms.EmailInput(attrs={'class': 'form-control shadow-sm'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control shadow-sm'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control shadow-sm', 'placeholder': 'Mot de passe'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control shadow-sm', 'placeholder': 'Confirmez le mot de passe'}),
            'birth_year': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control shadow-sm', 'type': 'date'}
            ),
            'gender': forms.Select(
                choices=[('', 'Sélectionnez'), ('Homme', 'Homme'), ('Femme', 'Femme')], 
                attrs={'class': 'form-select shadow-sm'}
            ),
           
            'city': forms.TextInput(attrs={'class': 'form-control shadow-sm'}),
            'country': forms.TextInput(attrs={'class': 'form-control shadow-sm'}),
            'street_number': forms.TextInput(attrs={'class': 'form-control shadow-sm'}),
            'code_postal': forms.TextInput(attrs={'class': 'form-control shadow-sm'}),
            'street_number': forms.TextInput(attrs={'class': 'form-control shadow-sm'}),
            'street_name': forms.TextInput(attrs={'class': 'form-control shadow-sm'}),
           
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Force la classe de base si elle n'existe pas
            existing_classes = field.widget.attrs.get('class', 'form-control shadow-sm')
            
            # Ajout du rouge si Django détecte une erreur au rechargement
            if self.errors.get(field_name):
                if 'is-invalid' not in existing_classes:
                    existing_classes = f"{existing_classes} is-invalid"
            
            field.widget.attrs['class'] = existing_classes.strip()
            field.widget.attrs['required'] = 'required'
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse email est déjà utilisée.")
        return email


    def clean(self):
        cleaned_data = super().clean()
        pays_code = cleaned_data.get('pays') # Renvoie 'BF', 'FR', 'CI', etc.
        phone_raw = cleaned_data.get('phone')

        if pays_code and phone_raw:
            try:
                # 1. On convertit l'objet PhoneNumber en chaîne brute
                phone_str = str(phone_raw)
                
                # 2. On parse le numéro avec le code pays en contexte
                # (Cela permet de valider même si l'utilisateur n'a pas tapé +226)
                parsed_number = phonenumbers.parse(phone_str, pays_code)
                
                # 3. On vérifie si le numéro est valide pour CETTE région spécifique
                if not phonenumbers.is_valid_number_for_region(parsed_number, pays_code):
                    # On récupère l'exemple de format pour aider l'utilisateur
                    example = phonenumbers.get_example_number(pays_code)
                    self.add_error('phone', f"Numéro invalide pour ce pays. Exemple attendu: {example.national_number}")
                    
            except Exception:
                self.add_error('phone', "Le format du numéro est incorrect.")
                
        return cleaned_data
    
    def save(self, commit=True):
        # 1. On récupère l'objet user (en mémoire, pas encore en base)
        user = super().save(commit=False)
        
        # 2. On lie l'email à l'username
        user.username = self.cleaned_data["email"]

        # 3. RÉCUPÉRATION MANUELLE DES CHAMPS HORS META
        # On va chercher les données nettoyées et on les injecte dans l'objet user
        user.statut = self.cleaned_data.get('statut')
        
        # Note : on récupère 'profil_name' du formulaire pour le mettre dans 'profil' du modèle
        user.profil = self.cleaned_data.get('profil_name') 
        
        # 4. Enregistrement réel dans PostgreSQL
        if commit:
            user.save()
        return user
#
class LoginForm(AuthenticationForm):
    # On renomme le label "Nom d'utilisateur" en "Email"
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control input-custom',
        'placeholder': "E-mail"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control input-custom',
        'placeholder': 'Mot de passe'
    }))
##
class MentorRegistrationForm(UserCreationForm):
    # Champs additionnels provenant du modèle MentorProfile
    job_title = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    activity_field = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    bank_rib = forms.CharField(max_length=34, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    mission_type = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    motivation = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))

    # Statut et Profil (souvent masqués ou pré-remplis pour les mentors)
    profil = forms.ModelChoiceField(
        queryset=ProfilUtilisateur.objects.all(),
        required=False,
        empty_label="Sélectionnez votre type de profil",
        widget=forms.Select(attrs={'class': 'form-select shadow-sm'})
    )
    statut = forms.ModelChoiceField(
        queryset=StatutUtilisateur.objects.all(),
        empty_label="Votre statut actuel",
        widget=forms.Select(attrs={'class': 'form-select shadow-sm'})
    )
    pays = CountryField(blank_label='Sélectionnez votre pays').formfield(
        widget=forms.Select(attrs={
            'class': 'form-select shadow-sm',
            'style': 'max-width: none !important; border-radius: 8px 0 0 8px;' # Correction affichage
        })
    )
    # Modifie cette ligne dans ton forms.py
    phone = forms.CharField( # On utilise CharField ici pour éviter la validation automatique trop stricte
        widget=forms.TextInput(attrs={
            'class': 'form-control shadow-sm',
            'placeholder': '70112233',
            'style': 'border-radius: 0 8px 8px 0;'
        })
    )
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'email', 'first_name', 'last_name', 'gender', 'phone', 
            'birth_year', 'nationality', 'country', 'city', 
            'code_postal', 'street_number', 'street_name',
        )
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_year': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(
                choices=[('', 'Sélectionnez'), ('Homme', 'Homme'), ('Femme', 'Femme')], 
                attrs={'class': 'form-select shadow-sm'}
            ),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'code_postal': forms.TextInput(attrs={'class': 'form-control'}),
            'street_number': forms.TextInput(attrs={'class': 'form-control'}),
            'street_name': forms.TextInput(attrs={'class': 'form-control'}),

            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        
        
         
  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            # 1. On récupère les classes existantes ou on initialise form-control
            existing_classes = field.widget.attrs.get('class', 'form-control shadow-sm')
            
            # 2. On force l'attribut HTML 'required' pour tous les champs
            # Sauf profil s'il est géré en automatique
            if field_name != 'profil':
                field.required = True
                field.widget.attrs['required'] = 'required'

            # 3. Si le formulaire a été soumis et que le champ est vide ou en erreur
            if self.is_bound and field_name in self.errors:
                if 'is-invalid' not in existing_classes:
                    existing_classes = f"{existing_classes} is-invalid"
            
            field.widget.attrs['class'] = existing_classes.strip()
    
    def clean(self):
        cleaned_data = super().clean()
        pays_code = cleaned_data.get('pays') # Code ISO (ex: 'BF')
        phone_raw = cleaned_data.get('phone')

        if pays_code and phone_raw:
            try:
                # On convertit en string (ex: '70112233')
                phone_str = str(phone_raw)
                
                # On parse le numéro EN UTILISANT le pays choisi comme contexte
                # C'est cette ligne qui permet de valider un numéro local
                parsed_number = phonenumbers.parse(phone_str, pays_code)
                
                # On vérifie si le numéro est valide pour ce pays précis
                if not phonenumbers.is_valid_number_for_region(parsed_number, pays_code):
                    example = phonenumbers.get_example_number(pays_code)
                    self.add_error('phone', f"Numéro invalide pour ce pays. Exemple attendu : {example.national_number}")
                else:
                    # OPTIONNEL : On remplace la valeur par le format international propre (+22670...)
                    cleaned_data['phone'] = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
            
            except Exception:
                self.add_error('phone', "Format de numéro incorrect.")
        
        return cleaned_data
    def save(self, commit=True):
        # 1. On récupère l'utilisateur créé par UserCreationForm
        user = super().save(commit=False)
        
        # 2. On injecte les données critiques
        email = self.cleaned_data.get("email")
        user.username = email
        user.email = email
        user.statut = self.cleaned_data.get('statut')
        
        # Attribution auto du profil Mentor
        if not self.cleaned_data.get('profil'):
            try:
                from .models import ProfilUtilisateur
                user.profil = ProfilUtilisateur.objects.filter(profil_name__icontains="Mentor").first()
            except:
                pass
        else:
            user.profil = self.cleaned_data.get('profil')

        if commit:
            user.save() # Sauvegarde l'User en base
            
            # 3. Création du profil Mentor
            from .models import MentorProfile
            MentorProfile.objects.update_or_create(
                user=user,
                defaults={
                    'job_title': self.cleaned_data.get('job_title'),
                    'activity_field': self.cleaned_data.get('activity_field'),
                    'bank_rib': self.cleaned_data.get('bank_rib'),
                    'mission_type': self.cleaned_data.get('mission_type'),
                    'motivation': self.cleaned_data.get('motivation'),
                }
            )
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'phone', 'birth_year', 
                  'nationality', 'country', 'city', 'statut', 'profil']
        widgets = {
            'birth_year': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            # Ajoute d'autres widgets stylisés ici
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control shadow-none'})