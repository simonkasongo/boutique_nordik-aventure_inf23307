"""
Redirige les vues si l'utilisateur n'est pas admin (voir ClientProfil).
"""

from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        profil = getattr(request.user, "profil", None)
        if profil is None or profil.role != "admin":
            messages.error(request, "Réservé aux administrateurs.")
            return redirect("accueil")
        return view_func(request, *args, **kwargs)

    return wrapper
