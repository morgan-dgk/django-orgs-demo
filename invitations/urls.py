from django.urls import path
import invitations.views as views 

urlpatterns = [
        path("<int:user>",  views.client_view, name="client_view")
]




