from django import forms

from organizations.models import Organization, OrganizationMembership, UserInvitation


class OrganizationCreateForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ["name", "slug", "description", "timezone"]


class InvitationCreateForm(forms.ModelForm):
    class Meta:
        model = UserInvitation
        fields = ["email", "role"]
        widgets = {"role": forms.Select(choices=OrganizationMembership.Role.choices)}
