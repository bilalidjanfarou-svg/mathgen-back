from django.db.models import Count, F, Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .checking import check_answer
from .generators import generate
from .models import Attempt, Chapter, Exercise
from .serializers import (
    AnswerRequestSerializer,
    ChapterSerializer,
    ExerciseSerializer,
    GenerateRequestSerializer,
    RegisterSerializer,
)


class ChapterListView(ListAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    pagination_class = None
    authentication_classes = []
    permission_classes = [AllowAny]


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {"access": str(refresh.access_token), "refresh": str(refresh)},
            status=status.HTTP_201_CREATED,
        )


class MeView(APIView):
    def get(self, request):
        return Response({"id": request.user.id, "username": request.user.username})


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

        exercise = Exercise.objects.create(
            chapter=chapter, difficulty=difficulty, user=request.user, **data
        )
        return Response(ExerciseSerializer(exercise).data, status=status.HTTP_201_CREATED)


class AnswerExerciseView(APIView):
    def post(self, request, pk):
        exercise = get_object_or_404(Exercise, pk=pk, user=request.user)
        payload = AnswerRequestSerializer(data=request.data)
        payload.is_valid(raise_exception=True)

        if exercise.attempts.exists():
            return Response(
                {"detail": "Cet exercice a déjà reçu une réponse."},
                status=status.HTTP_409_CONFLICT,
            )

        answer = payload.validated_data["answer"]
        correct = check_answer(exercise.answer_type, exercise.expected, answer)
        Attempt.objects.create(
            exercise=exercise, user=request.user, answer=answer, is_correct=correct
        )
        return Response({"correct": correct, "explanation_latex": exercise.explanation_latex})


class ProgressView(APIView):
    def get(self, request):
        rows = (
            Attempt.objects.filter(user=request.user)
            .values(chapter_id=F("exercise__chapter_id"))
            .annotate(
                attempts=Count("id"),
                correct=Count("id", filter=Q(is_correct=True)),
            )
            .order_by("chapter_id")
        )
        data = [
            {
                "chapter_id": r["chapter_id"],
                "attempts": r["attempts"],
                "correct": r["correct"],
                "success_rate": r["correct"] / r["attempts"],
            }
            for r in rows
        ]
        return Response(data)
