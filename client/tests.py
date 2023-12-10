from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import TestCase
from client.models import User as ClientUser, Client
from client.admin import ClientUserAdmin

from unittest.mock import Mock

class ClientUserAdminTests(TestCase):
    def test_delete_one_client_user_deletes_auth_user(self):
        User = get_user_model()
        auth_user = User.objects.create_user(pk=1, email="user@test.com", password="foo")
        auth_user.save()
        client = Client(name="Dummy Client", package=3)
        client.save()
        client_user = ClientUser.objects.create(user=auth_user, organization=client)
        client_user.save()
        client_user_admin = ClientUserAdmin(model=ClientUser, admin_site=admin.site)
        client_user_admin.delete_model(obj=client_user, request=Mock(auth_user))
        
        self.assertFalse(ClientUser.objects.filter(user_id=1))
        self.assertFalse(User.objects.filter(pk=1).exists()) 


    def test_delete_many_client_users_deletes_auth_users(self):
        User = get_user_model()

        user1, user2 = User.objects.bulk_create(
            [
                User(pk=1, email="user@test.com", password="foo"),
                User(pk=2, email="user2@test.com", password="bar")
            ]
        )

        client1, client2 = Client.objects.bulk_create(
            [
                Client(pk=1, name="Dummy Client", package=1),
                Client(pk=2, name="Dummy Client 2", package=2)

            ]
        )

        ClientUser.objects.bulk_create(
            [
                ClientUser(user1.id, client1.id),
                ClientUser(user2.id, client2.id)
            ]
        )

        client_user_admin = ClientUserAdmin(model=ClientUser, admin_site=admin.site)
        client_user_admin.delete_queryset(request=Mock(user1), queryset=ClientUser.objects.all())

        self.assertFalse(User.objects.exists())
        self.assertFalse(ClientUser.objects.exists())





