# Generated by Django 3.1.7 on 2021-12-08 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0002_detalleinventario_descripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalleinventario',
            name='es_oferta',
            field=models.BooleanField(default=False),
        ),
    ]
