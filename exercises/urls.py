from django.urls import path
from .views import AnswerExerciseView, ChapterListView, GenerateExerciseView
from django.urls import path




urlpatterns = [
    path("chapters/", ChapterListView.as_view(), name="chapter-list"),
    path("exercises/generate/", GenerateExerciseView.as_view(), name="exercise-generate"),
    path("exercises/<int:pk>/answer/", AnswerExerciseView.as_view(), name="exercise-answer"),






]