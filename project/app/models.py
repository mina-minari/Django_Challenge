from django.db import models
from django.contrib.auth.models import User  # Django 기본 유저 모델


class UserProfile(models.Model):
    user = models.OneToOneField( # Django 기본 User 확장
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    profile_image = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
    
class Challenge(models.Model):
    # current_participants, is_full은 계산으로 구함
    title = models.CharField(max_length=200)
    content = models.TextField()
    max_participants = models.PositiveIntegerField()  # 정원
    is_group = models.BooleanField(default=True)      # 그룹 vs 1인 챌린지

    master = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_challenges",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ChallengeParticipant(models.Model):
    # 어떤 유저가 어떤 챌린지에 참여 중인지 나타내는 중간 테이블 (N:M 관계)
    challenge = models.ForeignKey(
        Challenge,
        on_delete=models.CASCADE,
        related_name="participants",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="joined_challenges",
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("challenge", "user")  # 같은 유저가 같은 챌린지 2번 참여 금지

    def __str__(self):
        return f"{self.user.username} in {self.challenge.title}"


class Verification(models.Model):
    # 어떤 유저가 어떤 챌린지에서 언제 어떤 이미지를 올렸는지
    image = models.CharField(max_length=255)  # 나중에 ImageField로 교체 가능
    date = models.DateField()

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="verifications",
    )
    challenge = models.ForeignKey(
        Challenge,
        on_delete=models.CASCADE,
        related_name="verifications",
    )

    def __str__(self):
        return f"{self.user.username} - {self.challenge.title} ({self.date})"
