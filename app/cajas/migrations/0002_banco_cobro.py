# Generated by Django 3.1.7 on 2021-09-23 03:27

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0003_venta_anulado'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cajas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cobro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('fecha_eliminacion', models.DateField(blank=True, null=True)),
                ('user_updated_id', models.IntegerField(blank=True, null=True)),
                ('monto_cobrado', models.IntegerField(default=0)),
                ('medio_cobro', models.CharField(choices=[('efectivo', 'Efectivo'), ('cheque', 'Cheque')], default='efectivo', max_length=20)),
                ('banco', models.CharField(max_length=200)),
                ('fecha_cobro', models.DateField(default=datetime.datetime.now)),
                ('caja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cajas.caja')),
                ('cuota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.cuotaventa')),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.venta')),
            ],
            options={
                'verbose_name_plural': 'Cobro',
            },
        ),
        migrations.CreateModel(
            name='Banco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('fecha_eliminacion', models.DateField(blank=True, null=True)),
                ('user_updated_id', models.IntegerField(blank=True, null=True)),
                ('descripcion', models.CharField(error_messages={'unique': 'El campo Descripcion ya existe'}, max_length=200, unique=True)),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Banco',
            },
        ),
    ]
