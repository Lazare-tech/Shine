from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
import shine.views
# Gestion de l'erreur 404
###
app_name = "shine"

urlpatterns = [
    path('', shine.views.home, name='homepage'),
] +   static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static and media files during development