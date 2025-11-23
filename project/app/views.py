from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count
from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Challenge, Verification, UserProfile
from .serializers import UserProfileSerializer, MyChallengeSerializer


def get_current_user(request):
    # 현재는 username1 기준으로 확인할 수 있게 함
    return User.objects.get(username="username1")


def get_user_profile(user: User) -> UserProfile:
    profile, created = UserProfile.objects.get_or_create(user=user)
    return profile


def get_user_challenges(user: User):
    # Challenge.members(M2M) 기준으로 유저가 참여 중인 챌린지 조회
    return Challenge.objects.filter(members=user).distinct()


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
    challenges_qs = get_user_challenges(user)
    challenges_data = MyChallengeSerializer(challenges_qs, many=True).data

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
    challenges_qs = get_user_challenges(user)
    serializer = MyChallengeSerializer(challenges_qs, many=True)
    data = {"challenges": serializer.data}
    return Response(data)



def challenge_list(request):
    challenges = Challenge.objects.all().order_by("-created_at")
    return render(
        request,
        "challenge/challenge_list.html",
        {"challenges": challenges},
    )

def upload_history(request):
    user = get_current_user(request)  # 임시로 username1 고정

    verifications = (
        Verification.objects
        .filter(verified_member=user)
        .select_related("challenge")
        .order_by("-date")
    )

    context = {
        "verifications": verifications,
    }
    return render(request, "upload_history.html", context)
