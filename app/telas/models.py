from django.db import models
from django.forms import model_to_dict
from bases.models import ClaseModelo
from tipos.models import *

class Tela(ClaseModelo):
    codigo= models.CharField(max_length=200,
                            unique=True,
                            error_messages={
                                'unique': 'El campo Codigo ya existe'
                            })
    nombre = models.CharField(max_length=200)
    color = models.CharField(max_length=200)
    metraje = models.FloatField()
    precio_venta  = models.IntegerField()
    precio_compra = models.IntegerField()
    precio_compra_anterior = models.IntegerField()
    disenho = models.ForeignKey(Disenho, models.PROTECT)
    categoria = models.ForeignKey(Categoria, models.PROTECT)
    
    def toJSON(self):
        item = model_to_dict(self)
        item ['color'] = '<input type="color" value="'+self.color+'" name="color" class="form-control" disabled>' 
        item['oferta'] = 0
        return item


class TelaOferta(ClaseModelo):
    tela = models.ForeignKey(Tela, on_delete=models.CASCADE)
    metraje_oferta = models.FloatField()
    precio_oferta  = models.IntegerField()
    descripcion = models.CharField(max_length=100,blank=True,null=True)


    def toJSON(self):
        item = model_to_dict(self)
        item['nombre'] = self.tela.nombre
        item['codigo'] = self.tela.codigo
        item['precio_venta_tela'] = self.tela.precio_venta
        #print(item['precio_venta_tela'])
        item['precio_compra_tela'] = self.tela.precio_compra
        #print(item['precio_compra_tela'])
        item['tela_metraje'] = self.tela.metraje
        #print(item['tela_metraje'])
        item['precio_venta'] = self.precio_oferta
        item['metraje_vendido'] = 0
        item ['color'] = '<input type="color" value="'+self.tela.color+'" name="color" class="form-control" disabled>' 
        item['metraje'] = self.metraje_oferta
        item['text']= 'TELA: '+ self.tela.nombre + ' COD: ' + self.tela.codigo
        item['sub_total'] = 0
        item['id'] = self.id
        item['oferta'] = 1
        item['tela_id'] = self.tela.id
        return item