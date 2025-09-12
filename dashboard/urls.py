from django.urls import path
from .views import ProductForUser, ProductListCreateView, ProductRetreiveUpdateView, ProductReview, ProductSearchView
from dashboard import consumers


urlpatterns = [
    path("", ProductListCreateView.as_view(), name="products_all"),
    path("<str:username>/", ProductForUser.as_view()),
    path("<str:product>/reviews/", ProductReview.as_view(), name="product_review"),
    path("<str:id>/", ProductRetreiveUpdateView.as_view(), name="product"),
    path("search/<str:product>", ProductSearchView.as_view()),
]


websocket_urlpatterns = [
    path("ws/updates/", consumers.DataUpdateConsumer.as_asgi())   
]