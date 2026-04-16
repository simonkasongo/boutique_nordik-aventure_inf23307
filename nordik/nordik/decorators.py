"""
Décorateurs de contrôle d’accès (rôles).
"""

from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def admin_required(view_func):
    """Accès réservé aux utilisateurs dont le profil a le rôle « admin »."""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        profil = getattr(request.user, "profil", None)
        if profil is None or profil.role != "admin":
            messages.error(request, "Accès réservé aux administrateurs.")
            return redirect("accueil")
        return view_func(request, *args, **kwargs)

    return wrapper
