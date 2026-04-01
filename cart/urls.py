from django.urls import path
from .views import UserCartView, AddToCartView, RemoveFromCartView

urlpatterns = [
    path('', UserCartView.as_view()),              
    path('add/', AddToCartView.as_view()),         
    path('remove/<int:pk>/', RemoveFromCartView.as_view()),
]