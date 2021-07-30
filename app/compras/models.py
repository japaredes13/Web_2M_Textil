from datetime import datetime
from django.db import models

from django.forms import model_to_dict
from bases.models import ClaseModelo
from proveedores.models import Proveedor
from telas.models import Tela

class Compra(ClaseModelo):
    prov = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.cli.names

    def toJSON(self):
        item = model_to_dict(self)
        item['prov'] = self.prov.nombre_empresa
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detcompra_set.all()]
        return item

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'


class DetCompra(ClaseModelo):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    tela = models.ForeignKey(Tela, on_delete=models.CASCADE)
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    metraje = models.FloatField(default=0.00)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

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