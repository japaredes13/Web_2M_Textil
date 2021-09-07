from django.db import models
from bases.models import ClaseModelo

class ConfiguracionUsuario(ClaseModelo):
    metraje_minimo = models.FloatField(unique=True,
                                        error_messages={
                                            'unique': 'Metraje minimo ya existente'
                                        })

    class Meta:
        verbose_name_plural ="Configuracion Usuario"
