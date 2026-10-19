from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Level(models.TextChoices):
    SECONDE = "2nde", "Seconde"
    PREMIERE = "1ère", "Première"
    TERMINALE = "Tle", "Terminale"


class AnswerType(models.TextChoices):
    NUMBER = "number", "Nombre ou fraction"
    INTERVAL = "interval", "Intervalle"
    SET = "set", "Ensemble de solutions"
    VECTOR = "vector", "Vecteur"
    EXPRESSION = "expression", "Expression"


class Chapter(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)  # clé pour trouver le générateur
    level = models.CharField(max_length=10, choices=Level.choices)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.name} ({self.level})"


class Exercise(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="exercises")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="exercises",
    )
    difficulty = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(3)]
    )
    statement_latex = models.TextField()
    answer_type = models.CharField(max_length=20, choices=AnswerType.choices)
    hint = models.CharField(max_length=255, blank=True)
    expected = models.JSONField()  # jamais renvoyé avant la réponse
    explanation_latex = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"#{self.pk} {self.chapter.name} (niveau {self.difficulty})"


class Attempt(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="attempts")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="attempts",
    )
    answer = models.CharField(max_length=255)
    is_correct = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Exercice {self.exercise_id} : {'juste' if self.is_correct else 'faux'}"