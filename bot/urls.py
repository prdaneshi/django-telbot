from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from . import views
import os

token = os.getenv("TOKEN")
urlpatterns = [
    path('{}'.format(token), csrf_exempt(views.main))
]