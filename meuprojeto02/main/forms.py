from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(
        attrs={"placeholder": "Digite seu email", "class": "inputlogin"}
    ))
    password = forms.CharField(label="Senha", widget=forms.PasswordInput(
        attrs={"placeholder": "Digite sua senha", "class": "inputlogin"}
    ))


class CadastroForm(UserCreationForm):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(
        attrs={"placeholder": "Digite seu email", "class": "inputlogin"}
    ))

    class Meta:
        model = User
        fields = ("first_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"].lower()
        user.email = self.cleaned_data["email"].lower()
        if commit:
            user.save()
        return user
