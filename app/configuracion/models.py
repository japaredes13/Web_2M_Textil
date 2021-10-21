from django.db import models
from bases.models import ClaseModelo

class ConfiguracionUsuario(ClaseModelo):
    metraje_minimo = models.FloatField(unique=True,
                                        error_messages={
                                            'unique': 'Metraje minimo ya existente'
                                        })

    class Meta:
        verbose_name_plural ="Configuracion Usuario"

class ConfiguracionProducto(ClaseModelo):
    descripcion = models.CharField(max_length=200)
    porcentaje = models.FloatField()

    class Meta:
        verbose_name_plural ="Configuracion de Producto"


class ConfiguracionVenta(ClaseModelo):
    rubro = models.IntegerField()
    sucursal = models.IntegerField()
    numero = models.IntegerField()
    timbrado = models.IntegerField()
    fecha_inicio_timbrado = models.DateField()
    fecha_fin_timbrado = models.DateField()


    class Meta:
        verbose_name_plural ="Configuracion de Venta"

class ConfiguracionEgreso(ClaseModelo):
    monto_maximo = models.IntegerField(unique=True,
                                        error_messages={
                                            'unique': 'Monto Máximo ya existente'
                                        })

    class Meta:
        verbose_name_plural ="Configuracion Egreso"