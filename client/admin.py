from django.contrib import admin

from .models import Client

class ClientAdmin(admin.ModelAdmin):
    list_display = ["name", "package", "date_created"]


admin.site.register(Client, ClientAdmin)
