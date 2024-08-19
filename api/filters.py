from django_filters import rest_framework as filters
from .models import Task

class TaskFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')
    completed = filters.BooleanFilter(field_name='completed', lookup_expr='exact')

    class Meta:
        model = Task
        fields = ['title', 'description', 'completed']