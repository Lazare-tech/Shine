from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DemandeDevisForm, ContactMessageForm
# Create your views here.
def home(request):
    return render(request,'shine/body/index.html')
#............................................................................................

def contact_view(request):
    form = ContactMessageForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            # On peut ajouter un message de succès ici
            messages.success(request, "Votre message a été envoyé avec succès ! Nous vous répondrons dans les plus brefs délais.",extra_tags='contact_success')
            return redirect('shine:contact')
    
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