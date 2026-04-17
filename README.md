# Nordik Adventures (INF23307)

Site Django pour le cours d'analyse des applications en commerce électronique (UQAR, campus Lévis). Prototype : boutique avec panier, TPS/TVQ sur le sous-total, facture HTML + PDF, et un peu de PGI côté admin (stock, alertes, dashboard).

Livrable TP3. Le guide long (étapes, options) est dans `README.txt`.

## Contenu

- **Produits / stock** : catégories, fiches, mouvements quand une vente est créée.
- **Ventes** : panier en session, commande, facture, paiement simulé selon le flux du TP.
- **Clients** : inscription, connexion (`User` + `ClientProfil` client/admin), avis 1 à 5 après achat.
- **CRM** : liste clients, fiche avec `ActiviteClient`, tableau de bord basique.

Pour un compte admin il faut en général aller dans `/admin/` et mettre le bon rôle sur le profil (ou créer un superuser).

## Lancer

```bash
cd nordik
python -m venv venv
venv\Scripts\activate
pip install -r ..\requirements.txt
python manage.py migrate
python manage.py runserver
```

`http://127.0.0.1:8000/`

## Arborescence utile

- `requirements.txt` à la racine.
- `nordik/` : `manage.py`, apps `clients`, `ventes`, `produits`, `dashboard`, `templates`, `static`.

## Export SQL (remise)

```bash
cd nordik
sqlite3 db.sqlite3 .dump > export_tp3.sql
```

Démos / captures : voir `README.txt`.
