from django.db import models


# Create your models here.
class predictions(models.Model):
    image = models.ImageField('/media/')
    prediction = models.BooleanField()
    created = models.DateTimeField(auto_now=True)
