# Generated by Django 4.0 on 2023-05-04 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_rename_case_daresults_case_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daresults',
            name='taxa',
            field=models.CharField(max_length=500),
        ),
    ]