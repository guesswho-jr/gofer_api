from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import APIException
from django.core.exceptions import ValidationError, BadRequest, FieldDoesNotExist

def commonExceptions(exc, _):

    if isinstance(exc, MethodNotAllowed):
        return Response({
            "info": [f"Method {exc.args[0]} is not allowed."]
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    elif isinstance(exc, InvalidToken):
        return Response({
            "info": [
                "Your session is invalid or expired"
            ]
        },status=status.HTTP_401_UNAUTHORIZED) 
    elif isinstance(exc, APIException):
        return Response({
            "code": exc.default_code,
            "info": exc.detail
            
        })
    elif isinstance(exc, ValidationError):
        print(exc)
        return Response({
            "code": "validation_error",
            "info": "The information you submitted is not correct. If this issue persists report to us."
            
        })
    elif isinstance(exc, BadRequest):
        return Response({
            "code": "bad_request",
            "info": "The request you sent is not valid"
        },status=400)
    elif isinstance(exc, FieldDoesNotExist):
        return Response({
            "code": "field_does_not_exist",
            "info": "The field you requested does not exist"
        },status=400)
    # else:
    #     return Response({
    #         "code": "unknown",
    #         "info": ["Unknown error occured"],
    #         "debug": str(exc)
    #     })