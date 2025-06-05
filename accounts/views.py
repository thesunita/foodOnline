from django.http import HttpResponse
from django.shortcuts import redirect, render

from accounts.forms import UserForm
from vendor.forms import Vendorfrom
from accounts.models import User, UserProfile
from django.contrib import messages

# Create your views here.
def registerUser(request):
    if (request.method == 'POST'):
        print("POST DATA:", request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            print("CLEANED DATA:", form.cleaned_data)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role = User.CUSTOMER

            user.save()
            messages.success(request,'Your account has been registered successfully')
            return redirect('registerUser')
        else:
            print(form.errors)

    else:
        form = UserForm()

    context = {
        'form' : form
    } 
    return render(request,'accounts/registerUser.html',context)


def registerVendor(request):
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        v_from = Vendorfrom(request.POST, request.FILES)
        if form.is_valid() and v_from.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role = User.VENDOR
            user.save()

            vendor = v_from.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request,'Your account has been registered successfully. Please wait for approval')
            return redirect('registerVendor')

        else:
            print(form.errors)
    else:
        form = UserForm()
        v_from = Vendorfrom()
    context = {
        'form' : form,
        'v_form': v_from
    }
    return render(request,'accounts/registerVendor.html',context)