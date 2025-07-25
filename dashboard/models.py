from decimal import Decimal
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import UserProfile
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()


class Product(models.Model):
    id = models.UUIDField(editable=False, unique=True, primary_key=True, default=uuid.uuid4)
    product_name = models.CharField(max_length=100)
    product_description = models.CharField(max_length=512)
    product_original_price = models.DecimalField(decimal_places=2, max_digits=12)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    product_initial_time = models.DateTimeField(help_text=_("The time when the product is added to stock"), auto_now_add=True)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal(0.00))
    product_amount = models.PositiveIntegerField(default=0)
    product_image = models.ImageField(upload_to="products/", null=True)
    product_badge = models.CharField(max_length=128, null=True)
    def __str__(self):
        return self.product_name
    @property
    def final_price(self):
        return float(self.product_original_price - self.discount_amount)
    @property
    def is_discounted(self):
        return True if self.product_original_price - self.discount_amount > 0 else False
    # @property
    # def vendor_image(self):
    #     print(self.user)
    #     up = UserProfile(user=self.user)
    #     print(up.profile_picture)
    #     print("----")
    #     # return up.profile_picture