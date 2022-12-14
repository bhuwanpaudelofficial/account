from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate,logout
from account_module.models import Account
from account_module.form import RegistrationForm,AccountAuthenticationForm


def login_view(request,*args,**kwargs):
    context = {}
    return render(request,'login.html',context)


def signup_view(request,*args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"you are already authenticated as {user.email}.")
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email = email, password = raw_password)
            login(request,account)
            destination = get_redirect_if_exists(request)
            if destination:
                return redirect(destination)
            return redirect('home')
        else:
            context['registration_form'] = form
    return render(request,'signup.html',context)



def logout_view(request):
    logout(request)
    return redirect("index")



def login_view(request,*args,**kwargs):
    context ={}

    user = request.user

    if user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email = email, password = password)
            if user:
                login(request,user)
                destination = get_redirect_if_exists(request)
                if destination:
                    return redirect(destination)
                return redirect('home')
        else:
            context['login_form'] = form
    return render(request,'login.html',context)




def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get('next'):
            redirect = str(request.GET.get('next'))
    return redirect



