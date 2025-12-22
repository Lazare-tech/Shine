from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DemandeDevisForm, ContactMessageForm, NewsLetterForm
from django.http import JsonResponse
import phonenumbers
# Create your views here.
def home(request):
    return render(request,'shine/body/index.html')
#............................................................................................

# def contact_view(request):
#     form = ContactMessageForm(request.POST or None)
#     if request.method == 'POST':
#         data = request.POST.copy()
#         code_pays = data.get('pays') 
#         print("paaa",code_pays)
#         numero_local = data.get('numero_telephone') # Ex: '70112233'
#         print("numero_local",numero_local)
#         try:
#             # On parse le numéro en fonction du pays choisi
#             parsed_number = phonenumbers.parse(numero_local, code_pays)
#             if phonenumbers.is_valid_number(parsed_number):
#                 # On convertit au format international : +22670112233
#                 data['numero_telephone'] = phonenumbers.format_number(
#                     parsed_number, phonenumbers.PhoneNumberFormat.E164
#                 )
#                 print("numéro formaté",data['numero_telephone'])
#         except:
#             form = ContactMessageForm(data)
        
#             if form.is_valid():
#                 form.save()
#                 # On peut ajouter un message de succès ici
#                 messages.success(request, "Votre message a été envoyé avec succès ! Nous vous répondrons dans les plus brefs délais.",extra_tags='contact_success')
#                 return redirect('shine:contact')
#             else:
#                 form = ContactMessageForm()
    
#     return render(request, 'shine/body/contact.html', {'form': form})
from django.contrib import messages # Pour les messages de succès

def contact_view(request):
    if request.method == 'POST':
        data = request.POST.copy()
        code_pays = data.get('pays') 
        numero_local = data.get('numero_telephone')

        form = ContactMessageForm(data)

        if code_pays and numero_local:
            try:
                # On essaie de formater
                parsed_number = phonenumbers.parse(numero_local, code_pays)
                if phonenumbers.is_valid_number(parsed_number):
                    formatted = phonenumbers.format_number(
                        parsed_number, phonenumbers.PhoneNumberFormat.E164
                    )
                    data['numero_telephone'] = formatted
                    form.data = data # On met à jour le formulaire avec le format +226...
                else:
                    # MESSAGE D'ERREUR PERSONNALISÉ
                    form.add_error('numero_telephone', f"Le numéro saisi n'est pas valide pour le pays choisi ({code_pays}).")
            except Exception:
                form.add_error('numero_telephone', "Veuillez entrer un numéro de téléphone valide.")

        if form.is_valid():
            form.save()
            # 1. On ajoute un message de succès
            messages.success(request, "Votre message a été envoyé avec succès !")
            # 2. ON REDIRIGE pour vider le formulaire
            return redirect('shine:contact') 
    else:
        form = ContactMessageForm()
    
    return render(request, 'shine/body/contact.html', {'form': form})
#............................................................................................
def faq(request):
    return render(request,'shine/body/faq.html')    
#............................................................................................
def about(request):
    return render(request,'shine/body/about.html')    
#............................................................................................

def demande_devis_view(request):
    if request.method == 'POST':
        form = DemandeDevisForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre demande de devis a été envoyée avec succès ! Un conseiller vous contactera sous 24h.",extra_tags='devis_success')
            return redirect('shine:devis') 
    else:
        form = DemandeDevisForm()
    
    return render(request, 'shine/body/devis.html', {'form': form})
#............................................................................................
def mentorat(request):
    return render(request,'shine/body/mentorat.html')    
#............................................................................................
def infos_bourses(request):
    return render(request,'shine/body/infos_bourse.html')    
#............................................................................................ 

def about_us(request):
    return render(request,'shine/body/about.html')
#............................................................................................
def blog(request):
    return render(request,'shine/body/blog.html')
                                    # SERVICES PAGES
#............................................................................................ 
def etude(request):
    return render(request,'shine/services/etude.html')
#............................................................................................
def newsletter_subscribe(request):
    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Merci ! Vous êtes maintenant abonné à notre newsletter.'
            })
        else:
            # On récupère la première erreur du dictionnaire
            errors = form.errors.get('email', ["Une erreur est survenue."])
            return JsonResponse({
                'status': 'error',
                'message': errors[0]
            }, status=400)
            
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)