from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .forms import DemandeDevisForm, ContactMessageForm, NewsLetterForm,ConsultationForm,SoutienForm,MobiliteForm,EtablissementForm,EtudeInternationalForm,LogementForm
from .models import PackService, Service, News_letter,Blog,PaysDestination,Bourse,StatutBourse,Service,FAQ
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
import phonenumbers
from django.contrib import messages # Pour les messages de succès
from django.contrib.auth.decorators import login_required


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

        # Logique de validation du téléphone
        if code_pays and numero_local:
            try:
                parsed_number = phonenumbers.parse(numero_local, code_pays)
                if phonenumbers.is_valid_number(parsed_number):
                    formatted = phonenumbers.format_number(
                        parsed_number, phonenumbers.PhoneNumberFormat.E164
                    )
                    data['numero_telephone'] = formatted
                    form.data = data 
                else:
                    form.add_error('numero_telephone', f"Numéro invalide pour le pays ({code_pays}).")
            except Exception:
                form.add_error('numero_telephone', "Veuillez entrer un numéro valide.")

        # VERIFICATION AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if form.is_valid():
                form.save()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Votre message a été envoyé avec succès !'
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Veuillez corriger les erreurs ci-dessous.',
                    'errors': form.errors.get_json_data() # Envoie les erreurs par champ
                }, status=400)

        # Logique classique (si pas AJAX)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre message a été envoyé avec succès !")
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
@login_required
def demande_devis_view(request):
    form = DemandeDevisForm(request.POST or None)
    
    if request.method == 'POST':
        data = request.POST.copy()
        code_pays = data.get('pays') 
        numero_local = data.get('numero_telephone')

        # Nettoyage du téléphone
        if code_pays and numero_local:
            try:
                import phonenumbers
                parsed_number = phonenumbers.parse(numero_local, code_pays)
                if phonenumbers.is_valid_number_for_region(parsed_number, code_pays):
                    data['numero_telephone'] = phonenumbers.format_number(
                        parsed_number, phonenumbers.PhoneNumberFormat.E164
                    )
                    form.data = data 
                else:
                    form.add_error('numero_telephone', f"Invalide pour {code_pays}.")
            except Exception:
                form.add_error('numero_telephone', "Numéro invalide.")

        # --- LOGIQUE DE VALIDATION ET ENREGISTREMENT ---
        if form.is_valid():
            form.save() # ON SAUVEGARDE UNE SEULE FOIS ICI

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success', 
                    'message': 'Votre demande de devis a été envoyée avec succès !'
                })
            
            # Cas classique sans AJAX
            messages.success(request, "Votre demande a été envoyée !")
            return redirect('shine:devis')

        else:
            # GESTION DES ERREURS DE VALIDATION
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': 'Veuillez corriger les erreurs.',
                    'errors': form.errors.get_json_data()
                }, status=400)

    # Affichage initial ou retour d'erreurs classique
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

def souscrire_pack(request, pack_slug):
    pack = get_object_or_404(PackService, slug=pack_slug)
    service = pack.service
    
    forms_mapping = {
        'soutien-scolaire': (SoutienForm, 'shine/inscription_service/pack_soutien_scolaire.html'),
        'etudes-internationales': (EtudeInternationalForm, 'shine/inscription_service/etude_international.html'),
        'accompagnement-des-etablissements-scolaires': (EtablissementForm, 'shine/inscription_service/pack_accompagnement_etablissement.html'),
        'mobilite': (MobiliteForm, 'shine/inscription_service/mobilite_generale.html'),
        'logement-accueil': (LogementForm, 'shine/inscription_service/logement_accueil.html'),
    }

    form_class = None
    template_name = None # On part de None pour tester si on trouve

    # Recherche du mapping
    for key, (f_class, t_name) in forms_mapping.items():
        if key in service.slug:
            form_class = f_class
            template_name = t_name
            break

    # --- SECURITÉ ANTI-PAGE BLANCHE ---
    if not form_class or not template_name:
        # Si on ne trouve pas, on affiche un message d'erreur clair au lieu de planter
        return HttpResponse(f"Désolé, le formulaire pour le service '{service.slug}' n'est pas encore configuré dans forms_mapping.")

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.pack = pack
            instance.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # Si c'est de l'AJAX, on renvoie du JSON et on S'ARRÊTE LÀ
                return JsonResponse({
                    'status': 'success', 
                    'message': 'Votre demande a été enregistrée !',
                    'redirect_url': '/merci/'
                })
            
            # Si ce n'est PAS de l'AJAX (cas classique), on redirige
           
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error', 
                    'message': 'Erreur de validation.',
                    'errors': form.errors.get_json_data() 
                })
            context = {'pack': pack, 'service': service, 'form': form}
            return render(request, template_name, context)

    # GET : Affichage initial
    context = {
        'pack': pack,
        'service': service,
        'form': form_class(), 
    }
    return render(request, template_name, context)

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

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)