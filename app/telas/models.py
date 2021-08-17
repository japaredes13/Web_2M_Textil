from django.db import models
from django.forms import model_to_dict
from bases.models import ClaseModelo

class Tela(ClaseModelo):
    codigo= models.CharField(max_length=200)
    nombre = models.CharField(max_length=200)
    color = models.CharField(max_length=200)
    metraje = models.FloatField(default=0)
    precio_venta  = models.FloatField(default=0)
    precio_compra = models.FloatField(default=0)
    tipos = (('estampado', 'Estampado'),
            ('liso', 'Liso')
    )
    disenho = models.CharField(max_length=20, choices = tipos, default = 'Estampado')
    categorias = (  ('manteleria','Mantelería'),
                    ('pantaloneria','Pantalonería'),
                    ('camiseria','Camisería'),
    )
    categoria = models.CharField(max_length=20, choices = categorias, default = 'Mantelería')


    def toJSON(self):
        item = model_to_dict(self)
        item ['color'] = '<input type="color" value="'+self.color+'" name="color" class="form-control" disabled>' 
        return item