# Generated by Django 3.1.7 on 2021-09-16 15:42

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Caja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('fecha_eliminacion', models.DateField(blank=True, null=True)),
                ('user_updated_id', models.IntegerField(blank=True, null=True)),
                ('monto_apertura', models.IntegerField()),
                ('monto_cierre', models.IntegerField(null=True)),
                ('monto_efectivo', models.IntegerField(null=True)),
                ('monto_cheque', models.IntegerField(null=True)),
                ('monto_ingreso', models.IntegerField(null=True)),
                ('monto_egreso', models.IntegerField(null=True)),
                ('fecha_apertura', models.DateField(default=datetime.datetime.now)),
                ('fecha_cierre', models.DateField(null=True)),
                ('descripcion', models.CharField(max_length=200)),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Caja',
            },
        ),
    ]
