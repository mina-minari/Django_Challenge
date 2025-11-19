from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import UserProfile, Challenge
from .serializers import UserProfileSerializer, MyChallengeSerializer


def get_current_user(request):
    return User.objects.get(username="username2")


def get_user_profile(user: User) -> UserProfile:
    profile, created = UserProfile.objects.get_or_create(user=user)
    return profile


def get_user_challenges(user: User):
    return Challenge.objects.filter(participants__user=user).distinct()


def mypage(request):
    user = get_current_user(request)
    profile = get_user_profile(user)
    profile_data = UserProfileSerializer(profile).data
    menu_items = [
        {"name": "My Challenges", "url_name": "my_challenges"},
        {"name": "Upload History", "url_name": "upload_history"},
        {"name": "Edit Profile", "url_name": "edit_profile"},
        {"name": "Settings", "url_name": "#"},
        {"name": "Log Out", "url_name": "#"},
    ]
    context = {
        "profile": profile_data,
        "menu_items": menu_items,
    }
    return render(request, "mypage.html", context)


def my_challenges(request):
    user = get_current_user(request)
    challenges = get_user_challenges(user)
    challenges_data = MyChallengeSerializer(challenges, many=True).data
    context = {"challenges": challenges_data}
    return render(request, "my_challenges.html", context)


def edit_profile(request):
    return render(request, "edit_profile.html")


def upload_history(request):
    return render(request, "upload_history.html")


@api_view(["GET"])
def mypage_api(request):
    user = get_current_user(request)
    profile = get_user_profile(user)
    profile_data = UserProfileSerializer(profile).data
    menu_items = [
        {"name": "My Challenges", "url_name": "my_challenges"},
        {"name": "Upload History", "url_name": "upload_history"},
        {"name": "Edit Profile", "url_name": "edit_profile"},
        {"name": "Settings", "url_name": "#"},
        {"name": "Log Out", "url_name": "#"},
    ]
    data = {
        "profile": profile_data,
        "menu_items": menu_items,
    }
    return Response(data)


@api_view(["GET"])
def my_challenges_api(request):
    user = get_current_user(request)
    challenges = get_user_challenges(user)
    serializer = MyChallengeSerializer(challenges, many=True)
    data = {"challenges": serializer.data}
    return Response(data)
