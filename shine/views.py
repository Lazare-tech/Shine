from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .forms import DemandeDevisForm, ContactMessageForm, NewsLetterForm,ConsultationForm
from .models import PackService, Service, News_letter,Blog,PaysDestination,Bourse,StatutBourse,Service,FAQ
from django.core.paginator import Paginator
from django.http import JsonResponse
import phonenumbers
from django.contrib import messages # Pour les messages de succès

# Create your views here.
def home(request):
    articles = Blog.objects.all().order_by('-date_publication')[:3]
    pays_destinations = PaysDestination.objects.filter(is_active=True).order_by('nom')
   
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Votre réservation a été confirmée !'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Veuillez corriger les erreurs ci-dessous.',
                'errors': form.errors.get_json_data()
            }, status=400)

    # Pour le chargement initial de la page
    context = {
        'articles': articles,
        'pays_destinations': pays_destinations,
        'form': ConsultationForm()
    }
    return render(request, 'shine/body/index.html', context)
#............................................................................................



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
#.....................................................from .models import Service, FAQ # N'oubliez pas l'import

def faq(request):
    # On récupère tous les services pour les boutons de filtrage
    categorie_service = Service.objects.all()
    
    # On récupère toutes les questions pour l'accordéon
    faqs = FAQ.objects.all().select_related('service') 
    
    context = {
        'categorie_service': categorie_service,
        'faqs': faqs
    }
    return render(request, 'shine/body/faq.html', context)
#............................................................................................
def about(request):
    return render(request,'shine/body/about.html')    
#............................................................................................
def demande_devis_view(request):
    if request.method == 'POST':
        data = request.POST.copy()
        code_pays = data.get('pays') 
        numero_local = data.get('numero_telephone')
        form = DemandeDevisForm(data)

        # On fait notre validation personnalisée
        if code_pays and numero_local:
            try:
                import phonenumbers
                parsed_number = phonenumbers.parse(numero_local, code_pays)
                if phonenumbers.is_valid_number_for_region(parsed_number, code_pays):
                    # Succès : on formate
                    data['numero_telephone'] = phonenumbers.format_number(
                        parsed_number, phonenumbers.PhoneNumberFormat.E164
                    )
                    form.data = data 
                else:
                    # ERREUR PERSONNALISÉE EN FRANÇAIS
                    form.add_error('numero_telephone', f"Le numéro n'est pas valide pour le pays choisi ({code_pays}).")
            except Exception:
                form.add_error('numero_telephone', "Veuillez entrer un numéro de téléphone valide.")


        # Réponse AJAX
        if form.is_valid():
            form.save()
            messages.success(request, "Votre message a été envoyé avec succès !")
            return redirect('shine:devis') 


    else:
            # Ici, form.errors contiendra maintenant ton message en français
        form = DemandeDevisForm()
    return render(request, 'shine/body/devis.html', {'form': form})
#............................................................................................
def mentorat(request):
    return render(request,'shine/body/mentorat.html')    

#............................................................................................ 

def about_us(request):
    return render(request,'shine/body/about.html')
#............................................................................................
def blog(request, category_slug=None):
    # 1. On récupère toutes les catégories (Services) pour le menu de filtrage
    categories = Service.objects.all()
    
    # 2. On récupère les articles (Blog) triés par date
    articles = Blog.objects.all().order_by('-date_publication')
    
    selected_category = None

    # 3. Logique de filtrage si un slug est présent dans l'URL
    if category_slug:
        selected_category = get_object_or_404(Service, slug=category_slug)
        articles = articles.filter(services_associes=selected_category)

    context = {
        'articles': articles,
        'categorie_service': categories,
        'selected_category': selected_category,
    }
    
    # Vérifie bien le chemin de ton template
    return render(request, 'shine/blog/blog.html', context)
def detail_blog(request, slug):
    article = get_object_or_404(Blog, slug=slug)
    # On récupère 3 articles récents sauf celui en cours de lecture
    articles_recents = Blog.objects.exclude(id=article.id).order_by('-date_publication')[:3]
    
    context = {
        'article': article,
        'articles_recents': articles_recents
    }
    return render(request, 'shine/blog/detail.html', context)
    return render(request,'shine/body/blog.html')
                                    # SERVICES PAGES
                                    
       #............................................................................................ 
def services(request, slug):
    services=get_object_or_404(Service, slug=slug)
    print("slug",slug)
    services_hero=Service.objects.get(titre=services)
    pack_principal=Service.objects.exclude(id=services.id)
    #autres services sans leprincipal
    autres = Service.objects.exclude(id=services_hero.id)

    print("services",services)
    #REQUÊTE 2 : Tous les autres services sauf le principal
    autres_services = Service.objects.exclude(id=services.id).prefetch_related('packs')
    pack=services.packs.all()
    print("pack",pack)
    context={
        'pack':pack,
        'services_hero':services_hero,
        'autres_services':autres_services,
    }
    return render(request,'shine/services/services.html',context)

# 

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
#............................................................................................
def liste_bourses(request):
    bourses_list = Bourse.objects.filter(is_active=True)
    
    # Pagination : 6 bourses par page
    paginator = Paginator(bourses_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={
        'page_obj': page_obj,
    }

    return render(request, 'shine/bourse/infos_bourse.html', context)
##
def detail_bourse(request, slug):
    bourse = get_object_or_404(Bourse, slug=slug, is_active=True)
    context={
        'bourse': bourse,
    }
    return render(request, 'shine/bourse/detail_bourse.html', context)