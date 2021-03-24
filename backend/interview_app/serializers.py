from rest_framework import serializers

from .models import (
    Interview,
    Position,
    PositionQuestions,
    Question,
    Theme,
    Category,
    Candidate,
    Answer,
)


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = '__all__'


class AnswerCreateSerializer(AnswerSerializer):

    class Meta:
        model = Answer
        exclude = ['interview']



class AnswerDetailSerializer(AnswerSerializer):
    question = serializers.CharField(source='question.text')

    class Meta:
        model = Answer
        fields = ['question', 'mark', 'comment']


class InterviewResultsSerializer(serializers.Serializer):
    answers = AnswerDetailSerializer(many = True, read_only=True)
    total_mark = serializers.IntegerField(read_only=True)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['name',]


class ThemeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Theme
        fields = ['name',]


class CandidateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Candidate
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    theme = ThemeSerializer()

    class Meta:
        model = Question
        fields = '__all__'


class PositionQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = PositionQuestions
        fields = ['is_required', 'question']


class PositionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Position
        fields = ['id', 'name']


class PositionDetailSerializer(serializers.ModelSerializer):
    questions = PositionQuestionSerializer(source = 'position_questions', many = True)

    class Meta:
        model = Position
        fields = ['id', 'name', 'questions']


class InterviewSerializer(serializers.ModelSerializer):
    position = PositionListSerializer()
    candidate = CandidateSerializer()

    class Meta:
        model = Interview
        fields = '__all__'


class InterviewDetailSerializer(InterviewSerializer):
    position = PositionDetailSerializer()
