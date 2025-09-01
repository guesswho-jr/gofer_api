from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()
class GoferListCreateView(generics.ListCreateAPIView):
    """
    I assume the uploaded_by field is in it so don't forget
    """
    pagination_class = PageNumberPagination
    def get_user_from_token(self):
        raw_token = self.request.headers["Authorization"].split(" ")[1]
        t = AccessToken(raw_token)
        user = User.objects.get(pk=t["user_id"])
        return user
    def get_queryset(self): # type: ignore
        user = self.get_user_from_token()
        pre_follow_list = user.follows.all() # type: ignore
        follow_list = map(lambda x: x.follows, pre_follow_list)
        if self.queryset is None:
            raise Exception("Queryset is not optional in here")
        
        data = self.queryset.filter(uploaded_by__in=follow_list).exclude(uploaded_by=user)
        return data
    