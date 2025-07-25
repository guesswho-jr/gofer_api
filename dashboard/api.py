from decimal import Decimal
from typing import Any
from .serializer import ProductSerializer
from .models import Product
from asgiref.sync import sync_to_async
from django.core.exceptions import BadRequest, FieldDoesNotExist

@sync_to_async
def get_all_products_serialized():
        products = Product.objects.all()
        products_serialized = []
        for product in products:
            products_serialized.append(ProductSerializer(product).data) # type: ignore
    # return products
        # products = 123
        return products_serialized


   
async def get_specific_product(id: str):
    product = await Product.objects.aget(pk=id)
    product = await ProductSerializer(product).adata  # type: ignore
    return product


@sync_to_async
def createProduct(product_name: str,
                         product_description: str,
                         product_original_price: str,
                         product_vendor: str,
                         discount_amount: Decimal,
                         product_amount: int):
    Product.objects.create(product_name=product_name,
                           product_description=product_description,
                           product_original_price=product_original_price,
                           product_vendor=product_vendor,
                           discount_amount=discount_amount,
                           product_amount=product_amount)
    
    
async def updateProduct(product_id: str, updated_field: Any, updated_to: Any):
    p = await Product.objects.aget(id=product_id)
    if p:
        if updated_field in p.__dict__.keys():
            p.__dict__[updated_field] = updated_to
            await sync_to_async(p.save)()
        else:
            raise FieldDoesNotExist()
    else:
        raise BadRequest()