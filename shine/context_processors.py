from django.shortcuts import render
##
def social_media_links(request):
    context={
            'facebook_url': 'https://web.facebook.com/SHNAGENCY',
            'tiktok_url':'https://vm.tiktok.com/ZSHKLbam9tLDw-EzZ7y/',
            'instagram_url':'https://www.instagram.com/shineagency226?igsh=dGUxbmhvM2xia21x',
    }
    return context
##
def info_contact(request):
    context={
        'phone_number': '+226 70 24 24 24',
        'email_address':'shineagency226@gmail.com',
        'location':'Burkina-Faso,Bobo-Dioulasso,secteur 5 face à megamonde ',
    }