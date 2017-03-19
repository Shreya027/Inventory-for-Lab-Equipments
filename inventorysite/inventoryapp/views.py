

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Lender
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required



def logout_inventory(request):
    if request.user.is_authenticated():
        logout(request)
        return redirect('/login/')
    else:
        return HttpResponseRedirect('/login')

def index(request):
	return render(request,'index.html')
#if request.user.is_authenticated():
#currentuser = request.user

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        username = request.POST.get('sap_id')

        user = User.objects.create(
            first_name = name,
            username = username,
            email=email,
            )
        user.set_password(password)
        user.save()

        user = authenticate(username = username, password = password)
        login(request, user)
        return redirect('/index/')
    else:
        return render(request,'register.html')   

def login_inventory(request):
    if request.method == 'POST':
        username = request.POST.get('sap_id')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user :
            if user.is_active:
                login(request,user)
                return redirect('/index/')
            else:
                return HttpResponse('Disabled Account')
        else:
            return HttpResponse("Invalid Login details.Are you trying to Sign up?")
    else:
        return render(request,'login.html')


