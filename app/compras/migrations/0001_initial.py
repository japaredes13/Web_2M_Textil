# Generated by Django 3.1.7 on 2021-08-19 05:29

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('proveedores', '0008_auto_20210817_1742'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('telas', '0004_auto_20210818_2213'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('fecha_eliminacion', models.DateField(blank=True, null=True)),
                ('user_updated_id', models.IntegerField(blank=True, null=True)),
                ('nro_factura', models.CharField(max_length=30)),
                ('timbrado', models.CharField(max_length=30)),
                ('proveedor_ruc', models.CharField(max_length=20)),
                ('proveedor_nombre', models.CharField(max_length=20)),
                ('condicion_compra', models.CharField(choices=[('contado', 'Contado'), ('credito', 'Crédito')], default='contado', max_length=20)),
                ('fecha_compra', models.DateField(default=datetime.datetime.now)),
                ('inicio_timbrado', models.DateField(default=datetime.datetime.now)),
                ('fin_timbrado', models.DateField(default=datetime.datetime.now)),
                ('excentas', models.IntegerField(blank=True, default=0, null=True)),
                ('total_iva_5', models.IntegerField(blank=True, default=0, null=True)),
                ('total_iva_10', models.IntegerField(default=0)),
                ('plazo', models.IntegerField(blank=True, null=True)),
                ('monto_total', models.IntegerField(default=0)),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proveedores.proveedor')),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Compra',
                'verbose_name_plural': 'Compras',
            },
        ),
        migrations.CreateModel(
            name='OrdenCompra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('fecha_eliminacion', models.DateField(blank=True, null=True)),
                ('user_updated_id', models.IntegerField(blank=True, null=True)),
                ('fecha_orden', models.DateField(default=datetime.datetime.now)),
                ('excentas', models.IntegerField(blank=True, default=0, null=True)),
                ('total_iva_5', models.IntegerField(blank=True, default=0, null=True)),
                ('total_iva_10', models.IntegerField(default=0)),
                ('plazo', models.IntegerField(blank=True, null=True)),
                ('monto_total', models.IntegerField(default=0)),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proveedores.proveedor')),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Orden Compra',
                'verbose_name_plural': 'Orden de Compras',
            },
        ),
        migrations.CreateModel(
            name='DetalleOrdenCompra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('fecha_eliminacion', models.DateField(blank=True, null=True)),
                ('user_updated_id', models.IntegerField(blank=True, null=True)),
                ('descripcion', models.CharField(max_length=50)),
                ('precio_unitario', models.IntegerField(default=0)),
                ('metraje', models.FloatField(default=0.0)),
                ('sub_total_excentas', models.IntegerField(blank=True, default=0, null=True)),
                ('sub_total_iva_5', models.IntegerField(default=0)),
                ('sub_total_iva_10', models.IntegerField(default=0)),
                ('sub_total', models.IntegerField(default=0)),
                ('orden_compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compras.ordencompra')),
                ('tela', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='telas.tela')),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Detalle de la Orden de Compra',
                'verbose_name_plural': 'Detalle de la Orden de Compras',
            },
        ),
        migrations.CreateModel(
            name='DetalleCompra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('fecha_eliminacion', models.DateField(blank=True, null=True)),
                ('user_updated_id', models.IntegerField(blank=True, null=True)),
                ('descripcion', models.CharField(max_length=50)),
                ('precio_costo', models.IntegerField(default=0)),
                ('metraje_comprado', models.FloatField(default=0.0)),
                ('sub_total_excentas', models.IntegerField(blank=True, default=0, null=True)),
                ('sub_total_iva_5', models.IntegerField(default=0)),
                ('sub_total_iva_10', models.IntegerField(default=0)),
                ('sub_total', models.IntegerField(default=0)),
                ('compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compras.compra')),
                ('tela', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='telas.tela')),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Detalle  de Compra',
                'verbose_name_plural': 'Detalle de Compras',
            },
        ),
    ]
