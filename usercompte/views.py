from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import RegistrationForm,LoginForm
from .models import StatutUtilisateur, MentorProfile
# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Ravi de vous revoir {user.first_name} !")
            return redirect('shine:homepage') # Remplace par ta page d'accueil
        else:
            messages.error(request, "E-mail ou mot de passe incorrect.")
    else:
        form = LoginForm()
    
    return render(request, 'usercompte/login.html', {'form': form})
#
def user_register(request):
    return render(request, 'usercompte/register.html')
#
def user_register_mentor(request):
    return render(request, 'usercompte/userregister/mentorregister.html')
#
def user_register_business(request):
    return render(request, 'usercompte/userregister/businessregister.html')
#
def user_admin_client(request):
    return render(request, 'usercompte/useradmin/clientadmin.html')
#
def user_admin_mentor(request):
    return render(request, 'usercompte/useradmin/mentoradmin.html')
def register_client_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Ici, form.save() appelle la méthode que nous avons écrite au-dessus
            user = form.save() 
            messages.success(request, "Compte créé !")
            return redirect('usercompte:login')
        else:
            # En cas d'erreur, le script JS dans ton template 
            # te renverra à la bonne étape (1, 2 ou 4)
            messages.error(request, "Erreur dans le formulaire.")
    else:
        form = RegistrationForm()

    return render(request, 'usercompte/userregister/clientregister.html', {'form': form})