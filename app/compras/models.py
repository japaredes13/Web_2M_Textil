from datetime import datetime
from django.db import models
from django.forms import model_to_dict
from django.db.models import Sum
from bases.models import ClaseModelo
from proveedores.models import Proveedor
from telas.models import Tela

class OrdenCompra(ClaseModelo):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha_orden = models.DateField(default=datetime.now)
    excentas = models.IntegerField(default=0,null=True, blank=True)
    total_iva_5 = models.IntegerField(default=0,null=True, blank=True)
    total_iva_10 = models.IntegerField(default=0)
    plazo = models.IntegerField(null=True, blank=True)
    monto_total = models.IntegerField(default=0)    

    def __str__(self):
        return self.proveedor.nombre_empresa

    def toJSON(self):
        item = model_to_dict(self)
        item['proveedor'] = self.proveedor.toJSON()
        item['fecha_orden'] = self.fecha_orden.strftime('%d/%m/%Y')
        item['detalle'] = [i.toJSON() for i in self.detalleordencompra_set.all()]
        return item

    class Meta:
        verbose_name = 'Orden Compra'
        verbose_name_plural = 'Orden de Compras'


class DetalleOrdenCompra(ClaseModelo):
    orden_compra = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE)
    tela = models.ForeignKey(Tela, on_delete=models.CASCADE)
    descripcion =  models.CharField(max_length=50)
    precio_unitario = models.IntegerField(default=0)
    metraje = models.FloatField(default=0.00)
    sub_total_excentas = models.IntegerField(default=0,null=True, blank=True)
    sub_total_iva_5 = models.IntegerField(default=0)
    sub_total_iva_10 = models.IntegerField(default=0)
    sub_total = models.IntegerField(default=0)

    def __str__(self):
        return self.tela.nombre

    def toJSON(self):
        item = model_to_dict(self, exclude=['OrdenCompra'])
        item['tela'] = self.tela.toJSON()
        item['metraje'] = self.metraje
        item['precio_unitario'] = format(self.precio_unitario, '.2f')
        item['sub_total'] = format(self.sub_total, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de la Orden de Compra'
        verbose_name_plural = 'Detalle de la Orden de Compras'

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
    inicio_timbrado = models.DateField(default=datetime.now)
    plazo = models.IntegerField(null=True, blank=True)
    numero_cheque = models.IntegerField(default=0,null=True, blank=True)
    fin_timbrado = models.DateField(default=datetime.now)
    excentas = models.IntegerField(default=0,null=True, blank=True)
    total_iva_5 = models.IntegerField(default=0,null=True, blank=True)
    total_iva_10 = models.IntegerField(default=0)
    plazo = models.IntegerField(null=True, blank=True)
    monto_total = models.IntegerField(default=0)    

    def __str__(self):
        return self.proveedor.nombre_empresa

    def toJSON(self):
        item = model_to_dict(self)
        item['proveedor'] = self.proveedor.toJSON()
        item['fecha_compra'] = self.fecha_compra.strftime('%d/%m/%Y')
        #item['inicio_timbrado'] = self.inicio_timbrado.strftime('%d/%m/%Y')
        #item['fin_timbrado'] = self.fin_timbrado.strftime('%d/%m/%Y')
        item['detalle'] = [i.toJSON() for i in self.detallecompra_set.all()]
        item['detalle_credito'] = [i.toJSON() for i in self.cuotacompra_set.all()]
        item['detalle_pago'] = [i.toJSON() for i in self.cuotacompra_set.all()]
        cuota = CuotaCompra.objects.select_related('compra').filter(compra_id=self.id ,estado=False, compra__condicion_compra='credito')
        item['pendiente_pago'] = int(cuota.count())
        item['saldo_actual'] = cuota.aggregate(Sum('monto_cuota'))
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
        item = model_to_dict(self, exclude=['Compra'])
        item['tela'] = self.tela.toJSON()
        item['metraje_comprado'] = self.metraje_comprado
        item['precio_costo'] = format(self.precio_costo, '.2f')
        item['sub_total'] = format(self.sub_total, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle  de Compra'
        verbose_name_plural = 'Detalle de Compras'

class CuotaCompra(ClaseModelo):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    numero_cuota = models.IntegerField(default=0)
    monto_cuota = models.IntegerField(default=0)
    fecha_vencimiento = models.DateField(default=datetime.now)
    fecha_cancelacion = models.DateField(null=True)
    monto_cobrado =  models.IntegerField(default=0)
    def toJSON(self):
        from cajas.models import Pago
        item = model_to_dict(self)
        compra =  model_to_dict(self.compra)
        cantidad= Pago.objects.filter(cuota_id=self.id).count()
        if cantidad > 0 :
            pago=Pago.objects.get(cuota_id=self.id)
            item['banco']=pago.banco_id
            item['medio_pago']=pago.medio_pago
        else:
            item['banco']=''
            item['medio_pago']=''
        
        compra['fecha_compra'] = compra['fecha_compra'].strftime('%d/%m/%Y')
        item['compra'] = compra
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