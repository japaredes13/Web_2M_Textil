from django.db import models
from django.db.models import Sum
from bases.models import ClaseModelo
from clientes.models import Cliente
from telas.models import Tela

from datetime import datetime
from django.forms.models import model_to_dict

class Venta(ClaseModelo):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nro_factura = models.CharField(max_length=20)
    cliente_ruc = models.CharField(max_length=20,null=True, blank=True)
    cliente_razon_social = models.CharField(max_length=100)
    condiciones = ( ('contado', 'Contado'),
                    ('credito', 'Crédito'))
    condicion_venta = models.CharField(max_length=20, choices = condiciones, default = 'contado')
    anulado = models.BooleanField(default=False)
    plazo = models.IntegerField(null=True, blank=True)
    numero_cheque = models.IntegerField(default=0,null=True, blank=True)
    fecha_venta = models.DateField(default=datetime.now)
    monto_total = models.IntegerField(default=0)
    excentas = models.IntegerField(default=0,null=True, blank=True)
    total_iva_5 = models.IntegerField(default=0,null=True, blank=True)
    total_iva_10 = models.IntegerField(default=0)

    def toJSON(self):
        item = model_to_dict(self)
        item['fecha_venta'] = self.fecha_venta.strftime('%d/%m/%Y')
        #item['fecha_anular'] = self.fecha_venta + datetime.now.replace(day=2).strftime("%d/%m/%Y")
        #print(self.fecha_venta + datetime.now.replace(day=2))
        item['detalle'] = [i.toJSON() for i in self.detalleventa_set.all()]
        item['venta_anulada'] = '<span class="badge badge-danger">SI</span>' if (self.anulado) else '<span class="badge badge-success">NO</span>'
        item['detalle_credito'] = [i.toJSON() for i in self.cuotaventa_set.all()]
        #item['detalle_credito']['monto_total']='200000'
        item['detalle_cobro'] = [i.toJSON() for i in self.cuotaventa_set.all()]
        cuota = CuotaVenta.objects.select_related('venta').filter(venta_id=self.id ,estado=False, venta__condicion_venta='credito')
        item['pendiente_cobro'] = int(cuota.count())
        #print(int(cuota.count()))
        item['saldo_actual'] = cuota.aggregate(Sum('monto_cuota'))
        #print(cuota.aggregate(Sum('monto_cuota')))
        return item


class DetalleVenta(ClaseModelo):
    tela = models.ForeignKey(Tela, on_delete=models.CASCADE)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=100)
    metraje_vendido = models.FloatField(default=0)
    precio_unitario = models.IntegerField(default=0)
    sub_total_iva_5 = models.IntegerField(default=0,null=True)
    sub_total_iva_10 = models.IntegerField(default=0)
    sub_total = models.IntegerField(default=0)

    def toJSON(self):
        item = model_to_dict(self, exclude=['Venta'])
        item['descripcion'] = self.descripcion
        item['metraje_vendido'] = self.metraje_vendido
        item['precio_unitario'] = format(self.precio_unitario, '.2f')
        item['sub_total'] = format(self.sub_total, '.2f')
        return item

class CuotaVenta(ClaseModelo):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    numero_cuota = models.IntegerField(default=0)
    monto_cuota = models.IntegerField(default=0)
    fecha_vencimiento = models.DateField(default=datetime.now)
    fecha_cancelacion = models.DateField(null=True)
    monto_cobrado =  models.IntegerField(default=0)
    def toJSON(self):
        from cajas.models import Cobro
        item = model_to_dict(self)
        venta =  model_to_dict(self.venta)
        cantidad= Cobro.objects.filter(cuota_id=self.id).count()
        if cantidad > 0 :
            cobro=Cobro.objects.get(cuota_id=self.id)
            item['banco']=cobro.banco_id
            item['medio_cobro']=cobro.medio_cobro
        else:
            item['banco']=''
            item['medio_cobro']=''
        
        venta['fecha_venta'] = venta['fecha_venta'].strftime('%d/%m/%Y')
        item['venta'] = venta
        item['numero_cuota'] = self.numero_cuota
        item['monto_cuota'] = self.monto_cuota
        item['fecha_vencimiento'] = self.fecha_vencimiento.strftime('%d/%m/%Y')
        item['fecha_cancelacion'] = self.fecha_cancelacion.strftime('%d/%m/%Y') if (self.fecha_cancelacion) else ''
        if self.estado:
            estado = 'Pagado'
        else:
            estado = 'Pendiente'
        item['estado'] = estado
        return item