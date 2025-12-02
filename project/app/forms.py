from django import forms


class NicknameForm(forms.Form):
    nickname = forms.CharField(max_length=150, label="Nickname", required=True)
from .models import Challenge, Verification
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# 챌린지 생성폼
class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ['title', 'content', 'max_member', 'count', 'type']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '챌린지 제목을 입력하세요',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '어떤 챌린지인지 설명을 적어주세요',
            }),
            'max_member': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
            }),
            'count': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
            }),
            'type': forms.Select(attrs={
                'class': 'form-select',
            }),
        }


class VerificationForm(forms.ModelForm):
    class Meta:
        model = Verification
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }

# 임시 회원가입 폼 // 나중에 시우님 구글 아이디폼 연동
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
