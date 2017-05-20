from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
                                label='Usuário',
                                error_messages={'invalid': 'Usuário pode conter apenas letras e números'})

    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label='Email')
    password = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
                               label='Senha')
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
        label='Repita a senha')

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError("Esse usuário já existe")

    def clean(self):
        if 'password' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password2']:
                raise forms.ValidationError("O campo repita a senha deve ser igual a senha")

        return self.cleaned_data
