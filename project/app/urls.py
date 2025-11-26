from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

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