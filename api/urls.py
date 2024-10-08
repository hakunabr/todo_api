from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TaskViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include

router = DefaultRouter()

router.register(r'user', UserViewSet)
router.register(r'task', TaskViewSet)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('',include(router.urls))
]