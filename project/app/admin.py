from django.contrib import admin
from .models import UserProfile, Challenge, Verification


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "profile_image", "bio")


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "leader",        # 방장
        "max_member",    # 최대 인원
        "type",          # personal / group
        "category",
        "is_public",
        "current_member",
        "count",
        "created_at",
    )
    list_filter = (
        "type",
        "category",
        "is_public",
        "created_at",
    )
    search_fields = (
        "title",
        "content",
        "leader__username",
    )


@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "verified_member",   # 인증한 사람
        "challenge",
        "date",
        "image",
    )
    list_filter = (
        "date",
        "challenge",
        "verified_member",
    )
    search_fields = (
        "verified_member__username",
        "challenge__title",
    )
