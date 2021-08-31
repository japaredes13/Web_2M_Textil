from datetime import datetime
from django import forms
from .models import OrdenCompra, Compra

class CompraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Compra
        fields = '__all__'
        widgets = {
            'proveedor': forms.Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'disabled':'disabled'
            }),
            'nro_factura': forms.TextInput(attrs={
                'autocomplete': 'off',
                'class': 'form-control'
            }),
            'timbrado': forms.TextInput(attrs={
                'autocomplete': 'off',
                'class': 'form-control',
            }),
            'condicion_compra':forms.Select(attrs={
                'class': 'form-control' 
            }),
            'fecha_compra': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_compra',
                    'data-target': '#fecha_compra',
                    'onkeydown':'return false',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'inicio_timbrado': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'inicio_timbrado',
                    'data-target': '#inicio_timbrado',
                    'data-toggle': 'datetimepicker'
                }
            ),'fin_timbrado': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fin_timbrado',
                    'data-target': '#fin_timbrado',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'total_iva_10': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'monto_total': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            })
        }

class OrdenCompraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = OrdenCompra
        fields = '__all__'
        widgets = {
            'proveedor': forms.Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'fecha_orden': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_orden',
                    'data-target': '#fecha_orden',
                    'onkeydown':'return false',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'total_iva_10': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'monto_total': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            })
        }