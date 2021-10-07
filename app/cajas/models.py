from django.db import models
from bases.models import ClaseModelo
from datetime import datetime
from ventas.models import Venta, DetalleVenta, CuotaVenta
from django.forms.models import model_to_dict

class Caja(ClaseModelo):
    monto_apertura = models.IntegerField()
    monto_cierre = models.IntegerField(default=0,null=True)
    monto_efectivo = models.IntegerField(default=0,null=True)
    monto_cheque = models.IntegerField(default=0,null=True)
    monto_ingreso = models.IntegerField(default=0,null=True)
    monto_egreso = models.IntegerField(default=0,null=True)
    fecha_apertura = models.DateField(default=datetime.now)
    fecha_cierre = models.DateField(null=True)
    descripcion = models.CharField(max_length=200)

    def toJSON(self):
        item = model_to_dict(self)
        item['fecha_apertura'] = self.fecha_apertura.strftime('%d/%m/%Y')
        item['fecha_cierre'] = self.fecha_cierre.strftime('%d/%m/%Y') if (self.fecha_cierre) else ''
        item['caja_cerrada'] = '<span class="badge badge-success">NO</span>' if (self.estado) else '<span class="badge badge-danger">SI</span>'
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
    fecha_cobro = models.DateField(default=datetime.now)

    def toJSON(self):
        item = model_to_dict(self)
        item['fecha_cobro'] = self.fecha_cobro.strftime('%d/%m/%Y')
        return item

    class Meta:
        verbose_name_plural ="Cobro"

class Movimiento(ClaseModelo):
    caja = models.ForeignKey(Caja, models.PROTECT) 
    movimientos = ( ('ingreso', 'Ingreso'),
                    ('egreso',  'Egreso'))
    tipo_movimiento = models.CharField(max_length=20, choices=movimientos, default='Ingreso')
    fecha_movimiento = models.DateField(default=datetime.now)
    monto = models.IntegerField()
    descripcion = models.CharField(max_length=100,null=True, blank=True)
    numero_comprobante = models.CharField (max_length=20,null=True, blank=True)

    def toJSON(self):
        item = model_to_dict(self)
        item['fecha_movimiento'] = self.fecha_movimiento.strftime('%d/%m/%Y')
        item['tipo_movimiento'] = self.tipo_movimiento.upper()
        return item
