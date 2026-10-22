from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    AnswerExerciseView,
    ChapterListView,
    GenerateExerciseView,
    MeView,
    ProgressView,
    RegisterView,
)

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="auth-register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="auth-login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="auth-refresh"),
    path("auth/me/", MeView.as_view(), name="auth-me"),
    path("chapters/", ChapterListView.as_view(), name="chapter-list"),
    path("exercises/generate/", GenerateExerciseView.as_view(), name="exercise-generate"),
    path("exercises/<int:pk>/answer/", AnswerExerciseView.as_view(), name="exercise-answer"),
    path("progress/", ProgressView.as_view(), name="progress"),
]
