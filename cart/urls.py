from django.urls import path
from .views import UserCartView, AddToCartView, RemoveFromCartView
from . import views

urlpatterns = [
    path('', UserCartView.as_view()),              
    path('add/', AddToCartView.as_view()),         
    path('remove/<int:pk>/', RemoveFromCartView.as_view()),
    path('update/<int:item_id>/', views.UpdateCartItemView.as_view(), name='cart-update'),
]