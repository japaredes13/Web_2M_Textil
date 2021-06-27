from django import forms
from .models import Departamento, Ciudad


class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ['descripcion','estado']
        widgets = {'descripcion':forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })

class CiudadForm(forms.ModelForm):
    departamento=forms.ModelChoiceField(
        queryset=Departamento.objects.order_by('descripcion')

    )
    class Meta:
        model = Ciudad
        fields = ['departamento','descripcion','estado']
        labels = {'descripcion':"Ciudad",'estado':"Estado"}
        widgets = {'descripcion':forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
        self.fields['departamento'].empty_label = "Seleccione el Departamento"