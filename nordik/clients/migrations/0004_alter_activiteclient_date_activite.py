# Generated manually - passage date activite en DateTimeField

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0003_clientprofil"),
    ]

    operations = [
        migrations.AlterField(
            model_name="activiteclient",
            name="date_activite",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
