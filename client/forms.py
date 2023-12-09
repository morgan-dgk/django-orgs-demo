from django import forms
from django.conf import settings

from user_auth.models import CustomUser
from .models import ClientUserProfile

class ClientUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    active = forms.BooleanField(required=False)

    class Meta:
        exclude = ('user',) 
        model = ClientUserProfile

    def __init__(self, *args, **kwargs):
        super(ClientUserForm, self).__init__(*args, **kwargs)

        if self.instance.pk is not None:
            self.fields["first_name"].initial = self.instance.user.first_name
            self.fields["last_name"].initial = self.instance.user.last_name
            self.fields["email"].initial = self.instance.user.email
            self.fields["active"].initial = self.instance.user.is_active

    def save(self, *args, **kwargs):
        if self.instance.pk is None:
            user = CustomUser(email=self.cleaned_data["email"], 
                              first_name=self.cleaned_data["first_name"], 
                              last_name=self.cleaned_data["last_name"])
            user.save()
            self.instance.user = user
        self.instance.organization = self.cleaned_data["organization"]
        self.instance.user.first_name = self.cleaned_data["first_name"]
        self.instance.user.last_name = self.cleaned_data["last_name"]
        self.instance.user.email = self.cleaned_data["email"]
        self.instance.user.is_active = self.cleaned_data["active"]
        self.instance.user.save()
        return super(ClientUserForm, self).save(*args, **kwargs)
        
