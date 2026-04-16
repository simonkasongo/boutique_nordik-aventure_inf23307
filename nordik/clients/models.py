"""
models.py
---------
Définition des modèles liés aux clients :
- Client
- Activité client
- Avis client
- Profil utilisateur (rôle client/admin)
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Client(models.Model):
    """
    Représente un client de Nordik Adventures.
    """

    STATUT_CHOIX = [
        ("Actif", "Actif"),
        ("Inactif", "Inactif"),
        ("Prospect", "Prospect"),
        ("Fidele", "Fidèle"),
    ]

    nom_client = models.CharField(max_length=100)
    prenom_client = models.CharField(max_length=100)
    adresse = models.CharField(max_length=150)
    courriel = models.EmailField(max_length=100, unique=True)
    telephone = models.CharField(max_length=50)
    statut = models.CharField(max_length=10, choices=STATUT_CHOIX, default="Prospect")

    def __str__(self):
        return f"{self.prenom_client} {self.nom_client}"


class ActiviteClient(models.Model):
    """
    Historique des actions effectuées par un client (CRM).
    """

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="activites")
    date_activite = models.DateTimeField(auto_now_add=True)
    type_activite = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.type_activite} - {self.client}"


class AvisClient(models.Model):
    """
    Avis laissé par un client suite à une commande.
    """

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="avis")
    vente = models.ForeignKey(
        "ventes.Vente",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="avis"
    )
    note = models.IntegerField(default=5)  # Note de 1 à 5 étoiles
    commentaire = models.TextField(blank=True)
    date_avis = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avis {self.note}/5 - {self.client}"


class ClientProfil(models.Model):
    """
    Profil associé à un utilisateur Django.
    Permet de distinguer les rôles client / administrateur.
    """

    ROLE_CHOICES = [
        ("client", "Client"),
        ("admin", "Administrateur"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profil")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="client")

    def __str__(self):
        return f"{self.user.username} ({self.role})"


@receiver(post_save, sender=User)
def create_client_profil(sender, instance, created, **kwargs):
    """
    Signal déclenché automatiquement à la création d’un utilisateur Django.
    Crée :
    - un profil utilisateur (ClientProfil)
    - un client associé (Client)
    """

    if created:
        ClientProfil.objects.create(user=instance)

        Client.objects.create(
            nom_client=instance.last_name,
            prenom_client=instance.first_name or instance.username,
            adresse="Adresse non spécifiée",
            courriel=instance.email,
            telephone="000-000-0000",
            statut="Actif",
        )
