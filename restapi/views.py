from django.shortcuts import render
from django.http import HttpResponse
import requests

# Create your views here.

def home(request):
    return HttpResponse("Hello, Django")

def taskstring(request):
    result = "Rest API string!"
    return HttpResponse(result, content_type="text/plain")

