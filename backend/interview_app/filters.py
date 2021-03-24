from django_filters import rest_framework as filters
from .models import Interview

class InterviewFilter(filters.FilterSet):
    before_date = filters.filters.DateFilter('date', lookup_expr='lte')
    after_date = filters.filters.DateFilter('date', lookup_expr='gte')

    class Meta:
        model = Interview
        fields = ['state', 'before_date', 'after_date']
