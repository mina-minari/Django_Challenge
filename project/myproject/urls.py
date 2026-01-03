from django.contrib import admin
from django.urls import path, include

from app import views
from app.views import index, mypage

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("google_login/", views.google_login, name="google_login"),
    path("google_callback/", views.google_callback, name="google_callback"),
    path("logout/", views.user_logout, name="user_logout"),
    path("nickname/", views.nickname_form, name="nickname_form"),
    path("challenges/", include("app.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
