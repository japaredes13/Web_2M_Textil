# Generated by Django 3.1.7 on 2021-07-16 02:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ubicaciones', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('user_updated_id', models.IntegerField(blank=True, null=True)),
                ('nombre_empresa', models.CharField(max_length=100, unique=True)),
                ('direccion', models.CharField(blank=True, max_length=250, null=True)),
                ('contacto', models.CharField(blank=True, max_length=100)),
                ('telefono', models.CharField(blank=True, max_length=10, null=True)),
                ('nro_celular', models.CharField(blank=True, max_length=10, null=True)),
                ('ruc', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ubicaciones.ciudad')),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Proveedores',
            },
        ),
    ]