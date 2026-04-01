from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet

router = DefaultRouter()
router.register('', ProductViewSet)
router.register('categories', CategoryViewSet)

urlpatterns = router.urls