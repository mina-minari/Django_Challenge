from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count

from .models import Challenge, Verification
## form 부분도 import 해야함

# Create your views here.

def challenge_list(request):
    """
    생성된 챌린지 전체 목록 보기 (READ)
    """
    challenges = Challenge.objects.all().order_by('-created_at')
    return render(request, 'challenge/challenge_list.html', {
        'challenges': challenges,
    })