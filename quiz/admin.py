from django.contrib import admin
from .models import Topic, Question, QuizResult

admin.site.register(Topic)
admin.site.register(Question)

@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ["user", "topic", "correct", "wrong", "total", "score", "date"]
    list_filter = ["topic", "user"]
    search_fields = ["user__username", "topic__name"]
    ordering = ["-date"]
