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
    # product_image = models.ImageField(upload_to="products")
    badges = models.JSONField(max_length=512, null=True)
    location = models.CharField(max_length=512, blank=False, null=False)
    review_count = models.PositiveIntegerField(default=0)
    total_calories = models.PositiveIntegerField(null=False, blank=False)
    is_vegeterian = models.BooleanField()
    ingredients = models.JSONField()
    dietaryTags = models.JSONField()
    average_rating = models.DecimalField(decimal_places=2, max_digits=3, default=Decimal(0.00))

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
        return naturaltime(self.product_initial_time)
    @property
    def product_images(self):
        p= Product.objects.get(id=self.id)
        images=[]
        for image in p.images.all(): # type: ignore
            images.append(image.image.url)
        return images

class Image(models.Model):
    post = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/")
    def __str__(self) -> str:
        return self.post.product_name
class Review(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="reviewed_by")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviewed_product")
    review = models.TextField()
    def __str__(self) -> str:
        return self.user.username