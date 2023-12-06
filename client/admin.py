from django.contrib import admin

from .models import Client

class ClientAdmin(admin.ModelAdmin):
    list_display = ["name", "package", "date_created", "active"]
    list_filter = ["package", "active"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ["name"]}

admin.site.register(Client, ClientAdmin)
