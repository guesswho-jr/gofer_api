from django.urls import path
from rest_framework_simplejwt.views import  TokenRefreshView

from .views_user import UserGetView
from .views_auth import registerView,loginView

urlpatterns = [
path("user/<str:username>/", UserGetView.as_view()),
path("login/", loginView),
path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
path("register/", registerView),
] 

# When did it return 404