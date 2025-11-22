from django.shortcuts import render,redirect, HttpResponse
from django.http import JsonResponse
import os
import json
import requests
from .models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout

user=User()
google_user_info_url='https://www.googleapis.com/oauth2/v3/userinfo'
try:
    with open('/workspaces/Django_Challenge/project/app/secret.json', 'r') as f:
        secrets = json.load(f)#딕셔너리 형태
        client_id = secrets['web']['client_id']
        redirect_uri=secrets['web']['redirect_uris'][0]
        google_auth_uri=secrets['web']['auth_uri']
        client_secret=secrets['web']['client_secret']
        token_uri=secrets['web']['token_uri']
except FileNotFoundError:
    raise Exception(f"보안 파일을 찾을 수 없습니다. 경로를 확인하세요.")
except json.JSONDecodeError:
    raise Exception("보안 파일의 JSON 형식이 올바르지 않습니다.")

def index(request):
    return render(request, 'app/login.html')

def google_login(request):
    params={
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': 'openid%20profile%20email',
        'response_type': 'code'
    }
    auth_url=f"{google_auth_uri}?"+"&".join([f"{key}={value}" for key, value in params.items()])#"&".join(['a','b','c']) -> 'a&b&c'
    return redirect(auth_url)
def google_callback(request):
    code=request.GET.get('code')
    if not code:
        return HttpResponse("인증 코드가 제공되지 않았습니다.", status=400)
    token_data={
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    try:
        token_response=requests.post(token_uri, data=token_data)
        token_response.raise_for_status()#HTTP 상태 코드 확인 400~500대면 예외 발생
        access_token=token_response.json().get('access_token')
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"토큰 요청 중 오류가 발생했습니다: {e}", status=500)
    
    try:
        userinfo_res=requests.get(
            google_user_info_url,
            headers={'Authorization': f'Bearer {access_token}'}
        )
        userinfo_res.raise_for_status()
        user_info=userinfo_res.json()
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"사용자 정보 요청 중 오류가 발생했습니다: {e}", status=500)
    profile_image=user_info.get('picture')
    email=user_info.get('email')
    name=user_info.get('name',email)#name이 없거나 none이면 email로 대체
    try:
        user, created =User.objects.get_or_create(
            username=email,
            defaults={'name': name, 'profile_image': profile_image}
        )#사용자가 이름이나 프사를 바꿔도 업데이트 안됨
    except IntegrityError:
        return HttpResponse("데이터베이스 오류가 발생했습니다.", status=500)
    login(request,user)
    return redirect('/')
def user_logout(request):
    logout(request)
    return redirect('/')