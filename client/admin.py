from django.contrib import admin
from django.db.models import Count 
from .forms import ClientUserForm

from .models import Client, User 
from user_auth.models import CustomUser


class ClientAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super(ClientAdmin, self).get_queryset(request)
        return qs.annotate(users=Count("clientuserprofile__user", 0))

    def users(self, obj):
        return obj.users

    list_display = "name", "package", "date_created", "active", "users"
    list_filter = "package", "active",
    search_fields = ["name"]
    prepopulated_fields = {"slug": ["name"]}


class ClientUserAdmin(admin.ModelAdmin):
   form = ClientUserForm

   def delete_queryset(self, request, queryset):
       """Ensure related user_auth.user models are deleted
       when client.User models are removed.""" 
       
       linked_users = CustomUser.objects.filter(id__in=queryset)
       linked_users.delete()
       return super().delete_queryset(request, queryset) 

   def delete_model(self, request, obj):
       """Enure related user_auth.user is deleted when single
       client.User object is removed."""
       obj.user.delete()
       super().delete_model(request, obj)

   @admin.display(boolean=True)
   def active(self, obj):
       return obj.user.is_active

   def date_created(self, obj):
       return obj.user.date_joined

   def name(self, obj):
       return f"{obj.user.first_name} {obj.user.last_name}"

   def email(self, obj):
       return obj.user

   list_display = "email", "name", "organization", "active", "date_created"
   list_filter =  "user__is_active", "organization__name"

   search_fields = ("user__email",)



    

admin.site.register(Client, ClientAdmin)
admin.site.register(User, ClientUserAdmin)
