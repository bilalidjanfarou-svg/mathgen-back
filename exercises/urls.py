from django.urls import path

from .views import ChapterListView
from django.urls import path

from .views import ChapterListView, GenerateExerciseView


urlpatterns = [
    path("chapters/", ChapterListView.as_view(), name="chapter-list"),
    path("exercises/generate/", GenerateExerciseView.as_view(), name="exercise-generate"),
]