from django.contrib import admin

from .models import Client, ClientUserProfile
from .forms import ClientUserForm   

class ClientUserInline(admin.TabularInline):
    model = ClientUserProfile

    def get_queryset(self, request):
         qs = super(ClientUserInline, self).get_queryset(request)
         return qs.filter()

class ClientAdmin(admin.ModelAdmin):
    list_display = ["name", "package", "date_created", "active"]
    list_filter = ["package", "active"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ["name"]}
    
    inlines = [ClientUserInline]

admin.site.register(Client, ClientAdmin)
