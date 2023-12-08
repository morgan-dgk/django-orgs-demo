from django.db import models
from django_extensions.db.fields import AutoSlugField
from user_auth.models import CustomUser

class Client(models.Model):
    class ClientPackage(models.IntegerChoices):
        BASIC = 1
        PRO = 2
        PREMIUM = 3
    name = models.CharField(max_length=100)
    package = models.IntegerField(choices=ClientPackage.choices)
    slug = AutoSlugField(editable=True, populate_from="name")
    date_created = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ClientUserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    organization = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
   
    def __str__(self):
        return self.user.email
