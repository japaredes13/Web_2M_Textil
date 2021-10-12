from datetime import datetime
from django import forms
from .models import Venta, CuotaVenta
from clientes.models import Cliente

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = '__all__'
        labels = {
            'fecha_venta':"Fecha Venta:",
            'cliente':"Cliente:"
        }
        widgets = {
            'cliente':forms.Select(attrs={'class':'form-control' }),
            'fecha_venta': forms.DateInput(format='%Y-%m-%d',attrs={
                'class':'form-control datetimepicker-input',
                'id':'fecha_venta',
                'data-target':'#fecha_venta',
                'data-toggle':'datetimepicker',
                'onkeydown':'return false',
                'value':datetime.now().strftime('%Y-%m-%d')
            }),
            'condicion_venta':forms.Select(attrs={'class':'form-control','onchange':'condicionVentaSelect(this)' }),
            'sub_total_sin_iva': forms.NumberInput(attrs={'class':'form-control','readonly':True}),
			'monto_total' : forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
			'total_iva_10' : forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'numero_cheque' : forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete':'off',
            }),
        }

class CuotaVentaForm(forms.ModelForm):
    class Meta:
        model = CuotaVenta
        fields = '__all__'
        labels = {
            'fecha_vencimiento':"Fecha Vencimiento:",
        }
        widgets = {
            'fecha_vencimiento': forms.DateInput(format='%Y-%m-%d',attrs={
                'class':'form-control datetimepicker-input',
                'id':'fecha_vencimiento',
                'data-target':'#fecha_vencimiento',
                'data-toggle':'datetimepicker',
                'onkeydown':'return false',
                'value':datetime.now().strftime('%Y-%m-%d')
            }),
			'monto_cuota' : forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'numero_cuota' : forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            })
        }