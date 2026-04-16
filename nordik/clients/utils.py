"""
utils.py
--------
Fonctions utilitaires liées aux clients.
Contient la logique de journalisation des activités clients.
"""

from .models import ActiviteClient, Client


def log_activite(user, description):
    """
    Enregistre une activité client horodatée.

    :param user: utilisateur Django connecté
    :param description: description de l'action effectuée
    """

    if not user.is_authenticated:
        return

    try:
        client = Client.objects.get(courriel=user.email)
        ActiviteClient.objects.create(
            client=client,
            type_activite="Action",
            description=description
        )
    except Client.DoesNotExist:
        pass
