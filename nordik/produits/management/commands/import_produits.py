from django.core.management.base import BaseCommand
from produits.models import Produit, Fournisseur, Category
import openpyxl

class Command(BaseCommand):
    help = "Importe les produits du fichier Excel produits.xlsx"

    def handle(self, *args, **kwargs):
        file_path = "nordik/import/produits.xlsx"

        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active

        rows = sheet.iter_rows(min_row=2, values_only=True)

        for row in rows:
            (
                sku,                         # Col 0
                categorie_excel,             # Col 1
                nom_produit,                 # Col 2
                cout_achat,                  # Col 3
                prix_vente,                  # Col 4
                marge_brute,                 # Col 5 (IGNORE)
                quantite_stock,              # Col 6
                seuil_reappro,               # Col 7
                stock_minimum,               # Col 8 (IGNORE)
                delai_livraison,             # Col 9
                fournisseur_nom,             # Col 10
                code_fournisseur,            # Col 11
                remise_fournisseur,          # Col 12
                poids,                       # Col 13  -> devient poids_kg
                date_entree_stock,           # Col 14 (IGNORE)
                emplacement,                 # Col 15
                statut                       # Col 16
            ) = row

            # 1. Catégorie
            categorie_obj, _ = Category.objects.get_or_create(
                nom=categorie_excel
            )

            # 2. Fournisseur
            fournisseur_obj, _ = Fournisseur.objects.get_or_create(
                nom_fournisseur=fournisseur_nom,
                code_fournisseur=code_fournisseur,
                defaults={
                    "remise_fournisseur": remise_fournisseur or 0,
                    "delai_livraison": delai_livraison or 0
                }
            )

            # 3. Image basée sur le nom du produit
            image_name = f"{nom_produit}.png"

            # 4. Création du produit (NOUVEAU MODÈLE)
            Produit.objects.create(
                sku=sku,
                nom_produit=nom_produit,
                description="",  # vide par défaut, tu ajoutes dans l’admin

                categorie=categorie_obj,
                fournisseur=fournisseur_obj,

                prix_unitaire=prix_vente,
                cout_achat=cout_achat,

                quantite_stock=quantite_stock,
                seuil_reappro=seuil_reappro,

                statut=statut,
                delai_livraison=delai_livraison or 0,

                poids_kg=poids or 0,
                emplacement=emplacement or "",

                image=image_name
            )

            self.stdout.write(self.style.SUCCESS(
                f"✔ Produit importé : {nom_produit}"
            ))

        self.stdout.write(self.style.SUCCESS("🎉 Import terminé avec succès !"))
