from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm

from user_auth.models import CustomUser
from .models import ClientUserProfile

class ClientUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()

    class Meta:
        exclude = ('user',) 
        model = ClientUserProfile


    def __init__(self, *args, **kwargs):
        super(ClientUserForm, self).__init__(*args, **kwargs)

        if self.instance.pk is not None:
            self.fields["first_name"].initial = self.instance.user.first_name
            self.fields["last_name"].initial = self.instance.user.last_name
            self.fields["email"].initial = self.instance.user.email

    def save(self, *args, **kwargs):
        data = self.cleaned_data
        user = CustomUser(email=data["email"], first_name=data["first_name"], last_name=data["last_name"])
        user.save()
        self.instance.user = user
        self.instance.organization = data["organization"]
        return super(ClientUserForm, self).save(*args, **kwargs)
        
