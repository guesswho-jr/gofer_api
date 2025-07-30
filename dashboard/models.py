from decimal import Decimal
from typing import Iterable
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.humanize.templatetags.humanize import naturaltime


User = get_user_model()


class Product(models.Model):
    id = models.UUIDField(editable=False, unique=True, primary_key=True, default=uuid.uuid4)
    product_name = models.CharField(max_length=100)
    product_description = models.CharField(max_length=512)
    product_original_price = models.DecimalField(decimal_places=2, max_digits=12)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_initial_time = models.DateTimeField(help_text=_("The time when the product is added to stock"), auto_now_add=True)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal(0.00))
    product_amount = models.PositiveIntegerField()
    product_image = models.ImageField(upload_to="products")
    product_badge = models.CharField(max_length=512, null=True)
    location = models.CharField(max_length=512, blank=False, null=False)
    def __str__(self):
        return self.product_name
    @property
    def final_price(self):
        data = float(self.product_original_price - self.discount_amount)
        if data <=0:
            return None
        return data
    @property
    def is_discounted(self):
        return True if self.product_original_price - self.discount_amount > 0 else False
    @property
    def vendor_image(self):
        return self.user.profile.profile_picture.url # type: ignore
    @property
    def vendor(self):
        return self.user.username
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    @property
    def posted_at(self):
        # this is some time ago
        # return f"{timesince(self.product_initial_time, timezone.now() )} ago"
        return naturaltime(self.product_initial_time)
    @property
    def image(self):
        return [self.product_image.url]