from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count
from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Challenge, Verification, UserProfile
from .serializers import UserProfileSerializer, MyChallengeSerializer, VerificationSerializer

from rest_framework import status

from .forms import ProfileForm


def get_current_user(request):
    # 현재는 username1 기준으로 확인할 수 있게 함
    return User.objects.get(username="soyeon-kk")


def get_user_profile(user: User) -> UserProfile:
    profile, created = UserProfile.objects.get_or_create(user=user)
    return profile


def get_user_challenges(user: User):
    # Challenge.members(M2M) 기준으로 유저가 참여 중인 챌린지 조회
    return Challenge.objects.filter(members=user).distinct()


def mypage(request):
    user = get_current_user(request)
    profile = get_user_profile(user)  
    participating_count = user.joined_challenges.count()

    menu_items = [
        {"name": "My Challenges", "url_name": "my_challenges"},
        {"name": "Upload History", "url_name": "upload_history"},
        {"name": "Edit Profile", "url_name": "edit_profile"},
        {"name": "Settings", "url_name": "#"},
        {"name": "Log Out", "url_name": "#"},
    ]

    context = {
        "profile": profile,     
        "participating_count": participating_count,
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
    user = get_current_user(request)  # 나중에 request.user로 교체
    profile = get_user_profile(user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, user=user, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "프로필이 수정되었습니다.")
            return redirect("mypage")
    else:
        # GET 요청: 기존 값으로 채워진 폼 보여주기
        form = ProfileForm(user=user, instance=profile)

    context = {
        "form": form,
        "profile": profile,
    }
    return render(request, "edit_profile.html", context)


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

@api_view(["GET"])
def upload_history_api(request):
    user = get_current_user(request)

    verifications = (
        Verification.objects
        .filter(verified_member=user)
        .select_related("challenge")
        .order_by("-date")
    )

    serializer = VerificationSerializer(verifications, many=True)
    data = {
        "verifications": serializer.data,
    }
    return Response(data, status=status.HTTP_200_OK)



@api_view(["GET", "PUT", "PATCH"])
def profile_api(request):
    user = get_current_user(request)   # 나중에는 request.user
    profile = get_user_profile(user)

    if request.method == "GET":
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # PUT / PATCH 공통 처리
    partial = (request.method == "PATCH")  # PATCH면 부분 수정 허용
    serializer = UserProfileSerializer(
        profile,
        data=request.data,
        partial=partial,
    )
    if serializer.is_valid():
        serializer.save()  # 여기서 update() 호출됨 -> User + UserProfile 둘 다 저장
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
