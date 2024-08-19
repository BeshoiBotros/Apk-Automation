from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser

class LogoutView(View, LoginRequiredMixin):
    login_url = '/account/login/'

    def get(self, request, *args, **kwargs):
        print("logout", request.user.username)
        logout(request)
        return redirect('login')

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            return redirect('user-info')
        form = forms.RegisterForm()
        return render(request, 'accounts/register.html', {"form" : form})
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            return redirect('user-info')
        form = forms.RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        context = {
            "errors" : form.non_field_errors,
            "form" : form
        }
        return render(request, 'accounts/register.html',context=context )


class LoginView(View):

    def get(self, request, *args, **kwargs):
        form = forms.LoginForm()
        context = {
            "form": form,
        }
        return render(request, 'accounts/login.html', context)
    
    def post(self, request, *args, **kwargs):
        form = forms.LoginForm(data=request.POST)
        if form.is_valid():
            form.login(request)
            if not request.user.is_anonymous:
                form.REDIRECT_URL = 'user-info'
                return redirect(form.REDIRECT_URL)
        print("Form errors:", form.errors)

        context = {
            "form": form,
            "errors": form.non_field_errors()
        }
        return render(request, 'accounts/login.html', context=context, status=400)
    
class UserView(View, LoginRequiredMixin):
    
    
    login_url = "/accounts/login/"

    # view my info
    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('login')
        form = forms.UserForm()
        context = {
            "user" : request.user,
            "form" : form
        }
        return render(request, 'accounts/user-info.html', context)

    # update my info
    def post(self, request, *args, **kwargs):
        user = request.user
        form = forms.UserForm(data=request.POST)
        if request.POST:
            if form.is_valid():
                form.update(instance=user)
                return redirect('user-info')
            context = {
                'form' : form,
                'errors' : form.non_field_errors
            }
        return render(request, 'accounts/user-info.html', context)