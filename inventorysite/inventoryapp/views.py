

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Lender,Borrower
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from inventorysite.forms import LenderForm
from django.template import RequestContext
from django.shortcuts import render_to_response





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
        return redirect('/login/')
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
        return render(request,'register.html')



def lenderform(request):
    if request.method == 'POST':
        form = LenderForm(request.POST ,request.FILES or None )
        if form.is_valid():
            cd = form.cleaned_data
            Lender.objects.create(lender=cd['lender'],product_name=cd['product_name'],product_description=cd['product_description'],image=request.FILES['image'],department=cd['department'],safety_deposit=cd['safety_deposit'],contact_number=cd['contact_number'])
        form = LenderForm()    
        return render(request,'testlenderform.html',{'form': form})               
    else:
        form = LenderForm()
    return render(request, 'testlenderform.html', {'form': form})    




def inventorylist(request):
    if request.user.is_authenticated():
        currentuser = request.user


    errors = []
    if 'q' in request.GET :
        q = request.GET['q']
        if not q:
            errors.append('Enter a search term.')
        elif len(q) > 20:
            errors.append('Please enter at most 20 characters.')
        else:
            items = Lender.objects.filter(product_name__icontains=q)
            equipment=items[0]
            product_name=equipment.product_name
            name=currentuser.first_name
            sap_id=currentuser.username
            email=currentuser.email
            print currentuser


            student=Borrower(borrower=name,sap_id=sap_id,email=email,product_name=product_name)
            student.save()






            return render(request, 'inventoryresulttest.html',
                          {'items': items, 'query': q})

    full=Lender.objects.all()        
    return render(request, 'inventorytest.html',
              {'errors': errors,'full':full})





def cart(request):

    if request.user.is_authenticated():
        currentuser = request.user
        name=currentuser.first_name
        items = Borrower.objects.filter(borrower__icontains=name)
        return render(request, 'cart.html',
              {'items':items})










