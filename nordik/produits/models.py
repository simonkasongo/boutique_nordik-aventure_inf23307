from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


# ============================================================
# 1. Catégories
# ============================================================
class Category(models.Model):
    nom = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nom


# ============================================================
# 2. Fournisseurs
# ============================================================
class Fournisseur(models.Model):
    nom_fournisseur = models.CharField(max_length=100)
    code_fournisseur = models.CharField(max_length=50)
    remise_fournisseur = models.FloatField(default=0.0)
    delai_livraison = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nom_fournisseur} ({self.code_fournisseur})"


# ============================================================
# 3. Produits
# ============================================================
class Produit(models.Model):

    STATUT_CHOIX = [
        ('Actif', 'Actif'),
        ('Inactif', 'Inactif'),
    ]

    # ----- Champs principaux -----
    sku = models.CharField(max_length=50, unique=True)
    nom_produit = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    categorie = models.ForeignKey(Category, on_delete=models.PROTECT)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.PROTECT)

    # ----- Prix & coûts -----
    prix_unitaire = models.FloatField(validators=[MinValueValidator(0.01)])
    cout_achat = models.FloatField(validators=[MinValueValidator(0.01)])

    # ----- Stock -----
    quantite_stock = models.IntegerField(validators=[MinValueValidator(0)])
    seuil_reappro = models.IntegerField(validators=[MinValueValidator(1)])

    # ----- Autres infos -----
    statut = models.CharField(max_length=20, choices=STATUT_CHOIX, default='Actif')
    delai_livraison = models.IntegerField(default=5)
    poids_kg = models.FloatField(default=0)
    emplacement = models.CharField(max_length=50, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)

    # ------------------------------------------------------------
    # VALIDATION
    # ------------------------------------------------------------
    def clean(self):
        # Prix de vente doit être > coût d'achat
        if self.prix_unitaire <= self.cout_achat:
            raise ValidationError("❌ Le prix de vente doit être supérieur au coût d'achat.")

        # Produit inactif ne peut pas avoir un stock positif
        if self.statut == "Inactif" and self.quantite_stock > 0:
            raise ValidationError("❌ Un produit inactif ne peut pas être en stock.")

    # ------------------------------------------------------------
    # CALCUL MARGE BRUTE
    # ------------------------------------------------------------
    def marge_brute(self):
        return round(((self.prix_unitaire - self.cout_achat) / self.prix_unitaire) * 100, 2)

    # ------------------------------------------------------------
    # PROTECTION CONTRE SUPPRESSION
    # ------------------------------------------------------------
    def delete(self, *args, **kwargs):
        # Si mouvements stock → impossible de supprimer
        if self.stockmovement_set.exists():
            raise ValidationError("❌ Impossible de supprimer un produit lié à un mouvement de stock.")

        # Si ventes associées → impossible de supprimer
        from ventes.models import LigneVente
        if LigneVente.objects.filter(produit=self).exists():
            raise ValidationError("❌ Impossible de supprimer un produit lié à une vente.")

        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.nom_produit} ({self.sku})"


# ============================================================
# 4. Mouvements de stock
# ============================================================
class StockMovement(models.Model):

    TYPE_CHOIX = [
        ("IN", "Entrée"),
        ("OUT", "Sortie")
    ]

    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    type_mouvement = models.CharField(max_length=3, choices=TYPE_CHOIX)
    quantite = models.IntegerField()
    date_mouvement = models.DateTimeField(auto_now_add=True)
    motif = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.type_mouvement} - {self.produit.nom_produit} ({self.quantite})"


# ============================================================
# 5. Fonction utilitaire : enregistrer mouvement
# ============================================================
def enregistrer_mouvement(produit, quantite, type_mouvement, motif):
    StockMovement.objects.create(
        produit=produit,
        quantite=quantite,
        type_mouvement=type_mouvement,
        motif=motif
    )
