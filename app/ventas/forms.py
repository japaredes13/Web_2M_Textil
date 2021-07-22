from datetime import datetime
from django import forms
from .models import Venta
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
            'fecha_venta': forms.DateInput(format='%Y-%m-%d',attrs={'class':'form-control','value':datetime.now().strftime('%Y-%m-%d')}),
            'condicion_venta':forms.Select(attrs={'class':'form-control' }),
			'monto_total' : forms.NumberInput(attrs={'class':'form-control'}),
			'total_iva_10' : forms.NumberInput(attrs={'class':'form-control'}),
        }