from django import forms
from .models import ConfiguracionUsuario, ConfiguracionProducto, ConfiguracionVenta


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
            'rubro':forms.TextInput(attrs={'class':'form-control','autocomplete':'off', 'required':'required'}),
            'sucursal':forms.TextInput(attrs={'class':'form-control','autocomplete':'off', 'required':'required'}),
            'numero':forms.TextInput(attrs={'class':'form-control','autocomplete':'off', 'required':'required'}),
            'timbrado':forms.TextInput(attrs={'class':'form-control','autocomplete':'off', 'required':'required'}),
            'fecha_inicio_timbrado':forms.DateInput(attrs={'class':'form-control','autocomplete':'off', 'required':'required'}),
            'fecha_fin_timbrado':forms.DateInput(attrs={'class':'form-control','autocomplete':'off', 'required':'required'})
        }