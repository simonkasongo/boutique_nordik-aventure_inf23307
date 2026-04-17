from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required


import random

from django.template.loader import render_to_string
from django.templatetags.static import static
from django.http import HttpResponse
from clients.utils import log_activite
from produits.models import Produit, enregistrer_mouvement
from clients.models import Client, AvisClient
from .models import Vente, LigneVente, Facture, ParametreFiscal, Paiement

# PDF
from xhtml2pdf import pisa


# ============================================================
# 1. GESTION DU PANIER EN SESSION
#    (les produits sont stockés dans request.session["panier"])
# ============================================================

def _get_panier(request):
    """
    Récupère le panier depuis la session.
    Panier = dict { "produit_id": quantite }
    """
    return request.session.get("panier", {})


def _save_panier(request, panier):
    """
    Sauvegarde le panier dans la session.
    """
    request.session["panier"] = panier
    request.session.modified = True


# ------------------------------------------------------------
# 1.1 Ajouter un produit au panier
# ------------------------------------------------------------
def ajouter_au_panier(request, produit_id):

    # Vérifier si l'utilisateur est connecté
    if not request.user.is_authenticated:
        messages.error(request, "Vous devez être connecté pour ajouter un produit dans votre panier.")
        return redirect("login")

    # Récupérer le produit (maintenant on peut l'utiliser dans le log)
    produit = get_object_or_404(Produit, pk=produit_id)

    # Log activité client
    log_activite(request.user, f"A ajouté « {produit.nom_produit} » au panier")

    # Gestion du panier
    panier = _get_panier(request)
    panier[str(produit_id)] = panier.get(str(produit_id), 0) + 1
    _save_panier(request, panier)

    messages.success(request, f"{produit.nom_produit} a été ajouté au panier.")
    return redirect("liste_produits")






# ------------------------------------------------------------
# 1.2 Retirer complètement un produit du panier
# ------------------------------------------------------------
def retirer_du_panier(request, produit_id):
    """
    Supprime totalement un produit du panier (peu importe la quantité).
    """
    panier = _get_panier(request)
    produit_id = str(produit_id)

    if produit_id in panier:
        del panier[produit_id]
        _save_panier(request, panier)
        messages.info(request, "Produit retiré du panier.")

    return redirect("voir_panier")


# ------------------------------------------------------------
# 1.3 Vider entièrement le panier
# ------------------------------------------------------------
def vider_panier(request):
    """
    Vide le panier complet.
    """
    _save_panier(request, {})
    messages.info(request, "Panier vidé.")
    return redirect("voir_panier")


# ------------------------------------------------------------
# 1.4 Voir le panier
# ------------------------------------------------------------
def voir_panier(request):
    """
    Affiche le contenu du panier :
      - image, nom, catégorie
      - quantité, total par ligne
      - sous-total, TPS, TVQ, total
    """
    panier = _get_panier(request)

    lignes = []
    sous_total = 0

    for produit_id, quantite in panier.items():
        produit = get_object_or_404(Produit, pk=int(produit_id))
        quantite = int(quantite)

        ligne_total = produit.prix_unitaire * quantite
        sous_total += ligne_total

        lignes.append({
            "produit": produit,
            "quantite": quantite,
            "total": round(ligne_total, 2),
        })

    params = ParametreFiscal.get_actif()
    tps = round(sous_total * params.tps, 2)
    tvq = round(sous_total * params.tvq, 2)
    total = round(sous_total + tps + tvq, 2)

    return render(request, "ventes/panier.html", {
        "lignes": lignes,
        "sous_total": sous_total,
        "tps": tps,
        "tvq": tvq,
        "total": total,
    })


# ------------------------------------------------------------
# 1.5 Incrémenter / décrémenter la quantité d’un produit
# ------------------------------------------------------------
def incrementer_quantite(request, produit_id):
    """
    +1 sur la quantité d’un produit existant dans le panier.
    """
    panier = _get_panier(request)
    produit_id = str(produit_id)

    if produit_id in panier:
        panier[produit_id] += 1
        _save_panier(request, panier)

    return redirect("voir_panier")


def decrementer_quantite(request, produit_id):
    """
    -1 sur la quantité d’un produit.
    Si la quantité devient 0, on retire le produit du panier.
    """
    panier = _get_panier(request)
    produit_id = str(produit_id)

    if produit_id in panier:
        if panier[produit_id] > 1:
            panier[produit_id] -= 1
        else:
            del panier[produit_id]

        _save_panier(request, panier)

    return redirect("voir_panier")


# ============================================================
# 2. CHOIX DU MODE DE PAIEMENT
# ============================================================

@login_required
def choisir_paiement(request):
    """
    Page où le client choisit :
      - Paiement par carte
      - Paiement par virement
    Impossible d'accéder si panier vide.
    """
    if not _get_panier(request):
        messages.error(request, "Votre panier est vide.")
        return redirect("voir_panier")

    return render(request, "ventes/choisir_paiement.html")


# ============================================================
# 3. PAIEMENT PAR CARTE (FAUX FORMULAIRE)
# ============================================================

@login_required
def paiement_carte(request):
    """
    Simule un formulaire de paiement par carte.
    Si les données sont valides → on passe à passer_commande().
    """
    if request.method == "POST":
        numero = request.POST.get("numero")
        exp = request.POST.get("exp")
        cvv = request.POST.get("cvv")

        # Validation ultra simple (pour le TP)
        if len(numero or "") != 16 or not numero.isdigit():
            messages.error(request, "Numéro de carte invalide.")
            return redirect("paiement_carte")

        # On aurait pu stocker "mode de paiement" dans la session,
        # mais pour le TP, on simule que c'est payé par carte.
        return redirect("passer_commande")

    return render(request, "ventes/paiement_carte.html")


# ============================================================
# 4. PAIEMENT PAR VIREMENT
# ============================================================

@login_required
def paiement_virement(request):
    """
    Affiche une référence de virement bancaire.
    Quand le client clique sur "J'ai effectué le virement", on appelle passer_commande().
    """
    reference = f"NORDIK-{random.randint(10000,99999)}"

    if request.method == "POST":
        # Ici aussi on termine la commande (comme pour la carte)
        return redirect("passer_commande")

    return render(request, "ventes/paiement_virement.html", {"reference": reference})


# ============================================================
# 5. PASSER COMMANDE (création Vente + Facture + Paiement)
# ============================================================

@login_required
@transaction.atomic
def passer_commande(request):
    """
    Étapes :
      1) Vérifier panier non vide
      2) Récupérer / créer le Client lié à l'utilisateur connecté
      3) Vérifier que le client est 'Actif'
      4) Vérifier le stock pour chaque produit
      5) Créer Vente
      6) Créer Lignes de vente + mouvements de stock
      7) Créer Facture
      8) Simuler un paiement complet (Paiement)
      9) Vider le panier
     10) Rediriger vers la page d'avis client
    """

    # 1) Vérifier panier
    panier = _get_panier(request)
    if not panier:
        messages.error(request, "Votre panier est vide.")
        return redirect("voir_panier")

    # 2) Trouver ou créer le Client associé à l'utilisateur
    #    On utilise l'email du user comme courriel du client
    try:
        client = Client.objects.get(courriel=request.user.email)
    except Client.DoesNotExist:
        # Si pas encore de Client, on le crée automatiquement
        client = Client.objects.create(
            nom_client=request.user.last_name or "Nom",
            prenom_client=request.user.first_name or request.user.username,
            adresse="Adresse non spécifiée",
            courriel=request.user.email,
            telephone="000-000-0000",
            statut="Actif",
        )

    # 3) Vérifier statut client
    if client.statut != "Actif":
        messages.error(request, "Votre compte client est inactif. Vente non autorisée.")
        return redirect("voir_panier")

    premiere_commande = not Vente.objects.filter(client=client).exists()

    # 4) Vérifier stock et préparer les lignes
    sous_total = 0
    lignes_temp = []

    for pid, quant in panier.items():
        produit = get_object_or_404(Produit, pk=int(pid))
        quant = int(quant)

        if quant > produit.quantite_stock:
            messages.error(request, f"Stock insuffisant pour {produit.nom_produit}.")
            return redirect("voir_panier")

        ligne_total = produit.prix_unitaire * quant
        sous_total += ligne_total

        lignes_temp.append((produit, quant, produit.prix_unitaire, produit.cout_achat))

    # 5) Calcul des taxes
    params = ParametreFiscal.get_actif()
    tps = round(sous_total * params.tps, 2)
    tvq = round(sous_total * params.tvq, 2)
    montant_total = round(sous_total + tps + tvq, 2)

    # 6) Créer la Vente (état initial : réception)
    vente = Vente.objects.create(
        client=client,
        sous_total=sous_total,
        tps=tps,
        tvq=tvq,
        montant_total=montant_total,
        statut_commande="Réception",
    )
    log_activite(request.user, f"A passé une commande #{vente.id} d’un montant de {montant_total}$")

    # 7) Créer les lignes de vente + mise à jour du stock
    for produit, quant, prix_u, cout_u in lignes_temp:
        LigneVente.objects.create(
            vente=vente,
            produit=produit,
            quantite=quant,
            prix_unitaire=prix_u,
            cout_achat_unitaire=cout_u,
        )

        produit.quantite_stock -= quant
        produit.save()

        # Mouvement de stock OUT (sortie)
        enregistrer_mouvement(produit, quant, "OUT", "Vente")

    vente.statut_commande = "Préparation"
    vente.save()

    vente.statut_commande = "Expédiée"
    vente.save()

    # 8) Créer la facture
    facture = Facture.objects.create(
        vente=vente,
        montant_ht=sous_total,
        tps=tps,
        tvq=tvq,
        montant_ttc=montant_total,
        statut_paiement="Payée",   # payé après carte/virement
    )

    vente.statut_commande = "Facturée"
    vente.save()

    # 9) Créer un paiement simulé (total payé)
    Paiement.objects.create(
        facture=facture,
        montant=montant_total,
        mode_paiement="Carte",  # ou "Virement" si tu veux distinguer
        note="Paiement automatique (TP)",
    )

    vente.statut_commande = "Payée"
    vente.save()

    # 10) Vider le panier
    _save_panier(request, {})

    # 11) Rediriger vers la page d'avis client
    messages.success(request, "Merci pour votre commande ! Donnez-nous votre avis.")
    if premiere_commande:
        messages.info(request, "Première commande, merci.")
    return redirect("avis_client", facture_id=facture.id)




# ============================================================
# 6. PAGE FACTURE HTML
# ============================================================

@login_required(login_url="login")
def detail_facture(request, facture_id):
    """
    Affiche la facture en HTML (consultation après la commande).
    """

    facture = get_object_or_404(Facture, pk=facture_id)
    log_activite(request.user, f"A consulté la facture #{facture.numero}")

    return render(request, "ventes/facture_detail.html", {"facture": facture})


# ============================================================
# 7. GÉNÉRATION PDF DE LA FACTURE
# ============================================================

@login_required(login_url="login")
def facture_pdf(request, facture_id):
    """
    Génère un PDF de la facture (téléchargement).
    Utilise xhtml2pdf (pisa).
    """
    facture = get_object_or_404(Facture, pk=facture_id)

    # Chemin absolu pour le logo (obligatoire pour le PDF)
    logo_url = request.build_absolute_uri(static("images/logo_nordik.png"))

    # Génération du HTML à partir du template
    html = render_to_string(
        "ventes/facture_pdf.html",
        {
            "facture": facture,
            "logo_path": logo_url,
        },
    )

    # Création du PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="facture_{facture.numero}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("❌ Erreur lors de la génération du PDF", status=500)

    return response


# ============================================================
# 8. AVIS CLIENT APRÈS ACHAT
# ============================================================

@login_required(login_url="login")
def laisser_avis(request, vente_id):
    """
    Permet au client de donner une note (1 à 5) + commentaire
    après une commande. Ensuite il est redirigé vers le détail
    de la facture associée.
    """
    vente = get_object_or_404(Vente, pk=vente_id)

    if request.method == "POST":
        note = int(request.POST.get("note", 5))
        commentaire = request.POST.get("commentaire", "")

        AvisClient.objects.create(
            client=vente.client,
            vente=vente,
            note=note,
            commentaire=commentaire,
        )
        log_activite(request.user, f"A laissé un avis sur la commande #{vente.id}")

        messages.success(request, "🎉 Merci pour votre avis ! Votre commande est maintenant complétée.")
        return redirect("voir_panier")


    return render(request, "ventes/laisser_avis.html", {"vente": vente})


# ============================================================
# 9. DÉTAIL D’UNE VENTE POUR LE DASHBOARD (ADMIN)
# ============================================================

@login_required(login_url="login")
def detail_vente_dashboard(request, vente_id):
    """
    Vue utilisée depuis le Dashboard pour consulter le détail
    d’une vente spécifique.
    """
    vente = get_object_or_404(Vente, pk=vente_id)
    return render(request, "ventes/detail_vente.html", {"vente": vente})
