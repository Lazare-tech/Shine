from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import DemandeDevis,ContactMessage,SouscriptionLogement,SouscriptionEtablissement,SouscriptionEtude,SouscriptionMobilite,SouscriptionSoutien

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
@receiver(post_save, sender=DemandeDevis)
def envoyer_email_apres_devis(sender, instance, created, **kwargs):
    # On n'agit QUE si c'est une nouvelle création
    if created:
        try:
            # 1. Sécuriser la récupération du titre du service
            nom_service = "Non spécifié"
            if instance.service_souhaite:
                nom_service = getattr(instance.service_souhaite, 'titre', str(instance.service_souhaite))

            subject = "Confirmation de réception - Shine Agency"
            context = AGENCY_CONTEXT.copy()
            context['nom'] = instance.nom # Ajoute le nom pour le mail client
            
            html_message = render_to_string('shine/emails/accuse_devis.html', context)
            plain_message = strip_tags(html_message)
            
            # Email au Client
            send_mail(
                subject,
                plain_message,
                None, # Utilise DEFAULT_FROM_EMAIL des settings
                [instance.email],
                html_message=html_message,
                fail_silently=False # On laisse le try/except attraper l'erreur
            )

            # 2. Email à l'Administrateur
            subject_admin = f"⭐ NOUVEAU DEVIS : {instance.nom}"
            message_admin = (
                f"Bonjour Shine Agency,\n\n"
                f"Une nouvelle demande de devis a été soumise sur le site.\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"👤 INFOS CLIENT\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"● Nom complet : {instance.nom}\n"
                f"● Email : {instance.email}\n"
                f"● Téléphone : {instance.pays} {instance.numero_telephone}\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"💼 DÉTAILS DE LA DEMANDE\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"● Service : {nom_service}\n"
                f"● Message : \n\n{instance.contenu}\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📅 Date : {instance.date_created if hasattr(instance, 'date_created') else 'Maintenant'}\n"
            )

            send_mail(
                subject_admin,
                message_admin,
                None,
                ['yelmaniyel@gmail.com'],
                fail_silently=False,
            )
            print("Emails envoyés avec succès !")

        except Exception as e:
            # Crucial : On print l'erreur mais on ne bloque pas la réponse serveur
            # C'est cela qui évite l' "Erreur technique" sur le site
            print(f"ALERTE : L'enregistrement a réussi mais l'email n'est pas parti. Erreur : {e}")
            
@receiver(post_save, sender=ContactMessage) # Remplace 'Contact' par ton modèle
def envoyer_email_contact(sender, instance, created, **kwargs):
    if created:
        # 1. EMAIL POUR L'UTILISATEUR (HTML)
        subject_user = "Nous avons reçu votre message - Shine Agency"
        context = AGENCY_CONTEXT.copy()
        context.update({
            'nom': instance.nom,
            'service': "Demande de contact direct"
        })
        
        try:
            # Envoi Client
            html_message = render_to_string('shine/emails/accuse_contact.html', context)
            plain_message = strip_tags(html_message)
            send_mail(
                subject_user,
                plain_message,
                None,
                [instance.email],
                html_message=html_message
            )

            # 2. EMAIL POUR L'ADMINISTRATEUR (Stylisé)
            subject_admin = f"📩 NOUVEAU MESSAGE : {instance.nom}"
            
            # On stylise le corps du message pour l'admin
            message_admin = (
                f"Bonjour Shine Agency,\n\n"
                f"Vous avez reçu un nouveau message depuis le formulaire de contact.\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"👤 INFORMATIONS CLIENT\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"● Nom : {instance.nom}\n"
                f"● Email : {instance.email}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"💬 MESSAGE DU CLIENT\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"{instance.contenu}\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📅 Date de réception : {instance.date_envoi if hasattr(instance, 'date_envoi') else 'Maintenant'}\n"
            )

            send_mail(
                subject_admin,
                message_admin,
                None,
                ['yelmaniyel@gmail.com'],
                fail_silently=False,
            )
            print("Emails Contact (Client + Admin) envoyés avec succès !")

        except Exception as e:
            print(f"Erreur d'envoi contact : {e}")
# Fonction utilitaire pour éviter de répéter le code
def envoi_email_general(template_name, subject, context, recipient_email):
    try:
        html_message = render_to_string(template_name, context)
        plain_message = strip_tags(html_message)
        send_mail(subject, plain_message, None, [recipient_email], html_message=html_message)
        print(f"Email envoyé avec succès à {recipient_email}")
    except Exception as e:
        print(f"Erreur d'envoi email : {e}")
##
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

# Importe tous tes modèles de souscription
from .models import (
    SouscriptionSoutien, SouscriptionEtablissement, 
    SouscriptionEtude, SouscriptionMobilite, SouscriptionLogement
)
@receiver(post_save, sender=SouscriptionSoutien)
@receiver(post_save, sender=SouscriptionEtablissement)
@receiver(post_save, sender=SouscriptionEtude)
@receiver(post_save, sender=SouscriptionMobilite)
@receiver(post_save, sender=SouscriptionLogement)
def envoyer_emails_souscription(sender, instance, created, **kwargs):
    if created:
        try:
            user = instance.user
            pack = instance.pack
            service_nom = pack.service.titre
            nom_client = user.get_full_name() or user.username

            # 1. EMAIL POUR L'UTILISATEUR (Template HTML)
            subject_user = "Confirmation de votre souscription - Shine Agency"
            context_user = AGENCY_CONTEXT.copy()
            context_user.update({
                'nom': nom_client,
                'service': f"Pack {pack.titre_pack} ({service_nom})"
            })
            
            html_message = render_to_string('shine/emails/accuse_souscription.html', context_user)
            send_mail(
                subject_user,
                strip_tags(html_message),
                None,
                [user.email],
                html_message=html_message,
                fail_silently=True # Évite de bloquer si l'email client échoue
            )

            # 2. EMAIL POUR L'ADMINISTRATEUR (Même style que Devis/Contact)
            subject_admin = f"🚀 NOUVELLE SOUSCRIPTION : {nom_client}"
            
            message_admin = (
                f"Bonjour Shine Agency,\n\n"
                f"Une nouvelle souscription vient d'être effectuée sur le site.\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"👤 INFOS CLIENT\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"● Nom : {nom_client}\n"
                f"● Email : {user.email}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📦 PACK SOUSCRIT\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"● Service : {service_nom}\n"
                f"● Pack : {pack.titre_pack}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📂 DÉTAILS DU DOSSIER\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            )

            # Ajout dynamique de tous les autres champs du formulaire
            for field in instance._meta.fields:
                if field.name not in ['id', 'user', 'pack', 'date_souscription', 'date_demande']:
                    value = getattr(instance, field.name)
                    message_admin += f"● {field.verbose_name.capitalize()} : {value}\n"

            message_admin += f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            message_admin += f"📅 Date : {getattr(instance, 'date_souscription', 'Maintenant')}\n"

            send_mail(
                subject_admin,
                message_admin,
                None,
                ['yelmaniyel@gmail.com'],
                fail_silently=False,
            )
            print(f"Souscription de {nom_client} traitée avec succès !")

        except Exception as e:
            print(f"Erreur d'envoi souscription : {e}")