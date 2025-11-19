from django.contrib import admin
from .models import UserProfile, Challenge, ChallengeParticipant, Verification


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "profile_image", "bio")


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "master", "max_participants", "is_group", "created_at")
    list_filter = ("is_group", "created_at")
    search_fields = ("title", "content")


@admin.register(ChallengeParticipant)
class ChallengeParticipantAdmin(admin.ModelAdmin):
    list_display = ("id", "challenge", "user", "joined_at")
    list_filter = ("challenge", "user")


@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "challenge", "date", "image")
    list_filter = ("date", "challenge", "user")