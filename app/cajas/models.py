from django.db import models
from bases.models import ClaseModelo
from datetime import datetime
from django.forms.models import model_to_dict

class Caja(ClaseModelo):
    monto_apertura = models.IntegerField()
    monto_cierre = models.IntegerField(null=True)
    monto_efectivo = models.IntegerField(null=True)
    monto_cheque = models.IntegerField(null=True)
    monto_ingreso = models.IntegerField(null=True)
    monto_egreso = models.IntegerField(null=True)
    fecha_apertura = models.DateField(default=datetime.now)
    fecha_cierre = models.DateField(null=True)
    descripcion = models.CharField(max_length=200)

    def toJSON(self):
        item = model_to_dict(self)
        item['fecha_apertura'] = self.fecha_apertura.strftime('%d/%m/%Y')
        return item

    class Meta:
        verbose_name_plural ="Caja"