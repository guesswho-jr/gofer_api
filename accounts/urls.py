from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView
from .auth_utils import registerView,loginView

urlpatterns = [
path("login/", loginView),
path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
path("register/", registerView)
]