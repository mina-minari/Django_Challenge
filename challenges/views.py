from django.shortcuts import render
from .models import Challenge

def challenge_list(request):
    
    challenges = Challenge.objects.all().order_by('-id')
    
    context = {
        'challenges': challenges
    }
    
    return render(request, 'challenges/challenge_list.html', context)