from django.contrib import admin

from .models import Client, ClientUserProfile
from .forms import ClientUserForm   

class ClientAdmin(admin.ModelAdmin):
    list_display = ["name", "package", "date_created", "active"]
    list_filter = ["package", "active"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ["name"]}


class ClientUserAdmin(admin.ModelAdmin):
    form = ClientUserForm 

admin.site.register(ClientUserProfile, ClientUserAdmin)
admin.site.register(Client, ClientAdmin)
