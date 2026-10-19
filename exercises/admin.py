from django.contrib import admin

from .models import Attempt, Chapter, Exercise


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "order", "slug")
    list_filter = ("level",)


admin.site.register(Exercise)
admin.site.register(Attempt)