"""
Code borrowed from Django Organizations

Copyright (c) 2012-2019, Ben Lopatin and contributors
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.  Redistributions in binary
form must reproduce the above copyright notice, this list of conditions and the
following disclaimer in the documentation and/or other materials provided with
the distribution

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from django.urls import path, reverse 
from django.http import Http404
from django.shortcuts import redirect, render
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from organizations.backends import BaseBackend
from client.models import Client
from django.contrib.auth import authenticate, login

from invitations.forms import ClientUserCreationForm


class InvitationBackend(BaseBackend):
    registration_form_template = "invitations/register_form.html"

    def __init__(self, org_model=Client, namespace=None):
        self.user_model = get_user_model()
        self.org_model = org_model
        self.namespace = namespace

    def get_success_url(self, user_id):
        reverse("client_view", args=(user_id,))

    def activate_organizations(self, user):
        """
        Activates the related organization for the user.
        """
        relation_name = "clientuserprofile"
        organization = getattr(user, relation_name).organization
        if not organization.active:
            organization.active = True
            organization.save()


    def activate_view(self, request, user_id, token):
        """
        View function that activates the given User by setting `is_active` to
        true if the provided information is verified.
        """
        try:
            user = self.user_model.objects.get(id=user_id, is_active=False)
        except self.user_model.DoesNotExist:
            raise Http404("Your URL may have expired.")

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise Http404("Your URL may have expired.")
        form = self.get_form(
            data=request.POST or None, files=request.FILES or None, instance=user
        )
        if form.is_valid():
            form.instance.is_active = True
            user = form.save()
            user.set_password(form.cleaned_data["password1"])
            user.save()
            self.activate_organizations(user)
            user = authenticate(
              email=user.email,
              password=form.cleaned_data["password1"],
            )
            if user is None:
                raise Http404("Can't authenticate user")
            login(request, user)
            return redirect(self.get_success_url(user.id))
        return render(request, self.registration_form_template, {"form": form})


class CustomInvitations(InvitationBackend):
    invitation_subject = "invitations/email/invitation_subject.txt"
    invitation_body = "invitations/email/invitation_body.html"

    form_class = ClientUserCreationForm
    
    def get_success_url(self, user_id):
        return reverse("client_view", args=(user_id,))

    def get_urls(self):
        return [
                path("<int:user_id>-<token>/", 
                     view=self.activate_view, 
                     name="invitations_register")
        ]


    def invite_by_email(self, email, sender=None, request=None, **kwargs):
        try:
            user = self.user_model.objects.get(email=email)
        except self.user_model.DoesNotExist:
            user = self.user_model.objects.create(email=email,
                password=self.user_model.objects.make_random_password(),
            )
            user.is_active = False
            user.save()
        self.send_invitation(user, sender, **kwargs)
        return user

    def send_invitation(self, user, sender=None, **kwargs):
        if user.is_active:
            return False
        token = self.get_token(user)
        kwargs.update({"token": token})
        self.email_message(
            user, self.invitation_subject, self.invitation_body, sender, **kwargs
        ).send()
        return True

   
