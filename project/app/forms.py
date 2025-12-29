from django import forms
from .models import UserProfile, Challenge, Verification


class NicknameForm(forms.Form):
    nickname = forms.CharField(max_length=150, label="Nickname", required=True)


class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ["title", "content", "max_member", "count", "type"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "챌린지 제목을 입력하세요",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "어떤 챌린지인지 설명을 적어주세요",
                }
            ),
            "max_member": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                }
            ),
            "count": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                }
            ),
            "type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }


class VerificationForm(forms.ModelForm):
    class Meta:
        model = Verification
        fields = ["image"]
        widgets = {
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }


class ProfileForm(forms.ModelForm):
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

    remove_profile_image = forms.BooleanField(
        required=False,
        label="현재 프로필 이미지 삭제",
    )

    class Meta:
        model = UserProfile
        fields = ("profile_image", "bio")
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
        self.fields["username"].initial = user.username

    def save(self, commit=True):
        profile = super().save(commit=False)

        self.user.username = self.cleaned_data["username"]

        if self.cleaned_data.get("remove_profile_image"):
            profile.profile_image = None

        if commit:
            self.user.save()
            profile.user = self.user
            profile.save()

        return profile
