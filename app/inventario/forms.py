from datetime import datetime
from django import forms
from .models import Inventario, DetalleInventario
from telas.models import Tela

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = '__all__'
        labels = {
            'fecha_inventario':"Fecha Inventario:",
        }
        widgets = {
            'fecha_inventario': forms.DateInput(format='%Y-%m-%d',attrs={
                'class':'form-control datetimepicker-input',
                'id':'fecha_inventario',
                'data-target':'#fecha_inventario',
                'data-toggle':'datetimepicker',
                'onkeydown':'return false',
                'value':datetime.now().strftime('%Y-%m-%d')
            }),
        }