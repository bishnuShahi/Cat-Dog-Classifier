from django.db import models

class MyModel(models.Model):
    image = models.ImageField(upload_to='media/image.jpg')
    class Meta:
        app_label = 'Authenticator'
