# Generated by Django 3.1.7 on 2021-08-11 03:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0005_merge_20210719_2220'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cliente',
            options={'ordering': ['razon_social']},
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='cedula',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='nombre_cliente',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='nro_celular',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='tipo_cliente',
        ),
    ]