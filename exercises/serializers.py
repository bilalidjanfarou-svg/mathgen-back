from rest_framework import serializers

from .models import Chapter


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ["id", "name", "level"]



from .models import Chapter, Exercise


class GenerateRequestSerializer(serializers.Serializer):
    chapter_id = serializers.PrimaryKeyRelatedField(
        queryset=Chapter.objects.all(), source="chapter"
    )
    difficulty = serializers.IntegerField(min_value=1, max_value=3, default=1)


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ["id", "statement_latex", "answer_type", "hint"]