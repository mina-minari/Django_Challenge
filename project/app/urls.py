from django.urls import path
from . import views

urlpatterns = [
    path("", views.mypage, name="mypage"),
    path("mypage/", views.mypage, name="mypage"),
    path("my-challenges/", views.my_challenges, name="my_challenges"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("upload-history/", views.upload_history, name="upload_history"),
    path("api/mypage/", views.mypage_api, name="mypage_api"),
    path("api/my-challenges/", views.my_challenges_api, name="my_challenges_api"),
]
