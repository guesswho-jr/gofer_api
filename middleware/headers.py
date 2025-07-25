from django.http import HttpRequest, JsonResponse



class AuthorizationHeaderCheck:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request: HttpRequest):
        if 'auth' not in request.path:
            if 'admin' not in request.path:
                if 'HTTP_AUTHORIZATION' not in request.META:
                    return JsonResponse({
                        "info": [
                            "Required headers not set",
                        ]
                    }, status=400)
        # pass
        return self.get_response(request)