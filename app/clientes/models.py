from django.db import models
from django.forms import model_to_dict
from bases.models import ClaseModelo
from ubicaciones.models import Ciudad

class Cliente(ClaseModelo):
    nombre_cliente = models.CharField(max_length=200)
    razon_social = models.CharField(max_length=200,null=True, blank=True)
    cedula = models.CharField(max_length=50, unique=True)
    ruc = models.CharField(max_length=50,null=True, blank=True)
    email = models.EmailField(max_length = 200)
    tipos = (('persona_fisica', 'Persona Física'),
            ('persona_juridica', 'Persona Juridica'))
    tipo_cliente = models.CharField(max_length=20, choices = tipos, default = 'persona_fisica')
    nro_telefono = models.CharField(max_length=20,null=True, blank=True)
    nro_celular = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)
    ciudad = models.ForeignKey(Ciudad, models.PROTECT) 

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return '{}'.format(self.nombre_cliente)

    class Meta:
        # sort by "fecha" in descending order unless
        # overridden in the query with order_by()
        ordering = ['nombre_cliente']
