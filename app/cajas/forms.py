from django import forms
from datetime import datetime
from .models import Caja

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