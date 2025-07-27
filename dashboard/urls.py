from django.urls import path
from .views import ProductListCreateView, ProductRetreiveUpdateView

urlpatterns = [
    path("", ProductListCreateView.as_view(), name="products_all"),
    path("<str:id>/", ProductRetreiveUpdateView.as_view(), name="product"),
]