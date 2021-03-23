from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


interview_router = DefaultRouter()
interview_router.register(r'interviews', views.InterviewsViewSet)

# questions_router = DefaultRouter()
# questions_router.register(r'questions', views.QuestionsViewSet)

appname = 'interview_app'

urlpatterns = [
    path('', include(interview_router.urls)),
    # path('interviews/<int:interview_id>/questions', include(questions_router.urls)),
]