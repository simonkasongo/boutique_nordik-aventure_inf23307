"""
views.py
--------
Vues liées à la gestion des clients :
authentification, compte client, avis, historique des commandes.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

from nordik.decorators import admin_required

from .models import Client, ActiviteClient, AvisClient
from .utils import log_activite
from ventes.models import Facture, Vente


# =========================
# CLIENTS (ADMIN / LISTE)
# =========================

@login_required(login_url="login")
@admin_required
def liste_clients(request):
    clients = Client.objects.all().order_by("nom_client", "prenom_client")
    return render(request, "clients/liste_clients.html", {"clients": clients})


@login_required(login_url="login")
@admin_required
def detail_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    activites = ActiviteClient.objects.filter(client=client).order_by("-date_activite")

    if request.method == "POST":
        type_activite = (request.POST.get("type_activite") or "Note").strip()[:50]
        description = (request.POST.get("description") or "").strip()[:255]
        if not description:
            messages.error(request, "Veuillez saisir une description pour l’activité.")
        else:
            ActiviteClient.objects.create(
                client=client,
                type_activite=type_activite or "Note interne",
                description=description,
            )
            log_activite(
                request.user,
                f"A ajouté une entrée CRM pour le client {client} ({type_activite})",
            )
            messages.success(request, "Activité enregistrée dans l’historique CRM.")
            return redirect("detail_client", client_id=client.id)

    return render(
        request,
        "clients/detail_client.html",
        {"client": client, "activites": activites},
    )


# =========================
# AVIS CLIENT
# =========================

def avis_client(request, facture_id):
    """
    Permet au client de laisser un avis après une commande.
    """

    facture = get_object_or_404(Facture, pk=facture_id)
    vente = facture.vente
    client = vente.client

    if request.method == "POST":
        note = int(request.POST.get("note", 0))
        commentaire = request.POST.get("commentaire", "").strip()

        if not 1 <= note <= 5:
            messages.error(request, "Merci de choisir une note entre 1 et 5.")
        else:
            AvisClient.objects.create(
                client=client,
                vente=vente,
                note=note,
                commentaire=commentaire,
            )
            messages.success(request, "Merci pour votre avis !")
            return redirect("detail_facture", facture_id=facture.id)

    return render(request, "clients/avis_client.html", {
        "facture": facture,
        "vente": vente,
        "client": client,
    })


# =========================
# ESPACE CLIENT
# =========================

@login_required
def mon_compte(request):
    client = Client.objects.filter(courriel=request.user.email).first()
    return render(request, "clients/mon_compte.html", {
        "user": request.user,
        "client": client,
    })


@login_required
def mes_commandes(request):
    client = Client.objects.get(courriel=request.user.email)
    commandes = Vente.objects.filter(client=client).order_by("-date_vente")

    return render(request, "clients/mes_commandes.html", {
        "commandes": commandes
    })


# =========================
# AUTHENTIFICATION
# =========================

def register_view(request):
    """
    Création d’un compte utilisateur client.
    """

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur est déjà utilisé.")
            return redirect("register")

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Compte créé avec succès. Vous pouvez vous connecter.")
        return redirect("login")

    return render(request, "clients/register.html")


def login_view(request):
    """
    Connexion utilisateur avec journalisation d’activité.
    """

    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )

        if user is None:
            messages.error(request, "Identifiants incorrects.")
            return redirect("login")

        login(request, user)
        log_activite(user, "S'est connecté")

        if user.profil.role == "admin":
            return redirect("dashboard")

        return redirect("accueil")

    return render(request, "clients/login.html")


def logout_view(request):
    logout(request)
    return redirect("accueil")


# =========================
# MOT DE PASSE CLIENT
# =========================

@login_required
def changer_mot_de_passe_client(request):
    """
    Permet au client de changer son mot de passe.
    Les administrateurs sont redirigés vers Django Admin.
    """

    if request.user.profil.role == "admin":
        messages.error(
            request,
            "Les administrateurs doivent modifier leur mot de passe via l'administration Django."
        )
        return redirect("/admin/password_change/")

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("mot_de_passe_modifie")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "clients/changer_mot_de_passe.html", {"form": form})


@login_required
def mot_de_passe_modifie(request):
    return render(request, "clients/mot_de_passe_modifie.html")
