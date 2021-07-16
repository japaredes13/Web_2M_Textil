from django.db import models
from bases.models import ClaseModelo
from ubicaciones.models import Ciudad

class Cliente(ClaseModelo):
    nombre= models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    razon_social = models.CharField(max_length=200,null=True, blank=True)
    cedula = models.CharField(max_length=50, unique=True)
    ruc = models.CharField(max_length=50)
    email = models.EmailField(max_length = 200)
    tipos = (('persona_fisica', 'Persona Física'),
            ('persona_juridica', 'Persona Juridica'))
    tipo_cliente = models.CharField(max_length=20, choices = tipos, default = 'persona_fisica')
    nro_telefono = models.CharField(max_length=20)
    nro_celular = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)
    ciudad = models.ForeignKey(Ciudad, models.PROTECT) 

    class Meta:
        # sort by "fecha" in descending order unless
        # overridden in the query with order_by()
        ordering = ['nombre']
