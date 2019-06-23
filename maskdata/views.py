from django.shortcuts import render
from .machinelearning import MachineLearning
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from django.http import JsonResponse
from .forms import AddSubreddit

# Create your views here.
def getJsondata(request):

    jsonData=MachineLearning.dothething()
    response = JsonResponse(jsonData)
    response.__setitem__("Access-Control-Allow-Origin", "*")
    response.__setitem__("Access-Control-Allow-Headers", "x-requested-width")
    #jsonData=JSONRenderer().render(jsonData)
    return response

def searchresulthandling(request):

    if request.method=="POST":
        form=AddSubreddit(request.POST)
        if form.is_valid():
            value=form.cleaned_data('subReddit')
            print(value)
        jsonData = MachineLearning.dothething(value)
        response = JsonResponse(jsonData)
        response.__setitem__("Access-Control-Allow-Origin", "*")
        response.__setitem__("Access-Control-Allow-Headers", "x-requested-width")
        # jsonData=JSONRenderer().render(jsonData)
        return response
