from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Cliente
from ubicaciones.models import Ciudad

class ClienteForm(forms.ModelForm):
    ciudad=forms.ModelChoiceField(
        queryset=Ciudad.objects.order_by('descripcion')
    )
    class Meta:
        model = Cliente
        fields = [
            'nombre',
            'apellido',
            'razon_social',
            'cedula',
            'ruc',
            'email',
            'tipo_cliente',
            'nro_telefono',
            'nro_celular',
            'ciudad',
            'direccion',
            'estado',
        ]
        labels = {
            'nombre':'Nombres',
            'apellido':'Apellidos',
            'razon_social':'Razon Social',
            'cedula':'Cedula',
            'ruc':'Ruc',
            'email':'E-mail',
            'tipo_cliente':'Tipo de Cliente',
            'nro_telefono':'Numero de Telefono',
            'nro_celular':'Numero de Celular',
            'ciudad':'Ciudad',
            'direccion':'Direccion',
            'estado':'Estado',
		}
        widgets = {
            'nombre' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
			'apellido' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
			'razon_social' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
			'cedula' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
			'ruc' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
			'email' : forms.EmailInput(attrs={'class':'form-control','autocomplete':'off'}),
			'tipo_cliente' : forms.Select(attrs={'class':'form-control'}),
            'nro_telefono' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
			'nro_celular' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
			'ciudad' : forms.Select(attrs={'class':'form-control'}),
            'direccion' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
            'estado' : forms.CheckboxInput(attrs={'class':'form-control'}),
		}