from django import forms

from .models import Tela
from tipos.models import Categoria, Disenho

class TelaForm(forms.ModelForm):
    categoria=forms.ModelChoiceField(
        queryset=Categoria.objects.order_by('descripcion')
    )
    disenho=forms.ModelChoiceField(
        queryset=Disenho.objects.order_by('descripcion')

    )
    class Meta:
        model = Tela
        fields = [
            'codigo',
            'nombre',
            'color',
            'metraje',
            'precio_compra_anterior',
            'precio_compra',
            'precio_venta',
            'disenho',
            'categoria',
        ]
        labels = {
            'codigo':'Codigo',
            'nombre':'Nombre',
            'color':'Color',
            'metraje':'Metraje',
            'precio_compra_anterior':'Precio Compra Anterior',
            'precio_compra':'Precio Compra',
            'precio_venta':'Precio Venta',
            'disenho':'Diseño',
            'categoria':'Categoria',
		}
        widgets = {
            'codigo' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
            'nombre' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
			'color' : forms.TextInput(attrs={'type':'color','class':'form-control','autocomplete':'off'}),
			'metraje' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
			'precio_compra_anterior' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off','min':'1'}),
			'precio_compra' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off','min':'1'}),
			'precio_venta' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off','min':'1'}),
			'disenho' : forms.Select(attrs={'class':'form-control','autocomplete':'off'}),
			'categoria' : forms.Select(attrs={'class':'form-control','autocomplete':'off'}),
		}
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
        self.fields['categoria'].empty_label = "Seleccione la Categoria"
        self.fields['disenho'].empty_label = "Seleccione el Diseño"

