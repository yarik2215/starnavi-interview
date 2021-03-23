from django.http import response
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from .permissions import IsInterviewer
from .models import Interview
from .serializers import (
    InterviewSerializer,
    InterviewDetailSerializer,
    AnswerDetailSerializer, 
    AnswerCreateSerializer,
)

class InterviewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Interview.objects.filter(state=Interview.State.SCHEDULED)
    serializer_class = InterviewSerializer
    permission_classes = [IsAuthenticated, IsInterviewer]

    def get_queryset(self):
        return self.queryset.filter(interviewer = self.request.user)

    def get_serializer_class(self):
        serializer = InterviewDetailSerializer
        if self.action == 'list':
            serializer = InterviewSerializer
        elif self.action == 'answer':
            serializer = AnswerDetailSerializer
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


