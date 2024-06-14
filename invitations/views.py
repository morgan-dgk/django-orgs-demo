from django.shortcuts import HttpResponse

# Create your views here.

def client_view(request, user):
    context_object_name = "organizations"
    
    return HttpResponse("Logged in!")
