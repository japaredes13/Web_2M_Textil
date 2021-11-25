from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import model_to_dict

from django.conf import settings
#from django.conf.urls.static import static


class User(AbstractUser):
    image = models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True)

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'base/img/empty.png')

    def toJSON(self):
        item = model_to_dict(self, exclude=['password','groups', 'user_permissions', 'last_login'])
        item['usuario'] = self.first_name + ' ' + self.last_name
        #if self.last_login:
        #    item['last_login'] = self.last_login.strftime('%d/%m/%Y')
        item['active'] = '<span class="badge badge-success">SI</span>' if (self.is_active) else '<span class="badge badge-danger">NO</span>'
        item['date_joined'] = self.date_joined.strftime('%d/%m/%Y')
        item['image'] = self.get_image()
        return item