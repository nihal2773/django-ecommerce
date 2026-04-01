from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product
class UserCartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

class AddToCartView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)

        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity'))

        product = Product.objects.get(id=product_id)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=product_id,
            defaults={'quantity': quantity}
        )

        # STOCK VALIDATION
        if not created:
            if item.quantity + quantity > product.stock:
                return Response(
                    {"error": "Exceeds available stock"},
                    status=400
                )
            item.quantity += quantity
            item.save()
        else:
            if quantity > product.stock:
                return Response(
                    {"error": "Not enough stock"},
                    status=400
                )

        return Response({"message": "Item added to cart"})

class RemoveFromCartView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            item = CartItem.objects.get(id=pk, cart__user=request.user)
            item.delete()
            return Response({"message": "Item removed"})
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)