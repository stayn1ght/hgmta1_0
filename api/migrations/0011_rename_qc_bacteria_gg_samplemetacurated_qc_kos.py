# Generated by Django 4.2.17 on 2024-12-11 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_taxa2ncbi_assay_type_taxa2ncbi_scientific_short_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='samplemetacurated',
            old_name='QC_Bacteria_gg',
            new_name='QC_KOs',
        ),
    ]