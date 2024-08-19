from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate, login

def username_exists(username:str)->bool:
    return User.objects.filter(username=username).exists()

class RegisterForm(forms.Form):
    username  = forms.CharField(
        widget=forms.TextInput(attrs={'class' : 'form-control', "placeholder" : "Enter Username"}),
        max_length=255,
        required=True
    )
    email  = forms.EmailField(
        widget=forms.TextInput(attrs={'class' : 'form-control', "placeholder" : "Enter Username"}),
        max_length=255,
        required=True
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class' : 'form-control', "placeholder" : "Enter Password"}),
        required=True
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class' : 'form-control', "placeholder" : "Confirm Password"}),
        required=True
    )

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        username = cleaned_data.get('username')

        if password1 != password2:
            raise ValidationError("Confirm Password must be similar to the Password field")
        if username_exists(username):
            raise ValidationError("Username already exists")
        return cleaned_data
    
    def save(self):
        cleaned_data = self.cleaned_data
        user = User(
            username=cleaned_data['username'],
            email=cleaned_data['email']
        )
        user.set_password(cleaned_data['password1'])
        user.save()
        return user
    
class LoginForm(forms.Form):

    REDIRECT_URL = ''

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Username',
            'id': 'username',
            'autocomplete': 'username'
        }),
        max_length=255,
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password',
            'id': 'password',
            'autocomplete': 'current-password'
        }),
        required=True
    )

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(request=request, username=username, password=password)
        if not user:
            self.add_error(None, "username or password are incorrect")
            return
        login(request, user)



class UserForm(forms.ModelForm):
    username  = forms.CharField(
        widget=forms.TextInput(attrs={'class' : 'form-control', "placeholder" : "Enter Username"}),
        max_length=255,
        required=False
    )
    first_name  = forms.CharField(
        widget=forms.TextInput(attrs={'class' : 'form-control', "placeholder" : "Enter Firstname"}),
        max_length=255,
        required=False
    )
    last_name  = forms.CharField(
        widget=forms.TextInput(attrs={'class' : 'form-control', "placeholder" : "Enter Lastname"}),
        max_length=255,
        required=False
    )
    email  = forms.EmailField(
        widget=forms.TextInput(attrs={'class' : 'form-control', "placeholder" : "Enter Email"}),
        max_length=255,
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def update(self, instance):
        
        data = self.cleaned_data
        filtered_data = {}
        
        for key, val in data.items():
            if val not in [None, '']:
                filtered_data[key] = val
        
        for field, value in filtered_data.items():
            setattr(instance, field, value)

        instance.save()

        return instance