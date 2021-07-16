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
            'contacto',
            'telefono',
            'nro_celular',
            'email',
            'ruc',
            'estado',
        ]
        labels = {
            'ciudad':'Ciudad',
            'nombre_empresa':'Nombre de la Empresa',
            'direccion':'Dirección',
            'contacto':'Contacto',
            'telefono':'Teléfono',
            'nro_celular':'Número de Celular',
            'email':'E-mail',
            'ruc':'Ruc',
            'estado':'Estado'
		}
        widgets = {
            'ciudad' : forms.Select(attrs={'class':'form-control'}),
			'nombre_empresa' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
			'direccion' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
			'contacto' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
			'telefono' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
			'nro_celular' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
            'email':forms.EmailInput(attrs={'class':'form-control','autocomplete':'off'}),
			'ruc' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
            'estado' : forms.CheckboxInput(attrs={'class':'form-control'}),
		}