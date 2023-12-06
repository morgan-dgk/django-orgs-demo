from django.contrib import admin

from .models import Client

class ClientAdmin(admin.ModelAdmin):
    list_display = ["name", "package", "date_created", "active"]


admin.site.register(Client, ClientAdmin)
