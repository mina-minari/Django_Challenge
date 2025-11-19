from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=150)
    profile_image = models.URLField()
    challenge_point=models.IntegerField(default=0)
    #challenge=models.ManyToManyField()
    #username=email로 사용
    def __str__(self):
        return self.username