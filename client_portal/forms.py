from django import forms
from django.contrib.auth.forms import AuthenticationForm
from API.models import Client

class ClientRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = Client
        fields = ['nom', 'prenom', 'email', 'telephone', 'adresse']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Client.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords don't match")

class ClientLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email')