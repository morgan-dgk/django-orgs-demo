from django.contrib.auth import get_user_model
from organizations.backends import BaseBackend
from client.models import Client


class InvitationBackend(BaseBackend):

    def __init__(self, org_model=Client, namespace=None):
        self.user_model = get_user_model()
        self.org_model = org_model
        self.namespace = namespace

    def activate_organizations(self, user):
        """
        Activates the related organizations for the user.

        It only activates the related organizations by model type - that is, if
        there are multiple types of organizations then only organizations in
        the provided model class are activated.
        """
        relation_name = "client_clientuserprofile"
        organization = getattr(user, relation_name)
        organization_set = getattr(user, relation_name)
        for org in organization_set.filter(is_active=False):
            org.is_active = True
            org.save()

