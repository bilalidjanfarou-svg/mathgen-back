from django.shortcuts import render

from rest_framework.generics import ListAPIView

from .models import Chapter
from .serializers import ChapterSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .generators import generate
from .models import Exercise
from .serializers import ExerciseSerializer, GenerateRequestSerializer




class ChapterListView(ListAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    pagination_class = None


class GenerateExerciseView(APIView):
    def post(self, request):
        params = GenerateRequestSerializer(data=request.data)
        params.is_valid(raise_exception=True)
        chapter = params.validated_data["chapter"]
        difficulty = params.validated_data["difficulty"]

        try:
            data = generate(chapter.slug, difficulty)
        except KeyError:
            return Response(
                {"detail": "Aucun générateur pour ce chapitre."},
                status=status.HTTP_501_NOT_IMPLEMENTED,
            )

        user = request.user if request.user.is_authenticated else None
        exercise = Exercise.objects.create(
            chapter=chapter, difficulty=difficulty, user=user, **data
        )
        return Response(ExerciseSerializer(exercise).data, status=status.HTTP_201_CREATED)
