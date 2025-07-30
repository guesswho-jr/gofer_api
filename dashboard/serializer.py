from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework import serializers 
from Gofer_main.exception_classes import UnknownException
from .models import Product, User
from rest_framework.exceptions import ValidationError

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["id",
                  "product_name",
                  "product_description",
                  "posted_at",
                  "final_price",
                  "product_original_price",
                  "product_amount",
                  "is_discounted",
                  "product_badge",
                  "vendor_image",
                  "vendor",
                  "full_name",
                  "image",
                  "location"
                  ]



class ProductCreateUpdateSerializer(ModelSerializer):
    vendor = serializers.CharField()
    class Meta:
        model = Product
        fields = ("product_name", 
                  "product_description",
                  "product_original_price",
                  "discount_amount",
                  "product_image", 
                  "product_badge",
                  "vendor",
                  "location"
                  )
    def validate(self, attrs):
        if attrs["product_original_price"] <= attrs["discount_amount"]:
            raise ValidationError("Discount cannot be more than the price. Don't be that generous!")
        return attrs
    def create(self, validated_data: dict):
        username = validated_data.pop("vendor")
        try: 
            u = User.objects.get(username=username)
        except User.DoesNotExist: 
            raise ValidationError("The vendor you requested does not exist. ", "user_not_found")
        except Exception as e:
            raise UnknownException(e)
        return Product.objects.create(user=u, **validated_data)
    def update(self, instance, validated_data):
        username = validated_data.pop("vendor")
        try: 
            u = User.objects.get(username=username)
        except User.DoesNotExist: 
            raise ValidationError("The vendor you requested does not exist. ", "user_not_found")
        except Exception as e:
            raise UnknownException(e)
        return super().update(instance, {**validated_data, "user":u})
                                          
    
class UUIDField(serializers.UUIDField):
    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except serializers.ValidationError:
            raise serializers.ValidationError(["The id you entered is not found in our database. "])
        except Exception as e:
            raise UnknownException(e)

