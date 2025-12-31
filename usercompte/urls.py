
from django.urls import path,include
import usercompte.views
##
app_name= "usercompte"
urlpatterns = [
    path('login/',usercompte.views.login_view,name='login'),
    path('register/',usercompte.views.user_register,name='register'),
    path('logout/', usercompte.views.logout_view, name='logout'),
    path('register_client/', usercompte.views.register_client_view, name='registerclient'),
    path('mentorregister/',usercompte.views.register_mentor_view,name='registermentor'),
    path('businessregister/',usercompte.views.user_register_business,name='registerbusiness'),
    # ADMIN CLIENT

    path('clientadmin/', usercompte.views.dashboard_view, name='adminclient'),
    path('profile/edit/', usercompte.views.profile_edit_view, name='profile_edit'),
    path('update_mentor_profile/', usercompte.views.update_mentor_profile, name='update_mentor_profile'),
    path('mentoradmin/', usercompte.views.user_admin_mentor, name='adminmentor'),
]