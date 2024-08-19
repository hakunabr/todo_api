from django.contrib.auth.models import User
from .models import Task
from .serializers import TaskSerializer
from rest_framework import viewsets
from .filters import TaskFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = TaskFilter
    filter_backends = [DjangoFilterBackend]


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)