from django.urls import path
from . import views

urlpatterns = [

    # categories
    path('', views.categories, name='categories'),

    # liste produits
    path('liste/', views.liste_produits, name='liste_produits'),

    # par categorie (url)
    path('categorie/<str:nom_categorie>/', views.produits_par_categorie, name='produits_par_categorie'),

    # detail fiche
    path('<int:pk>/', views.detail_produit, name='detail_produit'),

    # import excel
    path('import-excel/', views.import_produits_page, name='import_excel'),
]
