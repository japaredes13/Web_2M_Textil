from django.forms import *

from user.models import User
from django.contrib.auth.models import Group


class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email', 'username', 'password'
        widgets = {
            'first_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre',
                }
            ),
            'last_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese el apellido',
                }
            ),
            'email': TextInput(
                attrs={
                    'placeholder': 'Ingrese el email',
                }
            ),
            'username': TextInput(
                attrs={
                    'placeholder': 'Ingrese el username',
                }
            ),
            'password': PasswordInput(render_value=True,
                attrs={
                    'placeholder': 'Ingrese el password',
                }
            ),
        }
        exclude = ['groups', 'user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class RolForm(ModelForm):
    class Meta:
        model= Group 

        fields=[ 
	        'name',
            'permissions'
        ]

        labels={
           
	        'name':'Nombre Rol:',
            'permissions':'Seleccione los permisos:'
        }

        widgets={
	        'name': TextInput(attrs={'class':'form-control','autocomplete':'off'}),
            'permissions':SelectMultiple(attrs={'class':'form-control select2','id':'grupos'}),
        }
