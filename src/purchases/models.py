from django.db import models
from django.conf import settings
from products.models import Product

# Create your models here.
class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    stripe_price = models.IntegerField(default=999) # 100 * price
    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField( auto_now_add=True)
    updated = models.DateTimeField( auto_now=True)

    def __str__(self) -> str:
        return f"{self.user}-{self.product.name}-{self.completed}"
    