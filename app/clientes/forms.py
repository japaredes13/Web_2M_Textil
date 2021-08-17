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
            'razon_social',
            'ruc',
            'email',
            'nro_telefono',
            'ciudad',
            'direccion',
        ]
        labels = {
            'razon_social':'Nombre o Razon Social',
            'ruc':'Cédula o Ruc',
            'email':'E-mail',
            'nro_telefono':'Nº de Telefono o Celular',
            'ciudad':'Ciudad',
            'direccion':'Direccion',
		}
        widgets = {
			'razon_social' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
			'ruc' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
			'email' : forms.EmailInput(attrs={'class':'form-control','autocomplete':'off'}),
            'nro_telefono' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
			'ciudad' : forms.Select(attrs={'class':'form-control'}),
            'direccion' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
		}

def clean (self):
    try:
        var = ClienteForm.objects.get(
            ruc = self.cleaned_data['ruc']
        )
        if not self.instance.pk:
            raise forms.ValidationError("Registro ya existe")
        elif self.instance.pk != var.pk:
            raise forms.ValidationError("Cambio no permitido, ya existe este regristro")
    except ClienteForm.DoesNotExist:
        pass
    return self.cleaned_data













