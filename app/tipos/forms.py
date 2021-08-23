from django import forms
from .models import Categoria, Disenho


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = [
            'descripcion',
            'estado'
        ]
        labels = {
            'descripcion':"Categoria:"
        }
        widgets = {
            'descripcion':forms.TextInput(attrs={'class':'form-control','autocomplete':'off', 'required':'required'}),
        }


class DisenhoForm(forms.ModelForm):
    class Meta:
        model = Disenho
        fields = [
            'descripcion',
            'estado'
        ]
        labels = {
            'descripcion':"Disenho:"
        }
        widgets = {
            'descripcion':forms.TextInput(attrs={'class':'form-control','autocomplete':'off', 'required':'required'}),
        }