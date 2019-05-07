"""medicine_resort_bot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = 'medicine_resort_bot'
urlpatterns = [
    path('callback/', views.callback),  # Line
    path('current_datetime/', views.current_datetime),  # test
    path('r/', views.r, name='r'),  # test

    # path('index/', views.index, name='homepage'),
    # path('tablemenu/', views.tablemenu, name='tablemenu'),
    # path('tablemenu/student/', views.student, name='students'),
    # path('tablemenu/student/<pk>/', views.studentdetail, name='student_detail'),
]
