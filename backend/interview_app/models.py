from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator


class Candidate(models.Model):
    email = models.EmailField(
        max_length = 255,
        unique = True,
        db_index = True,
    )
    first_name = models.CharField(
        _('first name'),
        max_length = 255
    )
    last_name = models.CharField(
        _('last name'),
        max_length = 255
    )
    phone = models.CharField(
        max_length = 15,
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Category(models.Model):
    name = models.CharField(
        _('category name'),
        max_length = 255,
    )

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
        return self.name


class Theme(models.Model):
    name = models.CharField(
        _('theme name'),
        max_length = 255,
    )
    category = models.ForeignKey(
        Category,
        on_delete = models.CASCADE,
        related_name = 'themes',
        help_text = _(
            'themes for specific category'
        )
    )

    def __str__(self) -> str:
        return self.name


class Question(models.Model):
    text = models.TextField(
        _('text')
    )
    additional_info = models.TextField(
        _('additional info'),
        blank = True,
        null = True
    )
    category = models.ForeignKey(
        Category,
        verbose_name = _('category'),
        on_delete = models.PROTECT,
        help_text = _(
            'question category'
        )
    )
    theme = models.ForeignKey(
        Theme,
        verbose_name = _('theme'),
        on_delete = models.SET_NULL,
        help_text = _(
            'question theme'
        ),
        null = True,
        blank = True,
    )

    def __str__(self) -> str:
        return self.text
    
    class Meta:
        ordering = ['category', 'theme']


class Position(models.Model):
    name = models.CharField(
        _('position name'),
        max_length = 255,
        unique = True,
    )
    description = models.TextField(
        _('description'),
        blank = True,
        null = True,
    )
    questions = models.ManyToManyField(
        Question,
        through = 'PositionQuestions'
    )

    def __str__(self) -> str:
        return self.name


class PositionQuestions(models.Model):
    position = models.ForeignKey(
        Position,
        on_delete = models.CASCADE,
        related_name = 'position_questions',
    )
    question = models.ForeignKey(
        Question,
        on_delete = models.CASCADE,
        related_name = 'position_questions',
    )
    is_required = models.BooleanField(
        _('is required'),
        default = True,
        help_text = _(
            'Show is this message required or not'
        )
    )


class Interview(models.Model):
    class State(models.TextChoices):
        CANCELED = 'canceled'
        SCHEDULED = 'scheduled'
        WAITING = 'waiting'
        PASSED = 'passed'
        FAILED = 'failed'

    State.CANCELED.name
    
    candidate = models.ForeignKey(
        Candidate,
        on_delete = models.CASCADE,
        related_name = 'interviews',
        verbose_name = _('candidate'),
    )
    interviewer = models.ForeignKey(
        get_user_model(),
        on_delete = models.CASCADE,
        related_name = 'interviews',
        verbose_name = _('interviewer'),
    )
    date = models.DateTimeField(
        _('interview date'),
        help_text=_(
            'Interview date and time'
        )
    )
    state = models.CharField(
        _('interview state'),
        max_length = 255,
        choices = State.choices,
        default = State.SCHEDULED,
    )
    position = models.ForeignKey(
        Position,
        on_delete = models.CASCADE,
        related_name = 'interviews',
        verbose_name = _('position'),
    )


class Answer(models.Model):
    interview = models.ForeignKey(
        Interview,
        on_delete = models.CASCADE,
        verbose_name=_(
            'interview'
        ),
        related_name = 'answers',
    )
    question = models.ForeignKey(
        Question,
        on_delete = models.CASCADE,
        verbose_name=_(
            'question'
        ),
        related_name = 'answers',
    )
    mark = models.IntegerField(
        _('mark'),
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ],
        help_text = _(
            'mark in range 0 - 10'
        )
    )
    comment = models.TextField(
        _('comment to answer'),
        blank = True,
        null = True,
    )

    class Meta:
        unique_together = ['question', 'interview'] 


class InterviewResult:
    def __init__(self, answers) -> None:
        self.answers = answers
        self.total_mark = sum([a.mark for a in answers])