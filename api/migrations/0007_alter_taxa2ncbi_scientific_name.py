# Generated by Django 4.1 on 2023-08-29 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0006_alter_taxa2ncbi_hgmt_micro_id_alter_taxa2ncbi_taxa"),
    ]

    operations = [
        migrations.AlterField(
            model_name="taxa2ncbi",
            name="scientific_name",
            field=models.CharField(max_length=300),
        ),
    ]
