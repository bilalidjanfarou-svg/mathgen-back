from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Chapter, Exercise

User = get_user_model()


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ["id", "name", "level"]


class GenerateRequestSerializer(serializers.Serializer):
    chapter_id = serializers.PrimaryKeyRelatedField(queryset=Chapter.objects.all(), source="chapter")
    difficulty = serializers.IntegerField(min_value=1, max_value=3, default=1)


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ["id", "statement_latex", "answer_type", "hint"]


class AnswerRequestSerializer(serializers.Serializer):
    answer = serializers.CharField(max_length=100)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
