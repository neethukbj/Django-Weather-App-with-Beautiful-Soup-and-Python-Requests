from django.urls import path
from . import views

urlpatterns =[
    path('',views.HOME,name='home'),
]