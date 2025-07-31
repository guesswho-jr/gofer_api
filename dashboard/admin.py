from django.contrib import admin
from .models import Image, Product, Review
# Register your models here.
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Review)
