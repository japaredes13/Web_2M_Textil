from django import forms

from .models import Proveedor
from ubicaciones.models import Ciudad

class ProveedorForm(forms.ModelForm):
    ciudad=forms.ModelChoiceField(
        queryset=Ciudad.objects.order_by('descripcion')
    )
    class Meta:
        model = Proveedor
        fields = [
            'ciudad',
            'nombre_empresa',
            'direccion',
            'telefono',
            'email',
            'ruc',
        ]
        labels = {
            'ciudad':'Ciudad',
            'nombre_empresa':'Nombre de la Empresa',
            'direccion':'Dirección',
            'telefono':'Teléfono/Celular',
            'email':'E-mail',
            'ruc':'Ruc',
		}
        widgets = {
            'ciudad' : forms.Select(attrs={'class':'form-control'}),
			'nombre_empresa' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
			'direccion' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
			'telefono' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
            'email':forms.EmailInput(attrs={'class':'form-control','autocomplete':'off'}),
			'ruc' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
		}