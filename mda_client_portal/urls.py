"""
URL configuration for mda_client_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.contrib.auth import views

from invitations.backend import CustomInvitations

urlpatterns = [
    path("", views.LoginView.as_view(template_name="user_auth/login.html")),
    path('client/', include('invitations.urls')),
    path('admin/', admin.site.urls),
    re_path('^invitations/', include(CustomInvitations().get_urls())),
    path("__debug__", include("debug_toolbar.urls"))
]
