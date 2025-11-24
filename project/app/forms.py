# app/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class ProfileForm(forms.ModelForm):
    # User 모델의 username도 같이 수정할 수 있게
    username = forms.CharField(
        max_length=150,
        label="Username",
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": "닉네임을 입력하세요",
            }
        ),
    )

    class Meta:
        model = UserProfile
        fields = ("profile_image", "bio")
        widgets = {
            "profile_image": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "프로필 이미지 URL 또는 경로",
                }
            ),
            "bio": forms.Textarea(
                attrs={
                    "class": "form-textarea",
                    "rows": 3,
                    "placeholder": "간단한 소개를 적어주세요.",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.user = user
        # 폼 처음 열 때 username 초기값 세팅
        self.fields["username"].initial = user.username

    def save(self, commit=True):
        # UserProfile(프로필) 먼저 저장 준비
        profile = super().save(commit=False)

        # User.username 업데이트
        self.user.username = self.cleaned_data["username"]

        if commit:
            self.user.save()
            profile.user = self.user  # 혹시 비어 있으면 연결
            profile.save()

        return profile
