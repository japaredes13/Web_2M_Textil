from django.db import models
from bases.models import ClaseModelo
from clientes.models import Cliente
from telas.models import Tela
from datetime import datetime

class Venta(ClaseModelo):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nro_factura = models.CharField(max_length=20)
    cliente_ruc = models.CharField(max_length=20,null=True, blank=True)
    cliente_razon_social = models.CharField(max_length=100)
    condiciones = ( ('contado', 'Contado'),
                    ('credito', 'Crédito'))
    condicion_venta = models.CharField(max_length=20, choices = condiciones, default = 'contado')
    plazo = models.IntegerField(null=True, blank=True)
    fecha_venta = models.DateField(default=datetime.now)
    monto_total = models.IntegerField(default=0)
    excentas = models.IntegerField(default=0,null=True, blank=True)
    total_iva_5 = models.IntegerField(default=0,null=True, blank=True)
    total_iva_10 = models.IntegerField(default=0)


class DetalleVenta(ClaseModelo):
    tela = models.ForeignKey(Tela, on_delete=models.CASCADE)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=100)
    precio_unitario = models.IntegerField()
    sub_total_iva_5 = models.IntegerField(default=0,null=True)
    sub_total_iva_10 = models.IntegerField(default=0)
