from rest_framework.response import Response
from .serializer import ProductCreateUpdateSerializer, ProductSerializer
from .models import Product
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView


class ProductRetreiveUpdateView(RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    lookup_field = 'id'
    def get_serializer_class(self): # type: ignore
        if self.request.method in ["PUT", "PATCH"]:
            return ProductCreateUpdateSerializer
        return ProductSerializer
class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.order_by("-product_initial_time")
    # serializer_class = ProductSerializer
    def perform_create(self, serializer):
        serializer.save()
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            return Response({
                "success": True
            }, status=201)
    def get_serializer_class(self): # type: ignore
        if self.request.method  == "POST":
            return ProductCreateUpdateSerializer
        return ProductSerializer

