from django import forms
from .models import ConfiguracionUsuario


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