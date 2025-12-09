
from django.urls import path,include
import usercompte.views
##
app_name= "usercompte"
urlpatterns = [
    path('login/',usercompte.views.user_login,name='login'),
    path('register/',usercompte.views.user_register,name='register'),
]