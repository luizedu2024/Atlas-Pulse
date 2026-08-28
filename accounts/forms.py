from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from accounts.models import User


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"autocomplete": "email"}))
    remember_me = forms.BooleanField(label="Remember me", required=False)


class RegistrationForm(UserCreationForm):
    accept_terms = forms.BooleanField(label="I agree to the Terms of Use")

    class Meta:
        model = User
        fields = ["full_name", "email", "password1", "password2", "accept_terms"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["full_name", "email", "timezone", "language"]
