from django.db import models
from user.models import User
#from django.contrib.auth.models import User

class ClaseModelo(models.Model):
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    fecha_eliminacion = models.DateField(blank=True, null=True)
    user_created = models.ForeignKey(User, on_delete=models.PROTECT)
    user_updated_id = models.IntegerField(blank=True, null=True)

    class Meta:
        abstract=True