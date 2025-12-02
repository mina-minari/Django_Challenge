from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout

## models와 form 가져오기
from .models import Challenge, Verification
from .forms import ChallengeForm, VerificationForm, SignUpForm

# 챌린지 목록
def challenge_list(request):
    challenges = Challenge.objects.all()
    return render(request, 'challenge/challenge_list.html', {
        'challenges': challenges,
    })

# 챌린지 상세
def challenge_detail(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk)
    verifications = challenge.verifications.select_related('verified_member')

    return render(request, 'challenge/challenge_detail.html', {
        'challenge': challenge,
        'verifications': verifications,
    })

# 챌린지 생성 뷰
@login_required
def challenge_create(request):
    if request.method == 'POST':
        form = ChallengeForm(request.POST)
        if form.is_valid():
            challenge = form.save(commit=False)
            challenge.leader = request.user
            challenge.current_member = 1
            challenge.save()

            # 방장도 참여자에 포함
            challenge.members.add(request.user)
            messages.success(request, '챌린지가 생성되었습니다')
            return redirect('challenge_detail', pk=challenge.pk)
    else:
        form = ChallengeForm()

    return render(request, 'challenge/challenge_form.html', {
        'form': form,
    })

@login_required
def challenge_join(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk)

    # 이미 참여중이면 막기
    if challenge.members.filter(id=request.user.id).exists():
        messages.info(request, '해당 챌린지에 참여중입니다.')
        return redirect('challenge_detail', pk=pk)
    
    challenge.members.add(request.user)
    challenge.current_member = challenge.members.count()
    challenge.save(update_fields=['current_member'])

    messages.succes(request, '챌린지에 참여했습니다.')
    return redirect('challenge_detail', pk=pk)

@login_required
def verification_create(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk)

    # 👉 챌린지 참가자만 인증하게 하고 싶다면
    if not challenge.members.filter(id=request.user.id).exists():
        messages.error(request, '이 챌린지에 참여 중인 회원만 인증할 수 있습니다.')
        return redirect('challenge_detail', pk=pk)

    if request.method == 'POST':
        form = VerificationForm(request.POST, request.FILES)
        if form.is_valid():
            verification = form.save(commit=False)
            verification.verified_member = request.user
            verification.challenge = challenge
            verification.save()

            messages.success(request, '인증이 완료되었습니다!')
            return redirect('challenge_detail', pk=pk)
    else:
        form = VerificationForm()

    return render(request, 'challenge/verification_form.html', {
        'challenge': challenge,
        'form': form,
    })

def signup(request):
    """
    아주 간단한 회원가입 페이지
    - 아이디, 비밀번호만 입력받아서 User 생성
    - 회원가입 후 자동 로그인 시키고 챌린지 목록으로 이동
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)               # 자동 로그인
            messages.success(request, '회원가입이 완료되었습니다.')
            return redirect('challenge_list')  # 챌린지 목록으로 이동
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {
        'form': form,
    })

def logout_view(request):
    """
    GET으로도 호출 가능한 간단 로그아웃 뷰
    - 세션에서 유저 로그아웃
    - 로그인 페이지로 리다이렉트
    """
    logout(request)
    return redirect('login')