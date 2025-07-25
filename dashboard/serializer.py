from adrf.serializers import ModelSerializer, Serializer
from rest_framework import serializers as srl
from utils.log import logger
from .models import Product

class ProductSerializer(srl.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id",
                  "product_name",
                  "product_description",
                  "product_initial_time",
                  "final_price",
                  "product_original_price",
                  "product_amount",
                  "is_discounted",
                  "product_image",
                  "product_badge",
                  "vendor_image",
                  "vendor"
                  ]

class ProductFormSerializer(Serializer):
        product_name = srl.CharField()
        product_description = srl.CharField()
        product_vendor = srl.CharField()
        product_original_price = srl.DecimalField(decimal_places=2, max_digits=12)
        product_amount = srl.IntegerField()
        discount_amount = srl.DecimalField(max_digits=12, decimal_places=2)

class UUIDField(srl.UUIDField):
    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except srl.ValidationError:
            raise srl.ValidationError(["The id you entered is not found in our database. "])
        except Exception as e:
            logger.critical(f"Unknown error occured at {__name__} {e}")
            raise Exception(["Unknown error occured"])

class UpdateSerializer(Serializer):
    product_id = UUIDField()
    updated_field = srl.CharField()
    updated_to = srl.CharField()