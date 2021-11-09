from django.db import models
from bases.models import ClaseModelo
from datetime import datetime
from configuracion.models import ConfiguracionEgreso
from ventas.models import Venta, CuotaVenta
from compras.models import Compra, CuotaCompra
from django.forms.models import model_to_dict

class Caja(ClaseModelo):
    monto_apertura = models.IntegerField()
    monto_cierre = models.IntegerField(default=0,null=True)
    monto_efectivo = models.IntegerField(default=0,null=True)
    monto_cheque = models.IntegerField(default=0,null=True)
    monto_ingreso = models.IntegerField(default=0,null=True)
    monto_egreso = models.IntegerField(default=0,null=True)
    monto_actual = models.IntegerField(null=True)
    fecha_apertura = models.DateField(default=datetime.now)
    fecha_cierre = models.DateField(null=True)
    descripcion = models.CharField(max_length=200)

    def toJSON(self):
        item = model_to_dict(self)
        caja=Caja.objects.get(id=self.id)
        item['fecha_apertura'] = self.fecha_apertura.strftime('%d/%m/%Y')
        item['fecha_cierre'] = self.fecha_cierre.strftime('%d/%m/%Y') if (self.fecha_cierre) else ''
        item['caja_cerrada'] = '<span class="badge badge-success">NO</span>' if (self.estado) else '<span class="badge badge-danger">SI</span>'
        item['detalle_caja']= [{
            'monto_apertura' : self.monto_apertura,
            'monto_ingreso' : self.monto_ingreso,
            'monto_egreso' : self.monto_egreso,
            'monto_efectivo' : self.monto_efectivo,
            'monto_cheque' : self.monto_cheque,
            'monto_actual' : self.monto_actual,
        }]
        print(self.estado)
        return item

    class Meta:
        verbose_name_plural ="Caja"

class Banco(ClaseModelo):
    descripcion = models.CharField(max_length=200,
                                unique=True,
                                error_messages={
                                    'unique': 'El campo Descripcion ya existe'
                                })

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Banco, self).save()

    class Meta:
        verbose_name_plural ="Banco"

class Cobro(ClaseModelo):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    cuota = models.ForeignKey(CuotaVenta,on_delete=models.CASCADE, null=True)
    caja = models.ForeignKey(Caja,on_delete=models.CASCADE)
    monto_cobrado = models.IntegerField(default=0)
    tipos_cobro = ( ('efectivo', 'Efectivo'),
                    ('cheque', 'Cheque'))
    medio_cobro = models.CharField(max_length=20, choices = tipos_cobro, default = 'efectivo')
    banco = models.ForeignKey(Banco, models.PROTECT, null=True)
    numero_cheque = models.IntegerField(default=0,null=True)
    fecha_cobro = models.DateField(default=datetime.now)

    def toJSON(self):
        item = model_to_dict(self)
        item['fecha_cobro'] = self.fecha_cobro.strftime('%d/%m/%Y')
        return item

    class Meta:
        verbose_name_plural ="Cobro"

class Pago(ClaseModelo):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    cuota = models.ForeignKey(CuotaCompra,on_delete=models.CASCADE, null=True)
    caja = models.ForeignKey(Caja,on_delete=models.CASCADE)
    monto_pagado = models.IntegerField(default=0)
    tipos_pago = ( ('efectivo', 'Efectivo'),
                    ('cheque', 'Cheque'))
    medio_pago = models.CharField(max_length=20, choices = tipos_pago, default = 'efectivo')
    banco = models.ForeignKey(Banco, models.PROTECT, null=True)
    numero_cheque = models.IntegerField(default=0,null=True)
    fecha_pago = models.DateField(default=datetime.now)

    def toJSON(self):
        item = model_to_dict(self)
        item['fecha_pago'] = self.fecha_pago.strftime('%d/%m/%Y')
        return item

    class Meta:
        verbose_name_plural ="Pago"

class Movimiento(ClaseModelo):
    caja = models.ForeignKey(Caja, models.PROTECT) 
    movimientos = ( ('ingreso', 'Ingreso'),
                    ('egreso',  'Egreso'))
    tipo_movimiento = models.CharField(max_length=20, choices=movimientos, default='Ingreso')
    fecha_movimiento = models.DateField(default=datetime.now)
    monto = models.IntegerField()
    descripcion = models.CharField(max_length=100,null=True, blank=True)
    numero_comprobante = models.CharField (max_length=20,null=True, blank=True, unique=True,
                                                                                error_messages={
                                                                                    'unique': 'Número de Comprobante ya existente'
                                                                                })

    def toJSON(self):
        item = model_to_dict(self)
        #configuracion = ConfiguracionEgreso.objects.filter(estado=True)
        #item['monto_maximo'] = configuracion.monto_maximo
        configuracion = ConfiguracionEgreso.objects.filter(estado=True).values('monto_maximo').first()
        #print(configuracion['monto_maximo'])
        item['fecha_movimiento'] = self.fecha_movimiento.strftime('%d/%m/%Y')
        item['tipo_movimiento'] = self.tipo_movimiento.upper()
        return item
