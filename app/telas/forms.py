from django import forms

from .models import Tela

class TelaForm(forms.ModelForm):
    class Meta:
        model = Tela
        fields = [
            'codigo',
            'nombre',
            'color',
            'metraje',
            'precio',
            'disenho',
            'categoria',
        ]
        labels = {
            'codigo':'Codigo',
            'nombre':'Nombre',
            'color':'Color',
            'metraje':'Metraje',
            'precio':'Precio',
            'disenho':'Diseño',
            'categoria':'Categoria',
		}
        widgets = {
            'codigo' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
            'nombre' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
			'color' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
			'metraje' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
			'precio' : forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
			'disenho' : forms.Select(attrs={'class':'form-control','autocomplete':'off'}),
			'categoria' : forms.Select(attrs={'class':'form-control','autocomplete':'off'}),
		}