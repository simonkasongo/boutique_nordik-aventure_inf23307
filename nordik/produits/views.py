from django.shortcuts import render, get_object_or_404
from .models import Produit

# Liste des produits (catalogue e-commerce)
def liste_produits(request):
    produits = Produit.objects.all()

    return render(request, 'produits/liste.html', {
        'produits': produits
    })


# Fiche produit détaillée
def detail_produit(request, pk):
    produit = get_object_or_404(Produit, pk=pk)

    # Alerte de stock faible
    stock_faible = produit.quantite_stock <= produit.seuil_reappro

    return render(request, 'produits/detail.html', {
        'produit': produit,
        'stock_faible': stock_faible
    })


# Page temporaire pour tester l'import Excel (optionnelle)
def import_produits_page(request):
    return render(request, 'produits/import_excel.html')

def categories(request):
    return render(request, 'produits/categories.html')

def produits_par_categorie(request, nom_categorie):
    produits = Produit.objects.filter(categorie__nom=nom_categorie)

    return render(request, 'produits/liste.html', {
        'produits': produits,
        'titre_categorie': nom_categorie
    })
