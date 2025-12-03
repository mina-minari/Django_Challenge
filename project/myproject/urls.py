from django.contrib import admin
<<<<<<< HEAD
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
=======
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app.urls")),
]
>>>>>>> main
