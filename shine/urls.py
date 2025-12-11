from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
import shine.views
# Gestion de l'erreur 404
###
app_name = "shine"

urlpatterns = [
    path('', shine.views.home, name='homepage'),
    contact_path := path('contact/', shine.views.contact, name='contact'),
    faq_path := path('faq/', shine.views.faq, name='faq'),
    about_path := path('about/', shine.views.about, name='about'),
    devis_path := path('devis/', shine.views.devis, name='devis'),
    mentorat_path := path('mentorat/', shine.views.mentorat, name='mentorat'),
    infos_bourses_path := path('infos_bourses/', shine.views.infos_bourses, name='infos_bourses'),
    
    # SERVICES PAGES
    etude_path := path('services/etude/', shine.views.etude, name='etude'),
] +   static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static and media files during development