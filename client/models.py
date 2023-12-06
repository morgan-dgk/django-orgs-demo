from django.db import models
from django_extensions.db.fields import AutoSlugField

class Client(models.Model):
    class ClientPackage(models.IntegerChoices):
        BASIC = 1
        PRO = 2
        PREMIUM = 3
    name = models.CharField(max_length=100)
    package = models.IntegerField(choices=ClientPackage.choices)
    slug = AutoSlugField(populate_from="name")
