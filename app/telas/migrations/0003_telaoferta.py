# Generated by Django 3.1.7 on 2021-11-23 03:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('telas', '0002_auto_20210824_2329'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelaOferta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('fecha_eliminacion', models.DateField(blank=True, null=True)),
                ('user_updated_id', models.IntegerField(blank=True, null=True)),
                ('metraje_oferta', models.FloatField()),
                ('precio_oferta', models.IntegerField()),
                ('descripcion', models.CharField(blank=True, max_length=100, null=True)),
                ('tela', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='telas.tela')),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]