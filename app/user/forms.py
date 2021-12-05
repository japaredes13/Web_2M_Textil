from django.forms import *
from django.contrib.auth.forms import UserCreationForm
from user.models import User
from django.contrib.auth.models import Group


class UserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    password1 = CharField(
            label=("Contraseña:"),
            strip=False,
            widget=PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
            
        )
    password2 = CharField(
            label=("Confirmación de Contraseña:"),
            widget=PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
            strip=False,
        )

    class Meta:
        model = User
        fields=[
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',

            'groups',
            'user_permissions',
        ]

        labels={
           
            'first_name':'Nombre:',
            'last_name':'Apellido:',
            'username':'Username:',
            'email' :'Correo:',
            'password1':'Contraseña:',
            'password2':'Contraseña:',
            'groups':'Roles:',
            'user_permissions':'Permisos Individuales:',
        }


        widgets={
            'first_name':TextInput(attrs={'class':'form-control'}),
            'last_name':TextInput(attrs={'class':'form-control'}),
            'username':TextInput(attrs={'class':'form-control'}),
            'email':EmailInput(attrs={'class':'form-control'}),
            'password1':PasswordInput(attrs={'class':'form-control','id':'password1'}),
            'password2':PasswordInput(attrs={'class':'form-control','id':'password2'}),
            'groups':SelectMultiple(attrs={'class':'form-control select2','id':'grupos'}),
            'user_permissions':SelectMultiple(attrs={'class':'form-control select2','id':'permisos'}),
        }
        #exclude = ['groups', 'user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff']

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
