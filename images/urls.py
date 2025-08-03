from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ARTargetViewSet

router = DefaultRouter()
router.register(r'targets', ARTargetViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
] 