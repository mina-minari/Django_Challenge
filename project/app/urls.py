from django.urls import path
from . import views

urlpatterns = [
    path("", views.challenge_list, name="challenge_list"),
    path("create/", views.challenge_create, name="challenge_create"),
    path("<int:pk>", views.challenge_detail, name="challenge_detail"),
    path("<int:pk>/join/", views.challenge_join, name="challenge_join"),
    path("<int:pk>/verify/", views.verification_create, name="verification_create"),
    path("ranking/", views.ranking_view, name="ranking"),

    path("mypage/", views.mypage, name="mypage"),
    path("my-challenges/", views.my_challenges, name="my_challenges"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("upload-history/", views.upload_history, name="upload_history"),

    path("api/mypage/", views.mypage_api, name="mypage_api"),
    path("api/my-challenges/", views.my_challenges_api, name="my_challenges_api"),
    path("api/upload-history/", views.upload_history_api, name="upload_history_api"),
    path("api/profile/", views.profile_api, name="profile_api"),
]
