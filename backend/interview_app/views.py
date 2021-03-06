from django.http import response
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django_filters import rest_framework as filters

from .filters import InterviewFilter
from .permissions import IsInterviewer
from .models import Interview, InterviewResult
from .serializers import (
    InterviewSerializer,
    InterviewDetailSerializer,
    AnswerSerializer, 
    AnswerCreateSerializer,
    InterviewResultsSerializer,
)


class InterviewsViewSet(viewsets.ReadOnlyModelViewSet):            
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
    permission_classes = [IsAuthenticated, IsInterviewer]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = InterviewFilter

    def get_queryset(self):
        if self.request.user.id:
            return self.queryset.filter(interviewer = self.request.user)

    def get_serializer_class(self):
        serializer = InterviewDetailSerializer
        if self.action == 'list':
            serializer = InterviewSerializer
        elif self.action == 'answer':
            serializer = AnswerSerializer
        elif self.action == 'results':
            serializer = InterviewResultsSerializer
        return serializer

    @swagger_auto_schema(request_body=AnswerCreateSerializer)
    @action(methods=['POST'], detail=True)
    def answer(self, request, pk):
        serializer = self.get_serializer_class()(
            data = {**request.data, 'interview': pk}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=200)

    @action(methods=['GET'], detail=True)
    def results(self, request, pk):
        interview = Interview.objects.get(pk=pk)
        answers = interview.answers.all()
        result = InterviewResult(answers)
        serializer = InterviewResultsSerializer(
            result
        )
        return Response(data=serializer.data, status=200)