from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import DemandeDevis,ContactMessage

AGENCY_CONTEXT = {
    'location': 'Burkina-Faso, Bobo-Dioulasso, secteur 5 face à Megamonde',
    'phone_number_bobo': 'Bobo-Dioulasso : +226 70 24 24 24',
    'phone_number_ouaga': 'Ouagadougou : +226 60 79 78 31',
    'phone_number_france': 'France : +33 7 59 86 92 56',
    'facebook_url': 'https://web.facebook.com/SHNAGENCY',
    'tiktok_url': 'https://vm.tiktok.com/ZSHKLbam9tLDw-EzZ7y/',
    'instagram_url': 'https://www.instagram.com/shineagency226?igsh=dGUxbmhvM2xia21x',
}
@receiver(post_save, sender=DemandeDevis)
def envoyer_email_apres_devis(sender, instance, created, **kwargs):
    if created:
        subject = "Confirmation de réception - Shine Agency"
        
        # On regroupe toutes les infos ici
        context = AGENCY_CONTEXT.copy()
        
        try:
            html_message = render_to_string('shine/emails/accuse_devis.html', context)
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject,
                plain_message,
                None,
                [instance.email],
                html_message=html_message
            )
            print("Email professionnel envoyé avec succès !")
        except Exception as e:
            print(f"Erreur d'envoi : {e}")
            
@receiver(post_save, sender=ContactMessage) # Remplace 'Contact' par ton modèle
def envoyer_email_contact(sender, instance, created, **kwargs):
    if created:
        subject = "Nous avons reçu votre message - Shine Agency"
        context = AGENCY_CONTEXT.copy()
        context.update({
            'nom': instance.nom,
            'message_client': instance.contenu # Supposons que ton champ s'appelle 'message'
        })
        
        envoi_email_general('shine/emails/accuse_contact.html', subject, context, instance.email)
        
# Fonction utilitaire pour éviter de répéter le code
def envoi_email_general(template_name, subject, context, recipient_email):
    try:
        html_message = render_to_string(template_name, context)
        plain_message = strip_tags(html_message)
        send_mail(subject, plain_message, None, [recipient_email], html_message=html_message)
        print(f"Email envoyé avec succès à {recipient_email}")
    except Exception as e:
        print(f"Erreur d'envoi email : {e}")