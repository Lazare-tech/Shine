
from django.urls import path,include
import usercompte.views
from django.contrib.auth import views as auth_views
##
app_name= "usercompte"
urlpatterns = [
    path('login/',usercompte.views.login_view,name='login'),
    path('register/',usercompte.views.user_register,name='register'),
    path('logout/', usercompte.views.logout_view, name='logout'),
    path('register_client/', usercompte.views.register_client_view, name='registerclient'),
    path('mentorregister/',usercompte.views.register_mentor_view,name='registermentor'),
    # ADMIN CLIENT

    path('clientadmin/', usercompte.views.dashboard_view, name='adminclient'),
    path('profile/edit/', usercompte.views.profile_edit_view, name='profile_edit'),
    path('update_mentor_profile/', usercompte.views.update_mentor_profile, name='update_mentor_profile'),
    path('mentoradmin/', usercompte.views.user_admin_mentor, name='adminmentor'),
    
    
    # 1. Page pour demander la réinitialisation (Email)
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='usercompte/connecting/password_reset.html',
        email_template_name='usercompte/connecting/password_reset_email.html',
        subject_template_name='usercompte/connecting/password_reset_subject.txt',
        success_url='/usercompte/password-reset/done/'
    ), name='password_reset'),

    # 2. Confirmation d'envoi de l'email
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='usercompte/connecting/password_reset_done.html'
    ), name='password_reset_done'),

    # 3. Le lien spécial reçu par email (Token)
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='usercompte/connecting/password_reset_confirm.html',
        success_url='/usercompte/password-reset-complete/'
    ), name='password_reset_confirm'),

    # 4. Message de succès final
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='usercompte/connecting/password_reset_complete.html'
    ), name='password_reset_complete'),
]