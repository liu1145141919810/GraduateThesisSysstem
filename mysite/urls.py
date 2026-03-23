"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from app00 import views

urlpatterns = [
    path("",views.login),
    path('index/',views.index),
    path("login/",views.login),
    path('register/',views.register,name='register'),#significant working form
    path("index/<str:page>.html", views.index_page, name="index_page"),
    path("profile/", views.profile, name="profile"),
    path('api/user/<int:user_id>/', views.user_detail),
    path('api/user/<int:user_id>/review/', views.review_user),
    #path("logout/", views.logout, name="logout"),
    #path('admin/', admin.site.urls),
]