from django.db import models

from bases.models import ClaseModelo
from ubicaciones.models import Ciudad

class Proveedor(ClaseModelo):
    ciudad = models.ForeignKey(Ciudad, models.PROTECT)

    nombre_empresa=models.CharField(
        max_length=100,
        unique=True
    )
    direccion=models.CharField(
        max_length=250,
        null=True, blank=True
    )
    contacto=models.CharField(
        max_length=100, blank=True
    )
    telefono=models.CharField(
        max_length=10,
        null=True, blank=True
    )
    nro_celular=models.CharField(
        max_length=10,
        null=True, blank=True
    )
    email=models.CharField(
        max_length=250,
    )
    ruc=models.CharField(
        max_length=100, blank=True
    )
    email =models.EmailField(
        max_length=254)

    def __str__(self):
        return '{}'.format(self.nombre_empresa)
    
    def save(self):
        self.nombre_empresa=self.nombre_empresa.upper()
        super(Proveedor, self).save()

    class Meta:
        verbose_name_plural = "Proveedores"