from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import View
from onlineapp.form.auth import *
from django.contrib.auth import authenticate,login,logout

class LoginView(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('/colleges/')
        form = LoginForm()
        return render(
            request,
            template_name='login.html',
            context={
                'form': form,
            }
        )

    def post(self,request,*args,**kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user = authenticate(
                request,
                username=username,
                password=password,
            )
            if user is not None:
                login(request,user)
                return redirect('/colleges/')
            else:
                messages.error(request,'Invalid user credentials')
        return render(
            request,
            template_name="login/",
            context={
                'form':form,
            }
        )

class SignupView(View):
    def get(self,request):
        form = SignUpForm()
        return render(
            request,
            template_name='signup.html',
            context={
                'form': form,
            }
        )

    def post(self,request,*args,**kwargs):
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(**form.cleaned_data)
            user.save()
            if user is not None:
                return redirect('/login/')
            else:
                messages.error(request,'Invalid user credentials')

        else:
            return render(
                request,
                template_name='signup/',
                context={
                    'form': form,
                }
            )

def logout_user(request):
    logout(request)
    return redirect('/login/')
