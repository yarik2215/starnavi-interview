from rest_framework.permissions import BasePermission

class IsInterviewer(BasePermission):
    """
    Allow acces only for interviewer of this interview.
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.interviewer