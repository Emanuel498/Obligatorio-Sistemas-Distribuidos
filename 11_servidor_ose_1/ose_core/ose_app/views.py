from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    print('HOLA')
    return HttpResponse("Hello, world.")


