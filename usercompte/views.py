from django.conf import settings
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .forms import RegistrationForm,LoginForm,MentorRegistrationForm,ProfileUpdateForm,MentorProfileForm
from .models import StatutUtilisateur, MentorProfile
from shine.models import DemandeDevis, ContactMessage,SouscriptionEtablissement,SouscriptionEtude,SouscriptionLogement,SouscriptionMobilite,SouscriptionSoutien
from .models import EtapeDossier,SuiviDossier
from django.contrib.auth.decorators import login_required
from django.db import transaction
###
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView
)
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
#
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            # 1. On récupère l'utilisateur
            user = form.get_user()
            
            # 2. On récupère le rôle choisi sur l'interface (bouton cliqué)
            chosen_role = request.POST.get('selected_role', '').lower()

            if not chosen_role:
                messages.error(request, "Veuillez sélectionner un profil (Client, Mentor, etc.)")
                return render(request, 'usercompte/connecting/login.html', {'form': form})

            # 3. VERIFICATION : Est-ce que le profil en base correspond au choix ?
            if user.profil:
                db_role = user.profil.profil_name.lower()
                
                # Comparaison (on vérifie si le mot clé est contenu dans le nom du profil)
                if chosen_role not in db_role:
                    messages.error(request, f"Ce compte n'est pas enregistré en tant que {chosen_role.capitalize()}.")
                    return render(request, 'usercompte/connecting/login.html', {'form': form})

                # 4. Si c'est ok, on connecte
                login(request, user)
                if request.POST.get('remember_me'):
                    # L'utilisateur a coché : on utilise la durée du settings (2 semaines)
                    request.session.set_expiry(settings.SESSION_COOKIE_AGE)
                else:
                    # L'utilisateur n'a PAS coché : on force l'expiration à la fermeture du navigateur
                    request.session.set_expiry(0)
                # 5. Redirection selon le profil confirmé
                if 'mentor' in db_role:
                    return redirect('usercompte:adminmentor')
                elif 'client' in db_role or 'étudiant' in db_role:
                    return redirect('usercompte:adminclient')
                elif 'apporteur' in db_role:
                    return redirect('shine:homepage')
            else:
                messages.error(request, "Ce compte n'a aucun profil associé.")
        else:
            messages.error(request, "Identifiants invalides.")
    else:
        form = LoginForm()
    
    return render(request, 'usercompte/connecting/login.html', {'form': form})

#
def user_register(request):
    return render(request, 'usercompte/connecting/register.html')
#


def user_admin_mentor(request):
    return render(request, 'usercompte/useradmin/mentoradmin.html')
#

def register_client_view(request):
    
    form = RegistrationForm(request.POST or None)
    
    if request.method == 'POST':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if form.is_valid():
                form.save()
                return JsonResponse({
                    'status': 'success', 
                    'message': 'Compte créé avec succès !',
                    'redirect_url': '/usercompte/login/'})
                
            else:
                return JsonResponse({
                    'status': 'error', 
                    'message': 'Veuillez corriger les erreurs ci-dessous.', 
                    'errors': form.errors.get_json_data()
                }, status=400)
    
    return render(request, 'usercompte/userregister/clientregister.html', {'form': form})
# ##
def register_mentor_view(request):
    form = MentorRegistrationForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            return JsonResponse({
                'status': 'success', 
                'message': "Félicitations ! Votre candidature a été soumise.",
                'redirect_url': '/usercompte/login/'
            })
        else:
            # On renvoie les erreurs au format JSON
            return JsonResponse({
                'status': 'error', 
                'errors': form.errors
            }, status=400)
            
    return render(request, 'usercompte/userregister/mentorregister.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect('usercompte:login') # Redirige vers la page de connexion





@login_required
def dashboard_view(request):
    user = request.user
    
    # 1. Récupération du dossier de suivi (Plan de route)
    try:
        dossier = SuiviDossier.objects.get(etudiant=user)
    except SuiviDossier.DoesNotExist:
        dossier = None

    # 2. Récupération de TOUTES les souscriptions de l'utilisateur
    # On récupère chaque type et on les transforme en liste
    soutiens = SouscriptionSoutien.objects.filter(user=user)
    etudes = SouscriptionEtude.objects.filter(user=user)
    mobilites = SouscriptionMobilite.objects.filter(user=user)
    etablissements = SouscriptionEtablissement.objects.filter(user=user)
    logements = SouscriptionLogement.objects.filter(user=user)

    # On combine tout dans une seule liste pour le template
    toutes_souscriptions = list(soutiens) + list(etudes) + list(mobilites) + list(etablissements) + list(logements)
    # Trier par date de demande (la plus récente en premier)
    toutes_souscriptions.sort(key=lambda x: x.date_demande, reverse=True)

    # 3. Récupération des devis (basé sur l'email)
    mes_demandes_devis = DemandeDevis.objects.filter(email=user.email).order_by('-date_envoi')
    
    # 4. Étapes pour le plan de route
    toutes_les_etapes = EtapeDossier.objects.all().order_by('ordre')

    context = {
        'dossier': dossier,
        'etapes': toutes_les_etapes,
        'souscriptions': toutes_souscriptions, # Nouvelle variable
        'mes_demandes': mes_demandes_devis,
    }
    return render(request, 'usercompte/useradmin/clientadmin.html', context)
@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('usercompte:adminclient')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    context = {
        'form': form,
        'completion': request.user.profile_completion_percentage()
    }
    return render(request, 'usercompte/useradmin/profile_cla.html', context)
#
@login_required
def user_admin_mentor(request):
    # 1. Récupération des demandes de devis associées à l'e-mail du mentor
    user = request.user
    # On s'assure que le profil mentor existe
    mentor_profile, created = MentorProfile.objects.get_or_create(user=user)
    
    completion = user.profile_completion_percentage()
    
    context = {
        'completion': completion,
        'mentor_profile': mentor_profile,
    }
    
    # 5. On renvoie le rendu final
    return render(request, 'usercompte/useradmin/mentoradmin.html', context)

@login_required
@transaction.atomic
def update_mentor_profile(request):
    user = request.user
    mentor_profile = user.mentor_profile 

    if request.method == 'POST':
        form = MentorProfileForm(request.POST, instance=mentor_profile)
        if form.is_valid():
            form.save() # Sauve job_title, motivation, etc.
            
            # Sauve les champs de l'User
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.phone = form.cleaned_data['phone']
            user.city = form.cleaned_data['city']
            user.country = form.cleaned_data['country_residence'] # Nouveau
            user.statut = form.cleaned_data['statut'] # Nouveau
            user.save()
            
            messages.success(request, "Profil mis à jour !")
            return redirect('usercompte:adminmentor')
    else:
        # N'oublie pas de charger les données actuelles ici
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone,
            'city': user.city,
            'country_residence': user.country,
            'statut': user.statut,
        }
        form = MentorProfileForm(instance=mentor_profile, initial=initial_data)

    return render(request, 'usercompte/useradmin/profile_m.html', {'form': form})
##
class MyPasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name = 'usercompte/connecting/password_reset.html'
    email_template_name = 'usercompte/connecting/password_reset_email.html'
    subject_template_name = 'usercompte/connecting/password_reset_subject.txt'
    success_url = reverse_lazy('usercompte:password_reset_done')
    success_message = "Un lien de réinitialisation a été envoyé à votre adresse email."

class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'usercompte/connecting/password_reset_done.html'

class MyPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = 'usercompte/connecting/password_reset_confirm.html'
    success_url = reverse_lazy('usercompte:password_reset_complete')
    success_message = "Votre mot de passe a été réinitialisé avec succès."

class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'usercompte/connecting/password_reset_complete.html'