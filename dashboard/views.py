from rest_framework.response import Response
from .serializer import ProductCreateUpdateSerializer, ProductReviewSerializer, ProductSerializer
from .models import Image, Product, Review
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from Gofer_main.exceptions import ValidationError
from rest_framework.decorators import api_view
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
    parser_classes = (MultiPartParser, FormParser)
    def perform_create(self, serializer):
        post = serializer.save()
        for image in self.request.FILES.getlist("images"):
            Image.objects.create(post=post, image=image)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            return Response({
                "success": True
            }, status=201)
    def get_serializer_class(self): # type: ignore
        if self.request.method in ["POST", "PUT"]:
            return ProductCreateUpdateSerializer
        return ProductSerializer


@api_view(["GET"])
def product_review(request, *args, **kwargs):
    product_id = kwargs.get("product")
        # product = Product.objects.get(id=product_id)
    data = Review.objects.filter(product__id=product_id)
    if not data.exists():
        raise ValidationError("Review doesn't exist for this product", "not_found")
    data = ProductReviewSerializer(data, many=True)
    if data:
        return Response(data.data)