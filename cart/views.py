from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product


# -------------------- USER CART --------------------
class UserCartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart


# -------------------- ADD TO CART --------------------
class AddToCartView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)

        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        # Validate quantity safely
        try:
            quantity = int(quantity)
            if quantity < 1:
                raise ValueError
        except (TypeError, ValueError):
            return Response(
                {"error": "Invalid quantity"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate product
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get or create cart item
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            if item.quantity + quantity > product.stock:
                return Response(
                    {"error": "Exceeds available stock"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            item.quantity += quantity
        else:
            if quantity > product.stock:
                return Response(
                    {"error": "Not enough stock"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        item.save()

        return Response(
            {"message": "Item added to cart"},
            status=status.HTTP_201_CREATED
        )


# -------------------- REMOVE FROM CART --------------------
class RemoveFromCartView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            item = CartItem.objects.get(id=pk, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        item.delete()

        return Response(
            {"message": "Item removed"},
            status=status.HTTP_200_OK
        )


# -------------------- UPDATE CART ITEM --------------------
class UpdateCartItemView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, item_id):
        quantity = request.data.get('quantity')

        # Safe validation
        try:
            quantity = int(quantity)
            if quantity < 1:
                raise ValueError
        except (TypeError, ValueError):
            return Response(
                {'error': 'Invalid quantity'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            item = CartItem.objects.get(
                id=item_id,
                cart__user=request.user
            )
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Item not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Stock validation
        if quantity > item.product.stock:
            return Response(
                {"error": "Exceeds available stock"},
                status=status.HTTP_400_BAD_REQUEST
            )

        item.quantity = quantity
        item.save()

        cart = Cart.objects.get(user=request.user)

        return Response(
            CartSerializer(cart).data,
            status=status.HTTP_200_OK
        )