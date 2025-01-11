from django import forms
from .models import Contato,Usuario


class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ['nome', 'email', 'mensagem']


class LoginForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['email', 'senha'] 

    email = forms.EmailField(
        label='Email', 
        widget=forms.EmailInput(attrs={'placeholder': 'Digite seu email', 'class':'inputlogin'})
    )

    senha = forms.CharField(
        label='Senha', 
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua senha', 'class':'inputlogin'})
    )

class CadastroForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome','email', 'senha'] 

    nome = forms.CharField(
        label='nome', 
        widget=forms.TextInput(attrs={'placeholder': 'Digite seu nome', 'class':'inputlogin'})
    )

    email = forms.EmailField(
        label='Email', 
        widget=forms.EmailInput(attrs={'placeholder': 'Digite seu email', 'class':'inputlogin'})
    )

    senha = forms.CharField(
        label='Senha', 
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua senha', 'class':'inputlogin'})
    )
    

