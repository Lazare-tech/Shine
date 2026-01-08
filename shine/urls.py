from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
import shine.views
# Gestion de l'erreur 404
###
app_name = "shine"
handler404 = 'shine.views.custom_404_view'
urlpatterns = [
    path('', shine.views.home, name='homepage'),
    contact_path := path('contact/', shine.views.contact_view, name='contact'),
    faq_path := path('faq/', shine.views.faq, name='faq'),
    about_path := path('about/', shine.views.about, name='about'),
    devis_path := path('devis/', shine.views.demande_devis_view, name='devis'),
    mentorat_path := path('mentorat/', shine.views.mentorat, name='mentorat'),
    
    # SERVICES PAGES
    etude_path := path('services/<slug:slug>/', shine.views.services, name='services'),
    
    #APROPOS US PAGE
    about_us_path := path('about_us/', shine.views.about_us, name='about_us'),

    # NEWSLETTER SUBSCRIPTION ENDPOINT
    path('newsletter/subscribe/', shine.views.newsletter_subscribe, name='newsletter'),
    
    # DETAIL BLOG PAGE
    blog_path := path('blog/', shine.views.blog, name='blog'),

    detail_blog_path := path('blog/<slug:slug>/', shine.views.detail_blog, name='detail_blog'),
    # 2. Filtrage par catégorie (Slug de la catégorie)
    blog_categorie_path := path('blog/categorie/<slug:category_slug>/', shine.views.blog, name='blog_by_category'),
    
    #BOURSE PAGE
    bourse_path := path('bourses/<slug:slug>/', shine.views.detail_bourse, name='bourse'),
    liste_bourses_path := path('bourses/', shine.views.liste_bourses, name='liste_bourses'),
    souscrire_path :=path('souscrire/<slug:pack_slug>/', shine.views.souscrire_pack, name='souscrire_pack'),
] +   static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static and media files during development