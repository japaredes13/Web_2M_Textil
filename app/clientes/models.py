from django.db import models
from django.forms import model_to_dict
from bases.models import ClaseModelo
from ubicaciones.models import Ciudad

class Cliente(ClaseModelo):
    razon_social = models.CharField(max_length=200,null=True, blank=True)
    ruc = models.CharField(max_length=50,null=True, blank=True,
                            unique=True,
                            error_messages={
                                'unique': 'El campo Cedula/Ruc ya existe'
                            })
    email = models.EmailField(max_length = 200,null=True, blank=True)
    nro_telefono = models.CharField(max_length=20,null=True, blank=True)
    direccion = models.CharField(max_length=200,null=True, blank=True)
    ciudad = models.ForeignKey(Ciudad, models.PROTECT) 

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return '{}'.format(self.razon_social)

    class Meta:
        # sort by "fecha" in descending order unless
        # overridden in the query with order_by()
        ordering = ['razon_social']
