# Generated by Django 4.0 on 2023-06-26 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_alter_samplemetacurated_bmi'),
    ]

    operations = [
        migrations.AddField(
            model_name='samplemetacurated',
            name='QC_Bacteria',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='samplemetacurated',
            name='QC_Bacteria_gg',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='samplemetacurated',
            name='QC_Fungi',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='samplemetacurated',
            name='QC_state',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]