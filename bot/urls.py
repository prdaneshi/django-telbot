from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('', csrf_exempt(views.main))
]