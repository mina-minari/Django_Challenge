from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Challenge


class UserProfileSerializer(serializers.ModelSerializer):
    # User 모델에서 username 끌어오기 (UserProfile에는 username 필드가 없음)
    username = serializers.CharField(source="user.username", read_only=True)

    # 모델 필드가 아니라, 계산해서 넣어주는 값
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
        return user.joined_challenges.count()


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
            "max_participants",
            "is_group",
            "created_at",
            "participants_count",
            "progress",
            "is_full",
        )

    def _get_capacity_and_count(self, obj):
        if obj.is_group:
            capacity = obj.max_participants
            participants_count = obj.participants.count()
        else:
            # 1인 챌린지: 방장 혼자 진행 -> 항상 1/1
            capacity = 1
            participants_count = 1
        return capacity, participants_count

    def get_participants_count(self, obj):
        capacity, participants_count = self._get_capacity_and_count(obj)
        return participants_count

    def get_progress(self, obj):
        # progress = 현재 인원 / 정원 * 100
        capacity, participants_count = self._get_capacity_and_count(obj)
        if capacity > 0:
            p = int(participants_count / capacity * 100)
            return min(p, 100)
        return 0

    def get_is_full(self, obj):
        capacity, participants_count = self._get_capacity_and_count(obj)
        return participants_count >= capacity
