# app/forms.py
from django import forms
from django.contrib.auth.models import User
from django.forms import ClearableFileInput
from .models import UserProfile


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

    # 프로필 이미지 삭제 여부 체크박스 (모델 필드 X, 폼용 필드)
    remove_profile_image = forms.BooleanField(
        required=False,
        label="현재 프로필 이미지 삭제",
    )

    class Meta:
        model = UserProfile
        fields = ("profile_image", "bio")  # 모델 필드만 적어두면 됨
        widgets = {
            "profile_image": forms.FileInput(
                attrs={
                    "class": "form-input",
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
        profile = super().save(commit=False)

        # User.username 업데이트
        self.user.username = self.cleaned_data["username"]

        # 삭제 체크되어 있으면 이미지 필드 비우기
        if self.cleaned_data.get("remove_profile_image"):
            # DB 필드만 비우는 버전 (파일까지 지우려면 delete(save=False) 쓰면 됨)
            profile.profile_image = None

        if commit:
            self.user.save()
            profile.user = self.user  # 혹시 비어 있으면 연결
            profile.save()

        return profile
