from django import forms
from datetime import datetime
from .models import ConfiguracionUsuario, ConfiguracionProducto, ConfiguracionVenta, ConfiguracionEgreso


class ConfiguracionUsuarioForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionUsuario
        fields = [
            'metraje_minimo'
        ]
        labels = {
            'metraje_minimo':"Metraje Minimo:"
        }
        widgets = {
            'metraje_minimo':forms.TextInput(attrs={'class':'form-control','autocomplete':'off', 'required':'required'}),
        }

class ConfiguracionProductoForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionProducto
        fields = [
            'descripcion',
            'porcentaje'
        ]
        labels = {
            'descripcion':"Descripcion:",
            'porcentaje':"Porcentaje:"
        }
        widgets = {
            'descripcion':forms.TextInput(attrs={'class':'form-control','autocomplete':'off', 'required':'required'}),
            'porcentaje':forms.TextInput(attrs={'class':'form-control','autocomplete':'off', 'required':'required'}),
        }

class ConfiguracionVentaForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionVenta
        fields = [
            'rubro',
            'sucursal',
            'numero',
            'timbrado',
            'fecha_inicio_timbrado',
            'fecha_fin_timbrado'
        ]
        labels = {
            'rubro':"Rubro:",
            'sucursal':"Sucursal:",
            'numero':"Numero:",
            'timbrado':"Timbrado:",
            'fecha_inicio_timbrado':"Fecha Inicio Timbrado:",
            'fecha_fin_timbrado':"Fecha Fin Timbrado:"
        }
        widgets = {
            'rubro':forms.TextInput(attrs={'class':'form-control','autocomplete':'off', 'required':'required','min':'1','max':'9'}),
            'sucursal':forms.TextInput(attrs={'class':'form-control','autocomplete':'off', 'required':'required','min':'1','max':'9'}),
            'numero':forms.TextInput(attrs={'class':'form-control','autocomplete':'off', 'required':'required', 'range':[1,9999999]}),
            'timbrado':forms.TextInput(attrs={'class':'form-control','autocomplete':'off', 'required':'required'}),
            'fecha_inicio_timbrado': forms.DateInput(
                format='%d-%m-%Y',
                attrs={
                    'value': datetime.now().strftime('%d/%m/%Y'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_inicio_timbrado',
                    'data-target': '#fecha_inicio_timbrado',
                    'onkeydown':'return false',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'fecha_fin_timbrado': forms.DateInput(
                format='%d-%m-%Y',
                attrs={
                    'value': datetime.now().strftime('%d/%m/%Y'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_fin_timbrado',
                    'data-target': '#fecha_fin_timbrado',
                    'onkeydown':'return false',
                    'data-toggle': 'datetimepicker'
                }
            ),
        }

class ConfiguracionEgresoForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionEgreso
        fields = [
            'monto_maximo'
        ]
        labels = {
            'monto_maximo':"Monto Máximo:"
        }
        widgets = {
            'monto_maximo':forms.TextInput(attrs={'class':'form-control','autocomplete':'off', 'required':'required'}),
        }