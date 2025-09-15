from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import APIException, ValidationError as RestValidationError
from django.core.exceptions import ValidationError, BadRequest, FieldDoesNotExist
from rest_framework.utils.serializer_helpers import ReturnDict

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
    elif isinstance(exc, RestValidationError):
        # print(type(exc.detail))
        condition = type(exc.detail) == ReturnDict and "non_field_errors" in exc.detail.keys()
        codes = exc.get_codes()
        code = codes["non_field_errors"] if condition else codes # type: ignore
        return Response({
                "error": True, 
                "code": code,
                "detail": exc.detail["non_field_errors"] if condition  else exc.detail  # type: ignore
            })
    
    elif isinstance(exc, ValidationError):
        return Response({
            "error": True, "code": exc.code if hasattr(exc, "code") else "validation_error",
            "info": exc.message if hasattr(exc, "message") else (exc if exc else "Validation error occured")
            
        }, status=403)
    
    elif isinstance(exc, BadRequest):

        return Response({
            
            "error": True, "code": "bad_request",
            "info": str(exc) if exc else "The request you sent is not valid"
        },status=400)
    elif isinstance(exc, FieldDoesNotExist):
        return Response({
            "error": True, 
            "code": "field_does_not_exist",
            "info": "The field you requested does not exist"
        },status=400)
    elif isinstance(exc, APIException):
        
        return Response({
            "error": True, "code": exc.default_code,
            "info": exc.detail
            
        }, status=403)
    # else:
    #     print(exc)
    #     # logger.critical(f"Unknown error occured {str(exc)}")
    #     return Response({
    #         "error": True, 
    #         "info": ["Unknown error occured"],
    #     })
        
