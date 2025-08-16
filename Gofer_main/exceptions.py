from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import APIException
from django.core.exceptions import ValidationError, BadRequest, FieldDoesNotExist
from utils.log import logger


def commonExceptions(exc, _):

    if isinstance(exc, MethodNotAllowed):
        return Response({
            "info": [f"Method {exc.args[0]} is not allowed."]
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    elif isinstance(exc, InvalidToken):
        return Response({
            "error": True, 
            "code": "TOKEN_INVALID",
            "info": [
                "Your account information is invalid or expired. Please log in again."
            ]
        },status=status.HTTP_401_UNAUTHORIZED) 
    elif isinstance(exc, APIException):
        return Response({
            "error": True, "code": exc.default_code,
            "info": exc.detail
            
        }, status=403)
    elif isinstance(exc, ValidationError):
        return Response({
            "error": True, "code": exc.code,
            "info": exc.message
            
        }, status=403)
    elif isinstance(exc, BadRequest):
        return Response({
            "error": True, "code": "bad_request",
            "info": "The request you sent is not valid"
        },status=400)
    elif isinstance(exc, FieldDoesNotExist):
        return Response({
            "error": True, 
            "code": "field_does_not_exist",
            "info": "The field you requested does not exist"
        },status=400)
    
    # else:
    #     logger.critical(f"Unknown error occured {str(exc)}")
    #     return Response({
    #         "error": True, 
    #         "info": ["Unknown error occured"],
    #     })
        
