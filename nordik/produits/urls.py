from django.urls import path
from . import views

urlpatterns = [

    # 🟦 Page des catégories
    path('', views.categories, name='categories'),

    # 🟦 Liste complète des produits
    path('liste/', views.liste_produits, name='liste_produits'),

    # 🟦 Produits filtrés par catégorie
    path('categorie/<str:nom_categorie>/', views.produits_par_categorie, name='produits_par_categorie'),

    # 🟦 Fiche d’un produit
    path('<int:pk>/', views.detail_produit, name='detail_produit'),

    # 🟦 Import Excel (optionnel)
    path('import-excel/', views.import_produits_page, name='import_excel'),
]
