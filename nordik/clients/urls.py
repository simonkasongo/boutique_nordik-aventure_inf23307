"""
urls.py
-------
Routes liées à la gestion des clients :
authentification, compte, avis, commandes.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Clients
    path("", views.liste_clients, name="liste_clients"),
    path("<int:client_id>/", views.detail_client, name="detail_client"),

    # Avis client
    path("avis/<int:facture_id>/", views.avis_client, name="avis_client"),

    # Authentification
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Espace client
    path("mon-compte/", views.mon_compte, name="mon_compte"),
    path("mes-commandes/", views.mes_commandes, name="mes_commandes"),

    # Mot de passe (client uniquement)
    path("changer-mot-de-passe/", views.changer_mot_de_passe_client, name="changer_mot_de_passe"),
    path("mot-de-passe-modifie/", views.mot_de_passe_modifie, name="mot_de_passe_modifie"),
]
