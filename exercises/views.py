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
from django.shortcuts import get_object_or_404

from .checking import check_answer
from .models import Attempt, Exercise
from .serializers import AnswerRequestSerializer








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

class AnswerExerciseView(APIView):
    def post(self, request, pk):
        exercise = get_object_or_404(Exercise, pk=pk)
        payload = AnswerRequestSerializer(data=request.data)
        payload.is_valid(raise_exception=True)

        if exercise.attempts.exists():
            return Response(
                {"detail": "Cet exercice a déjà reçu une réponse."},
                status=status.HTTP_409_CONFLICT,
            )

        answer = payload.validated_data["answer"]
        correct = check_answer(exercise.answer_type, exercise.expected, answer)
        user = request.user if request.user.is_authenticated else None
        Attempt.objects.create(
            exercise=exercise, user=user, answer=answer, is_correct=correct
        )
        return Response(
            {"correct": correct, "explanation_latex": exercise.explanation_latex}
        )










