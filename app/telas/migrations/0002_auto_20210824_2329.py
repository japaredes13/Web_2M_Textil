# Generated by Django 3.1.7 on 2021-08-25 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tela',
            name='metraje',
            field=models.FloatField(),
        ),
    ]
