
from django.urls import path,include
import usercompte.views
##
app_name= "usercompte"
urlpatterns = [
    path('login/',usercompte.views.user_login,name='login'),
    path('register/',usercompte.views.user_register,name='register'),
    path('clientregister/',usercompte.views.user_register_client,name='registerclient'),
    path('mentorregister/',usercompte.views.user_register_mentor,name='registermentor'),
    path('businessregister/',usercompte.views.user_register_business,name='registerbusiness'),
    # ADMIN CLIENT
    path('clientadmin/',usercompte.views.user_admin_client,name='adminclient'),
    path('mentoradmin/',usercompte.views.user_admin_mentor,name='adminmentor'),
]