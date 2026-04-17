README.txt - Projet Nordik Adventures

============================================================
1. PRÉSENTATION GÉNÉRALE DU PROJET
============================================================
Nordik Adventures est un site transactionnel développé avec le framework Django dans le cadre du cours INF23307 – Analyse des applications en commerce électronique à l’Université du Québec à Rimouski (UQAR), campus de Lévis. Le projet implémente un PGI simplifié intégrant la gestion des produits, du stock, des clients, des commandes, de la facturation, un tableau de bord administrateur et un module CRM de suivi des activités clients.

============================================================
2. RESSOURCES À INSTALLER EN PREMIER (PRÉREQUIS)
============================================================
2.1 Python
Version requise : Python 3.10 ou plus récent
Commande de vérification :
python --version

2.2 Visual Studio Code
Téléchargement :
https://code.visualstudio.com/

2.3 Git (optionnel mais recommandé)
Téléchargement :
https://git-scm.com/

============================================================
3. OUVERTURE DU PROJET DANS VISUAL STUDIO CODE
============================================================
3.1 Décompresser l’archive du projet Nordik_Adventures
3.2 Ouvrir Visual Studio Code
3.3 Cliquer sur Fichier → Ouvrir un dossier
3.4 Sélectionner le dossier racine contenant le fichier manage.py

============================================================
4. CRÉATION ET ACTIVATION DE L’ENVIRONNEMENT VIRTUEL
============================================================
4.1 Création de l’environnement virtuel

Sous Windows :
python -m venv venv

Sous macOS / Linux :
python3 -m venv venv

4.2 Activation de l’environnement virtuel

Sous Windows :
venv\Scripts\activate

Sous macOS / Linux :
source venv/bin/activate

Le terminal doit afficher (venv) une fois l’environnement activé.

============================================================
5. INSTALLATION DES DÉPENDANCES DU PROJET
============================================================
5.1 Le fichier requirements.txt est obligatoire et déjà inclus dans le projet
5.2 Installation des dépendances
Commande :
pip install -r requirements.txt

============================================================
6. BASE DE DONNÉES UTILISÉE
============================================================
6.1 Base de données : SQLite
6.2 SQLite est la base de données par défaut de Django
6.3 Aucun export ou import n’est requis
6.4 Le fichier db.sqlite3 est automatiquement reconnu par Django
6.5 Cette configuration facilite la correction du projet sans configuration supplémentaire

============================================================
7. MIGRATIONS DE LA BASE DE DONNÉES
============================================================
7.0 être dans le chemin du projet avant, exemple: (venv) PS P:\Analyse des apps en CE\Travail pratique 3\Nordik_Adventurs> cd nordik (obligatoire) 

7.1 Génération des migrations :
python manage.py makemigrations

7.2 Application des migrations :
python manage.py migrate

============================================================
8. CRÉATION ET ACTIVATION D’UN ADMINISTRATEUR
============================================================
8.1 Création du superutilisateur Django :
python manage.py createsuperuser

8.2 Accéder à l’interface d’administration :
http://127.0.0.1:8000/admin/

8.3 Ouvrir la section ClientProfil
8.4 Modifier le champ role du compte créé de client vers admin
8.5 Enregistrer les modifications

Cette étape est obligatoire pour accéder au tableau de bord administrateur.

============================================================
9. LANCEMENT DU SERVEUR DJANGO (a faire avant 8.2, 8.3, 8.4, 8.5)
============================================================
Commande :
python manage.py runserver

============================================================
10. ACCÈS AU SITE WEB
============================================================
10.1 Site principal :
http://127.0.0.1:8000/

10.2 Interface d’administration Django :
http://127.0.0.1:8000/admin/

10.3 Tableau de bord administrateur :
http://127.0.0.1:8000/dashboard/

============================================================
11. STRUCTURE DES APPLICATIONS DJANGO
============================================================
clients :
admin.py
models.py
urls.py
views.py
utils.py
tests.py

dashboard :
views.py
urls.py
tests.py

produits :
admin.py
models.py
urls.py
views.py
tests.py

ventes :
admin.py
models.py
urls.py
views.py
tests.py

nordik (projet principal) :
settings.py
urls.py
wsgi.py
asgi.py

============================================================
12. STRUCTURE DES TEMPLATES HTML
============================================================
templates/clients :
avis_client.html
changer_mot_de_passe.html
login.html
register.html
mon_compte.html
mes_commandes.html
mot_de_passe_modifie.html

templates/produits :
categories.html
liste.html
detail.html
import_excel.html

templates/ventes :
panier.html
choisir_paiement.html
facture_detail.html

templates/dashboard :
tableau_de_bord.html

templates :
base.html
accueil.html

============================================================
13. VIDÉO DE DÉMONSTRATION
============================================================
Une vidéo complète de démonstration du site Nordik Adventures  sur YouTube en visitant ce  https://youtu.be/eR3rnc4v5ek.
Le lien vers la vidéo se trouve dans le dépôt du projet.
Cette vidéo remplace entièrement les captures d’écran dans le rapport technique.

============================================================
14. FIN DU FICHIER README
============================================================
