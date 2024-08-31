"""
URL configuration for tournements project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from .views import list_tournements,open_tournement,accept_invitation,close_tournement,finish_tournement,start_match,finish_match


urlpatterns = [
    path('list/',list_tournements),
    path('open/',open_tournement),
    path('accept_invitation/',accept_invitation),
    path('close/',close_tournement),
    path('finish/',finish_tournement),
    path('start_match/',start_match),
    path('finish_match/',finish_match),

]
