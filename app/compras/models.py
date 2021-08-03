from datetime import datetime
from django.db import models
from django.forms import model_to_dict
from bases.models import ClaseModelo
from proveedores.models import Proveedor
from telas.models import Tela

class Compra(ClaseModelo):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    nro_factura = models.CharField(max_length=30)
    timbrado = models.CharField(max_length=30)
    proveedor_ruc = models.CharField(max_length=20)
    proveedor_nombre =  models.CharField(max_length=20)
    condiciones = ( ('contado', 'Contado'),
                    ('credito', 'Crédito'))
    condicion_compra = models.CharField(max_length=20, choices = condiciones, default = 'contado')
    fecha_compra = models.DateField(default=datetime.now)
    excentas = models.IntegerField(default=0,null=True, blank=True)
    total_iva_5 = models.IntegerField(default=0,null=True, blank=True)
    total_iva_10 = models.IntegerField(default=0)
    plazo = models.IntegerField(null=True, blank=True)
    monto_total = models.IntegerField(default=0)    

    def __str__(self):
        return self.cli.names

    def toJSON(self):
        item = model_to_dict(self)
        item['proveedor'] = self.proveedor.nombre_empresa
        #item['detalle'] = [i.toJSON() for i in self.detcompra_set.all()]
        return item

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'


class DetalleCompra(ClaseModelo):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    tela = models.ForeignKey(Tela, on_delete=models.CASCADE)
    descripcion =  models.CharField(max_length=50)
    precio_costo = models.IntegerField(default=0)
    metraje_comprado = models.FloatField(default=0.00)
    sub_total_excentas = models.IntegerField(default=0,null=True, blank=True)
    sub_total_iva_5 = models.IntegerField(default=0)
    sub_total_iva_10 = models.IntegerField(default=0)
    sub_total = models.IntegerField(default=0)

    def __str__(self):
        return self.tela.nombre

    def toJSON(self):
        item = model_to_dict(self, exclude=['compra'])
        item['tela'] = self.tela.toJSON()
        item['precio'] = format(self.precio, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Compra'
        verbose_name_plural = 'Detalle de Compras'