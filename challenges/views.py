from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Challenge, Comment

def challenge_list(request):
    
    challenges = Challenge.objects.all().order_by('-id')
    
    context = {
        'challenges': challenges
    }
    
    return render(request, 'challenges/challenge_list.html', context)


def challenge_detail(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk)
    
    if request.method == 'POST':
   
        if not request.user.is_authenticated:
            return redirect('login') 
            
        content = request.POST.get('content') 
        if content:
            Comment.objects.create(
                challenge=challenge,
                user=request.user,
                content=content
            )
        return redirect('challenges:detail', pk=challenge.pk) 

 
    context = {
        'challenge': challenge,
        'comments': challenge.comments.all().order_by('-created_at') 
    }
    return render(request, 'challenges/challenge_detail.html', context)