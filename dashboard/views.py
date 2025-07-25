from django.core.exceptions import ValidationError
from adrf.decorators import api_view
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
import os
from .api import get_all_products_serialized, get_specific_product, createProduct, updateProduct
from rest_framework.response import Response
from .serializer import ProductFormSerializer, UpdateSerializer
from .models import Product



@api_view(["GET"])
async def product(_, **kwargs):
    product_id = kwargs["product_id"]
    return Response(
        await get_specific_product(product_id)
    )
@api_view(["GET"])
async def products_all(_):
    products = await get_all_products_serialized()
    return Response(products)
@api_view(["POST"])
async def create_product(request):
    serializer = ProductFormSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        data = await serializer.adata  # type: ignore
        await createProduct(product_name=data["product_name"],
                           product_description=data["product_description"],
                           product_original_price=data["product_original_price"],
                           product_vendor=data["product_vendor"],
                           discount_amount=data["discount_amount"],
                           product_amount=data["product_amount"])
    else:
        raise ValidationError("Validation valid when creating product")
    return Response({
        "success": True
    })

@api_view(["POST"])
async def update_product(request):
    serializer =  UpdateSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        data = await serializer.adata  # type: ignore
        await updateProduct(product_id=data["product_id"], updated_field=data["updated_field"], updated_to=data["updated_to"])
        return Response({"success": True})
    else:
        raise ValidationError("")

# def download_image(request, url):
#     obj = get_object_or_404(Product, )

# async def upload_story(request: HttpRequest):
#     serializer = StorySerializer(data=request.POST)