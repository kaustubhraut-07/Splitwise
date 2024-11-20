from django.shortcuts import render
from .models import User , Group, Expense, Settlement
from rest_framework import response

# Create your views here.

def user_login(request):
    name = request.POST['name']
    email = request.POST['email']
    password = request.POST['password']

    user = User.objects.create(name=name, email=email, password=password)

    return response.status_code(200).message("User created successfully")