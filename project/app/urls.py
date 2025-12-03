from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.mypage, name="mypage"),
    path("mypage/", views.mypage, name="mypage"),
    path("my-challenges/", views.my_challenges, name="my_challenges"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("upload-history/", views.upload_history, name="upload_history"),
    path("api/mypage/", views.mypage_api, name="mypage_api"),
    path("api/my-challenges/", views.my_challenges_api, name="my_challenges_api"),
]


urlpatterns = [
    path('', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('challenges/', views.challenge_list, name='challenge_list'),
    path('challenges/create/', views.challenge_create, name='challenge_create'),
    path('challenges/<int:pk>', views.challenge_detail, name='challenge_detail'),
    path('challenges/<int:pk>/join/', views.challenge_join, name='challenge_join'),
    path('challenges/<int:pk>/verify/', views.verification_create, name='verification_create'),
]
