from django.db import models
from django.forms import model_to_dict
from bases.models import ClaseModelo
from tipos.models import *

class Tela(ClaseModelo):
    codigo= models.CharField(max_length=200,
                            unique=True,
                            error_messages={
                                'unique': 'El campo Codigo ya existe'
                            })
    nombre = models.CharField(max_length=200)
    color = models.CharField(max_length=200)
    metraje = models.FloatField()
    precio_venta  = models.IntegerField()
    precio_compra = models.IntegerField()
    precio_compra_anterior = models.IntegerField()
    disenho = models.ForeignKey(Disenho, models.PROTECT)
    categoria = models.ForeignKey(Categoria, models.PROTECT)
    
    def toJSON(self):
        item = model_to_dict(self)
        item ['color'] = '<input type="color" value="'+self.color+'" name="color" class="form-control" disabled>' 
        return item