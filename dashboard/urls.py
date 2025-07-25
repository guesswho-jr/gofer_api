from django.urls import path
from .views import product, products_all, create_product, update_product

urlpatterns = [
    path("product/<str:product_id>/", product, name="product"),
    path("all/", products_all, name="products_all"),
    path("create/", create_product),
    # path("image/", download_image),
    path("update/", update_product),
]