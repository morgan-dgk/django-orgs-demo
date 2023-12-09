from django.contrib import admin
from django.db.models import Count 

from .models import Client, ClientUserProfile
from .forms import ClientUserForm   

class ClientAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super(ClientAdmin, self).get_queryset(request)
        return qs.annotate(users=Count("clientuserprofile__user", 0))

    def users(self, obj):
        return obj.users
  
    list_display = "name", "package", "date_created", "active", "users"
    list_filter = "package", "active"
    search_fields = ["name"]
    prepopulated_fields = {"slug": ["name"]}
    

admin.site.register(Client, ClientAdmin)
