from django.contrib.auth.forms import UserCreationForm

from user_auth.models import CustomUser

class ClientUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email",)


