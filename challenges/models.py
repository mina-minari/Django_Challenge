from django.db import models
from django.conf import settings

class Challenge(models.Model):
    # [챌린지 제목
    title = models.CharField(max_length=200, verbose_name="제목")
    
    # 챌린지 내용
    content = models.TextField(verbose_name="내용")
    
    # 최대 회원 수
    max_members = models.IntegerField(default=10, verbose_name="최대 인원")
    
    # 기간 
    start_date = models.DateField(verbose_name="시작일")
    end_date = models.DateField(verbose_name="종료일")

    # 방장
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="created_challenges"
    )

    # Member
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name="joined_challenges",
        blank=True
    )
    
    # 썸네일
    image = models.ImageField(upload_to="challenge_thumbs/", blank=True, null=True)

    # 카테고리
    CATEGORY_CHOICES = [
        ('study', '학습'),
        ('workout', '운동/건강'),
        ('reading', '독서/기록'),
        ('habit', '생활습관'),
        ('hobby', '취미/창작'),
        ('mind', '멘탈'),
    ]
    
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES, 
        default='coding', 
        verbose_name="카테고리"
    )