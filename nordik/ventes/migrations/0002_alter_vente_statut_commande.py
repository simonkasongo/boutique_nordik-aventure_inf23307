# Generated manually — alignement statuts commande (énoncé TP3)

from django.db import migrations, models


def migrer_statuts_anciens(apps, schema_editor):
    Vente = apps.get_model("ventes", "Vente")
    correspondance = {
        "Brouillon": "Réception",
        "Facturée": "Facturée",
        "Payée": "Payée",
        "Annulée": "Annulée",
    }
    for ancien, nouveau in correspondance.items():
        Vente.objects.filter(statut_commande=ancien).update(statut_commande=nouveau)


class Migration(migrations.Migration):

    dependencies = [
        ("ventes", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(migrer_statuts_anciens, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="vente",
            name="statut_commande",
            field=models.CharField(
                choices=[
                    ("Réception", "Réception"),
                    ("Préparation", "Préparation"),
                    ("Expédiée", "Expédiée"),
                    ("Facturée", "Facturée"),
                    ("Payée", "Payée"),
                    ("Annulée", "Annulée"),
                ],
                default="Réception",
                max_length=20,
            ),
        ),
    ]
