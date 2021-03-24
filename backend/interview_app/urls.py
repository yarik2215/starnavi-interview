from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


interview_router = DefaultRouter()
interview_router.register(r'interviews', views.InterviewsViewSet)

appname = 'interview_app'

urlpatterns = [
    path('', include(interview_router.urls)),
]