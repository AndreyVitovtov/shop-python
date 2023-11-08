from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, decorators, logout, password_validation, update_session_auth_hash, \
    hashers
from django.core import exceptions
from django.core.validators import EmailValidator
from django.http import HttpResponse, JsonResponse
from .forms import CustomerCreationForm, CustomerAuthenticationForm


# Create your views here.

def register_view(request):
    if request.method == 'POST':
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, email=email, password=password)
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse(render(request, 'accounts/register.html', {'form': form}))

    form = CustomerCreationForm()
    return HttpResponse(render(request, 'accounts/register.html', {'form': form}))


def login_view(request):
    if request.method == 'POST':
        form = CustomerAuthenticationForm(request, request.POST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        return HttpResponse(render(request, 'accounts/login.html', {'form': form}))
    else:
        form = CustomerAuthenticationForm()
        return HttpResponse(render(request, 'accounts/login.html', {'form': form}))


@decorators.login_required
def logout_view(request):
    logout(request)
    return redirect('home')


@decorators.login_required
def update_profile(request):
    user = request.user
    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    username = request.POST['username']
    surname = request.POST['surname']
    phoneNumber = request.POST['phoneNumber']
    address = request.POST['address']
    error = ''

    email_validator = EmailValidator(message='Incorrect email')
    try:
        email_validator(email)
    except exceptions.ValidationError as e:
        error = e.message

    if password != confirm_password:
        error += ' Password mismatch'

    try:
        password_validation.validate_password(password, request.user)
    except exceptions.ValidationError as e:
        error += ' ' + ' '.join(list(e.messages))

    if error == '':
        user.email = email
        user.password = hashers.make_password(password)
        user.username = username
        user.surname = surname
        user.phoneNumber = phoneNumber
        user.address = address
        user.save()

        return JsonResponse({
            'sc': True
        })
    else:
        return JsonResponse({
            'sc': False,
            'error': error
        })
