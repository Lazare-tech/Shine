from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, StatutUtilisateur
from django.contrib.auth.forms import AuthenticationForm

class RegistrationForm(UserCreationForm):
    statut = forms.ModelChoiceField(
        queryset=StatutUtilisateur.objects.all(),
        empty_label="Sélectionnez votre statut",
        widget=forms.Select(attrs={'class': 'form-select shadow-sm'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        # Note : on ne met pas 'password' ici, UserCreationForm gère password1/password2
        fields = (
             'email', 'first_name', 'last_name', 'gender', 
            'phone','birth_year', 'nationality', 'country', 'city', 
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
                attrs={
                    'class': 'form-control shadow-sm',
                    'type': 'date'
                }
            ),
            'gender': forms.Select(
                choices=[('', 'Sélectionnez'), ('Homme', 'Homme'), ('Femme', 'Femme')], 
                attrs={'class': 'form-select shadow-sm'}
            ),
            'phone': forms.TextInput(attrs={'class': 'form-control shadow-sm'}),
            'city': forms.TextInput(attrs={'class': 'form-control shadow-sm'}),
            'country': forms.TextInput(attrs={'class': 'form-control shadow-sm'}),
            'street_number': forms.TextInput(attrs={'class': 'form-control shadow-sm'}),
            'street_name': forms.TextInput(attrs={'class': 'form-control shadow-sm'}),
            'username': forms.TextInput(attrs={'class': 'form-control shadow-sm'}),
            # Widgets pour les mots de passe internes à UserCreationForm
            }
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse email est déjà utilisée.")
        return email
    def save(self, commit=True):
       def save(self, commit=True):
        # 1. On appelle le save du parent (UserCreationForm) avec commit=False 
        # pour obtenir l'objet user sans l'enregistrer tout de suite en base
        user = super().save(commit=False)
        
        # 2. On lie l'email à l'identifiant technique (username)
        user.username = self.cleaned_data["email"]
        
        # 3. On enregistre vraiment si commit est True
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