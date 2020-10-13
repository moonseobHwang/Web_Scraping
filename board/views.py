from django.shortcuts import render
from django.http import HttpResponse
import requests
from pymongo import MongoClient
# Create your views here.

def listwithmongo(request):
    data = request.GET.copy()
    with MongoClient('mongodb://172.17.0.1:27017/') as client:
        mydb = client.mydb
        result = list(mydb.economic.find({}))
        data['page_obj']=result
    return render(request, 'board/listwithmongo.html', context=data)

def workwithmongo(request):
    data2 = request.GET.copy()
    with MongoClient('mongodb://172.17.0.1:27017/') as client:
        work = client.work
        result = list(work.sampleCollection.find({}))
        data2['page_obj2']=result
    return render(request, 'board/workwithmongo.html', context=data2)