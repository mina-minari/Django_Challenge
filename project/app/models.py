from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=150)
    nickname = models.CharField(max_length=150, unique=True, null=True)
    profile_image = models.URLField(blank=True, null=True)
    challenge_point = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
    )
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


class Challenge(models.Model):
    CHALLENGE_TYPE_CHOICES = [
        ("personal", "개인"),
        ("group", "단체"),
    ]

    title = models.CharField("챌린지 제목", max_length=100)
    content = models.TextField("챌린지 설명")

    current_member = models.PositiveIntegerField("현재 인원", default=1)
    max_member = models.PositiveIntegerField("최대 인원", default=1)

    type = models.CharField(
        "챌린지 종류(인원)",
        max_length=20,
        choices=CHALLENGE_TYPE_CHOICES,
        default="group",
    )

    CATEGORY_CHOICES = [
        ("study", "학습"),
        ("workout", "운동/건강"),
        ("reading", "독서/기록"),
        ("habit", "생활습관"),
        ("hobby", "취미/창작"),
        ("mind", "멘탈"),
    ]

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="study",
        verbose_name="카테고리",
    )

    is_public = models.BooleanField(
        "공개 여부",
        default=True,
    )

    private_password = models.CharField(
        "비공개 비밀번호",
        max_length=50,
        blank=True,
    )

    leader = models.ForeignKey(
        User,
        verbose_name="챌린지 장",
        on_delete=models.CASCADE,
        related_name="leading_challenge",
        null=True,
        blank=True,
    )

    members = models.ManyToManyField(
        User,
        verbose_name="챌린지 참여자들",
        related_name="joined_challenges",
        blank=True,
    )

    count = models.PositiveIntegerField("목표 인증 횟수", default=0)
    start_date = models.DateField("시작일", null=True, blank=True)
    end_date = models.DateField("종료일", null=True, blank=True)
    created_at = models.DateTimeField("생성일", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Verification(models.Model):
    image = models.ImageField("인증 이미지", upload_to="verifications/")
    date = models.DateTimeField("인증 일시", auto_now_add=True)

    verified_member = models.ForeignKey(
        User,
        verbose_name="인증한 사람",
        on_delete=models.CASCADE,
        related_name="verifications",
    )

    challenge = models.ForeignKey(
        Challenge,
        verbose_name="챌린지",
        on_delete=models.CASCADE,
        related_name="verifications",
    )

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.verified_member.username if self.verified_member else 'Unknown'} - {self.challenge.title} ({self.date.date()})"


class Comment(models.Model):
    challenge = models.ForeignKey(
        Challenge, related_name="comments", on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="응원의 한마디")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.content}"
