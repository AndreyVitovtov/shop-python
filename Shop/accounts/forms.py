from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Customer


class CustomerCreationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['username', 'surname', 'email', 'phoneNumber', 'address']


class CustomerAuthenticationForm(AuthenticationForm):
    class Meta:
        model = Customer
        fields = ['email', 'password']
