# Boutique Nordik Adventures (INF23307)

Prototype Django : site transactionnel et mini-PGI (produits, stock, ventes, facturation, tableau de bord, CRM).

**Cours :** Analyse des applications en commerce électronique (INF23307), UQAR.

## Démarrage rapide

```bash
cd nordik
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r ..\requirements.txt
python manage.py migrate
python manage.py runserver
```

Ouvrir http://127.0.0.1:8000/ — créer un compte ou utiliser l’admin Django (`/admin/`) pour les données de démo.

## Remise (export SQL)

Depuis le dossier `nordik` :

```bash
sqlite3 db.sqlite3 .dump > export_tp3.sql
```

Le détail du projet et des modules est dans [README.txt](README.txt).
