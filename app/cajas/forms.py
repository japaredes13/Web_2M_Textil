from django import forms
from datetime import datetime
from django.db.models import fields
from .models import Caja, Banco, Cobro, Movimiento

class CajaForm(forms.ModelForm):
    class Meta:
        model = Caja
        fields = [
            'monto_apertura',
            'fecha_apertura',
            'descripcion'
        ]
        labels = {
            'monto_apertura':"Monto Apertura",
            'fecha_apertura':"Fecha de Apertura",
            'descripcion':"Descripcion"

        }
        widgets = {
            'monto_apertura':forms.TextInput(attrs={'class':'form-control','autocomplete':'off', 'required':'required'}),
            'fecha_apertura': forms.DateInput(
                format='%d-%m-%Y',
                attrs={
                    'value':datetime.now().strftime('%d/%m/%Y'),
                    'autocomplete': 'off',
                    'class':'form-control datetimepicker-input',
                    'id':'fecha_apertura',
                    'data-target':'#fecha_apertura',
                    'data-toggle':'datetimepicker',
                    'onkeydown':'return false',
            }),
            'descripcion':forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),

        }

class CobroForm(forms.ModelForm):
    class Meta:
        model: Cobro
        fields = '__all__'
        widgets = {
            'fecha_cobro': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_cobro',
                    'data-target': '#fecha_cobro',
                    'onkeydown':'return false',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'monto_cobrado': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'medio_cobro':forms.Select(attrs={
                'class': 'form-control' 
            }),
            'banco': forms.Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'numero_cheque': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete':'off',
            }),
        }

class BancoForm(forms.ModelForm):
    class Meta:
        model = Banco
        fields = [
            'descripcion',
            'estado'
        ]
        labels = {
            'descripcion':"Banco:"
        }
        widgets = {
            'descripcion':forms.TextInput(attrs={'class':'form-control','autocomplete':'off', 'required':'required'}),
        }

        
class CajaMovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = [
            'tipo_movimiento',
            'fecha_movimiento',
            'monto',
            'descripcion',
            'numero_comprobante'
        ]
        labels = {
            'tipo_movimiento':'Tipo de Movimiento',
            'fecha_movimiento':'Fecha Movimiento',
            'monto':'Monto',
            'descripcion':'Motivo',
            'numero_comprobante': 'N° de Comprobante',
        }
        widgets = {
			'tipo_movimiento' : forms.Select(attrs={'class':'form-control'}),
            'fecha_movimiento': forms.DateInput(
                format='%d-%m-%Y',
                attrs={
                    'value':datetime.now().strftime('%d/%m/%Y'),
                    'autocomplete': 'off',
                    'class':'form-control datetimepicker-input',
                    'id':'fecha_movimiento',
                    'data-target':'#fecha_movimiento',
                    'data-toggle':'datetimepicker',
                    'onkeydown':'return false',
            }),
            'monto':forms.TextInput(attrs={'class':'form-control','autocomplete':'off', 'required':'required'}),
            'descripcion':forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
            'numero_comprobante':forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
        }