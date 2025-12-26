from django.shortcuts import render
from .models import Service,AvisClient,Equipe
##
def social_media_links_processor(request):
    context={
            'facebook_url': 'https://web.facebook.com/SHNAGENCY',
            'tiktok_url':'https://vm.tiktok.com/ZSHKLbam9tLDw-EzZ7y/',
            'instagram_url':'https://www.instagram.com/shineagency226?igsh=dGUxbmhvM2xia21x',
    }
    return context
##
def info_contact_processor(request):
    context={
        'phone_number': '+226 70 24 24 24',
        'email_address':'shineagency226@gmail.com',
        'location':'Burkina-Faso,Bobo-Dioulasso,secteur 5 face à megamonde ',
    }
####
def services_list_processor(request):
    services = Service.objects.all()
    return {'services': services}
###
def avis_clients_processor(request):
    avis = AvisClient.objects.filter(is_published=True).order_by('-id')
    
    context={
        'avis':avis,
    }
    return context
###
def equipe_list_processor(request):
    membres = Equipe.objects.filter(is_active=True).order_by('nom')
    context={
        'membres':membres,
    }
    return context