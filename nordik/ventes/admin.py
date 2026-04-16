from django.contrib import admin
from .models import Vente, LigneVente, Facture, Paiement, ParametreFiscal

@admin.register(Vente)
class VenteAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "date_vente", "statut_commande", "montant_total")
    list_filter = ("statut_commande", "date_vente")
    search_fields = ("id", "client__nom_client", "client__prenom_client")

@admin.register(LigneVente)
class LigneVenteAdmin(admin.ModelAdmin):
    list_display = ("vente", "produit", "quantite", "prix_unitaire")

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ("numero", "vente", "montant_ttc", "statut_paiement", "date_facture")
    list_filter = ("statut_paiement", "date_facture")

@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ("facture", "montant", "mode_paiement", "date_paiement")



admin.site.register(ParametreFiscal)