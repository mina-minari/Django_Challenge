from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Django 기본 User를 확장하는 프로필 정보
    """
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
    """
    챌린지 정보

    - title: 챌린지 제목
    - content: 챌린지 설명
    - current_member: 현재 참여 인원
    - max_member: 최대 참여 가능 인원
    - leader: 챌린지 장 (챌린지 생성자)
    - members: 챌린지 참여자들 (방장 포함)
    - count: 목표 인증 횟수
    - type: 개인 / 단체
    - category: 챌린지 카테고리
    - is_public: 공개 / 비공개
    - challenge_date: 주 몇 일, 특정 날짜 등 일정 표현
    - private_password: 비공개 챌린지 비밀번호
    """

    CHALLENGE_TYPE_CHOICES = [
        ("personal", "개인"),
        ("group", "단체"),
    ]

    title = models.CharField("챌린지 제목", max_length=100)
    content = models.TextField("챌린지 설명")

    current_member = models.PositiveIntegerField("현재 인원", default=1)
    max_member = models.PositiveIntegerField("최대 인원")

    # 개인 / 단체
    type = models.CharField(
        "챌린지 종류(인원)",
        max_length=20,
        choices=CHALLENGE_TYPE_CHOICES,
    )

    # 카테고리 (운동, 공부, 식습관 등)
    category = models.CharField(
        "챌린지 카테고리",
        max_length=50,
        blank=True,
    )

    # 공개 여부
    is_public = models.BooleanField(
        "공개 여부",
        default=True,
    )

    # 주에 몇 일/날짜 등 – 일단 문자열로 저장
    challenge_date = models.CharField(
        "챌린지 일정(요일/날짜)",
        max_length=100,
        blank=True,
    )

    # 비공개 비밀번호 (challenge_public_false_pw)
    private_password = models.CharField(
        "비공개 비밀번호",
        max_length=50,
        blank=True,
    )

    # 방장
    leader = models.ForeignKey(
        User,
        verbose_name="챌린지 장",
        on_delete=models.CASCADE,
        related_name="leading_challenge",
    )

    # 챌린지 참여자들 (방장 포함 가능)
    members = models.ManyToManyField(
        User,
        verbose_name="챌린지 참여자들",
        related_name="joined_challenges",
        blank=True,
    )

    # 목표 인증 횟수
    count = models.PositiveIntegerField("목표 인증 횟수", default=0)

    created_at = models.DateTimeField("생성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Verification(models.Model):
    """
    인증 기록

    - image: 인증 이미지
    - date: 인증 시간
    - verified_member: 인증한 회원
    - challenge: 어떤 챌린지에서 한 인증인지
    """

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
        return f"{self.verified_member.username} - {self.challenge.title} ({self.date.date()})"
