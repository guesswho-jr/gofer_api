from django.urls import path
from .views import ProductListCreateView, ProductRetreiveUpdateView, product_review

urlpatterns = [
    path("", ProductListCreateView.as_view(), name="products_all"),
    path("<str:product>/reviews/", product_review, name="product_review"),
    path("<str:id>/", ProductRetreiveUpdateView.as_view(), name="product"),
]