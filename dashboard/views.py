from collections import defaultdict
from django.http import Http404
from rest_framework.response import Response

from Gofer_main.classes import GoferListCreateView
from .serializer import ProductCreateSerializer, ProductListSerailizer, ProductSerializer, ProductReviewSerializer, ProductUpdateSerializer
from .models import Image, Product, Review, User
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from Gofer_main.exceptions import ValidationError
from rest_framework.views import APIView
from django.db.utils import IntegrityError
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination
from django.dispatch import Signal
from Gofer_main.exceptions import BadRequest
class ProductRetreiveUpdateView(RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    lookup_field = 'id'
    pagination_class = PageNumberPagination
    def get_serializer_class(self): # type: ignore
        if self.request.method in ["PUT", "PATCH"]:
            return ProductUpdateSerializer
        return ProductSerializer
product_created = Signal()
class ProductListCreateView(GoferListCreateView):
    queryset = Product.objects.order_by("-product_initial_time").all()
    def perform_create(self, serializer):
        post = serializer.save()
        for image in self.request.FILES.getlist("images"):
            Image.objects.create(post=post, image=image)
        return post
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            post = self.perform_create(serializer)
            product_created.send(sender=self.__class__, instance=post)
            return Response({
                "success": True
            }, status=201)
        else:
            raise BadRequest()
    
    def get_serializer_class(self): # type: ignore
        if self.request.method == "POST":
            return ProductCreateSerializer
        return ProductListSerailizer
    def list(self, request, *args, **kwargs):
        grouped = defaultdict(list)
        paginator = self.pagination_class()
        queryset = self.get_queryset()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer_class()
        if page is not None:
            for product in self.queryset.all():
                serialized = dict(serializer(product).data)
                if product.is_provider:
                    grouped[product.category].append(serialized)
            result = [{"category": cat, "products": prods} for cat, prods in grouped.items()]
            return paginator.get_paginated_response(result)
        else:
            raise APIException(code="fetch_error", detail="Cannot fetch data from database. ")
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