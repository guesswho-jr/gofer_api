from collections import defaultdict
from django.http import Http404
from rest_framework.response import Response
from .serializer import ProductCreateUpdateSerializer, ProductListSerailizer, ProductReviewSerializer, ProductSerializer
from .models import Image, Product, Review, User
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from Gofer_main.exceptions import ValidationError
from rest_framework.views import APIView
from django.db.utils import IntegrityError
from rest_framework.exceptions import APIException


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
        return ProductListSerailizer
    def list(self, request, *args, **kwargs):
        grouped = defaultdict(list)
        for product in self.queryset.all():
            serializer = self.get_serializer_class()
            serialized = serializer(product).data
            grouped[product.category].append(serialized)
        result = [{"category": cat, "products": prods} for cat, prods in grouped.items()]
        return Response(result)
        # return super().list(request, *args, **kwargs)


#REviw post not done.
class ProductReview(APIView):
    serializer = ProductReviewSerializer
    def get(self, *args, **kwargs):
        product_id = kwargs.get("product")
        data = Review.objects.filter(product__id=product_id)
        if not data.exists():
            raise ValidationError("Review doesn't exist for this product", "not_found")
        data = self.serializer(data, many=True).data
        if data:
            return Response(data)
        else:
            raise Http404()
    def post(self, *args, **kwargs):
        product_id = kwargs.get("product")
        data = self.serializer(data=self.request.POST)
        if data.is_valid(raise_exception=True):
            product = Product.objects.get(id=product_id)
            username = data.data.get("username") # type: ignore
            user = User.objects.get(username=username)
            review = data.data.get('review') # type: ignore
            try:
                Review.objects.create(product=product, user=user, review=review)
            except IntegrityError:
                raise APIException("You can't review one product more than once", code="not_allowed")
            return Response({"success": True})
        return Response({"success": False})