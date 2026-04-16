"""
urls.py
-------
Fichier de routage principal du projet Nordik Adventures.

Rôle :
- Centraliser toutes les routes principales du site
- Déléguer les sous-routes aux applications métiers
  (produits, clients, ventes, dashboard)
"""

from django.contrib import admin
from django.urls import path, include

# Vue d'accueil principale du site
from .views import accueil

urlpatterns = [

    # ==============================
    # PAGE D’ACCUEIL
    # ==============================
    path('', accueil, name='accueil'),

    # ==============================
    # APPLICATION PRODUITS
    # ==============================
    path('produits/', include('produits.urls')),

    # ==============================
    # APPLICATION CLIENTS
    # (authentification, compte, commandes)
    # ==============================
    path('clients/', include('clients.urls')),

    # ==============================
    # APPLICATION VENTES
    # (panier, facturation, paiement)
    # ==============================
    path('ventes/', include('ventes.urls')),

    # ==============================
    # DASHBOARD ADMINISTRATEUR
    # ==============================
    path('dashboard/', include('dashboard.urls')),

    # ==============================
    # INTERFACE ADMIN DJANGO
    # ==============================
    path('admin/', admin.site.urls),
]
