"""
URL configuration for myproject project.

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
from app import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("",views.index, name="index"),
    path("google_login/",views.google_login, name="google_login"),
    path("challenge_list/",views.google_callback, name="google_callback"),
    path("logout/",views.user_logout, name="user_logout"),
    path("nickname/",views.nickname_form, name="nickname_form"),
]