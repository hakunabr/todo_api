from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TaskViewSet

router = DefaultRouter()

router.register(r'user', UserViewSet)
router.register(r'task', TaskViewSet)

urlpatterns = router.urls