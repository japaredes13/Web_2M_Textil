# Generated by Django 2.2.12 on 2021-07-16 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tela',
            name='fecha_eliminacion',
            field=models.DateField(blank=True, null=True),
        ),
    ]