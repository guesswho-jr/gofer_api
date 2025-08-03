from django.urls import path
from .views import ProductListCreateView, ProductRetreiveUpdateView, ProductReview

urlpatterns = [
    path("", ProductListCreateView.as_view(), name="products_all"),
    path("<str:product>/reviews/", ProductReview.as_view(), name="product_review"),
    path("<str:id>/", ProductRetreiveUpdateView.as_view(), name="product"),
]