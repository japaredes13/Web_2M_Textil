from django.db import models
from bases.models import ClaseModelo

class Departamento(ClaseModelo):
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Departamento, self).save()

    class Meta:
        verbose_name_plural ="Departamento"

class Ciudad(ClaseModelo):
    descripcion = models.CharField(max_length=200)
    departamento = models.ForeignKey(Departamento, models.PROTECT) 

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Ciudad, self).save()
    