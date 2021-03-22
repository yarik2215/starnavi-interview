from django.contrib import admin

from .models import (
    Answer,
    Interview,
    Question,
    Candidate,
    Position,
    PositionQuestions,
    Category,
    Theme,
)


class AnswerInline(admin.StackedInline):
    model = Answer


class InterviewInline(admin.StackedInline):
    model = Interview


class PositionQuestionInline(admin.StackedInline):
    model = PositionQuestions
    extra = 1


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    pass


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [PositionQuestionInline]


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    inlines = [PositionQuestionInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    pass

