from django.shortcuts import render
from django.http import HttpResponse

def main(request, name):
    string: str = f'PRIVET {name}!'
    return HttpResponse(string)
