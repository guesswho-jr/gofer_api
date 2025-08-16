from django.contrib.auth import get_user_model, password_validation, authenticate
from django.db import IntegrityError
from django.forms import ValidationError
from rest_framework.response import Response
from accounts.models import Provider, UserProfile
from .serializers import RegisterSerializer, LoginSerializerAsync
from adrf.decorators import api_view
from asgiref.sync import sync_to_async
from rest_framework import status
from django.contrib.auth.validators import UnicodeUsernameValidator
import re
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from Gofer_main.exception_classes import UnknownException
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser


NAME_REGEX = r"[a-zA-Z]+"


username_validator = UnicodeUsernameValidator()

User = get_user_model()

@api_view(["POST"])
def registerView(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.data 
        user_type = data.pop("user_type") 
        profile_picture = request.FILES["profile_picture"]
        if not user_type in ["provider", "user"]:
            raise ValidationError("Not a valid data")
        ###################-Password validation-##################
        if data["password"] == data["cpassword"]:
            try:
                password_validation.validate_password(password=data["password"])
            except ValidationError:
                return Response({"info": ["The password is not strong enough"]}, status=status.HTTP_403_FORBIDDEN)
        else: # Fail validation block
            return Response({"info": ["Passwords don't match"]}, status=status.HTTP_403_FORBIDDEN)
        ################################################################
        #####################USERNAME##################################
        try:
            username_validator(data["username"])
        
        except ValidationError: 
            return Response({"info": ["Username is not valid"]})
        
        except Exception as e:
            raise UnknownException(e)
        #---------------------------------------------------------------
        if not (re.match(NAME_REGEX, data["last_name"]) and re.match(NAME_REGEX, data["first_name"])):
            return Response({"info": ["Your name is not valid"]})
        #----------------------------------------------------------------
        #################################################################
        try:
            user = User.objects.create_user(username=data["username"],
                                email=data["email"],
                                password=data["password"],
                                first_name=data["first_name"],
                                last_name=data["last_name"])
            if not user:
                return Response({"error" : ["Error occured when trying to create user"]})
            up = UserProfile.objects.create(user=user, profile_picture=profile_picture)
            
            if user_type == "provider":
                Provider.objects.create(user_profile=up, location=data["location"])
                
            
        except IntegrityError:
            return Response({"info": ["Already signed up"]}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
           raise UnknownException(e)
        return Response({"success":True}, status.HTTP_201_CREATED)
        
    else:
        return Response({"info": ["Validation failed"]}, status.HTTP_400_BAD_REQUEST)
    
    
    
@api_view(["POST"])
async def loginView(request):
    serializer = LoginSerializerAsync(data=request.POST)
    if serializer.is_valid():
        data = await serializer.adata # type: ignore
        username = data['username']
        password = data['password']
        try:
            username_validator(data["username"])
        except ValidationError:
            
            return Response({"info":[ "The data you provided is not valid"]}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            raise UnknownException(e)
        
        user = await sync_to_async(authenticate)(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            access = AccessToken.for_user(user)
            
            return Response({
                "refresh": str(refresh),
                "access": str(access)
            }, status.HTTP_200_OK)
        return Response({
            "info": ["Couldn't log you in. Check username and/or password" ],
            "code" : "unauthorized"
        },  status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"info": ["Validation failed"]}, status.HTTP_400_BAD_REQUEST) 