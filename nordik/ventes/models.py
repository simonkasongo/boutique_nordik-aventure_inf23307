from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from produits.models import Produit
from clients.models import Client


# ============================================================
# Paramètres fiscaux (TPS / TVQ)
# ============================================================
class ParametreFiscal(models.Model):
    tps = models.FloatField(default=0.05)      # 5 %
    tvq = models.FloatField(default=0.09975)   # 9.975 %
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f"TPS {self.tps*100:.2f}% / TVQ {self.tvq*100:.2f}%"

    @classmethod
    def get_actif(cls):
        obj = cls.objects.filter(actif=True).first()
        if obj:
            return obj
        # Valeurs par défaut si aucun en BD
        return cls(tps=0.05, tvq=0.09975)


# ============================================================
# Vente (commande principale)
# ============================================================
class Vente(models.Model):
    # États alignés sur l’énoncé TP3 (suivi administrateur)
    STATUT_CHOIX = [
        ("Réception", "Réception"),
        ("Préparation", "Préparation"),
        ("Expédiée", "Expédiée"),
        ("Facturée", "Facturée"),
        ("Payée", "Payée"),
        ("Annulée", "Annulée"),
    ]

    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    date_vente = models.DateTimeField(auto_now_add=True)
    statut_commande = models.CharField(
        max_length=20, choices=STATUT_CHOIX, default="Réception"
    )

    sous_total = models.FloatField(default=0)
    tps = models.FloatField(default=0)
    tvq = models.FloatField(default=0)
    montant_total = models.FloatField(default=0)

    def __str__(self):
        return f"Vente #{self.id} - {self.client}"


# ============================================================
# Lignes de vente
# ============================================================
class LigneVente(models.Model):
    vente = models.ForeignKey(Vente, on_delete=models.CASCADE, related_name="lignes")
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)
    quantite = models.IntegerField(validators=[MinValueValidator(1)])
    prix_unitaire = models.FloatField()
    cout_achat_unitaire = models.FloatField()

    def sous_total(self):
        return self.quantite * self.prix_unitaire

    def __str__(self):
        return f"{self.quantite} x {self.produit.nom_produit} (Vente #{self.vente_id})"


# ============================================================
# Facture
# ============================================================
class Facture(models.Model):
    STATUT_PAIEMENT_CHOIX = [
        ("En attente", "En attente"),
        ("Partielle", "Partielle"),
        ("Payée", "Payée"),
    ]

    vente = models.OneToOneField(Vente, on_delete=models.PROTECT, related_name="facture")
    numero = models.IntegerField(unique=True, blank=True, null=True)

    montant_ht = models.FloatField()
    tps = models.FloatField()
    tvq = models.FloatField()
    montant_ttc = models.FloatField()

    montant_paye = models.FloatField(default=0)
    statut_paiement = models.CharField(
        max_length=20, choices=STATUT_PAIEMENT_CHOIX, default="En attente"
    )

    date_facture = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Facture #{self.numero or self.id} - Vente #{self.vente_id}"

    # Numéro de facture unique & séquentiel
    def save(self, *args, **kwargs):
        if self.numero is None:
            last = Facture.objects.order_by("-numero").first()
            if last and last.numero:
                self.numero = last.numero + 1
            else:
                self.numero = 1
        super().save(*args, **kwargs)

    @property
    def reste_a_payer(self):
        return round(self.montant_ttc - self.montant_paye, 2)

    # Règle : facture non payée ne peut être supprimée
    def delete(self, *args, **kwargs):
        if self.statut_paiement != "Payée":
            raise ValidationError("❌ Une facture non payée ne peut pas être supprimée.")
        super().delete(*args, **kwargs)


# ============================================================
# Paiements
# ============================================================
class Paiement(models.Model):
    MODE_CHOIX = [
        ("Carte", "Carte"),
        ("Virement", "Virement"),
        ("Comptant", "Comptant"),
    ]

    facture = models.ForeignKey(Facture, on_delete=models.PROTECT, related_name="paiements")
    date_paiement = models.DateTimeField(auto_now_add=True)
    mode_paiement = models.CharField(max_length=20, choices=MODE_CHOIX, default="Carte")
    montant = models.FloatField(validators=[MinValueValidator(0.01)])
    note = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Paiement {self.montant}$ - Facture #{self.facture.numero}"

    def clean(self):
        # Paiement ne peut pas excéder le reste à payer
        if self.montant > self.facture.reste_a_payer:
            raise ValidationError("❌ Le paiement ne peut pas excéder le montant dû.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

        # Mise à jour automatique de la facture
        self.facture.montant_paye += self.montant
        if self.facture.montant_paye >= self.facture.montant_ttc:
            self.facture.montant_paye = self.facture.montant_ttc
            self.facture.statut_paiement = "Payée"
        elif 0 < self.facture.montant_paye < self.facture.montant_ttc:
            self.facture.statut_paiement = "Partielle"
        else:
            self.facture.statut_paiement = "En attente"
        self.facture.save()
