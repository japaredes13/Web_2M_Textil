# Generated by Django 2.2.12 on 2021-07-27 03:23

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('telas', '0002_tela_fecha_eliminacion'),
        ('clientes', '0005_merge_20210719_2220'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('fecha_eliminacion', models.DateField(blank=True, null=True)),
                ('user_updated_id', models.IntegerField(blank=True, null=True)),
                ('nro_factura', models.CharField(max_length=20)),
                ('cliente_ruc', models.CharField(blank=True, max_length=20, null=True)),
                ('cliente_razon_social', models.CharField(max_length=100)),
                ('condicion_venta', models.CharField(choices=[('contado', 'Contado'), ('credito', 'Crédito')], default='contado', max_length=20)),
                ('plazo', models.IntegerField(blank=True, null=True)),
                ('fecha_venta', models.DateField(default=datetime.datetime.now)),
                ('monto_total', models.IntegerField(default=0)),
                ('excentas', models.IntegerField(blank=True, default=0, null=True)),
                ('total_iva_5', models.IntegerField(blank=True, default=0, null=True)),
                ('total_iva_10', models.IntegerField(default=0)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientes.Cliente')),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('fecha_eliminacion', models.DateField(blank=True, null=True)),
                ('user_updated_id', models.IntegerField(blank=True, null=True)),
                ('descripcion', models.CharField(max_length=100)),
                ('metraje_vendido', models.FloatField(default=0)),
                ('precio_unitario', models.IntegerField(default=0)),
                ('sub_total_iva_5', models.IntegerField(default=0, null=True)),
                ('sub_total_iva_10', models.IntegerField(default=0)),
                ('sub_total', models.IntegerField(default=0)),
                ('tela', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='telas.Tela')),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.Venta')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
