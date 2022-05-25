from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

# Create your views here.


class application(View):
    def get(self,request):
        data = {
            'sucsess' : True
        }
        return JsonResponse(data=data)