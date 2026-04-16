from django.urls import path
from . import views

urlpatterns = [
    path('', views.tableau_de_bord, name='dashboard'),
]
