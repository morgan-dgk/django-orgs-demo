from django.contrib import admin
from django.db.models import Count 
from .forms import ClientUserForm

from .models import Client, User 

class UserOrgListFilter(admin.SimpleListFilter):
    title = "Client"

    parameter_name = "org_id"

    def lookups(self, request, model_admin):
        return Client.objects.values_list("id", "name")

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(organization__id=self.value())
        else:
            return queryset

class UserActiveListFilter(admin.SimpleListFilter):
    title = "Active"

    parameter_name = "active"

    def lookups(self, request, model_admin):
        return [
            ("1", "Yes"),
            ("0", "No")
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user__is_active=self.value())
        else:
            return queryset


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

   @admin.display(boolean=True)
   def active(self, obj):
       return obj.user.is_active

   def date_created(self, obj):
       return obj.user.date_joined

   def name(self, obj):
       user = obj.user
       return f"{user.first_name} {user.last_name}"

   def email(self, obj):
       return obj.user

   list_display = "email", "name", "organization", "active", "date_created"
   list_filter =  (UserOrgListFilter, UserActiveListFilter)

    

admin.site.register(Client, ClientAdmin)
admin.site.register(User, ClientUserAdmin)
