from django.shortcuts import render,redirect

# Create your views here.
def index(request):
    return render(request, 'app/login.html')
def google_login(request):
    params={
        'client_id': 
    }
    auth_url="https://accounts.google.com/o/oauth2/v2/auth?client_id:"192516169686-pirpgfr064aukj0nranq46o6spn6rvli.apps.googleusercontent.com"&redirect_uri:"http://localhost:8000/google/callback"&response_type=code&scope=email%20profile%20openid"
    return render(request, 'https://accounts.google.com/o/oauth2/auth')