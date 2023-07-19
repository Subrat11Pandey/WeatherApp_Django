
from django.contrib import admin
from django.urls import path
from mausam_app import views

urlpatterns = [
    path("", views.your_view, name="your_view"),


]