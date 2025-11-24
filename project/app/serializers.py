from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Challenge, Verification


class MyChallengeSerializer(serializers.ModelSerializer):
    participants_count = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()
    is_full = serializers.SerializerMethodField()

    class Meta:
        model = Challenge
        fields = (
            "id",
            "title",
            "content",
            "max_member",        # 정원
            "type",              # personal / group
            "category",
            "is_public",
            "challenge_date",
            "participants_count",
            "progress",
            "is_full",
        )

    def _get_capacity_and_count(self, obj):
        # 정원과 현재 인원 계산 (members M2M 기반)
        capacity = obj.max_member or 0
        participants_count = obj.members.count()
        return capacity, participants_count

    def get_participants_count(self, obj):
        _, participants_count = self._get_capacity_and_count(obj)
        return participants_count

    def get_progress(self, obj):
        # progress = 현재 인원 / 정원 * 100
        capacity, participants_count = self._get_capacity_and_count(obj)
        if capacity <= 0:
            return 0
        p = int(participants_count / capacity * 100)
        return min(p, 100)

    def get_is_full(self, obj):
        capacity, participants_count = self._get_capacity_and_count(obj)
        return capacity > 0 and participants_count >= capacity

class VerificationSerializer(serializers.ModelSerializer):
    challenge_title = serializers.CharField(source="challenge.title", read_only=True)

    class Meta:
        model = Verification
        fields = (
            "id",
            "image",
            "date",
            "challenge",       # FK id
            "challenge_title", 
        )
        read_only_fields = ("id", "date", "challenge_title")


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")

    participating_count = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "username",
            "profile_image",
            "bio",
            "participating_count",
        )

    def get_participating_count(self, obj):
        user = obj.user
        return user.joined_challenges.distinct().count()

    def update(self, instance, validated_data):

        # user.username 업데이트
        user_data = validated_data.pop("user", None)
        if user_data:
            new_username = user_data.get("username")
            if new_username:
                instance.user.username = new_username
                instance.user.save()

        # profile_image, bio 등은 기본 업데이트
        return super().update(instance, validated_data)
