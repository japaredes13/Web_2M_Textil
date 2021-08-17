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

    '''def clean (self):
        try:
            proveedor = Proveedor.objects.get(
                ruc = self.cleaned_data["ruc"]
            )
            if not self.instance.pk:
                raise forms.ValidationError("Registro ya existe")
            elif self.instance.pk != proveedor.pk:
                raise forms.ValidationError("Cambio no permitido, ya existe este regristro")
        except Proveedor.DoesNotExist:
            pass
        return self.cleaned_data'''
