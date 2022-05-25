
from django.contrib import admin
from django.urls import path, include
from home.views import application
urlpatterns = [
    path('application',application.as_view())
]
