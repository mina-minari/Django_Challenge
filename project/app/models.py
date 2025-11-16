from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    #profile_image = models.ImageField()
    challenge_point=models.IntegerField(default=0)
    #challenge=models.ManyToManyField()

    def __str__(self):
        return self.username