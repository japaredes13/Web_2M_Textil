from django import forms
from .models import Departamento, Ciudad


class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = [
            'descripcion',
            'estado'
        ]
        labels = {
            'descripcion':"Departamento:"
        }
        widgets = {
            'descripcion':forms.TextInput(attrs={'class':'form-control','autocomplete':'off', 'required':'required'}),
        }


class CiudadForm(forms.ModelForm):
    departamento=forms.ModelChoiceField(
        queryset=Departamento.objects.order_by('descripcion')

    )
    class Meta:
        model = Ciudad
        fields = ['departamento','descripcion']
        labels = {
            'descripcion':"Ciudad"
        }
        widgets = {
            'descripcion':forms.TextInput(attrs={'class':'form-control','autocomplete':'off', 'required':'required'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
        self.fields['departamento'].empty_label = "Seleccione el Departamento"