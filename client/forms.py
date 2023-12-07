from django import forms
from django.conf import settings

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
            self.fields["first_name"].intial = self.instance.user.first_name
            self.fields["last_name"].inital = self.instance.user.last_name
            self.fields["email"].intial = self.instance.user.email

    field_order = ["email", "first_name", "last_name", "organization"]
