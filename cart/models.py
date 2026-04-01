from django.db import models

# Create your models here.
from django.conf import settings
from products.models import Product


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Cart - {self.user.username}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def _str_(self):
        return f"{self.product.name} ({self.quantity})"