from django.db import models
from bases.models import ClaseModelo

class Disenho(ClaseModelo):
    descripcion = models.CharField(max_length=200,
                                    unique=True,
                                    error_messages={
                                        'unique': 'El campo Descripcion ya existe'
                                    })

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Disenho, self).save()

    class Meta:
        verbose_name_plural ="Disenho"

class Categoria(ClaseModelo):
    descripcion = models.CharField(max_length=200,
                                unique=True,
                                error_messages={
                                    'unique': 'El campo Descripcion ya existe'
                                })

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Categoria, self).save()

    class Meta:
        verbose_name_plural ="Categoria"