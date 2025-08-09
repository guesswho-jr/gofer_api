from rest_framework.serializers import ModelSerializer
from rest_framework import serializers 
from Gofer_main.exception_classes import UnknownException
from .models import Product, Review, User
from rest_framework.exceptions import ValidationError
from django.core.exceptions import BadRequest

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["id",
                  "product_name",
                  "product_description",
                  "posted_at",
                  "final_price",
                  "product_original_price",
                  "is_discounted",
                  "vendor_image",
                  "vendor",
                  "full_name",
                  "location",
                  "product_images",
                  "dietaryTags",
                  "ingredients",
                  "is_vegeterian",
                  "total_calories",
                  "review_count",
                  "tags",
                  "average_rating",
                  "category"
                  ]

class ProductListSerailizer(ModelSerializer):
    # make it vendor_image, vendor, at, location, name, full_name, average_rating
    class Meta:
        fields = ["vendor_image",
                  "vendor",
                  "posted_at",
                  "location",
                  "name",
                  "full_name",
                  "average_rating"]
class ProductCreateUpdateSerializer(ModelSerializer):
    vendor = serializers.CharField()
    rating = serializers.IntegerField()
    # images = serializers.ImageField()
    class Meta:
        model = Product
        fields = ("product_name", 
                  "product_description",
                  "product_original_price",
                  "discount_amount",
                  "vendor",
                  "location",
                "category",
                  "dietaryTags",
                  "ingredients",
                  "is_vegeterian",
                  "total_calories",
                  "review_count",
                  "tags",
                  "rating"
                  )
    def validate(self, attrs):
        if attrs["product_original_price"] <= attrs["discount_amount"]:
            raise ValidationError("Discount cannot be more than the price. Don't be that generous!")
        return attrs
    def create(self, validated_data: dict):
        username = validated_data.pop("vendor")
        if "rating" in validated_data.keys():
            validated_data.pop("rating")
        try: 
            u = User.objects.get(username=username)
        except User.DoesNotExist: 
            raise ValidationError("The vendor you requested does not exist. ", "user_not_found")
        except Exception as e:
            raise UnknownException(e)
        post = Product.objects.create(user=u, **validated_data)
        return post
    def update(self, instance: Product, validated_data):
        username = validated_data.pop("vendor")
        ratingReceived = validated_data.pop("rating")
        try:
            ratingReceived = int(ratingReceived)
            if ratingReceived < 0:
                raise Exception()
        except:
            raise BadRequest()
        try: 
            u = User.objects.get(username=username)
            # p = Product.objects.get(id=validated_data["id"])
        except User.DoesNotExist: 
            raise ValidationError("The vendor you requested does not exist. ", "user_not_found")
        except Product.DoesNotExist:
            raise ValidationError("The product you requested does not exist", "product_doesn't_exist")
        except Exception as e:
            raise UnknownException(e)
        rating = (ratingReceived + instance.average_rating) / 2
        return super().update(instance, {**validated_data, "user":u, "rating": rating})
                                          
    
class UUIDField(serializers.UUIDField):
    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except serializers.ValidationError:
            raise serializers.ValidationError(["The id you entered is not found in our database. "])
        except Exception as e:
            raise UnknownException(e)

class ProductReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    class Meta:
        model = Review
        fields = ("review", "username", "username")
