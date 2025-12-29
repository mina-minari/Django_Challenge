from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import JsonResponse
import json
import requests
from .models import User, Challenge, Verification, UserProfile
from django.db import IntegrityError
from django.contrib.auth import login, logout
from .forms import NicknameForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer, MyChallengeSerializer
from .forms import ChallengeForm, VerificationForm

user = User()
google_user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
try:
    with open("app/secret.json", "r") as f:
        secrets = json.load(f)  # 딕셔너리 형태
        client_id = secrets["web"]["client_id"]
        redirect_uri = secrets["web"]["redirect_uris"][0]
        google_auth_uri = secrets["web"]["auth_uri"]
        client_secret = secrets["web"]["client_secret"]
        token_uri = secrets["web"]["token_uri"]
except FileNotFoundError:
    raise Exception(f"보안 파일을 찾을 수 없습니다. 경로를 확인하세요.")
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
    )  # "&".join(['a','b','c']) -> 'a&b&c'
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
        token_response.raise_for_status()  # HTTP 상태 코드 확인 400~500대면 예외 발생
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
    name = user_info.get("name", email)  # name이 없거나 none이면 email로 대체
    try:
        user = User.objects.get(
            username=email
        )  # 사용자가 이름이나 프사를 바꿔도 업데이트 안됨
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
        # 만약 세션에 데이터가 없다면? (URL로 직접 접속한 경우)
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
            messages.error(
                request, "닉네임이 이미 사용 중입니다. 다른 닉네임을 선택해주세요."
            )
            return redirect("nickname_form")
        login(request, user)
        return redirect("index")
    else:
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
                # 랜덤 프로필 이미지 (실제 이미지 주소 대신 placeholder 사용)
                "profile_image": f"https://picsum.photos/id/{i+10}/50/50",
                "challenge_point": 3000 - (i * 100),  # 2900, 2800... 점수 내림차순
            }
        )
    # users = User.objects.all().order_by('-challenge_point')
    return render(request, "challenge/challenge_rank.html", {"users": users})


def user_logout(request):
    logout(request)
    return redirect("index")


def get_current_user(request):
    # 현재는 username1 기준으로 확인할 수 있게 함
    return User.objects.get(username=request.user.username)


def get_user_profile(user: User) -> UserProfile:
    profile, created = UserProfile.objects.get_or_create(user=user)
    return profile


def get_user_challenges(user: User):
    # Challenge.members(M2M) 기준으로 유저가 참여 중인 챌린지 조회
    return Challenge.objects.filter(members=user).distinct()


@login_required
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
    return render(request, "challenge/mypage.html", context)


@login_required
def my_challenges(request):
    user = get_current_user(request)
    challenges_qs = get_user_challenges(user)
    challenges_data = MyChallengeSerializer(challenges_qs, many=True).data

    context = {"challenges": challenges_data}
    return render(request, "challenge/my_challenges.html", context)


@login_required
def edit_profile(request):
    return render(request, "challenge/edit_profile.html")


@login_required
def upload_history(request):
    return render(request, "challenge/upload_history.html")


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

    data = {
        "profile": profile_data,
        "menu_items": menu_items,
    }
    return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_challenges_api(request):
    user = get_current_user(request)
    challenges_qs = get_user_challenges(user)
    serializer = MyChallengeSerializer(challenges_qs, many=True)
    data = {"challenges": serializer.data}
    return Response(data)


@login_required
def challenge_list(request):
    challenges = Challenge.objects.all().order_by("-created_at")
    return render(
        request,
        "challenge/challenge_list.html",
        {"challenges": challenges},
    )


# 챌린지 상세
@login_required
def challenge_detail(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk)
    verifications = challenge.verifications.select_related("verified_member")

    return render(
        request,
        "challenge/challenge_detail.html",
        {
            "challenge": challenge,
            "verifications": verifications,
        },
    )


# 챌린지 생성 뷰
@login_required
def challenge_create(request):
    if request.method == "POST":
        form = ChallengeForm(request.POST)
        if form.is_valid():
            challenge = form.save(commit=False)
            challenge.leader = request.user
            challenge.current_member = 1
            challenge.save()

            # 방장도 참여자에 포함
            challenge.members.add(request.user)
            messages.success(request, "챌린지가 생성되었습니다")
            return redirect("challenge_detail", pk=challenge.pk)
    else:
        form = ChallengeForm()

    return render(
        request,
        "challenge/challenge_form.html",
        {
            "form": form,
        },
    )


@login_required
def challenge_join(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk)

    # 이미 참여중이면 막기
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

    # 👉 챌린지 참가자만 인증하게 하고 싶다면
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
        {
            "challenge": challenge,
            "form": form,
        },
    )
