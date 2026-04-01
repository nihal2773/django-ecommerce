from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .permissions import IsAdminUserRole

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'price']
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUserRole()]
        return [IsAuthenticatedOrReadOnly()]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer