from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from django.db import transaction

from cart.models import Cart
from .models import Order, OrderItem
from .serializers import OrderSerializer

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        payment_method = request.data.get('payment_method', 'cod')
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=404)

        items = cart.items.all()

        if not items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        for item in items:
            if item.quantity > item.product.stock:
                return Response(
                    {"error": f"{item.product.name} out of stock"},
                    status=400
                )

        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                payment_method=payment_method,
                status='pending'
            )

            total_price = 0

            for item in items:
                product = item.product
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item.quantity,
                    price=product.price
                )

                
                product.stock -= item.quantity
                product.save()

                total_price += product.price * item.quantity

            
            order.total_price = total_price

            if payment_method == 'cod':
                order.status = 'completed'
            order.save()
            items.delete()

        return Response(
            {
                "message": "Order placed successfully",
                "order_id": order.id,
                "payment_method": order.payment_method,
                "status": order.status
            },
            status=status.HTTP_201_CREATED
        )


# PAYMENT 
class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        user = request.user

        try:
            order = Order.objects.get(id=order_id, user=user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        
        if order.payment_method == 'cod':
            return Response(
                {"error": "COD orders do not require payment"},
                status=400
            )

        
        if order.status == 'completed':
            return Response(
                {"error": "Order already paid"},
                status=400
            )

        order.status = 'completed'
        order.save()

        return Response(
            {
                "message": "Payment successful",
                "order_id": order.id,
                "status": order.status
            },
            status=status.HTTP_200_OK
        )


class OrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')