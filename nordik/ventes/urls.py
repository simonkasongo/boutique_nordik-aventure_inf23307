from django.urls import path
from . import views

urlpatterns = [
    path("panier/", views.voir_panier, name="voir_panier"),
    path("panier/ajouter/<int:produit_id>/", views.ajouter_au_panier, name="ajouter_au_panier"),
    path("panier/retirer/<int:produit_id>/", views.retirer_du_panier, name="retirer_du_panier"),
    path("panier/vider/", views.vider_panier, name="vider_panier"),

    path("commande/paiement/", views.choisir_paiement, name="choisir_paiement"),
    path("paiement/carte/", views.paiement_carte, name="paiement_carte"),
    path("paiement/virement/", views.paiement_virement, name="paiement_virement"),

    path("commande/passer/", views.passer_commande, name="passer_commande"),

    path("panier/increment/<int:produit_id>/", views.incrementer_quantite, name="incrementer_quantite"),
    path("panier/decrement/<int:produit_id>/", views.decrementer_quantite, name="decrementer_quantite"),


    path("facture/<int:facture_id>/", views.detail_facture, name="detail_facture"),
    path("facture/<int:facture_id>/pdf/", views.facture_pdf, name="facture_pdf"),
    path("dashboard/vente/<int:vente_id>/", views.detail_vente_dashboard, name="detail_vente_dashboard"),

]
