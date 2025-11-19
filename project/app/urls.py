from django.urls import path
from . import views

urlpatterns = [
    path("", views.mypage, name="home"),

    path("mypage/", views.mypage, name="mypage"),
    path("my-challenges/", views.my_challenges, name="my_challenges"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("upload-history/", views.upload_history, name="upload_history"),
]
