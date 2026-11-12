from datetime import timedelta
from django.db.models import Count, F, Q
from django.db.models.functions import TruncDate
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .checking import UnreadableAnswer, check_answer
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
        try:
            correct = check_answer(exercise.answer_type, exercise.expected, answer)
        except UnreadableAnswer as err:
            # Réponse mal écrite : on la refuse sans l'enregistrer, l'élève peut réessayer.
            return Response({"detail": str(err)}, status=status.HTTP_400_BAD_REQUEST)
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


class HistoryView(APIView):
    def get(self, request):
        try:
            limit = max(1, min(int(request.query_params.get("limit", 30)), 100))
        except ValueError:
            limit = 30
        attempts = (
            Attempt.objects.filter(user=request.user)
            .select_related("exercise__chapter")
            .order_by("-created_at", "-id")[:limit]
        )
        return Response(
            [
                {
                    "id": a.id,
                    "chapter": a.exercise.chapter.name,
                    "level": a.exercise.chapter.level,
                    "difficulty": a.exercise.difficulty,
                    "statement_latex": a.exercise.statement_latex,
                    "answer": a.answer,
                    "is_correct": a.is_correct,
                    "explanation_latex": a.exercise.explanation_latex,
                    "created_at": a.created_at,
                }
                for a in attempts
            ]
        )

class StatsView(APIView):
    """Données du tableau de board de l'élève connecté."""
    def get(self, request):
        attempts = Attempt.objects.filter(user=request.user)

        # Activité par jour (dans le fuseau horaire du projet).
        per_day = {
            row["day"]: row
            for row in attempts.annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(n=Count("id"), ok=Count("id", filter=Q(is_correct=True)))
        }
        today = timezone.localdate()
        last_7_days = []
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            row = per_day.get(day)
            last_7_days.append(
                {
                    "date": day.isoformat(),
                    "attempts": row["n"] if row else 0,
                    "correct": row["ok"] if row else 0,
                }
            )

        # Série : jours consécutifs avec au moins un exercice.
        # Si l'élève n'a encore rien fait aujourd'hui, la série d'hier reste valable.
        day = today if today in per_day else today - timedelta(days=1)
        streak = 0
        while day in per_day:
            streak += 1
            day -= timedelta(days=1)

        # Résultats par chapitre (tous les chapitres, même ceux jamais essayés).
        by_chapter = {
            row["chapter_id"]: row
            for row in attempts.values(chapter_id=F("exercise__chapter_id")).annotate(
                n=Count("id"), ok=Count("id", filter=Q(is_correct=True))
            )
        }
        chapters = []
        for chapter in Chapter.objects.all():
            row = by_chapter.get(chapter.id)
            n, ok = (row["n"], row["ok"]) if row else (0, 0)
            chapters.append(
                {
                    "chapter_id": chapter.id,
                    "name": chapter.name,
                    "level": chapter.level,
                    "attempts": n,
                    "correct": ok,
                    "success_rate": ok / n if n else None,
                }
            )

        total = sum(c["attempts"] for c in chapters)
        correct = sum(c["correct"] for c in chapters)
        return Response(
            {
                "totals": {
                    "attempts": total,
                    "correct": correct,
                    "success_rate": correct / total if total else None,
                },
                "streak_days": streak,
                "today": {
                    "attempts": last_7_days[-1]["attempts"],
                    "correct": last_7_days[-1]["correct"],
                },
                "last_7_days": last_7_days,
                "chapters": chapters,
            }
        )
        
        