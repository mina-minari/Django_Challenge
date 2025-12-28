from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import JsonResponse
import json
import requests
from django.db import IntegrityError
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import User, Challenge, Verification, UserProfile
from .forms import NicknameForm, ChallengeForm, VerificationForm, ProfileForm
from .serializers import UserProfileSerializer, MyChallengeSerializer, VerificationSerializer


user = User()
google_user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
try:
    with open("app/secret.json", "r") as f:
        secrets = json.load(f)
        client_id = secrets["web"]["client_id"]
        redirect_uri = secrets["web"]["redirect_uris"][0]
        google_auth_uri = secrets["web"]["auth_uri"]
        client_secret = secrets["web"]["client_secret"]
        token_uri = secrets["web"]["token_uri"]
except FileNotFoundError:
    raise Exception("보안 파일을 찾을 수 없습니다. 경로를 확인하세요.")
except json.JSONDecodeError:
    raise Exception("보안 파일의 JSON 형식이 올바르지 않습니다.")


def index(request):
    if request.user.is_authenticated:
        return redirect("challenge_list")
    return render(request, "accounts/login.html")


def google_login(request):
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": "openid%20profile%20email",
        "response_type": "code",
    }
    auth_url = f"{google_auth_uri}?" + "&".join(
        [f"{key}={value}" for key, value in params.items()]
    )
    return redirect(auth_url)


def google_callback(request):
    code = request.GET.get("code")
    if not code:
        return HttpResponse("인증 코드가 제공되지 않았습니다.", status=400)

    token_data = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }

    try:
        token_response = requests.post(token_uri, data=token_data)
        token_response.raise_for_status()
        access_token = token_response.json().get("access_token")
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"토큰 요청 중 오류가 발생했습니다: {e}", status=500)

    try:
        userinfo_res = requests.get(
            google_user_info_url, headers={"Authorization": f"Bearer {access_token}"}
        )
        userinfo_res.raise_for_status()
        user_info = userinfo_res.json()
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"사용자 정보 요청 중 오류가 발생했습니다: {e}", status=500)

    profile_image = user_info.get("picture")
    email = user_info.get("email")
    name = user_info.get("name", email)

    try:
        user = User.objects.get(username=email)
    except User.DoesNotExist:
        request.session["social_login_data"] = {
            "name": name,
            "email": email,
            "profile_image": profile_image,
        }
        return redirect("nickname_form")
    except IntegrityError:
        return HttpResponse("데이터베이스 오류가 발생했습니다.", status=500)

    login(request, user)
    return redirect("index")


def nickname_form(request):
    if request.method == "POST":
        social_data = request.session.get("social_login_data")
        if not social_data:
            messages.error(request, "잘못된 접근입니다. 다시 로그인해주세요.")
            return redirect("index")

        nickname = request.POST.get("nickname")
        name = social_data.get("name")
        email = social_data.get("email")
        profile_image = social_data.get("profile_image")

        try:
            user = User.objects.create_user(
                username=email,
                password=None,
                nickname=nickname,
                name=name,
                profile_image=profile_image,
            )
        except IntegrityError:
            return HttpResponse(
                "닉네임이 이미 사용 중입니다. 다른 닉네임을 선택해주세요.", status=400
            )

        login(request, user)
        return redirect("index")

    form = NicknameForm()
    return render(request, "accounts/nickname.html", {"form": form})


@login_required
def ranking_view(request):
    users = []
    for i in range(1, 31):
        users.append(
            {
                "id": i,
                "name": f"홍길동{i}",
                "nickname": f"챌린저_{i}",
                "profile_image": f"https://picsum.photos/id/{i+10}/50/50",
                "challenge_point": 3000 - (i * 100),
            }
        )
    return render(request, "challenge/challenge_rank.html", {"users": users})


def user_logout(request):
    logout(request)
    return redirect("index")


def get_current_user(request):
    return User.objects.get(username=request.user.username)


def get_user_profile(user: User) -> UserProfile:
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return profile


def get_user_challenges(user: User):
    return Challenge.objects.filter(members=user).distinct()


@login_required
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

    return render(
        request,
        "challenge/mypage.html",
        {
            "profile": profile,
            "participating_count": participating_count,
            "menu_items": menu_items,
        },
    )


@login_required
def my_challenges(request):
    user = get_current_user(request)
    challenges_qs = get_user_challenges(user)
    challenges_data = MyChallengeSerializer(challenges_qs, many=True).data
    return render(request, "challenge/my_challenges.html", {"challenges": challenges_data})


@login_required
def edit_profile(request):
    user = get_current_user(request)
    profile = get_user_profile(user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, user=user, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "프로필이 수정되었습니다.")
            return redirect("mypage")
    else:
        form = ProfileForm(user=user, instance=profile)

    return render(
        request,
        "challenge/edit_profile.html",
        {
            "form": form,
            "profile": profile,
        },
    )


@login_required
def upload_history(request):
    user = get_current_user(request)

    verifications = (
        Verification.objects.filter(verified_member=user)
        .select_related("challenge")
        .order_by("-date")
    )

    return render(
        request,
        "challenge/upload_history.html",
        {"verifications": verifications},
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
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

    return Response({"profile": profile_data, "menu_items": menu_items})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_challenges_api(request):
    user = get_current_user(request)
    challenges_qs = get_user_challenges(user)
    serializer = MyChallengeSerializer(challenges_qs, many=True)
    return Response({"challenges": serializer.data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def upload_history_api(request):
    user = get_current_user(request)

    verifications = (
        Verification.objects.filter(verified_member=user)
        .select_related("challenge")
        .order_by("-date")
    )

    serializer = VerificationSerializer(verifications, many=True)
    return Response({"verifications": serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET", "PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def profile_api(request):
    user = get_current_user(request)
    profile = get_user_profile(user)

    if request.method == "GET":
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    partial = request.method == "PATCH"
    serializer = UserProfileSerializer(profile, data=request.data, partial=partial)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
def challenge_list(request):
    challenges = Challenge.objects.all().order_by("-created_at")
    return render(request, "challenge/challenge_list.html", {"challenges": challenges})


@login_required
def challenge_detail(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk)
    verifications = challenge.verifications.select_related("verified_member")
    return render(
        request,
        "challenge/challenge_detail.html",
        {"challenge": challenge, "verifications": verifications},
    )


@login_required
def challenge_create(request):
    if request.method == "POST":
        form = ChallengeForm(request.POST)
        if form.is_valid():
            challenge = form.save(commit=False)
            challenge.leader = request.user
            challenge.current_member = 1
            challenge.save()
            challenge.members.add(request.user)
            messages.success(request, "챌린지가 생성되었습니다")
            return redirect("challenge_detail", pk=challenge.pk)
    else:
        form = ChallengeForm()

    return render(request, "challenge/challenge_form.html", {"form": form})


@login_required
def challenge_join(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk)

    if challenge.members.filter(id=request.user.id).exists():
        messages.info(request, "해당 챌린지에 참여중입니다.")
        return redirect("challenge_detail", pk=pk)

    challenge.members.add(request.user)
    challenge.current_member = challenge.members.count()
    challenge.save(update_fields=["current_member"])

    messages.success(request, "챌린지에 참여했습니다.")
    return redirect("challenge_detail", pk=pk)


@login_required
def verification_create(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk)

    if not challenge.members.filter(id=request.user.id).exists():
        messages.error(request, "이 챌린지에 참여 중인 회원만 인증할 수 있습니다.")
        return redirect("challenge_detail", pk=pk)

    if request.method == "POST":
        form = VerificationForm(request.POST, request.FILES)
        if form.is_valid():
            verification = form.save(commit=False)
            verification.verified_member = request.user
            verification.challenge = challenge
            verification.save()

            messages.success(request, "인증이 완료되었습니다!")
            return redirect("challenge_detail", pk=pk)
    else:
        form = VerificationForm()

    return render(
        request,
        "challenge/verification_form.html",
        {"challenge": challenge, "form": form},
    )
