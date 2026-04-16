"""
admin.py
---------
Configuration de l’interface d’administration Django pour l’application clients.
Permet aux administrateurs de gérer les clients, leurs activités et leurs avis.
"""

from django.contrib import admin
from .models import Client, ActiviteClient, AvisClient, ClientProfil


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    Configuration de l’affichage des clients dans l’admin Django.
    """
    list_display = ("nom_client", "prenom_client", "courriel", "telephone", "statut")
    search_fields = ("nom_client", "prenom_client", "courriel")


@admin.register(ActiviteClient)
class ActiviteClientAdmin(admin.ModelAdmin):
    """
    Administration des activités clients (CRM).
    """
    list_display = ("client", "type_activite", "date_activite")
    list_filter = ("type_activite",)


# Enregistrement simple sans configuration avancée
admin.site.register(AvisClient)
admin.site.register(ClientProfil)
