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


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0


class PositionQuestionInline(admin.StackedInline):
    model = PositionQuestions
    extra = 1


class ThemeInline(admin.StackedInline):
    model = Theme
    extra = 1


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    pass


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'position',
        'date',
        'state',
        'candidate',
        'interviewer',
    )
    search_fields = ['candidate']
    date_hierarchy = 'date'
    list_filter = ['position', 'interviewer']
    inlines = [AnswerInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [PositionQuestionInline]
    list_display = (
        'text',
        'category',
        'theme'
    )
    list_filter = ['position', 'category', 'theme']
    search_fields = ['text']


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    inlines = [PositionQuestionInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [ThemeInline]



