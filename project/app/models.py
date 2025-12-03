from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=150)
    nickname= models.CharField(max_length=150,unique=True,null=True)
    profile_image = models.URLField()
    challenge_point=models.IntegerField(default=0)
    #challenge=models.ManyToManyField()
    #username=email로 사용
    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    profile_image = models.CharField(max_length=255, blank=True)
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

    category = models.CharField(
        "챌린지 카테고리",
        max_length=50,
        blank=True,
    )

    is_public = models.BooleanField(
        "공개 여부",
        default=True,
    )

    challenge_date = models.CharField(
        "챌린지 일정(요일/날짜)",
        max_length=100,
        blank=True,
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

    created_at = models.DateTimeField("생성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

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
        null=True,
        blank=True,
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
