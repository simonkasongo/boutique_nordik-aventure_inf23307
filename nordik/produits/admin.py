"""
admin.py
--------
Configuration de l’interface d’administration Django
pour la gestion des produits, catégories, fournisseurs
et mouvements de stock.
"""

from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Produit, Category, Fournisseur, StockMovement


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    """
    Configuration avancée de l'administration des produits :
    - affichage des champs clés
    - filtres rapides
    - recherche par nom et SKU
    """

    list_display = (
        'nom_produit',
        'sku',
        'prix_unitaire',
        'cout_achat',
        'quantite_stock',
        'statut'
    )
    list_filter = ('statut', 'categorie', 'fournisseur')
    search_fields = ('nom_produit', 'sku')

    def delete_model(self, request, obj):
        """
        Surcharge de la suppression :
        empêche la suppression d’un produit
        si des règles métiers ne sont pas respectées.
        """
        try:
            obj.delete()
        except ValidationError as e:
            self.message_user(request, str(e), level='error')


# Enregistrement simple des autres modèles
admin.site.register(Category)
admin.site.register(Fournisseur)
admin.site.register(StockMovement)
