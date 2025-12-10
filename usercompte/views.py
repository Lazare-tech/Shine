from django.shortcuts import render

# Create your views here.
def user_login(request):
    return render(request, 'usercompte/login.html')
#
def user_register(request):
    return render(request, 'usercompte/register.html')
#
def user_register_client(request):
    return render(request, 'usercompte/userregister/clientregister.html')
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