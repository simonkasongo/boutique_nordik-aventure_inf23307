"""
views.py
---------
Vues liées au tableau de bord administrateur.
Ce module centralise les statistiques et indicateurs du PGI Nordik Adventures.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import models
from django.db.models import F, Q

from nordik.decorators import admin_required

# Import des modèles métier
from produits.models import Produit
from clients.models import Client, ActiviteClient, AvisClient
from ventes.models import Vente, Facture


@login_required(login_url="login")
@admin_required
def tableau_de_bord(request):
    """
    Vue principale du dashboard administrateur.

    Rôle :
    - Fournir une vue d’ensemble du système PGI
    - Afficher les indicateurs clés :
        • clients
        • produits
        • ventes
        • revenus
        • alertes stock
        • activités clients
        • avis récents
    """

    # ==============================
    # STATISTIQUES GLOBALES
    # ==============================

    # Nombre total de clients
    total_clients = Client.objects.count()

    # Nombre total de produits
    total_produits = Produit.objects.count()

    # Nombre total de ventes enregistrées
    total_ventes = Vente.objects.count()

    # ==============================
    # REVENUS ET FACTURATION
    # ==============================

    # Calcul du total des revenus (factures payées uniquement)
    revenus_totaux = (
        Facture.objects
        .filter(statut_paiement="Payée")
        .aggregate(models.Sum("montant_ttc"))["montant_ttc__sum"]
        or 0
    )

    # Nombre de factures en attente de paiement
    ventes_en_attente = Facture.objects.filter(
        statut_paiement="En attente"
    ).count()

    # ==============================
    # ALERTES DE STOCK
    # ==============================

    # Produits dont le stock est inférieur ou égal au seuil de réapprovisionnement
    # OU produits sans seuil défini mais stock très faible (<= 5)
    produits_stock_faible = Produit.objects.filter(
        Q(quantite_stock__lte=F("seuil_reappro")) |
        Q(seuil_reappro__isnull=True, quantite_stock__lte=5)
    )

    # ==============================
    # DONNÉES RÉCENTES (CRM)
    # ==============================

    # Dernières ventes (les 5 plus récentes)
    ventes_recent = (
        Vente.objects
        .select_related("client")
        .order_by("-date_vente")[:5]
    )

    # Activités clients récentes (CRM)
    activites_recent = (
        ActiviteClient.objects
        .select_related("client")
        .order_by("-date_activite")[:5]
    )

    # Avis clients récents
    avis_recents = (
        AvisClient.objects
        .select_related("client")
        .order_by("-date_avis")[:5]
    )

    # ==============================
    # CONTEXTE ENVOYÉ AU TEMPLATE
    # ==============================

    context = {
        "total_clients": total_clients,
        "total_produits": total_produits,
        "total_ventes": total_ventes,
        "revenus_totaux": revenus_totaux,
        "ventes_en_attente": ventes_en_attente,
        "produits_stock_faible": produits_stock_faible,
        "ventes_recent": ventes_recent,
        "activites_recent": activites_recent,
        "avis_recents": avis_recents,
    }

    return render(request, "dashboard/tableau_de_bord.html", context)
