from django.db import models
from django.contrib.auth.models import User # 회원가입/로그인/비밀번호 암호화를 처리해주는 인증 django내 인증앱

class Challenge(models.Model):
    """

    챌린지 정보
    - title: 챌린지 제목
    - content: 챌린지 설명
    - current_member: 현재 참여 인원
    - max_member: 최대 참여 가능 인원
    - leader: 챌린지 장 (챌린지 생성자)
    - members: 챌린지 참여자들
    - count: 목표 인증 횟수
    - type: 개인 / 단체

    """

    CHALLENGE_TYPE_CHOICES = [
        ('personal', '개인'),
        ('group', '단체'),
    ]

    title = models.CharField("챌린지", max_length=100)
    content = models.CharField("설명")
    current_member = models.PositiveIntegerField("현재 인원", default=1)
    max_member = models.PositiveIntegerField("최대 인원")
    
    leader = models.ForeignKey(
        User,
        verbose_name = "챌린지 장",
        on_delete = models.CASCADE,
        related_name ='leading_challenge',
    )

    # 챌린지 참여자들 (방장도 포함)
    members = models.ManyToManyField(
        User,
        verbose_name = "챌린지 참여자들",
        related_name = "joined_challenges",
        blank = True,
    )

    count = models.PositiveIntegerField("목표 인증 횟수", default = 0)

    # 개인 / 팀원
    type = models.CharField(
        "챌린지 종류(인원)",
        max_length = 20,
        chocies = CHALLENGE_TYPE_CHOICES,
    )

    created_at = models.DateTimeField("생성일", auto_now_add = True)
    updated_at = models.DateTimeField("수정일", auto_now = True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    

class Verification(models.Model):
    """
    
    인증 기록
    - image: 인증 이미지
    - date: 인증 시간
    - verified_member : 인증한 회원
    - challenge: 어떤 챌린지에서 한 인증인지
    
    """
    
    image = models.ImageField("인증 이미지", upload_to = 'verifications/')
    date = models.DateTimeField("인증 일시", auto_now_add = True)

    verified_member = models.ForeignKey(
        User,
        verbose_name = "인증한 사람",
        on_delete = models.CASCADE,
        related_name = 'verifications',
    )

    challenge = models.ForeignKey(
        Challenge,
        verbose_name = "챌린지",
        on_delete = models.CASCADE,
        related_name = 'verifications', 
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.member.username} - {self.challenge.title} ({self.date.date()})"