from django.db import models
from bases.models import ClaseModelo
from datetime import datetime
from telas.models import Tela
from django.forms.models import model_to_dict

class Inventario(ClaseModelo):
    fecha_inventario = models.DateField(default=datetime.now)

    def toJSON(self):
        item = model_to_dict(self)
        item['fecha_inventario'] = self.fecha_inventario.strftime('%d/%m/%Y')
        item['detalle'] = [i.toJSON() for i in self.detalleinventario_set.all()]
        #print(item['detalle'])
        return item

        
class DetalleInventario(ClaseModelo):
    tela = models.ForeignKey(Tela, on_delete=models.CASCADE)
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    metraje_deposito = models.FloatField()
    metraje_ajustado = models.FloatField(null=True,blank=True)

    def toJSON(self):
        item = model_to_dict(self, exclude=['Inventario'])
        return item