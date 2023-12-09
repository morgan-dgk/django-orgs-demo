from django.contrib.admin.apps import AdminConfig

class CustomAdminConfig(AdminConfig):
    defaut_site = "mda_client_portal.admin.CustomAdminSite"


